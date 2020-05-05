# Formio Helm Chart

Formio Helm Chart

## Chart Details

This chart will do the following:

* Deploy Formio to the cluster

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/formio
```

## Configuration

The following tables list the configurable parameters of the Forum-Api chart and their default values.



| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `replicaCount    `                | How many pods to start up            | 1                                         |
| `image.repository`                | Where to pull the frontend image from | bcgovimages/forum-api                    |
| `image.tag`                       | Which tag to use                     | edge                                      |
| `image.pullPolicy`                | Pull Policy for the image            | IfNotPresent                              |
| `service.type    `                | What type of service to use          | ClusterIP                                 |
| `service.port    `                | What port should be exposed          | 80                                        |
| `apiPort    `                     | Port the api runs on                 | 3000                                      |
| `logLevel    `                    | Api Log Verbosity Level              | error                                     |
| `global.jwtSecret    `            | Secret JWT is signed with            | ssh this is a secret                      |
| `database.host        `           | Mongo DB Host                        | mc-formio-mongo.mc:27017                  |
| `database.username        `       | Mongo DB Username                    | forumApi                                  |
| `database.password        `       | Mongo DB Password                    | password                                  |
| `database.dbName        `         | Mongo DB Collection Name             | oc_db                                     |
| `username    `                    | Formio admin username                | admin@example.com                         |
| `password    `                    | Formio admin password                | CHANGEME                                  |
| `nodeConfig  `                    | Formio pod nodeConfig env var content | '{\"mongo\": \"mongodb://forumApi:password@ocwa-formio-mongo.ocwa:27017/formioapp\", \"jwt\": { \"secret\": \"ssh this is a secret\" } }' |



| `ingress.enabled    `             | Create an ingress                    | false                                     |
| `ingress.annotations    `         | Annotations to add to the ingress    | {}                                        |
| `ingress.path    `                | Path for the ingress                 | /                                         |
| `ingress.hosts[].name    `        | Url for host  to run on              | chart-example.local                       |
| `ingress.hosts[].service    `     | Service to link with                 | ocwa-forum-api-ws                         |
| `ingress.hosts[].port    `        | Port to expose on                    | 3001                                      |
| `ingress.tls[].secretName    `    | Secret holding SSL information       | ''                                        |
| `ingress.tls[].hosts    `         | List of ssl hosts as per ingress.hosts | []                                      |

| `wsPort    `                      | Port WS runs on                      | 3001                                      |



| `defaultAccessIsGroup    `        | Default Access Is Group (as opposed to individual) | true                        |
| `requiredRoleToCreateTopic    `   | Require Role to create topic         | exporter                                  |
| `ignoreGroups    `                | String of comma delimited groups to ignore for access | ["\"/oc\""]              |
| `adminGroup    `                  | Admin permission group level           | admin                                   |
| `user.idField    `                | Which field in JWT to use as id        | Email                                   |
| `user.emailField    `             | Which field in JWT to use as email     | Email                                   |
| `user.givenNameField    `         | Which field in JWT to use as first name | GivenName                              |
| `user.surNameField    `           | Which field in JWT to use as last name | Surname                                 |
| `user.groupField    `             | Which field in JWT to use as groups    | Groups                                  |
| `createDatabase    `              | Create database pod?                   | true                                    |
| `storageClassName    `            | Which storage class to use for PVCs    | default                                 |
| `storageClassAnnotations  `       | Annotations for the storage            | {volume.beta.kubernetes.io/storage-provisioner: netapp.io/trident} |
| `dbPod.persistence    `           | Which folder to persist                | /data/db                                |
| `dbPod.adminEnv    `              | Admin environment variable name        | MONGO_INITDB_ROOT_USERNAME              |
| `dbPod.admin    `                 | Admin username (value of above var)    | root                                    |
| `dbPod.passEnv    `               | Admin pass environment variable name   | MONGODB_ADMIN_PASSWORD                  |
| `dbPod.pass    `                  | Admin pass (value of above var)        | root                                    |
| `dbPod.dbEnv    `                 | ENV Var name for init database         | MONGO_INITDB_DATABASE                   |
| `dbPod.addAdminPassEnv    `       | Add admin environment to pod           | false                                   |
| `dbPod.adminPassEnv    `          | admin password env variable            | MONGODB_ADMIN_PASSWORD                  |
| `dbPod.initDb    `                | initialize database collection         | true                                    |
| `mongoImage.repository    `       | Image to use for mongo db if making db | mongo                                   |
| `mongoImage.tag    `              | Tag to use for above image             | 4.1                                     |
| `resources    `                   | Resource limits and requests         | {}                                        |
| `nodeSelector    `                | Node Selection criteria              | {}                                        |
| `tolerations     `                | Tolerations                          | []                                        |
| `affinity        `                | Affinity                             | {}                                        |
