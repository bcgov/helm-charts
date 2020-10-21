# backup-storage

Helm chart to deploy the `bcgov/backup-container` solution.

See: https://github.com/BCDevOps/backup-container for the code.

## Chart Details

This chart will do the following:

* Deploy a backup solution for databases (PostgresSQL/Patroni, MongoDB, MSSQL)

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm repo add bcgov https://bcgov.github.io/helm-charts
$ helm install my-release bcgov/backup-storage
```

## Configuration

The following tables list the configurable parameters of the `backup-storage` chart and their default values.



| Parameter                         | Description                          | Default                                   |
| --------------------------------- | ------------------------------------ | ----------------------------------------- |
| `backupConfig           `           | Backup config details          |     See below               |
| `persistence.backup.mountPath          `           | Where the volume for storing backups is mounted   |   /backups/   |
| `persistence.backup.claimName           `           | If the PVC is created outside the chart, specify the name here   |      |
| `persistence.backup.size           `           | To create the PVC, omit the `claimName` and specify the size  |      |
| `persistence.backup.storageClassName           `           | To create the PVC, omit the `claimName` and specify the storageClassName   |  netapp-block-standard    |
| `persistence.verification.mountPath          `           | Where the volume for the verification database is mounted   |   /var/lib/pgsql/data   |
| `persistence.verification.claimName           `           | If the PVC is created outside the chart, specify the name here   |      |
| `persistence.verification.size           `           | To create the PVC, omit the `claimName` and specify the size  |      |
| `persistence.verification.storageClassName           `           | To create the PVC, omit the `claimName` and specify the storageClassName   |     netapp-block-standard |
| `db.secretName           `          | The secret that has the database credentials      |                                       |
| `db.usernameKey           `     | The key in the secret that has the db username        |                                         |
| `db.passwordKey           `         | The key in the secret that has the db password |             |
| `env.*           `         | Environment variables for the solution - see `values.yaml` |               |
| `env.MONGODB_AUTHENTICATION_DATABASE           `         | This is only required if you are backing up mongo database with a separate authentication database. |               |
| `env.MSSQL_SA_PASSWORD           `         | The database password to use for the local backup database. |               |
| `env.TABLE_SCHEMA           `         | The table schema for your database.  Used for Postgres backups. |               |
| `env.BACKUP_STRATEGY           `         | The strategy to use for backups; for example daily, or rolling. | rolling              |
| `env.FTP_SECRET_KEY           `         | The FTP secret key is used to wire up the credentials associated to the FTP. |               |
| `env.FTP_URL           `         | The URL of the backup FTP server |               |
| `env.FTP_USER           `         | FTP user name |               |
| `env.FTP_PASSWORD           `         | FTP password |               |
| `env.WEBHOOK_URL           `         | The URL of the webhook to use for notifications.  If not specified, the webhook integration feature is disabled. |               |
| `env.ENVIRONMENT_FRIENDLY_NAME           `         | The human readable name of the environment.  This variable is used by the webhook integration to identify the environment in which the backup notifications originate. |               |
| `env.ENVIRONMENT_NAME           `         | The name or Id of the environment.  This variable is used by the webhook integration to identify the environment in which the backup notifications originate. |               |
| `env.BACKUP_DIR           `         | The name of the root backup directory.  The backup volume will be mounted to this directory. | /backups/              |
| `env.BACKUP_CONF          `         | Location of the backup configuration file | /conf/backup.conf              |
| `env.NUM_BACKUPS           `         | Used for backward compatibility only.  Ignored when using the recommended `rolling` backup strategy.  The number of backup files to be retained.  Used for the `daily` backup strategy. |               |
| `env.DAILY_BACKUPS           `         | The number of daily backup files to be retained.  Used for the `rolling` backup strategy. |  12             |
| `env.WEEKLY_BACKUPS           `         | The number of weekly backup files to be retained.  Used for the `rolling` backup strategy. | 8              |
| `env.MONTHLY_BACKUPS           `         | The number of monthly backup files to be retained.  Used for the `rolling` backup strategy. | 2              |

The `env.*` format follows:

```
  ENV_VAR_NAME:
    value: "ENV_VAR_VALUE"
    secure: false
```

The `secure` parameter is by default `false`; if it set to `true` then the value will be put into a secret and referenced in the deployment.

**backup.conf Default**: 

```
backupConfig: |
  postgres=patroni:5432/db

  0 1 * * * default ./backup.sh -s
  0 4 * * * default ./backup.sh -s -v all
```

**Volume Claims:** Please note, when using the recommended nfs-backup storage class the name of the pvc MUST be taken from the manually provisioned claim; nfs-backup storage MUST be provisioned manually.

## Example

### Build the container image using Github Actions

```
    - name: Get Dockerfile for DB Backups Image
      run: |
        git clone https://github.com/BCDevOps/backup-container.git

    - name: Docker Image for DB Backups
      uses: docker/build-push-action@v1
      env:
        DOCKER_BUILDKIT: 1
      with:
        path: backup-container/docker
        dockerfile: backup-container/docker/Dockerfile
        registry: docker.pkg.github.com
        username: $GITHUB_ACTOR
        password: ${{ secrets.GITHUB_TOKEN }}
        repository: [owner]/[repo]/backup-db-job
        tag_with_ref: true
        tag_with_sha: false
        add_git_labels: true
        push: true
```

### Add a pull image secret to your Kubernetes environment

You can create this in many different ways, but an example using `Terraform`:

```
data "template_file" "docker-registry" {
    template = <<EOT
{
  "auths": {
    "docker.pkg.github.com": {
      "username": "username",
      "password": "${var.githubAccessToken}",
      "email": "ops@nowhere.com",
      "auth": "${base64encode("username:${var.githubAccessToken}")}"
    }
  }
}
    EOT
}

resource "kubernetes_secret" "github-read-packages-creds" {
  metadata {
    name = "github-read-packages-creds"
    namespace = var.namespace
  }

  data = {
    ".dockerconfigjson": "${data.template_file.docker-registry.rendered}"
  }

  type = "kubernetes.io/dockerconfigjson"
}
```

### Helm deploy

```
echo '
image:
  repository: docker.pkg.github.com/[owner]/[repo]/backup-db-job
  pullPolicy: Always
  tag: dev

imagePullSecrets:
    - name: github-read-packages-creds

backupConfig: |
  postgres=patroni:5432/db

  0 1 * * * default ./backup.sh -s
  0 4 * * * default ./backup.sh -s -v all

db:
  secretName: patroni
  usernameKey: username-superuser
  passwordKey: password-superuser

env:
  DATABASE_SERVICE_NAME:
    value: patroni
  ENVIRONMENT_FRIENDLY_NAME:
    value: "Patroni DB Backups"
' > config.yaml

helm repo add bcgov http://bcgov.github.io/helm-charts
helm repo update
helm upgrade --install patroni-backup-storage -f config.yaml bcgov/backup-storage
```
