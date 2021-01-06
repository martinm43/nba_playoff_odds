rem This is a file for Windows that 
rem deletes the previous build folders
rem and artefacts and then creates a new 
rem Windows extension.
del /s /q build
del *.pyd
del mcss_ext2.cpp
python cpp_setup.py build_ext --inplace 
