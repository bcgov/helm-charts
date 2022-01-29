# Tekton Pipelines Helm Chart

Tekton Pipelines Helm Chart for OCP

## Chart Details

This chart will do the following:

* Deploy A Tekton pipeline to suit your needs as you configure based on the values.

## Examples
Examples are available in the [examples](/charts/tekton-pipelines/examples) directory, if you have examples you can share please make a PR.

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/tekton-pipelines
```

## Configuration

The following tables list the configurable parameters of the Metadata-Curator chart and their default values.



| Parameter                         | Description                           | Default                                  |
| --------------------------------- | ------------------------------------  | ---------------------------------------- |
| `serviceAccountName`              | Which Service Account to use          | build-bot                                |
| `nameOverride      `              | Override the name of deploy with      | ""                                       |
| `fullnameOverride`                | Override the name of deploy with      | ""                                       |
| `tasks`                           | [See Task Block Below](#tasks)        | [See Task Block Below](#tasks)           |
| `pipelines`                       | [See Pipeline Block Below](#pipelines)| [See Pipeline Block Below](#pipelines)   |
| `events`                          | [See Events Block Below](#events)     | [See Events Block Below](#events)        |


### Tasks

These are the configurable values for the tasks array, these will create new tasks in your namespace

| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `name              `              | The name for the task                | helm3-spark                               |
| `volumes              `           | Array of volumes to be mounted       | nil                                       |
| `steps             `              | Array of steps that make up the task | Array of size 1 object described below    |
| `steps[0].name     `              | Name for this step                   | install-spark                             |
| `steps[0].image     `             | The container image to use for this step | alpine/helm:3.0.2                     |
| `steps[0].command   `             | The command to run in the container  | [/bin/ash, -c, helm repo add...]          |
| `steps[0].volumeMounts   `        | Specifies mountPath for volumes      | nil                                       |
| `steps[0].resources   `           | Can supply requests/limits memory and cpu | nil                                  |

### Pipelines

These are the configurable values for the pipelines array, these will create new pipelines in your namespace

| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `name              `              | The name for the pipeline            | spark-pipeline                            |
| `triggerName       `              | Trigger Name to create for this pipeline (for events) | spark-trigger-template   |
| `bindingName    `                 | Binding Name for pipeline andtrigger | spark-binding                             |
| `workspaces[].name   `            | Name of workspace to make available  | nil                                       |
| `workspaces[].workspace `         | Workspace to make available          | nil                                       |
| `workspaces[].persistentVolumeClaim ` | PVC name for workspace           | emptyDir                                  |
| `workspaces[].podTemplate `       | Override default pod template, e.g. securityContext | nil                        |


| `tasks     `                      | Array of tasks to run                | Arary of size 1 described below           |
| `tasks[0].name   `                | Name of task in pipeline             | create-namespace                          |
| `tasks[0].ref.name   `            | Name of task to run                  | create-namespace                          |
| `tasks[0].ref.kind   `            | Type of task set to ClusterTask for non namespace task | nil                     |
| `tasks[0].workspaces[].name   `   | Name of workspace for task           | nil                                       |
| `tasks[0].workspaces[].workspace` | Name of workspace to use             | nil                                       |
| `tasks[0].params[].name   `       | Name of task parameter               | nil                                       |
| `tasks[0].params[].value   `      | Value of parameter                   | nil                                       |
| `pipeline_params[].name   `       | Name of pipeline parameter shared across multiple tasks | nil                    |
| `pipeline_params[].default   `    | Default value of pipeline parameter shared across multiple tasks | ''            |
| `pipeline_params[].type   `       | Type of pipeline parameter shared across multiple tasks: string/array | string   |
| `pipeline_params[].incomingValue` | JSONPath string used by TemplateBinding to extract value from WebHook | nil     |
| `pipeline_params[].resourceTemplate` | Used to assign value to parameter in TemplateTrigger  | nil                   |

### Events

These are the configurable values for the events array, these will create new trigger templates, bindings, listeners, services and ingresses in your namespace

| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `install              `           | Install events                       | true                                      |
| `defaultRB       `                | Create RB for default to allow edit  | false                                     |
| `token    `                       | Value to store in secret for webhooks (currently unused) | token                 |
| `listeners   `                    | Array of listeners to create         | Array of size 1 described below           |
| `listeners[].name `               | Name of listener to create           | ds-infra-listener                         |
| `listeners[].triggers     `       | Array of triggers for this listener  | Arary of size 1 described below           |
| `listeners[].triggers[].trigger`  | Name of trigger to fire              | spark-trigger-template                    |
| `listeners[].triggers.binding `   | Name of binding to use               | spark-binding                             |
| `listeners[].triggers.interceptors ` | Array of trigger [interceptors](https://tekton.dev/vault/triggers-main/interceptors/)     | Empty array                               |
| `listeners[].ingress   `          | Ingress options for listener         | See below                                 |
| `listeners[].ingress.enabled`     | Ingress enabled                      | true                                      |
| `listeners[].ingress.name`        | Ingress name                         | spark-pipeline-ingress                    |
| `listeners[].ingress.annotations` | Ingress annotations                  | kubernetes.io/ingress.class: nginx        |
| `listeners[].ingress.path`        | Ingress path                         | /                                         |
| `listeners[].ingress.hosts`       | Ingress hosts array                  | Array of size 1 described below           |
| `listeners[].ingress.hosts[].name` | Ingress hosts name (url without proto) | chart.example.local                    |
| `listeners[].ingress.hosts[].service` | Ingress service to use           | el-RELEASE-NAME-el                        |
| `listeners[].ingress.hosts[].port` | Ingress port to use (should be 8080) | 8080                                     |
