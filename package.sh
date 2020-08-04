#!/bin/bash

echo "helm chart releaser must be installed prior to running this (https://github.com/helm/chart-releaser)"
echo "You MUST be on the master branch before proceeding"
read -p "You must set CR_TOKEN in env before running this, proceed? [yN]" yn
case $yn in
    [Yy]* ) echo "Proceeding";;
    * ) echo "Aborting"; exit;;
esac

git checkout master

charts=("ckan-ui" "formio" "forum-api" "metadata-curator" "nifi" "ocp-pipeline" "ocp-route" "ocp-terraform-pipeline" "storage-api" "userguide-bridge-api" "vdi-project-api" "vdi-virtual-display" "konga")

rm -rf ./packages/*.tgz

for chart in ${charts[@]}; do
    read -p "Release $chart? [yN]" yn
    case $yn in
        [Yy]* ) cd $chart;
                helm dep up;
                cd ..;
                helm package $chart;;
        * ) echo "Skipping";;
    esac
done

mv *.tgz packages/.

cr upload --owner bcgov --git-repo helm-charts --package-path ./packages

rm -rf ./packages/*.tgz
for chart in ${charts[@]}; do
    helm package $chart;
done

mv *.tgz packages/.
rm packages/.gitkeep
cr index --owner bcgov --git-repo helm-charts --package-path ./packages --index-path ./docs/index.yaml --charts-repo https://github.com/bcgov/helm-charts/releases
touch packages/.gitkeep

git add docs
git commit -m "Automated pages update"
git push origin master