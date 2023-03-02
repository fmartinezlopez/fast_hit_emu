SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo Installation location: $SCRIPT_DIR

export BUILD_DIR=$SCRIPT_DIR/build
mkdir $BUILD_DIR
cd $BUILD_DIR

cmake -DCMAKE_OSX_ARCHITECTURES="x86_64" ..
make
cd ..

export PYTHONPATH="$PYTHONPATH:$BUILD_DIR:$SCRIPT_DIR/python/fast_hit_emu"
export PATH="$PATH:$SCRIPT_DIR/scripts"