# Userguide Bridge Helm Chart

Userguide Bridge Helm Chart

## Chart Details

This chart will do the following:

* Deploy the Userguide Bridge to the cluster

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/userguide-bridge-api
```

## Configuration

The following table list the configurable parameters of the Userguide Bridge chart and their default values.


| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `replicaCount    `                | How many pods to start up            | 1                                         |
| `image.repository`                | Where to pull the  image from | quay.io/ikethecoder/vdi-userguide-bridge-api                    |
| `image.tag`                       | Which tag to use                     | edge                                      |
| `image.pullPolicy`                | Pull Policy for the image            | IfNotPresent                              |
| `service.type    `                | What type of service to use          | ClusterIP                                 |
| `service.port    `                | What port should be exposed          | 80                                        |
| `ingress.enabled    `             | Create an ingress                    | false                                     |
| `ingress.annotations    `         | Annotations to add to the ingress    | {}                                        |
| `ingress.hosts[].host    `        | Url for host  to run on              | chart-example.local                       |
| `ingress.hosts[].paths    `        | Paths to run on              | `/`                    |
| `ingress.tls[].secretName    `    | Secret holding SSL information       | ''                                        |
| `ingress.tls[].hosts    `         | List of ssl hosts as per ingress.hosts | []                                      |
| `userguide.logLevel    `         | Log level for application | `INFO`                                     |
| `userguide.helpApiHost    `         | The Documize endpoint for sourcing the content |                                     |
| `userguide.helpApiToken    `         | The Documize token for sourcing the content |                                     |
| `userguide.helpApps    `         | A list of tags that will be used to filter content |            `\"bbsae\",\"ocwa\"`                         |
| `userguide.corsWhitelist    `         | A list of domains for doing CORS checks | `\"*\"`                                    |
| `resources    `                   | Resource limits and requests         | {}                                        |
| `nodeSelector    `                | Node Selection criteria              | {}                                        |
| `tolerations     `                | Tolerations                          | []                                        |
| `affinity        `                | Affinity                             | {}                                        |
