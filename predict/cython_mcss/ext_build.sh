#!/bin/sh
rm -r build && rm -r mcss_ext2.so
python2 cpp_setup.py build_ext --inplace -lsqlite3 
