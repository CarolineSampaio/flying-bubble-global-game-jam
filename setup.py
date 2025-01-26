import cx_Freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('bubble.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "Flying bubble",
    options = {"build_exe" : 
        {"packages" : ["pygame"], "include_files" : ['gallery/']}},
    executables = executables
)