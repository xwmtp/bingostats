import os, shutil, sys


def mk(name):
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    path = os.path.join(path, name)
    if not os.path.exists(path):
        os.makedirs(path)


def rm(name):
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    path = os.path.join(path, name)
    if os.path.exists(path):
        shutil.rmtree(path)
