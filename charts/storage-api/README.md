# Storage-Api Helm Chart

Storage Api Helm Chart

## Chart Details

This chart will do the following:

* Deploy Storage Api to the cluster

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/storage-api
```

## Configuration

The following tables list the configurable parameters of the Forum-Api chart and their default values.



| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `replicaCount    `                | How many pods to start up            | 1                                         |
| `access_key    `                  | S3 style access key for minio        | key                                       |
| `access_secret    `               | S3 style secret for minio            | secret                                    |
| `tus.image`                       | Image to use for tusd                | h3brandon/tusd_py3                        |
| `tus.tag`                         | Tag to use for above image           | latest                                    |
| `tus.bucket`                      | Bucket to use in minio               | bucket                                    |
| `tus.region `                     | S3 style region for tus likely irrelevant | us-east-1                            |
| `tus.jwtHook`                     | Validate JWTS (tus hook)             | true                                      |
| `caddy.image`                     | Image to use for caddy               | abiosoft/caddy                            |
| `caddy.tag`                       | Tag to use for above image           | no-stats                                  |
| `global.jwtSecret    `            | Secret JWT is signed with            | ssh this is a secret                      |
| `jwtAud`                          | Tus hook expected audience for jwt   | foo                                       |
| `minio.image`                     | Image to use for minio               | minio/minio                               |
| `minio.tag`                       | Tag for above image                  | latest                                    |
| `minio.server`                    | Run as a server (true) or gateway    | false                                     |
| `minio.serverPath`                | Path if running as a server to store data | /data                                |
| `minio.gatewayType`               | If running as a gateway what to      | azure                                     |
| `minio.proto`                     | Minio protocol                       | http                                      |
| `service.type    `                | What type of service to use          | ClusterIP                                 |
| `service.tusPort    `             | What port should be exposed for tusd | 80                                        |
| `service.minioPort    `           | What port should be exposed for minio | 9000                                     |
| `service.tusPort    `             | What port should be exposed for tusd | 80                                        |
| `ingress.enabled    `             | Create an ingress                    | false                                     |
| `ingress.annotations    `         | Annotations to add to the ingress    | {}                                        |
| `ingress.path    `                | Path for the ingress                 | /                                         |
| `ingress.hosts[].name    `        | Url for host  to run on              | chart-example.local                       |
| `ingress.hosts[].service    `     | Service to link with                 | ocwa-forum-api-ws                         |
| `ingress.hosts[].port    `        | Port to expose on                    | 3001                                      |
| `ingress.tls[].secretName    `    | Secret holding SSL information       | ''                                        |
| `ingress.tls[].hosts    `         | List of ssl hosts as per ingress.hosts | []                                      |
| `storageClassName    `            | Which storage class to use for PVCs  | default                                 |
| `storageClassAnnotations  `       | Annotations for the storage            | {volume.beta.kubernetes.io/storage-provisioner: netapp.io/trident} |
| `storageSize         `            | Size for PVC                         | 1Gi                                       |
| `resources    `                   | Resource limits and requests         | {}                                        |
| `nodeSelector    `                | Node Selection criteria              | {}                                        |
| `tolerations     `                | Tolerations                          | []                                        |
| `affinity        `                | Affinity                             | {}                                        |

