import os

def read_instructions(file_path):
    # Step 1: Read the TXT File
    with open(file_path, "r", errors='ignore') as file:
        file_content = file.read()

    # Step 2: Extract Variables
    variables = {}
    current_key = None
    current_value_lines = []

    lines = file_content.split("\n")
    for line in lines:
        line = line.strip()
        if line:
            if "=" in line:
                if current_key is not None:
                    variables[current_key] = "\n".join(current_value_lines)
                    current_value_lines = []
                current_key, current_value = line.split(" = ")
                current_value_lines.append(current_value)
            else:
                current_value_lines.append(line)

    # Store the last variable
    if current_key is not None:
        variables[current_key] = "\n".join(current_value_lines)

    # Access the 'variables' Dictionary
    project_name = variables.get("project_name", "")
    root = variables.get("root", "")
    prompt = variables.get("prompt", "")
    output_folder = variables.get("output_folder", "")

    # Print the 'variables' dictionary
    print(variables)
    return variables