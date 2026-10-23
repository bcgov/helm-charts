# Tekton CI/CD for Terraform Deployment

Helm chart to create a tekton pipeline on OCP to deploy a terraform plan

## Chart Details

This chart will do the following:

* Generate a single tekton pipeline to deploy terraform plan to multiple environments

## Pre-requisites

- Generate a unique and secure webhook secret. Assign the secret to `githubWebhookSecret` in your `values.yaml` file  

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/ocp-tkn-terraform-pipeline
```

## Configuration

The following tables list the configurable parameters of the ocp-terraform-pipeline chart and their default values.


| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `githubAccessToken`           | Personal access token to access private repository | ""                       |
| `githubWebhookSecret`     | Secret key - GitHub uses it to create a hash signature with each payload. This hash signature is included with the headers of each request as `X-Hub-Signature-25`. The intention is to calculate a hash using your `githubWebhookSecret`, and ensure that the result matches the hash from GitHub | ""                               |
| `pvc`         | Persistence Volume Claim  |                                                              |
| `pvc.storage`         | Storage Size  | `1Gi` |
| `pvc.storageClassName`         | Storage Class Name  | `netapp-file-standard` |
| `pvc.volumeMode`         | Volume Mode  | `Filesystem` |
| `serviceAccount` | The service account that holds git access token and used for cloning private repo |                                                 |
| `serviceAccount.create` | The service account used for cloning the private repository  |`true`|
| `serviceAccount.annotations` | The service account used for cloning the private repository  |{}|
| `serviceAccount.name` | The service account used for cloning the private repository  |""|
| `npmPackageRef`         | The NPM package that holds the terraform configuration | `bcgov-dss/api-serv-infra` |
| `pipelineRunsRetentionDays` | The pipelineruns are kept upto the number of days | `5` |
| `terraformConfig`         | Terraform configuration |      |
| `terraformConfig.sourceFolder` | Folder that contains terraform source code |  |
| `terraformConfig.pgUser` | Username of the database owner that holds terraform state |      |
| `terraformConfig.pgPassword` | Password of the database owner that holds terraform state |      |
| `terraformConfig.pgInstance` | Postgres instance name |                          |
| `terraformConfig.releaseNamespace         ` | The namespace where the apps to be deployed |      |
| `terraformConfig.environments` | A map object containing key value pairs, where key is the environment name and value is an object that holds environment specific properties | <pre>dev:<br>  gitBranch: "deploy/dev"<br>  pgDatabase: "terraform_dev"</pre> |
| `terraformConfig.environments['<ENVIRONMENT_NAME>']` | `<ENVIRONMENT_NAME>` is the name of the environment (ex.: dev, test or prod) | `dev` |
| `<ENVIRONMENT_NAME>.gitBranch` | The github branch that has the `package-tag` file containing the version to deploy | `deploy/dev` |
| `<ENVIRONMENT_NAME>.pgDatabase` | Database that hold environment specific terraform state | `terraform_dev` |
| `notifications.enabled` | Enable failure notifications | `false` |
| `notifications.msteams.webhook` | MS Teams Webhook URL | |
| `notifications.title` | Notification message title | |
| `notifications.ocp4Link` | Openshift link | `silver`: https://console.apps.silver.devops.gov.bc.ca<br> `gold`: https://console.apps.gold.devops.gov.bc.ca |
| `notifications.type` | Type of notifications | `all`: sends all notifications<br>`failed`: sends only failed notifications |

## Create a webhook

- Navigate to `https://github.com/<YOUR-GIT-REPO>/settings/hooks`
- Click on `Add webhook`
- Navigate to your OCP namespace and under routes, use host from `el-my-release-ocp-tkn-terraform-pipeline-listener-route` as payload URL
- Use `githubWebhookSecret` from your `values` file as the secret 
- Since this pipeline supports only push events, choose `Just the push event` option
- Click `Add webhook`

## Grant `Pipeline` Service Account Acesss to Environment Projects

```bash
export tools=<TOOLS_NAMESPACE>

oc -n $tools policy add-role-to-user admin system:serviceaccount:$tools:pipeline

export project=<DEV_NAMESPACE>
oc -n $project policy add-role-to-user admin system:serviceaccount:$tools:pipeline

export project=<TEST_NAMESPACE>
oc -n $project policy add-role-to-user admin system:serviceaccount:$tools:pipeline

export project=<PROD_NAMESPACE>
oc -n $project policy add-role-to-user admin system:serviceaccount:$tools:pipeline
```
## Supplemental Vault inputs

