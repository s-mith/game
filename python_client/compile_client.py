import cx_Freeze

executables = [cx_Freeze.Executable("client.py")]

cx_Freeze.setup(
    name="thing",
    options={"build_exe": {"packages":["pygame", "random", "math", "threading", "time", "socket"]}},
    executables = executables

    )
