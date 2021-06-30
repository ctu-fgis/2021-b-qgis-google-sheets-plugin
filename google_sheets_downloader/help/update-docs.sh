#!/usr/bin/env bash
# build docs
git checkout gh-pages
rm -rf *
touch .nojekyll
git checkout master google_sheets_downloader/help
cd google_sheets_downloader/help
make clean
make html
cd ../..
mv google_sheets_downloader/help/build/html/* ./
rm -rf google_sheets_downloader
git add -A
git commit -m "publishing updated docs..."
git push origin gh-pages
# switch back
git checkout master