`tasks.installSourceCode.annotations` (default `{}`) adds annotations only to
`install-source-code` through the generated PipelineRun's
`taskRunSpecs[].metadata.annotations`. Confirm the installed Tekton CRD supports
this field. Manually created PipelineRuns need equivalent task metadata.
Annotations are rendered literally with `toYaml`, not Helm `tpl`.

`tasks.installSourceCode.vaultInputPath` (default `""`) is an optional readable
path to JSON compatible with the existing `../../scripts/split-tfvars.js` in the
installed source package. Use the same shape as a Kubernetes Secret: a `data`
object with base64-encoded string values. Dotted keys represent map entries:

```json
{
  "data": {
    "example": "dmF1bHQ=",
    "vault_only": "c3VwcGxlbWVudA=="
  }
}
```

The chart invokes the existing splitter directly against this input, generating
`000-vault.auto.tfvars` in the Terraform source folder. It continues generating
`terraform.secret.auto.tfvars` from the existing Kubernetes Secret. The apply
task is unchanged; Terraform loads both files automatically.

Terraform loads `terraform.tfvars` and `terraform.tfvars.json` before auto-tfvars,
then loads `*.auto.tfvars` / `*.auto.tfvars.json` in lexical order. Consequently,
`terraform.secret.auto.tfvars` overrides `000-vault.auto.tfvars` for duplicate
variables. Other auto-tfvars follow their filenames' lexical order. Plain
`terraform.tfvars` and `TF_VAR_*` environment values do not override the Vault
auto-tfvars file. Explicit CLI `-var-file` / `-var` arguments take precedence.
Maps/objects are replaced as whole variables, not merged by nested key.

Example configuration stores the full Secret-shaped JSON document in Vault's
`tfvars_json` field; substitute your existing role and secret path:

```yaml
tasks:
  installSourceCode:
    vaultInputPath: /vault/secrets/terraform-inputs.json
    annotations:
      vault.hashicorp.com/agent-inject: "true"
      vault.hashicorp.com/agent-pre-populate-only: "true"
      vault.hashicorp.com/role: terraform-pipeline
      vault.hashicorp.com/agent-inject-secret-terraform-inputs.json: secret/data/terraform
      vault.hashicorp.com/agent-inject-template-terraform-inputs.json: |
        {{- with secret "secret/data/terraform" -}}
        {{ .Data.data.tfvars_json }}
        {{- end }}
```

The Vault role must authorize the install task's service account (`pipeline` in
this chart) and namespace. `serviceAccount.name` controls the clone service
account only. Use init-only injection for this finite task and confirm injector
networking and OpenShift security-context compatibility.

A configured missing/unreadable input or splitter failure stops the source task.
The supplemental output is mode 0600 and remains on the shared PVC like existing
secret tfvars; restrict workspace access and retain normal cleanup. The next
source install clears its package directory. No supplemental output is generated
when the input path is empty. Compatibility and supported value types are those
of the existing source package's splitter; this chart does not add a second parser.

Run `helm lint charts/ocp-tkn-terraform --set serviceAccount.name=terraform` and
`python3 charts/ocp-tkn-terraform/tests/test_vault_inputs.py` (Helm, Node.js,
Terraform and Python PyYAML required). Tests take the existing splitter path via
`SPLIT_TFVARS_SCRIPT`. Verify Pod annotations, Vault init completion, generated
files, precedence and pipeline completion in a test cluster before production.

### Source-package splitter compatibility

The currently inspected api-serv-infra `terraform/scripts/split-tfvars.js`
helper omits a closing brace when its final sorted key is a dotted map entry.
A certificate-only payload containing `ssl_certs.sdx-crt` / `ssl_certs.sdx-key`
therefore produces invalid HCL. Correct that helper in the source package before
using such inputs; chart 2.0.7 deliberately reuses it without a second parser or
an implicit repair. The helper also owns base64 decoding, trimming and string
escaping behavior. Validate its generated tfvars with your actual input shape.
