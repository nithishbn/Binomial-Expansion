from distutils.core import setup
import py2exe

setup(
    console = [
        {
            "script": "main.py",
            "dest_base": "Binomial Expansion"
        }
    ],
    options={
        "py2exe":{
            "bundle_files":1
        }
    }
)