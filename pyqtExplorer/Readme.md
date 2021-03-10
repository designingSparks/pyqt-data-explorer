## Setting up the python path for Visual Studio Code

If you have a global version of pyqtgraph that is installed in site package but you want to use a local version for development, one way to do this is to append the path in a .env file.
Create a .env file in the root directory. The contents of the .env file should be as follows:

`PYTHONPATH=C:\\path\\to\\local_package;${PYTHONPATH}`