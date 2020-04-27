echo "helm chart releaser must be installed prior to running this (https://github.com/helm/chart-releaser)"
echo "You MUST be on the master branch before proceeding"
read -p "You must set CR_TOKEN in env before running this, proceed? [yN]" yn
case $yn in
    [Yy]* ) echo "Proceeding";;
    * ) echo "Aborting"; exit;;
esac

git checkout master

rm -rf packages/*

cd forum-api
helm dep up
cd ..
helm package forum-api

cd forum-api
helm dep up
cd ..
helm package nifi

cd formio
helm dep up
cd ..
helm package formio

cd forum-api
helm dep up
cd ..
helm package storage-api

cd forum-api
helm dep up
cd ..
helm package vdi-virtual-display


mv *.tgz packages/.

cr upload --owner bcgov --git-repo helm-charts --package-path ./packages

cr index --owner bcgov --git-repo helm-charts --package-path ./packages --charts-repo https://github.com/bcgov/helm-charts/releases --index-path docs/index.yaml

git add docs
git commit -m "Automated pages update"
git push origin master