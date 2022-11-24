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