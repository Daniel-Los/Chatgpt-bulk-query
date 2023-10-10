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


def load_instructons(instruction_file):

    variables = read_instructions(instruction_file)
    project_root = variables['root']
    prompt = variables['prompt']
    project_name = variables['project_name']
    output_folder = variables['output_folder']

    return project_root, prompt, project_name, output_folder

if __name__ == "__main__":
    instruction_file = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\instructie_voorjaarsnota.txt"
    instruction_file = r"C:\Users\d.los\PycharmProjects\documentsearch\instruction_voorjaarsnota.txt"
    instructions = load_instructons(instruction_file)

    print(instructions)