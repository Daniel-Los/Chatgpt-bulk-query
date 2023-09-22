folder_path = r"C:\Users\d.los\Berenschot\Energie en Leefomgeving - Uitlezen bestanden\tabel output"
import os
from docx import Document
import pandas as pd

def parse_document(file_path):
    # Load the document
    doc = Document(file_path)
    # Extract the text from the document
    text = []
    for para in doc.paragraphs:
        text.append(para.text)

    # Prepare the data structure for the dataframe
    data = {
        "Documentnaam": [],
        "Maatregel thema": [],
        "Gemeente": [],
        "Naam maatregel": [],
        "Beschrijving van de maatregel": [],
        "Hoe": []  # Added "Hoe" column
    }

    # Prepare a temporary list to hold a block of lines
    temp = []

    # Function to process a block and append to data
    def process_block(block, data):
        if len(block) == 6:  # Changed from 5 to 6
            data["Documentnaam"].append(block[0].split(": ")[1].strip() if ": " in block[0] else block[0])
            data["Maatregel thema"].append(block[1].split(": ")[1].strip() if ": " in block[1] else block[1])
            data["Gemeente"].append(block[2].split(": ")[1].strip() if ": " in block[2] else block[2])
            data["Naam maatregel"].append(block[3].split(": ")[1].strip() if ": " in block[3] else block[3])
            data["Beschrijving van de maatregel"].append(block[4].split(": ")[1].strip() if ": " in block[4] else block[4])
            data["Hoe"].append(block[5].split(": ")[1].strip() if ": " in block[5] else block[5])  # Added "Hoe" line

    for line in text:
        # If the line starts with "1. Documentnaam: ", it's the start of a new block
        if line.startswith("1. Documentnaam: "):
            # If we have a non-empty block, process it and start a new one
            if temp:
                process_block(temp, data)
                temp = []
        # If the line is not empty, add it to our temporary list
        if line.strip() != "":
            temp.append(line)

    # Process the last block if it wasn't processed
    if temp:
        process_block(temp, data)

    return pd.DataFrame(data)


# Create an empty DataFrame to store all data
all_data = pd.DataFrame()

# Loop over all Word documents in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".docx"):
        file_path = os.path.join(folder_path, filename)
        df = parse_document(file_path)
        all_data = pd.concat([all_data, df], ignore_index=True)

# Now all_data contains the data from all Word documents in the folder
print(all_data.head())

# To save the DataFrame to a CSV file:
# all_data.to_csv("output.csv", index=False)

all_data.to_csv(r"C:\Users\d.los\Berenschot\Energie en Leefomgeving - Uitlezen bestanden\tabel output\Tabeloverzicht maatregelen 27_7.csv", index=False)