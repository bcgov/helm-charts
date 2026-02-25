# SOBA Helm Chart
This is a helm chart for deploying SOBA on Kubernetes or OpenShift. 
It includes configurable values for the docker image, service, replicas, resources, and ingress.

## Installation
helm install soba ./soba -f ../config/soba.yaml

## Values

The following table describes the configurable values of the soba helm chart.

| Parameter | Description | Default |
| --- | --- | --- |
| `be_image.repository` | Repository of the docker image | `quay.io/ikethecoder/soba` |
| `be_image.tag` | Tag of the docker image | `latest` |
| `be_image.pullPolicy` | Pull policy for the docker image | `IfNotPresent` |
| `fe_image.repository` | Repository of the docker image | `quay.io/ikethecoder/soba` |
| `fe_image.tag` | Tag of the docker image | `latest` |
| `fe_image.pullPolicy` | Pull policy for the docker image | `IfNotPresent` |
| `service.type` | Type of service to use | `ClusterIP` |
| `service.port` | Port number to expose | `80` |
| `replicaCount` | Number of replicas to run | `1` |
| `resources.requests.cpu` | Maximum number of CPU cores to allocate to each pod | `0.5` |
| `resources.requests.memory` | Maximum amount of memory to allocate to each pod | `128Mi` |
| `resources.limits.cpu` | Minimum number of CPU cores to allocate to each pod | `0.5` |
| `resources.limits.memory` | Minimum amount of memory to allocate to each pod | `128Mi` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.hosts` | List of ingress hosts | `[{"host": "soba.bc.gov", "paths": ["/"]}]` |
| `ingress.tls` | List of ingress TLS configurations | `[{"hosts": ["soba.bc.gov"], "secretName": "soba-tls"}]` |
