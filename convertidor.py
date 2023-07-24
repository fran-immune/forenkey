import auto_py_to_exe

from auto_py_to_exe import APTEndUserAPI

print(dir(auto_py_to_exe))
api = APTEndUserAPI()
api.convert_script_to_executable(script_path="interfaz.py", output_path="interfaz.exe")