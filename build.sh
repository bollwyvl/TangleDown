rm -rf index.html site_media build
mkdir build
cd build
httrack http://localhost:8000
cd localhost_8000
cp -r * ../../
cd ../../
git status