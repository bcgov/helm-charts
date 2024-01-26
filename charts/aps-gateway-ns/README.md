# aps-gateway-ns

Use this helm chart to keep your API Gateway configuration updated.

## Getting Started

**Pre-requisites:**

- The `gwa` CLI (command line interface). You can download the latest version for your operating system from https://github.com/bcgov/gwa-cli/releases/latest

**Steps:**

Run `gwa login` with your IDIR credentials

Run `gwa namespace create`

The `generate-config` command can be used to setup a typical use case that includes:

- a vanity URL with SSL
- protected using the Common Single Signon (CSS) Keycloak Identity Provider using Oauth2 Client Credential Grant
- a draft product on our API Directory where people interested in your API can request access

```sh
gwa generate-config
```

This will produce a file `gw-config.yml` that includes resources for the Kong Gateway, the API Directory (DraftDataset and Product) and integrating to the CSS Keycloak Identity Provider (CredentialIssuer).

To update configuration, you must create a Service Account (SA) that has `Namespace.Manage`, `CredentialIssuer.Admin` and `GatewayConfig.Publish` permissions for the namespace that you created above. Go to https://api.gov.bc.ca/manager/namespaces , select your new namespace and go to `Service Accounts` to create the new SA.

You can then use that as part of the helm release:

```sh
helm upgrade --install \
  --set-file config=gw-config.yml \
  --set env.NAMESPACE.value=$NAMESPACE \
  --set env.CLIENT_ID.value=$CLIENT_ID \
  --set env.CLIENT_SECRET.value=$CLIENT_SECRET \
  myapi \
  bcgov/aps-gateway-ns
```
