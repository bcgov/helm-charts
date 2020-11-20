# Patroni Helm Chart

This directory contains a Kubernetes chart to deploy a five node [Patroni](https://github.com/zalando/patroni/) cluster using a [Spilo](https://github.com/zalando/spilo) and a StatefulSet.

## Prerequisites Details
* Kubernetes 1.5+
* PV support on the underlying infrastructure

## StatefulSet Details
* https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

## StatefulSet Caveats
* https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#limitations

## Todo
* Make namespace configurable

## Chart Details
This chart will do the following:

* Implement a HA scalable PostgreSQL 10 cluster using a Kubernetes StatefulSet.

## Build patroni for OpenShift,

```
oc new-build https://github.com/ll911/patroni.git --context-dir=kubernetes --strategy=docker --name=patroni
```

## Installing the Chart

```console
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm dependency update
$ helm install --generate-name bcgov/patroni
```

To install the chart with the release name `my-release`:

```console
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm dependency update
$ helm install my-release bcgov/patroni
```

## Connecting to PostgreSQL

Your access point is a cluster IP. In order to access it spin up another pod:

```console
$ kubectl run -i --tty --rm psql --image=postgres --restart=Never -- bash -il
```

Then, from inside the pod, connect to PostgreSQL:

```console
$ psql -U admin -h my-release-patroni.default.svc.cluster.local postgres
<admin password from values.yaml>
postgres=>
```

## Configuration

The following table lists the configurable parameters of the patroni chart and their default values. credential will be random generated in secrets

|       Parameter                   |           Description                       |                         Default                     |
|-----------------------------------|---------------------------------------------|-----------------------------------------------------|
| `nameOverride`                    | Override the name of the chart              | `nil`                                               |
| `fullnameOverride`                | Override the fullname of the chart          | `nil`                                               |
| `replicaCount`                    | Amount of pods to spawn                     | `3`                                                 |
| `image.repository`                | The image to pull                           | `image-registry.openshift-image-registry.svc:5000/bcgov/patroni`        |
| `image.tag`                       | The version of the image to pull            | `latest`                                            |
| `image.pullPolicy`                | The pull policy                             | `IfNotPresent`                                      |
| `credentials.superuser`           | Username of the superuser                   | `postgres`                                          |
| `credentials.admin`               | Username of the app admin                   | `app`                                               |
| `credentials.dbname`              | defaul created app dbname                   | `app`                                       |
| `credentials.replication`         | Password of the replication user            | `replication`                                       |
| `clusterName`                     | value for [PATRONI_SCOPE](https://patroni.readthedocs.io/en/latest/ENVIRONMENT.html#global-universal)              | `pgc`                                       |
| `kubernetes.enable`               | Using Kubernetes as DCS                     | `true`                                              |
| `kubernetes.ep.enable`            | Using Kubernetes endpoints                  | `false`                                             |
| `resources`                       | Any resources you wish to assign to the pod | `{}`                                                |
| `nodeSelector`                    | Node label to use for scheduling            | `{}`                                                |
| `tolerations`                     | List of node taints to tolerate             | `[]`                                                |
| `affinity`                        | Affinity settings                           | Preferred on hostname                               |
| `persistentVolume.accessModes`    | Persistent Volume access modes              | `[ReadWriteOnce]`                                   |
| `persistentVolume.annotations`    | Annotations for Persistent Volume Claim`    | `{}`                                                |
| `persistentVolume.mountPath`      | Persistent Volume mount root path           | `/home/postgres/pgdata`                             |
| `persistentVolume.size`           | Persistent Volume size                      | `2Gi`                                               |
| `persistentVolume.storageClass`   | Persistent Volume Storage Class             | `volume.alpha.kubernetes.io/storage-class: default` |
| `persistentVolume.subPath`        | Subdirectory of Persistent Volume to mount  | `pgroot`                                                |
| `rbac.create`                     | Create required role and rolebindings       | `true`                                              |
| `serviceAccount.create`           | If true, create a new service account	      | `true`                                              |
| `serviceAccount.name`             | Service account to be used. If not set and `serviceAccount.create` is `true`, a name is generated using the fullname template | `nil` |

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```console
$ helm install --name my-release -f values.yaml bcgov/patroni
```

> **Tip**: You can use the default [values.yaml](values.yaml)

## Cleanup

To remove the spawned pods you can run a simple `helm delete <release-name>`.

Helm will however preserve created persistent volume claims and configmap or endpoint generated by service accout,
to also remove them execute the commands below.

```console
$ release=<release-name>
$ helm delete $release
$ kubectl delete pvc -l release=$release
$ kubectl delete configmap -l release=$release
$ kubectl delete ep -l release=$release
```
