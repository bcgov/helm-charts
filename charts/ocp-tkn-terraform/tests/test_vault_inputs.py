"""Render and exercise the real apply wrapper with local-only Terraform inputs."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import yaml

CHART = Path(__file__).resolve().parents[1]


def render(root, configured):
    values = {'serviceAccount': {'name': 'terraform'}}
    if configured:
        values['tasks'] = {'installSourceCode': {
            'vaultInputPath': '/vault/secrets/terraform.json',
            'annotations': {
                'vault.hashicorp.com/agent-inject': 'true',
                'vault.hashicorp.com/agent-pre-populate-only': 'true',
                'vault.hashicorp.com/agent-inject-template-input': '{{ .Data.data | toJSON }}',
            },
        }}
    path = root / 'values.yaml'
    path.write_text(yaml.safe_dump(values))
    output = subprocess.check_output(['helm', 'template', 'test', str(CHART), '-f', str(path)], text=True)
    return list(yaml.safe_load_all(output))


class VaultInputs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docs = render(self.root, True)
        task = next(d for d in self.docs if d['kind'] == 'Task' and d['metadata']['name'].endswith('-terraform-apply'))
        self.script = task['spec']['steps'][0]['script']
        # Exercise the exact rendered secret-consuming tail, including its exit trap.
        self.tail = 'set -eu\n' + self.script[self.script.index("trap 'rm -f .vault-inputs.json' 0"):]
        (self.root / 'main.tf').write_text('''
variable "choice" { type = string }
variable "only_vault" { type = string }
variable "environment" { type = string }
variable "settings" { type = map(string) }
output "result" { value = { choice = var.choice, only_vault = var.only_vault, environment = var.environment, settings = var.settings } }
''')
        subprocess.run(['terraform', 'init', '-backend=false', '-input=false'], cwd=self.root, check=True, capture_output=True)

    def run_tail(self):
        env = {**os.environ, 'TF_VAR_environment': 'existing-environment', 'TF_IN_AUTOMATION': '1'}
        return subprocess.run(['sh', '-c', self.tail], cwd=self.root, env=env, text=True, capture_output=True)

    def test_annotations_are_task_scoped_and_literal(self):
        trigger = next(d for d in self.docs if d['kind'] == 'TriggerTemplate')
        run = trigger['spec']['resourcetemplates'][0]
        specs = run['spec']['taskRunSpecs']
        install = next(s for s in specs if s['pipelineTaskName'] == 'install-source-code')
        self.assertEqual(install['metadata']['annotations']['vault.hashicorp.com/agent-inject-template-input'], '{{ .Data.data | toJSON }}')
        self.assertNotIn('annotations', run['metadata'])
        self.assertEqual(len(specs), 2)
        self.assertNotIn('set -x', self.script)

    def test_tfvars_override_vault_and_preserve_normal_order(self):
        # Keep shell metacharacters and multiline values literal.
        literal = 'line one\n$(touch SHOULD_NOT_EXIST) `id` "quoted"'
        (self.root / '.vault-inputs.json').write_text(json.dumps({
            'choice': 'vault', 'only_vault': literal, 'environment': 'vault',
            'settings': {'vault': 'default'},
        }))
        (self.root / 'terraform.tfvars').write_text('choice = "standard"\n')
        (self.root / 'terraform.tfvars.json').write_text(json.dumps({'choice': 'json'}))
        (self.root / 'a.auto.tfvars.json').write_text(json.dumps({'choice': 'auto-json'}))
        (self.root / 'terraform.secret.auto.tfvars').write_text('choice = "secret"\nsettings = { explicit = "wins" }\n')
        result = self.run_tail()
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(subprocess.check_output(['terraform', 'output', '-json', 'result'], cwd=self.root, text=True))
        self.assertEqual(values, {'choice': 'secret', 'only_vault': literal, 'environment': 'existing-environment', 'settings': {'explicit': 'wins'}})
        self.assertFalse((self.root / '.vault-inputs.json').exists())
        self.assertFalse((self.root / 'SHOULD_NOT_EXIST').exists())

    def test_missing_or_invalid_input_fails_and_cleans_up(self):
        for value in [None, 'invalid-secret-content', '[]', '{"bad-key": "secret"}']:
            with self.subTest(value=value):
                path = self.root / '.vault-inputs.json'
                if value is not None:
                    path.write_text(value)
                result = self.run_tail()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Invalid or missing Vault Terraform input JSON object', result.stderr)
                self.assertNotIn('invalid-secret-content', result.stderr)
                self.assertFalse(path.exists())

    def test_source_copy_requires_file_and_restricts_permissions(self):
        task = next(d for d in self.docs if d['kind'] == 'Task' and d['metadata']['name'].endswith('-pull-source-code'))
        script = task['spec']['steps'][0]['script']
        self.assertNotIn('set -x', script)
        subprocess.run(['sh', '-n'], input=script, text=True, check=True)
        tail = 'set -eu\n' + script[script.index('if [ -n "${VAULT_INPUT_PATH}" ]; then'):]
        path = self.root / 'injected.json'
        env = {**os.environ, 'VAULT_INPUT_PATH': str(path)}
        failed = subprocess.run(['sh', '-c', tail], cwd=self.root, env=env, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        path.write_text('{"choice":"vault"}')
        subprocess.run(['sh', '-c', tail], cwd=self.root, env=env, check=True)
        copy = self.root / '.vault-inputs.json'
        self.assertEqual(copy.read_text(), path.read_text())
        self.assertEqual(copy.stat().st_mode & 0o777, 0o600)

    def test_terraform_failure_removes_supplemental_copy(self):
        (self.root / '.vault-inputs.json').write_text('{}')
        result = self.run_tail()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / '.vault-inputs.json').exists())

    def test_unconfigured_chart_keeps_original_apply(self):
        docs = render(self.root, False)
        trigger = next(d for d in docs if d['kind'] == 'TriggerTemplate')
        self.assertEqual(len(trigger['spec']['resourcetemplates'][0]['spec']['taskRunSpecs']), 1)
        task = next(d for d in docs if d['kind'] == 'Task' and d['metadata']['name'].endswith('-terraform-apply'))
        script = task['spec']['steps'][0]['script']
        self.assertIn('terraform apply -no-color --auto-approve', script)
        self.assertNotIn('node -e', script)
        subprocess.run(['sh', '-n'], input=script, text=True, check=True)


if __name__ == '__main__':
    unittest.main()
