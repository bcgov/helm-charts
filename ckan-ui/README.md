# CKAN-UI Helm Chart

Ckan UI Helm Chart

## Chart Details

This chart will do the following:

* Deploy the Ckan UI to the cluster and an optional OCP pipeline

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/ckan-ui
```

## Configuration

The following tables list the configurable parameters of the Ckan-ui chart and their default values.



| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `replicaCount    `                | How many pods to start up            | 1                                         |
| `image.repository.frontend`       | Where to pull the frontend image from | bcgovimages/ckan-ui-frontend             |
| `image.repository.backend`        | Where to pull the backend image from | bcgovimages/ckan-ui                       |
| `image.tag    `                   | Which tag to use                     | stable                                    |
| `image.pullPolicy    `            | Pull Policy for Image                | IfNotPresent                              |
| `service.type    `                | What type of service to use          | ClusterIP                                 |
| `service.port    `                | What port should be exposed          | 80                                        |
| `ingress.enabled    `             | Create an ingress                    | false                                     |
| `ingress.annotations    `         | Annotations to add to the ingress    | {}                                        |
| `ingress.path    `                | Path for the ingress                 | /                                         |
| `ingress.hosts    `               | List of hostnames to run on          | [chart-example.local]                     |
| `ingress.tls    `                 | List tls information                 | []                                        |
| `ingress.tls[].secretName    `    | Secret holding SSL information       | ''                                        |
| `ingress.tls[].hosts    `         | List of ssl hosts as per ingress.hosts | []                                      |
| `resources    `                   | Resource limits and requests         | {}                                        |
| `nodeSelector    `                | Node Selection criteria              | {}                                        |
| `tolerations     `                | Tolerations                          | []                                        |
| `affinity        `                | Affinity                             | {}                                        |
| `openshiftCICD        `           | Deploy an Openshift pipeline         | False                                     |
| `tillerNamespace        `         | Namespace for the pipeline           | TILLER                                    |
| `repo.tag        `                | What to tag the pipeline image as    | latest                                    |
| `repo.ref        `                | What github branch to use            | master                                    |
| `repo.url        `                | What github url to use               | https://github.com/bcgov/ckan-ui          |
| `webhookKey        `              | Webhook key to restrict pipeline trigger | 12345678                              |
| `solr        `                    | The full url to solr                 | http://127.0.0.1:8983/solr                |
| `solrCore        `                | The name of the ckan core in solr    | ckan                                      |
| `ckan            `                | Full url to reach ckan at            | https://127.0.0.1:5000                    |
| `frontend        `                | The full url to reach the frontend   | http://127.0.0.1:3000                     |
| `sessionSecret   `                | The secret to hash sessions with     | secret                                    |
| `classicUi       `                | Where to reach the old ckan ui at    | http://127.0.0.1:5000                     |
| `oidc.issuer     `                | Issuer for your SSO connection       | issuer                                    |
| `oidc.authorizationURL `          | Authorization url for your SSO connection       | authurl                        |
| `oidc.tokenURL     `              | Token Url for your SSO connection    | tokenUrl                                  |
| `oidc.userInfoURL     `           | User Info Url for your SSO connection | userInfoUrl                              |
| `oidc.clientID     `              | Client Id for your SSO connection       | clientId                               |
| `oidc.clientSecret    `           | Client Secret for your SSO connection       | clientSecret                       |
| `oidc.callbackURL     `           | Callback Url -- should be frontend+/api/callback | callbackUrl                   |
| `pow.past_orders_nbr        `     | Pow Setting                          | 0                                         |
| `pow.custom_aoi_url         `     | Pow Setting                          | http://maps.gov.bc.ca/                    |
| `pow.persist_config         `     | Pow Setting                          | true                                      |
| `pow.enable_mow             `     | Pow Setting                          | False                                     |
| `pow.public_url             `     | Pow Setting                          | publicPowUrl                              |
| `pow.secure_url             `     | Pow Setting                          | securePowUrl                              |
| `pow.ui_path         `            | Pow Setting                          | UIPath                                    |
| `pow.order_source           `     | Pow Setting                          | bcdc                                      |
| `pow.order_details.aoi_type `     | Pow Setting                          | 0                                         |
| `pow.order_details.aoi      `     | Pow Setting                          | 'null'                                    |
| `pow.order_details.clipping_method_type_id` | Pow Setting                | 0                                         |
| `pow.order_details.ordering_application` | Pow Setting                   | BCDC                                      |
| `pow.order_details.format_type`   | Pow Setting                          | 3                                         |
| `pow.order_details.csr_type `     | Pow Setting                          | 4                                         |
| `pow.order_details.metadata_url`  | Pow Setting                          | "https://catalogue.data.gov.bc.ca/dataset/" |
| `ofi.api.convert_to_single_res`   | OFI Setting                          | true                                      |
| `ofi.api.dev_secure_call`         | OFI Setting                          | true                                      |
| `ofi.api.public_url           `   | OFI Setting                          | publicOfiUrl                              |
| `ofi.api.secure_url           `   | OFI Setting                          | secureOfiUrl                              |
| `googleAnalytics.enabled      `   | Enable Google Analytics Tracking     | "false"                                   |
| `googleAnalytics.id           `   | Google Analytics Tracking Id         | "UA-XXX-X"                                |
| `snowplow.enabled             `   | Enable Snowplow Tracking             | "false"                                   |
| `snowplow.collector             ` | Snowplow Tracking Collctor Url       | snowPlowCollectorUrl                      |
| `snowplow.proto                 ` | Snowplow Tracking Protocol for url   | http                                      |
| `snowplow.port                 `  | Snowplow Tracking Port for url       | 8080                                      |
| `snowplow.appId                `  | Snowplow Tracking AppId              | ckan                                      |
| `authGroupSeperator            `  | What delimits groups in jwts ie org/admin | /                                    |
| `sysAdminGroup                 `  | sysadmin group name (ckan)           | admin                                     |
