# ocp-terraform-pipeline Terraform

Helm chart to create a pipeline on OCP to use jenkins to deploy a terraform plan

## Chart Details

This chart will do the following:

* Deploy A pipeline to deploy using terraform with jenkins
* Deploy Jenkins if it is not already deployed (OCP does this not in this chart)

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
| `chart.name           `           | Name of the chart to deploy          | metadata-curator                          |
| `chart.repo           `           | Repo where the chart can be found    | http://bcgov.github.io/helm-charts        |
| `webhookKey           `           | Key to add to the webhook to trigger pipeline | "12345678"                       |
| `releaseName           `          | Helm release name to create/use      | mc                                        |
| `releaseNamespace           `     | Helm namespace to release to         | mc                                        |
| `deployValues           `         | Object containing values the helm chart needs | {example: value}                 |
