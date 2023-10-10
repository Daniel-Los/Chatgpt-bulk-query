import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import os
import time
# command = ['python', 'test.py', 'project_name', 'folder_path', 'str(test_run)', 'prompt_input', 'output_folder']

def start_program():
    project_name = project_name_var.get()
    folder_path = folder_path_var.get()
    test_run = test_run_var.get()
    prompt_input = prompt_input_entry.get("1.0", "end-1c")  # Get text from Text widget
    output_folder = output_folder_var.get()
    word_formatting = word_formatting_var.get()

    if not project_name or not folder_path or not output_folder:
        console.config(state=tk.NORMAL)
        console.insert(tk.END, "Please fill in all the required fields.\n", "error")
        console.config(state=tk.DISABLED)
    else:
        console.config(state=tk.NORMAL)
        console.insert(tk.END, f"Starting program with parameters:\n"
                               f"Project Name: {project_name}\n"
                               f"Folder Path: {folder_path}\n"
                               f"Test Run: {test_run}\n"
                               f"Prompt Input:\n'{prompt_input}'\n"
                               f"Output Folder: {output_folder}\n\n", "info") #"info" is the formatting (color)
        console.config(state=tk.DISABLED)

        def run_script():
            try:
                command = ['python', 'main.py', project_name, folder_path, str(test_run), prompt_input,
                           output_folder, str(word_formatting)]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True)

                while process.poll() is None:
                    output_line = process.stdout.readline()
                    if output_line:
                        root.after(0, update_console, output_line)
            except subprocess.CalledProcessError as e:
                root.after(0, update_console, "Error executing the program:\n" + str(e.output), "error")

        def update_console(output_line, tag=None):
            console.config(state=tk.NORMAL)
            console.insert(tk.END, output_line, tag)
            console.see(tk.END)
            console.config(state=tk.DISABLED)

    # Create a thread to run the script
    threading.Thread(target=run_script, daemon=True).start()





root = tk.Tk()
root.title("BT GPT Summarizer")

# Create a frame for input elements on the left
input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Selector for a folder
folder_path_var = tk.StringVar()
folder_path_label = tk.Label(input_frame, text="Select an input Folder:")
folder_path_label.pack()
folder_path_entry = tk.Entry(input_frame, textvariable=folder_path_var)
folder_path_entry.insert(0, str(os.getcwd())+r'\test documenten')
folder_path_entry.pack(fill='both')
folder_path_button = tk.Button(input_frame, text="Browse",
                               command=lambda: folder_path_var.set(filedialog.askdirectory()))
folder_path_button.pack()

# Input bar for the name of the project
project_name_var = tk.StringVar()
project_name_label = tk.Label(input_frame, text="Project Name:")
project_name_label.pack()
project_name_entry = tk.Entry(input_frame, textvariable=project_name_var)
# Get the current time
current_time = time.localtime()
# Format the current time as a string. For example, "20231004_123025" for "2023-10-04 12:30:25"
timestamp = time.strftime("%Y-%m-%d_%H%M%S", current_time)
project_name_entry.insert(0, ' _'+ timestamp)
project_name_entry.pack(fill='both')

# Toggle for "test run"
test_run_var = tk.BooleanVar()
test_run_var.set(True)
test_run_checkbox = tk.Checkbutton(input_frame, text="Test Run", variable=test_run_var)
test_run_checkbox.pack()

# Toggle for "Formatting"
word_formatting_var = tk.BooleanVar()
word_formatting_var.set(True)
word_formatting_checkbox = tk.Checkbutton(input_frame, text="Word Formatting", variable=word_formatting_var)
word_formatting_checkbox.pack()


# Input bar for "prompt input"
prompt_input_label = tk.Label(input_frame, text="Prompt Input:")
prompt_input_label.pack()

# Create a scrollbar for the Text widget
scrollbar = tk.Scrollbar(input_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create the Text widget and associate it with the scrollbar
prompt_input_entry = tk.Text(input_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
prompt_input_entry.pack(fill=tk.BOTH, expand=True)  # Fill the entire window and expand with it

# Configure the scrollbar to work with the Text widget
scrollbar.config(command=prompt_input_entry.yview)

# Selector for an output folder
output_folder_var = tk.StringVar()
output_folder_label = tk.Label(input_frame, text="Select an Output Folder:")
output_folder_label.pack()
output_folder_entry = tk.Entry(input_frame, textvariable=output_folder_var)
output_folder_entry.insert(0, str(os.getcwd())+r'\output')
output_folder_entry.pack(fill="both")
output_folder_button = tk.Button(input_frame, text="Browse",
                                 command=lambda: output_folder_var.set(filedialog.askdirectory()))
output_folder_button.pack()

# Create a frame for the console on the right
console_frame = tk.Frame(root)
console_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Configure row and column weights for dynamic scaling
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=1)

# Start Program Button
start_button = tk.Button(input_frame, text="Start Program", command=start_program)
start_button.pack()

# Console
# Create a scrollbar for the console Text widget
console_scrollbar = tk.Scrollbar(console_frame)
console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create the console Text widget and associate it with the scrollbar
console = tk.Text(console_frame, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=console_scrollbar.set)
console.pack(expand=True, fill="both")

# Configure the scrollbar to work with the console Text widget
console_scrollbar.config(command=console.yview)

console.tag_config("info", foreground="green")
console.tag_config("error", foreground="red")

root.mainloop()
