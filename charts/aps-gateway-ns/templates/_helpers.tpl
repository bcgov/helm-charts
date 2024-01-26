{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "aps-gateway-ns.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "aps-gateway-ns.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" $name .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "aps-gateway-ns.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "aps-gateway-ns.labels" -}}
helm.sh/chart: {{ include "aps-gateway-ns.chart" . }}
{{ include "aps-gateway-ns.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- range $index, $val := .Values.extraLabels }}
{{ $index }}: {{ $val }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "aps-gateway-ns.selectorLabels" -}}
app.kubernetes.io/name: {{ include "aps-gateway-ns.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "aps-gateway-ns.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "aps-gateway-ns.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Return secure environment variables
*/}}
{{- define "aps-gateway-ns.secureEnvVars" -}}
{{- $newList := list -}}
{{- range $key, $value := .Values.env -}}
  {{- if .secure -}}
  {{ $newList = append $newList $key }}
  {{- end -}}
{{- end -}}
{{- toJson $newList -}}
{{- end -}}

{{/*
Adds Vault Annotations
*/}}
{{- define "aps-gateway-ns.vaultAnnotations" -}}
vault.hashicorp.com/auth-path: '{{ .Values.vault.authPath }}'
vault.hashicorp.com/namespace: '{{ .Values.vault.namespace }}'
vault.hashicorp.com/role: '{{ .Values.vault.role }}'
vault.hashicorp.com/agent-inject-secret-creds: '{{ .Values.vault.secret }}'
vault.hashicorp.com/agent-inject-template-creds: |
  {{`
  {{- with secret "`}}{{ .Values.vault.secret }}{{`" }}
  {{- range $key, $val := .Data.data }}
  export {{ $key }}="{{ $val }}"
  {{- end }}
  {{ end }}
  `}}
vault.hashicorp.com/agent-inject: 'true'
vault.hashicorp.com/agent-inject-token: 'false'
vault.hashicorp.com/agent-pre-populate-only: 'true'
vault.hashicorp.com/agent-requests-cpu: '100m'
vault.hashicorp.com/agent-limits-cpu: '100m'
vault.hashicorp.com/agent-requests-mem: '256Mi'
vault.hashicorp.com/agent-limits-mem: '256Mi'
{{- end -}}