#!/bin/sh
rm -r build && rm -r *.so
python cpp_setup.py build_ext --inplace -lsqlite3 
