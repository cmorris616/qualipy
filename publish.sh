#!/usr/bin/env bash

echo "*********************"
echo "* Copying readme.md *"
echo "*********************"

SCRIPT_DIR=$(cd "$(dirname $BASH_SOURCE)" && pwd)
cp $SCRIPT_DIR/readme.md $SCRIPT_DIR/qualipy/readme.md

echo "************************"
echo "* Cleaning dist folder *"
echo "************************"
rm -rf $SCRIPT_DIR/qualipy/dist

echo "********************"
echo "* Building QualiPy *"
echo "********************"

cd qualipy
python -m build

echo "**********************"
echo "* Publishing QualiPy *"
echo "**********************"

twine upload dist/*

echo "***********************************"
echo "* Removing temp copy of readme.md *"
echo "***********************************"

rm $SCRIPT_DIR/qualipy/readme.md
