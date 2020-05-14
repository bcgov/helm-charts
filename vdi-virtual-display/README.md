# VDI Virtual Display Hub Helm Chart

VDI Virtual Display Hub Helm Chart

## Chart Details

This chart will do the following:

* Deploy the Virtual Display Hub to the cluster

This chart is based on the Zero-to-Jupyterhub chart found here: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/tree/master/jupyterhub


## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/vdi-virtual-display
```

## Configuration

The following tables list the configurable parameters of the Forum-Api chart and their default values.

For `hub.*`, `singleuser.*`, `auth.*` and `proxy.*` references, you can get further detail: https://zero-to-jupyterhub.readthedocs.io/en/latest/reference/reference.html#helm-chart-configuration-reference



| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| **HUB**                                                                 |
| `hub.service.type    `                | What type of service to use          | `ClusterIP `                                |
| `hub.service.ports.nodePort    `             | What port should be exposed when type is NodePort | `80`                                        |
| `hub.baseUrl    `                | Base path         | `/`                                 |
| `hub.cookieSecret    `                | A 64-byte cryptographically secure randomly generated string used to sign values of secure cookies set by the hub        |                                  |
| `hub.initContainers    `                | Add custom init containers       |                                  |
| `hub.uid    `                | User ID that the container will be run with       |    `1000`                              |
| `hub.fsGid    `                | The gid the hub process should be using when touching any volumes mounted.    |      `1000`                            |
| `hub.nodeSelector    `                | Node Selection criteria     |                                  |
| `hub.concurrentSpawnLimit    `                | Maximum number of spawned applications running at one time      |   `64`                               |
| `hub.consecutiveFailureLimit    `                | Maximum number of consecutive failures to allow before shutting down JupyterHub.     |         `5`                         |
| `hub.deploymentStrategy.type    `                | The deployment strategy to use to replace existing pods with new ones.      |        `Recreate`                          |
| `hub.db.type    `                | Type of database for persistence storage     |       `sqlite-pvc`                           |
| `hub.db.user    `                | User ID for access to database     |                                  |
| `hub.db.password    `                | Password for access to database     |                               |
| `hub.db.pvc.storage    `                | Storage size for the database   |       `1Gi`                         |
| `hub.db.pvc.storageClassName    `                | Storage class for the database   |                                |
| `hub.db.pvc.accessModes    `                | Array of Kubernetes access modes  |     `[ReadWriteOnce]`                            |
| `hub.labels    `                | Extra labels to add to the hub pod.  |                               |
| `hub.annotations    `                | Extra annotations to add to the hub pod.  |                               |
| `hub.extraConfig    `                | If you want to configure Hub to do something specific that is not present here as an option, you can just write the raw Python to do it here.  |                               |
| `hub.extraEnv    `                | Extra environment variables to add to the hub pod.  |                               |
| `hub.extraContainers    `                | Extra containers to add to the hub pod.  |                               |
| `hub.extraVolumes    `                | Extra volumes to add to the hub pod.  |                               |
| `hub.extraVolumeMounts    `                | Extra volume mounts to add to the hub pod.  |                               |
| `hub.image.name    `                | Name of the Hub image  |                               |
| `hub.image.tag    `                | Tag for the Hub image  |                               |
| `hub.resources    `                   | Resource limits and requests         | `{}`                                        |
| `hub.networkPolicy.enabled    `                   | Enable custom network policy for Hub        | `false`                                       |
| `hub.allowNamedServers    `                   | Allow named servers to be used       | `false`                                       |
| `hub.namedServerLimitPerUser    `                   | Max number of named servers allowed per user       |                                        |
| `hub.livenessProbe.enabled    `                | Enable a liveness probe for the Hub pod  |  `false`                             |
| `hub.readinessProbe.enabled    `                | Enable a readiness probe for the Hub pod  |  `false`                             |
| **RBAC**                                                                 |
| `rbac.enabled    `                | Role-based access control Enabled |  `true`                             |
| **Proxy**                                                                 |
| `proxy.secretToken    `                | A 64-byte cryptographically secure randomly generated string used to secure communications between the hub and the configurable-http-proxy.  |                               |
| `proxy.service.type    `                | What type of service to use for the Proxy         | `LoadBalancer`                                 |
| `proxy.service.nodePorts.https    `             | What port should be exposed when type is NodePort |                                         |
| `proxy.chp.image.name   `             | Configurable http proxy image |  `jupyterhub/configurable-http-proxy`                                       |
| `proxy.chp.image.tag   `             | Configurable http proxy image tag |  `4.2.0`                                      |
| `proxy.chp.livenessProbe.enabled    `                | Enable a liveness probe for the Proxy pod  |  `true`                             |
| `proxy.chp.readinessProbe.enabled    `                | Enable a readiness probe for the Proxy pod  |  `true`                             |
| `proxy.chp.resources    `                   | Resource limits and requests for the Proxy         | `{}`                                        |
| **Authentication**                                                                 |
| `auth.type  `                   | Type of authentication       | `custom `                                      |
| `auth.state.enabled  `                   | Enable persisting auth_state (if available)      | `false`                                       |
| `auth.state.cryptoKey  `                   | auth_state will be encrypted and stored in the Hub’s database    |                                        |
| `auth.custom.className  `                   | The Python class that implements the custom authentication scheme    |                                        |
| `auth.custom.config.login_service  `                   | Custom configuration |       `keycloak`                                 |
| `auth.custom.config.client_id  `                   | Custom configuration |                                        |
| `auth.custom.config.client_secret  `                   | Custom configuration |                                        |
| `auth.custom.config.token_url  `                   | Custom configuration |                                        |
| `auth.custom.config.userdata_url  `                   | Custom configuration |                                        |
| `auth.custom.config.userdata_method  `                   | Custom configuration |                                        |
| `auth.custom.config.userdata_params  `                   | Custom configuration |                                        |
| **Singleuser**                                                                 |
| `singleuser.nodeSelector    `                | Node Selection criteria     |                                  |
| `singleuser.uid    `                | User ID that the virtual display process will be run with       |    `1000`                              |
| `singleuser.fsGid    `                | The gid the virtual display process should be using when touching any volumes mounted.    |      `1000`                            |
| `singleuser.startTimeout    `                | How long to wait for the virtual display process to start      |    `600`                              |
| `singleuser.storage.homeMountPath    `                | Path where the user's private storage is mounted      |    `/home/jovyan/work`                              |
| `singleuser.storage.type    `                | Type of storage      |   `dynamic`                           |
| `singleuser.storage.capacity    `                | Size of user's private storage      |    `2Gi `                             |
| `singleuser.memory.limit    `                | Set Memory limits & guarantees that are enforced for each user.     |    `8G`                             |
| `singleuser.memory.guarantee    `                | Set Memory limits & guarantees that are enforced for each user.     |    `1G`                              |
| `singleuser.cpu.limit    `                | Set CPU limits & guarantees that are enforced for each user.     |    `500m`                             |
| `singleuser.cpu.guarantee    `                | Set CPU limits & guarantees that are enforced for each user.     |    `250m`                              |
| `singleuser.initContainers    `                | Add custom init containers       |                                  |
| `singleuser.networkPolicy.enabled    `                | Enable a custom network policy     |      `false`                            |
| **Ingress**                                                                 |
| `ingress.enabled`                                                           | Enables Ingress                                                                                                    | `false`                         |
| `ingress.annotations`                                                       | Ingress annotations                                                                                                | `{}`                            |
| `ingress.path`                                                              | Path to access frontend                                                                                            | `/`                             |
| `ingress.hosts`                                                             | Ingress hosts                                                                                                      | `[]`                            |
| `ingress.tls`                                                               | Ingress TLS configuration                                                                                          | `[]`                            |

