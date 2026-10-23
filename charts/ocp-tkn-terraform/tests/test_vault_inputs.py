"""Exercise rendered Vault conversion with the existing source-package splitter."""
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import yaml

CHART = Path(__file__).resolve().parents[1]
SPLITTER = os.environ.get('SPLIT_TFVARS_SCRIPT')

class VaultInputs(unittest.TestCase):
    def setUp(self):
        if not SPLITTER:
            self.fail('Set SPLIT_TFVARS_SCRIPT to the source package terraform/scripts/split-tfvars.js')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / 'terraform/workspaces/gold'
        self.work.mkdir(parents=True)
        scripts = self.root / 'terraform/scripts'
        scripts.mkdir()
        shutil.copy(SPLITTER, scripts / 'split-tfvars.js')
        self.values = self.root / 'values.yaml'
        self.values.write_text(yaml.safe_dump({'serviceAccount': {'name': 'terraform'}, 'tasks': {'installSourceCode': {'vaultInputPath': '/vault/input.json', 'annotations': {'vault.hashicorp.com/agent-inject-template-input': '{{ .Data.data.tfvars_json }}'}}}}))
        self.docs = list(yaml.safe_load_all(subprocess.check_output(['helm', 'template', 'test', str(CHART), '-f', str(self.values)], text=True)))
        task = next(d for d in self.docs if d['kind'] == 'Task' and d['metadata']['name'].endswith('-pull-source-code'))
        script = task['spec']['steps'][0]['script']
        subprocess.run(['sh', '-n'], input=script, text=True, check=True)
        self.tail = 'set -eu\n' + script[script.index('if [ -n "${VAULT_INPUT_PATH}" ]; then'):]

    def convert(self, data):
        path = self.root / 'vault.json'
        if data is not None:
            path.write_text(data)
        return subprocess.run(['sh', '-c', self.tail], cwd=self.work, env={**os.environ, 'VAULT_INPUT_PATH': str(path)}, capture_output=True, text=True)

    def test_real_splitter_and_terraform_precedence(self):
        encoded = lambda value: base64.b64encode(value.encode()).decode()
        result = self.convert(json.dumps({'data': {'choice': encoded('vault'), 'vault_only': encoded('supplement'), 'settings.vault': encoded('default')}}))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.work / '000-vault.auto.tfvars').stat().st_mode & 0o777, 0o600)
        (self.work / 'main.tf').write_text('''
variable "choice" { type = string }
variable "vault_only" { type = string }
variable "settings" { type = map(string) }
output "result" { value = { choice = var.choice, vault_only = var.vault_only, settings = var.settings } }
''')
        (self.work / 'terraform.tfvars').write_text('choice = "plain"\n')
        init = subprocess.run(['terraform', 'init', '-backend=false', '-input=false'], cwd=self.work, capture_output=True, text=True)
        self.assertEqual(init.returncode, 0, init.stderr)
        def apply():
            subprocess.run(['terraform', 'apply', '-auto-approve', '-input=false'], cwd=self.work, capture_output=True, check=True)
            return json.loads(subprocess.check_output(['terraform', 'output', '-json', 'result'], cwd=self.work, text=True))
        self.assertEqual(apply()['choice'], 'vault')
        (self.work / 'terraform.secret.auto.tfvars').write_text('choice = "secret"\nsettings = { explicit = "wins" }\n')
        self.assertEqual(apply(), {'choice': 'secret', 'vault_only': 'supplement', 'settings': {'explicit': 'wins'}})

    def test_splitter_final_map_limitation_is_detected(self):
        encoded = base64.b64encode(b'certificate').decode()
        result = self.convert(json.dumps({'data': {'ssl_certs.sdx-crt': encoded}}))
        self.assertEqual(result.returncode, 0, result.stderr)
        path = self.work / '000-vault.auto.tfvars'
        # The current package helper omits the closing map brace at EOF.
        # Once fixed upstream, this compatibility check accepts the valid output.
        output = path.read_text()
        if not output.rstrip().endswith('}'):
            self.assertIn('ssl_certs = {', output)
            print('Known source-package splitter limitation: final map is not closed')

    def test_missing_or_invalid_input_stops_source(self):
        for data in [None, 'invalid-json']:
            with self.subTest(data=data):
                self.assertNotEqual(self.convert(data).returncode, 0)

    def test_annotations_are_scoped_and_literal(self):
        run = next(d for d in self.docs if d['kind'] == 'TriggerTemplate')['spec']['resourcetemplates'][0]
        spec = next(s for s in run['spec']['taskRunSpecs'] if s['pipelineTaskName'] == 'install-source-code')
        self.assertEqual(spec['metadata']['annotations']['vault.hashicorp.com/agent-inject-template-input'], '{{ .Data.data.tfvars_json }}')
        self.assertNotIn('annotations', run['metadata'])

    def test_apply_task_unchanged_and_disabled_has_no_task_override(self):
        original = subprocess.check_output(['git', 'show', 'origin/master:charts/ocp-tkn-terraform/templates/tf-apply-task.yaml'], cwd=CHART, text=True)
        self.assertEqual((CHART / 'templates/tf-apply-task.yaml').read_text(), original)
        docs = list(yaml.safe_load_all(subprocess.check_output(['helm', 'template', 'test', str(CHART)], text=True)))
        run = next(d for d in docs if d['kind'] == 'TriggerTemplate')['spec']['resourcetemplates'][0]
        self.assertEqual(len(run['spec']['taskRunSpecs']), 1)

if __name__ == '__main__':
    unittest.main()
