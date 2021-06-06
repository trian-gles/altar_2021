import sys
from cx_Freeze import setup, Executable

setup(name = "GUI TEST" ,
      version = "0.1" ,
      description = "" ,
      options={"build_exe": {"packages":["pygame", "pyo"],
                             "include_files":['JetBrainsMono-Medium.ttf']}},
      executables = [Executable("dx7_gui.py")])
