import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import os
import time
import signal
import read_variables_from_instructions
from begrippenlijst import begrippenlijst
from text_miner import Text_Miner
import os
from read_variables_from_instructions import read_instructions
import sys
import load_instructions
import subprocess
import main_loop
from api_import import api_import
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import time


from read_variables_from_instructions import read_instructions
import load_instructions
from api_import import api_import
from main_loop import main

if __name__ == '__main__':
    running_process = None

    def start_program():
        global running_process

        folder_path = folder_path_var.get()
        test_run = str(test_run_var.get())
        prompt_input = prompt_input_entry.get("1.0", "end-1c")
        output_folder = output_folder_var.get()
        project_name = project_name_var.get()
        word_formatting = str(word_formatting_var.get())
        api_key_path = os.path.join(os.getcwd(), api_key_var.get())

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
                                   f"Output Folder: {output_folder}\n"
                                   f"API key document: {api_key_path}\n", "info"
                           )
            console.config(state=tk.DISABLED)

            if running_process:
                console.config(state=tk.NORMAL)
                console.insert(tk.END, "The program is already running.\n", "error")
                console.config(state=tk.DISABLED)
            else:
                try:
                    print('Starting Analysis')
                    console.config(state=tk.NORMAL)
                    console.insert(tk.END, "\nStarting Analysis...", "info")
                    console.config(state=tk.DISABLED)
                    main(folder_path, prompt_input, output_folder, project_name, word_formatting, api_key_path,
                         test_run)
                except Exception as e:
                    console.config(state=tk.NORMAL)
                    console.insert(tk.END, f"Error executing the program: {str(e)}\n", "error")
                    console.config(state=tk.DISABLED)
                finally:
                    running_process = None  # Reset the running_process variable

    def stop_program():
        global running_process
        if running_process:
            try:
                console.insert(tk.END, "Process stopped by user.\n", "error")
                running_process.terminate()
                running_process.wait()
            except Exception as e:
                console.config(state=tk.NORMAL)
                console.insert(tk.END, f"Error stopping the program: {str(e)}\n", "error")
                console.see(tk.END)
                console.config(state=tk.DISABLED)
            finally:
                running_process = None
        else:
            console.config(state=tk.NORMAL)
            console.insert(tk.END, "No running program to stop.\n", "error")
            console.config(state=tk.DISABLED)


    class ConsoleRedirect:
        def __init__(self, console_widget):
            self.console_widget = console_widget

        def write(self, message):
            self.console_widget.config(state=tk.NORMAL)
            self.console_widget.insert(tk.END, message)
            self.console_widget.config(state=tk.DISABLED)
            self.console_widget.see(tk.END)
    def redirect_stdout_to_console(console_widget):
        ConsoleRedirect(console_widget)


    root = tk.Tk()
    root.title("BT GPT Summarizer")

    # Create a frame for input elements on the left
    input_frame = tk.Frame(root)
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="snew")

    # Input bar for the name of the project
    project_name_var = tk.StringVar()
    project_name_label = tk.Label(input_frame, text="Project Name:")
    project_name_label.pack()
    project_name_entry = tk.Entry(input_frame, textvariable=project_name_var)
    # Get the current time
    current_time = time.localtime()
    # Format the current time as a string. For example, "20231004_123025" for "2023-10-04 12:30:25"
    timestamp = time.strftime("%Y-%m-%d_%H%M%S", current_time)
    project_name_entry.insert(0, ''+ timestamp)
    project_name_entry.pack(fill='both')

    # Selector for a folder
    folder_path_var = tk.StringVar()
    folder_path_label = tk.Label(input_frame, text="Select an input Folder:")
    folder_path_label.pack()

    folder_path_entry = tk.Entry(input_frame, textvariable=folder_path_var)
    folder_path_entry.pack()
    folder_path_entry.insert(0, str(os.getcwd())+r'\test documenten')
    folder_path_entry.pack(fill='both')
    folder_path_button = tk.Button(input_frame, text="Browse",
                                   command=lambda: folder_path_var.set(filedialog.askdirectory()))
    folder_path_button.pack()

    api_key_var = tk.StringVar()
    api_key_label = tk.Label(input_frame, text="Insert API Key path:")
    api_key_label.pack(fill='both')
    api_key_entry = tk.Entry(input_frame, textvariable=api_key_var)
    try:
        open('openai_key.txt')
        api_key_path = 'openai_key.txt'
    except:
        print('Error: Add the file "openai_key.txt" to the folder!')
        api_key_path = 'openai_key.txt'

    api_key_entry.insert(0, api_key_path)
    api_key_entry.pack()

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
    prompt_input_entry = tk.Text(input_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=10)
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
    root.grid_columnconfigure(0, weight=3)
    root.grid_columnconfigure(1, weight=1)

    # # Start Program Button
    # start_button = tk.Button(input_frame, text="Start Program", command=start_program)
    # start_button.pack()
    # Create a frame for the start and stop buttons
    button_frame = tk.Frame(input_frame)
    button_frame.pack(fill='both')

    # Start Program Button
    start_button = tk.Button(button_frame, text="Start Program", command=start_program)
    start_button.pack(side='left')

    # Stop Program Button
    stop_button = tk.Button(button_frame, text="Stop Program", command=stop_program)
    stop_button.pack(side='left')

    # Console
    # Create a scrollbar for the console Text widget
    console_scrollbar = tk.Scrollbar(console_frame)
    console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create the console Text widget and associate it with the scrollbar
    console = tk.Text(console_frame, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=console_scrollbar.set)
    console.pack(expand=True, fill="both")

    redirect_stdout_to_console(console)  # Omleiden van stdout naar de console-widget

    # Configure the scrollbar to work with the console Text widget
    console_scrollbar.config(command=console.yview)

    console.tag_config("info", foreground="green")
    console.tag_config("error", foreground="red")

    root.mainloop()
