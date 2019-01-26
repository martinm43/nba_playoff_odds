#!/bin/sh
rm -r build && rm -r *.so
python3 cpp_setup.py build_ext --inplace -lsqlite3 
