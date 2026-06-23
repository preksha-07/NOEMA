from hardware_client import execute_plotter

result = execute_plotter([
    "G01 X10 Y10",
    "G01 X20 Y20"
])

print(result)