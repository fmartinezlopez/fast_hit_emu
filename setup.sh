SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo Installation location: $SCRIPT_DIR

export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/build:$SCRIPT_DIR/python/fast_hit_emu"
export PATH="$PATH:$SCRIPT_DIR/scripts"