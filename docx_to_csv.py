import re
import csv
from docx import Document


def convert_docx_to_csv(docx_path, csv_path, column_names=None):
    # Read the DOCX file
    document = Document(docx_path)

    # Extract text from the document
    doc_text = [para.text for para in document.paragraphs]

    # Initialize lists to hold the extracted fields
    document_names = []
    provinces = []
    policy_themes = []
    descriptions = []

    # Regular expression pattern to identify records
    record_pattern = re.compile(
        r'documentnaam\s*:\s*(.*?\.pdf),\s*provincie\s*:\s*(.*?),\s*gevonden beleidsthema\s*:\s*(.*?),\s*beschrijving\s*:\s*(.*)')

    # Filter out headers and parse records
    for line in doc_text:
        if not line.startswith("documentnaam"):
            continue  # Skip headers and other irrelevant lines

        match = record_pattern.match(line)
        if match:
            document_names.append(match.group(1))
            provinces.append(match.group(2))
            policy_themes.append(match.group(3))
            descriptions.append(match.group(4))

    # Default column names
    if column_names is None:
        column_names = ['Document Name', 'Province', 'Policy Theme', 'Description']

    # Write the extracted data to a CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header
        csvwriter.writerow(column_names)

        # Write the records
        for doc_name, province, policy_theme, description in zip(document_names, provinces, policy_themes,
                                                                 descriptions):
            csvwriter.writerow([doc_name, province, policy_theme, description])


# Example usage
docx_path = "your_input_file_path_here.docx"
csv_path = "your_output_file_path_here.csv"
custom_column_names = ["Custom Document Name", "Custom Province", "Custom Policy Theme", "Custom Description"]
convert_docx_to_csv(docx_path, csv_path, column_names=custom_column_names)
