import json

with open("etc/intercepted_data.json", "r") as f:
    intercepted = json.load(f)

n, y, t, b_list, c_list, d_list = intercepted