# ocp-tkn-terraform-pipeline Terraform

Helm chart to create a pipeline on OCP to use Tekton to deploy a terraform plan

## Chart Details

This chart will do the following:

* Deploy A pipeline to deploy using terraform with Tekton

## Pre-requisites

- Generate a unique and secure webhook secret. Assign the secret to `githubWebhookSecret` in your `values` file  

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
| `githubAccessToken`           | Key to add to the webhook to trigger pipeline | "12345678"                       |
| `githubWebhookSecret`     | Helm namespace to release to         | xxxxx-dev                                 |
| `pvc`         | Version of the Terraform CLI | 0.12.29    |
| `serviceAccount` | The Postgres backend connection details | "conn_str=postgres://[USER]:[PSWD]@[HOST]/[DATABASE]?sslmode=disable"    |
| `npmPackageRef`         | Folder in the package that contains the terraform configuration | terraform/workspaces/dev     |
| `terraformConfig           `         | The NPM package that holds the terraform configuration | @bcgov-dss/api-serv-infra     |
| `deployRepo           `         | The repo that holds the deployment release versions | https://github.com/bcgov-dss/api-serv-infra.git     |
| `deployBranch         `         | The branch that has the `package-tag` file containing the version to deploy | deploy/dev     |
| `githubAccessToken`         | Token for accessing the `bcgov-dss/api-serv-infra` repository | deploy/dev     |

## Create a webhook

- Navigate to `https://github.com/<YOUR-GIT-REPO>/settings/hooks`
- Click on `Add webhook`
- Use host from `el-my-release-ocp-tkn-terraform-pipeline-listener-route` as payload URL
- Use `githubWebhookSecret` from your `values` file as the secret 
- Since this pipeline supports only push events, choose `Just the push event` option
- Click `Add webhook`
