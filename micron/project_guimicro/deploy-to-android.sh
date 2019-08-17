#!/usr/bin/env bash

pyqtdeploy-build shutterbtn.pdy --target android-64
cd build-android-64

# https://blog.lasconic.com/compiling-qt-android-app-with-docker/

sudo docker pull lasconic/qt:5.4-android
sudo docker run -i -t -v /home/sunyudong/git/photonLauncher/micron/project_guimicro/build-android-64:/source lasconic/qt:5.4-android


# IN DOCKER
mkdir ~/build
cd ~/build
qmake -r /source/myproject.pro
make -j2
mkdir ~/dist
make install INSTALL_ROOT=~/dist
androiddeployqt --input android-libmyproject.so-deployment-settings.json --output ~/dist --name myapp --deployment bundled --gradle --release
