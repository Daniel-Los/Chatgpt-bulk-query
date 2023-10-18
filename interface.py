import tkinter as tk
from tkinter import filedialog

from text_miner import Text_Miner


class ProgramGUI:
    def __init__(self, master = tk.Tk()):
        self.master = master
        self.master.title("Chatgpt Bulk interpreter")

        # Browse knop
        self.folder_path = None
        self.browse_button = tk.Button(self.master, text="Selecteer map", command=self.browse_folder)
        self.browse_button.pack(pady=10)


        # Prompt label
        self.prompt_label = tk.Label(self.master, text="")

        # Prompt entry
        self.prompt_entry = tk.Entry(self.master)

        # Kosten label
        self.cost_label = None #tk.Label(self.master, text="")

        # Toestemmingsknop
        self.confirm_button = tk.Button(self.master, text="Toestemming geven", command=self.confirm_cost)

        # Klaar melding
        self.done_label = tk.Label(self.master, text="")

    def run_steps(self):
        self.browse_folder()

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()


        if self.folder_path:
            self.prompt_for_program()


    def prompt_for_program(self):
        # Prompt voor het programma
        self.prompt_label.config(text="Geef het programma op")
        self.prompt_label.pack()
        # root = self.folder_path
        mode = self.prompt_entry.pack()

        self.program = Text_Miner(root=self.folder_path, mode=mode)


        self.cost_label = True

        self.cost_indication()

    def cost_indication(self):
        # Kostenindicatie
        if self.cost_label:
            self.program.get_structure()
            self.program.read_files()
            costs = self.program.estimate_costs
            self.cost_label = tk.Label(self.master, text = costs)
            self.cost_label.config(text = costs)
            self.cost_label.pack()

            self.confirm_button.pack(pady=10)

    def confirm_cost(self):
        # Implementeer hier uw functie om de kosten te verwerken en toestemming te verkrijgen
        self.done_notification()

    def done_notification(self):
        # Klaar melding
        self.done_label.config(text="Het programma is klaar.")
        self.done_label.pack(pady=10)

    def start(self):
        self.run_steps()
        root = self.master
        root.mainloop()

if __name__ == "__main__":
    ProgramGUI().start()