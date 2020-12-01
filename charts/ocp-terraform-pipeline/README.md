# ocp-terraform-pipeline Terraform

Helm chart to create a pipeline on OCP to use jenkins to deploy a terraform plan

## Chart Details

This chart will do the following:

* Deploy A pipeline to deploy using terraform with jenkins
* Deploy Jenkins if it is not already deployed (OCP does this not in this chart (only in OCP3))

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/ocp-terraform-pipeline
```

## Configuration

The following tables list the configurable parameters of the ocp-terraform-pipeline chart and their default values.



| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `webhookKey           `           | Key to add to the webhook to trigger pipeline | "12345678"                       |
| `releaseNamespace           `     | Helm namespace to release to         | xxxxx-dev                                 |
| `terraformVersion`         | Version of the Terraform CLI | 0.12.29    |
| `terraformBackendPostgresql` | The Postgres backend connection details | "conn_str=postgres://[USER]:[PSWD]@[HOST]/[DATABASE]?sslmode=disable"    |
| `terraformFolder`         | Folder in the package that contains the terraform configuration | terraform/workspaces/dev     |
| `packageRef           `         | The NPM package that holds the terraform configuration | @bcgov-dss/api-serv-infra     |
| `deployRepo           `         | The repo that holds the deployment release versions | https://github.com/bcgov-dss/api-serv-infra.git     |
| `deployBranch         `         | The branch that has the `package-tag` file containing the version to deploy | deploy/dev     |
| `githubAccessToken`         | Token for accessing the `bcgov-dss/api-serv-infra` repository | deploy/dev     |

