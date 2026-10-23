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
`taskRunSpecs[].metadata.annotations`. The installed Tekton CRD must support
that field. Manually created PipelineRuns must supply equivalent task metadata.
Annotation values are rendered literally with `toYaml`, not evaluated with
Helm `tpl`, so Vault templates remain intact.

`tasks.installSourceCode.vaultInputPath` (default `""`) optionally names a readable
absolute path in the source task containing a **JSON object** of Terraform
variable names and values. The existing Kubernetes Secret-to-tfvars processing
continues unchanged. With a path configured, a missing/unreadable file fails the
source task; invalid JSON/object keys fail before Terraform apply. There is no
silent fallback to stale data.

Example values (use your existing Vault auth role and secret path):

```yaml
serviceAccount:
  name: terraform

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
        {{ .Data.data | toJSON }}
        {{- end }}
```

The Vault role must authorize the task's service account (`pipeline` in the
current generated PipelineRun) and namespace. `serviceAccount.name` above
configures the clone service account; it does not change the install task's
identity. Confirm injector networking and OpenShift security-context compatibility.
Use init-only injection so a long-running Vault sidecar does not hold the task
open after its step exits.

The source task copies the JSON to a mode-0600 `.vault-inputs.json` file in the
Terraform source directory on the shared PVC. The apply task reads it and runs
Terraform with its values as `TF_VAR_*` environment defaults, without shell
evaluation or logging secret contents. Existing `TF_VAR_*` values override these
defaults. Terraform's standard tfvars files (including the generated
`terraform.secret.auto.tfvars`) override both. This preserves the normal order
among `terraform.tfvars`, JSON tfvars and lexically ordered auto-tfvars files.
Values are passed to the variable-consuming `terraform apply` command; init,
version and workspace commands do not need variable inputs.

Precedence is **per Terraform variable**, not per nested map key. For example,
if both Vault and the existing tfvars define `ssl_certs`, the tfvars map replaces
the entire Vault map. If individual certificate entries must be combined, use
separate Terraform inputs and an explicit `merge` in the consuming module.
Strings remain strings; numbers, booleans, lists and objects are JSON-encoded
for Terraform environment parsing.

The supplemental copy is removed when the apply script exits normally or with
an error. A killed pod or PVC failure may leave it behind; shared workspace access
must remain restricted and normal workspace cleanup must still run. This is
supplemental secret material on the same PVC already used for generated tfvars.
With the input path empty, the chart uses the original apply command.

Validate with `helm lint` and
`python3 charts/ocp-tkn-terraform/tests/test_vault_inputs.py` (requires Helm,
Node.js, Terraform and Python PyYAML). On a test cluster, verify generated
TaskRun/Pod annotations, Vault init completion, precedence and task completion
before upgrading the production chart. No Vault policy or live secret changes
are performed by installing the chart itself.
