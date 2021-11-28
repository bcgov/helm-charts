# ocp-tkn-terraform-pipeline Terraform

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
| `pvc.storage`         | Persistence Volume Claim  | `1Gi` |
| `pvc.storageClassName`         | Persistence Volume Claim  | netapp-file-standard |
| `pvc.volumeMode`         | Persistence Volume Claim  | Filesystem |
| `serviceAccount` | The service account that holds git access token and used for cloning the private repository |                                                 |
| `serviceAccount.create` | The service account used for cloning the private repository  |true|
| `serviceAccount.annotations` | The service account used for cloning the private repository  |{}|
| `serviceAccount.name` | The service account used for cloning the private repository  |""|
| `npmPackageRef`         | The NPM package that holds the terraform configuration | bcgov-dss/api-serv-infra |
| `terraformConfig`         | Terraform configuration |      |
| `terraformConfig.sourceFolder` | Folder that contains terraform source code |  |
| `terraformConfig.pgUser` | Username of the database owner that holds terraform state |      |
| `terraformConfig.pgPassword` | Password of the database owner that holds terraform state |      |
| `terraformConfig.pgInstance` | Postgres instance name |                          |
| `terraformConfig.releaseNamespace         ` | The namespace where the apps to be deployed |      |
| `terraformConfig.environments` | A map object containing key value pairs, where key is the environment name and value is an object that holds environment specific properties | [dev: [gitBranch: "deploy/dev", gitTriggerBranch: "dev", pgDatabase: "terraform_dev"]] |
| `terraformConfig.environments['ENVIRONMENT_NAME']` | `ENVIRONMENT_NAME` is the name of the environment (ex.: dev, test or prod) | dev |
| `gitBranch` | The github branch that has the `package-tag` file containing the version to deploy | deploy/dev |
| `gitTriggerBranch` (optional) | The github branch that triggers webhook. Leave it empty if same as `gitBranch` | dev |
| `pgDatabase` | Database that hold environment specific terraform state | terraform_dev |

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