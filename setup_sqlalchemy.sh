#!/bin/bash

cd $HOME/workspace/sqlalchemy
if [ "$1" = "python" ]; then
    $HOME/workspace/cpython_org/python -m pip uninstall sqlalchemy -y
    $HOME/workspace/cpython_org/python -m pip install .
elif [ "$1" = "pypper" ]; then
    $HOME/workspace/cpython/python -m pip uninstall sqlalchemy -y
    $HOME/workspace/cpython/python setup.py install --install-lib ~/.local/lib/python3.12/site-packages
else
    echo "Invalid argument for python executable"
    exit 1
fi
exit