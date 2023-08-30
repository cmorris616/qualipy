#!/usr/bin/env bash

echo "************************"
echo "* Cleaning dist folder *"
echo "************************"
rm -rf $SCRIPT_DIR/qualipy/dist

echo "********************"
echo "* Building QualiPy *"
echo "********************"

cd $SCRIPT_DIR/qualipy
python -m build

echo "**********************"
echo "* Publishing QualiPy *"
echo "**********************"

twine upload dist/*
