print("Post-Commit Hook")

with open('config.py', 'r') as file:
    # read a list of lines into data
    data = file.readlines()
    for i, line in enumerate(data):
        if 'side_of_window' in data[i]:
            data[i] = f"side_of_window = 'r'\n"
            print("Side of window changed to right")
with open('config.py', 'w') as file:
    file.writelines(data)
