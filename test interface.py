import threading
import subprocess
import tkinter as tk

root = tk.Tk()
# [The rest of your Tkinter GUI setup code should be here]

console = tk.Text(root)  # Assuming 'console' is a Text widget, add proper setup if not
console.pack()

def run_script():
    try:
        command = ['python', 'test.py', 'project_name', 'folder_path', 'str(test_run)', 'prompt_input', 'output_folder']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

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

# Ensuring Tkinter mainloop is running in the main thread
if __name__ == "__main__":
    threading.Thread(target=run_script, daemon=True).start()
    root.mainloop()
