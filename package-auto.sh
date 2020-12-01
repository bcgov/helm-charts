#!/bin/bash

echo "helm chart releaser must be installed prior to running this (https://github.com/helm/chart-releaser)"
echo "You MUST be on the master branch before proceeding"

charts=("api-serv-ui" "api-serv-gwa" "backup-storage" "batch-job" "ckan-ui" "formio" "forum-api" "generic-api" "metadata-curator" "nifi" "ocp-pipeline" "ocp-route" "ocp-terraform-pipeline" "patroni" "storage-api" "userguide-bridge-api" "vdi-project-api" "vdi-virtual-display" "konga")

rm -rf ./packages/*.tgz

change_list=()
for chart in ${charts[@]}; do
    changed=`git diff HEAD $chart/Chart.yaml | grep +version | wc -l`
    echo $changed
    if [ $changed -eq 1 ]; then
        echo "YES!"
        change_list+=($chart)
    fi
done
echo $change_list
exit
for chart in ${change_list}; do
    echo "Releasing $chart"
    cd $chart;
    helm dep up;
    cd ..;
    helm package $chart;;
done

mv *.tgz packages/.

cr upload --owner bcgov --git-repo helm-charts --package-path ./packages

rm -rf ./packages/*.tgz
for chart in ${charts[@]}; do
    helm package $chart;
done

mv *.tgz packages/.
rm packages/.gitkeep
cr index --owner bcgov --git-repo helm-charts --package-path ./packages --index-path ./docs/index.yaml --charts-repo https://bcgov.github.io/helm-charts
touch packages/.gitkeep

git add docs
git commit -m "Automated pages update"
git push origin master
