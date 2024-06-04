import pdfplumber
import os

class Pdfatxt:
    @staticmethod
    def extract_and_align_text(pdf_path):
        data = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Extract tables from the page
                    tables = page.extract_tables()

                    for table in tables:
                        for row in table:
                            # Filter empty rows or rows with empty elements
                            if any(cell and cell.strip() for cell in row):
                                data.append(row)

            # Process and align the extracted text
            aligned_data = []
            for row in data:
                # Assume labels are in the first column and values in the second
                if len(row) >= 2:
                    label = row[0].strip().lower() if row[0] else ""
                    value = row[1].strip() if row[1] else ""

                    # Filter rows containing "saldo" or "mora"
                    if "saldo" in label or "mora" in label:
                        aligned_data.append((label, value))

            return aligned_data
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return []

    @staticmethod
    def save_to_txt(aligned_data, txt_path):
        # print(txt_path)
        try:
            with open(txt_path, 'w', encoding='utf-8') as file:
                for label, value in aligned_data:
                    # Remove underscore characters
                    label = label.replace('_', '')
                    value = value.replace('_', '')
                    file.write(f"{label}: {value}\n")
        except Exception as e:
            print(f"Error saving text to file: {e}")

    @staticmethod
    def convertir_pdf_txt(archivo_pdf , ruta_txt):
        aligned_text = Pdfatxt.extract_and_align_text(archivo_pdf)

        if not aligned_text:
            print("No data extracted from PDF.")
            return None

        nombre_base = os.path.splitext(os.path.basename(archivo_pdf))[0]

        # Path to the text file where the data will be saved
        txt_path = f"{ruta_txt}\\{nombre_base}.txt"

        Pdfatxt.save_to_txt(aligned_text, txt_path)

        # Optional: Print the aligned labels and values
        for label, value in aligned_text:
            # Remove underscore characters also in the print
            label = label.replace('_', '')
            value = value.replace('_', '')
            # print(f"{label}: {value}")

        return f"{nombre_base}.txt"
