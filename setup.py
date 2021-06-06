import sys
from cx_Freeze import setup, Executable

setup(name = "ALTAR_6-5" ,
      version = "0.1" ,
      description = "" ,
      options={"build_exe": {"packages":["pygame", "pyo"]}},
      executables = [Executable("client_gui.py")])
