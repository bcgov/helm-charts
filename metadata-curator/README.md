# Metadata-Curator Helm Chart

Metadata Curator Helm Chart

## Chart Details

This chart will do the following:

* Deploy Metadata Curator to the cluster

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/metadata-curator
```

## Configuration

The following tables list the configurable parameters of the Metadata-Curator chart and their default values.



| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `replicaCount    `                | How many pods to start up            | 1                                         |
| `feImage.repository`              | Where to pull the frontend image from | bcgovimages/metadata-curator-ui          |
| `feImage.tag`                     | Which tag to use                     | edge                                      |
| `feImage.pullPolicy`              | Pull Policy for the image            | IfNotPresent                              |
| `beImage.repository`              | Where to pull the frontend image from | bcgovimages/metadata-curator-api         |
| `beImage.tag`                     | Which tag to use                     | edge                                      |
| `beImage.pullPolicy`              | Pull Policy for the image            | IfNotPresent                              |
| `imagePullSecrets    `            | Name of secrets to pull images       | []                                        |
| `nameOverride    `                | Name override (helm)                 | ""                                        |
| `fullNameOverride    `            | Fullname override (helm)             | ""                                        |
| `serviceAccount.create    `       | Create a service account             | true                                        |
| `serviceAccount.name    `         | Name for service account if blank generate | ""                                  |
| `podSecurityContext    `          | Pod Security Context settings        | {}                                        |
| `securityContext    `             | Security Context settings            | {}                                        |
| `service.type    `                | What type of service to use          | ClusterIP                                 |
| `service.port    `                | What port should be exposed          | 80                                        |
| `ingress.enabled    `             | Create an ingress                    | false                                     |
| `ingress.annotations    `         | Annotations to add to the ingress    | {}                                        |
| `ingress.hosts[].host    `        | Name of host to run on               | chart-example.local                       |
| `ingress.hosts[].path    `        | List of paths for the ingress        | []                                        |
| `ingress.tls[].secretName    `    | Secret holding SSL information       | ''                                        |
| `ingress.tls[].hosts    `         | List of ssl hosts as per ingress.hosts | []                                      |
| `tls.enabled    `                 | Is TLS Enabled?                      | false                                     |
| `tls.crt    `                     | TLS Cert content                     | ""                                        |
| `tls.key    `                     | TLS Key content                      | ""                                        |
| `resources    `                   | Resource limits and requests         | {}                                        |
| `nodeSelector    `                | Node Selection criteria              | {}                                        |
| `tolerations     `                | Tolerations                          | []                                        |
| `affinity        `                | Affinity                             | {}                                        |
| `database.host        `           | Mongo DB Host                        | mc-formio-mongo.mc:27017                  |
| `database.username        `       | Mongo DB Username                    | forumApi                                  |
| `database.password        `       | Mongo DB Password                    | password                                  |
| `database.dbName        `         | Mongo DB Collection Name             | oc_db                                     |
| `sessionSecret   `                | The secret to hash sessions with     | secret                                    |
| `frontend        `                | The full url to reach the frontend   | http://127.0.0.1:3000                     |
| `oidc.issuer     `                | Issuer for your SSO connection       | issuer                                    |
| `oidc.authorizationURL `          | Authorization url for your SSO connection       | authurl                        |
| `oidc.tokenURL     `              | Token Url for your SSO connection    | tokenUrl                                  |
| `oidc.userInfoURL     `           | User Info Url for your SSO connection | userInfoUrl                              |
| `oidc.clientID     `              | Client Id for your SSO connection       | clientId                               |
| `oidc.clientSecret    `           | Client Secret for your SSO connection       | clientSecret                       |
| `oidc.callbackURL     `           | Callback Url -- should be frontend+/api/callback | callbackUrl                   |
| `uploadUrl   `                    | Full url for tusd including /files     | mc-storage-api.mc                       |
| `base64EncodedPGPPublicKey   `    | Base64 encoded PGP Key to encrypt with | b64Here                                 |
| `approverGroups   `               | List of group names for approver groups | [metadata_approver_1, metadata_approver 2] |
| `alwaysNotifyList   `             | List of businessCategory to email info  | **                                     |
| `alwaysNotifyList.business_category_1` | List of name emails to notify for businessCategory 1 | **                   |
| `alwaysNotifyList.business_category_1.name` | Name of person emailing       | **                                     |
| `alwaysNotifyList.business_category_1.email` | email of person emailing     | **                                     |
| `email.enabled   `                | Whether email is enabled or not        | false                                   |
| `email.service   `                | Email service url                      | smtp.gmail.com                          |
| `email.secure   `                 | Is Email Service secure?               | true                                    |
| `email.port   `                   | Port to use for email                  | 465                                     |
| `email.user   `                   | Username for email service             | ""                                      |
| `email.pass   `                   | Password for email service             | ""                                      |
| `email.from   `                   | Who the email should be from           | mc@example.com                          |
| `email.subject   `                | Subject line for the email             | Data Upload Update                      |
| `forum-api   `                    | Forum-api helm chart values            | [Forum-Api](/forum-api/README.md)       |
| `storage-api   `                  | Storage-api helm chart values          | [Storage-Api](/storage-api/README.md)   |
| `formio   `                       | Formio helm chart values               | [Formio](/formio/README.md)             |