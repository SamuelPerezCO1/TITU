import pdfplumber
import os

class Pdfatxt:
    @staticmethod
    def extract_and_align_text(pdf_path):
        data = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        for line in text.split('\n'):
                            # Process each line of text
                            if line.strip():
                                data.append(line.strip())

            aligned_data = []
            for line in data:
                label_value = line.split(':')
                if len(label_value) >= 2:
                    label = label_value[0].strip().lower()
                    value = label_value[1].strip()

                    if "saldo" in label or "mora" in label:
                        aligned_data.append((label, value))

            return aligned_data
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return []

    @staticmethod
    def save_to_txt(aligned_data, txt_path):
        try:
            with open(txt_path, 'w', encoding='utf-8') as file:
                for label, value in aligned_data:
                    label = label.replace('_', '')
                    value = value.replace('_', '')
                    file.write(f"{label}: {value}\n")
        except Exception as e:
            print(f"Error saving text to file: {e}")

    @staticmethod
    def convertir_pdf_txt(archivo_pdf, ruta_txt):
        aligned_text = Pdfatxt.extract_and_align_text(archivo_pdf)

        if not aligned_text:
            print("No data extracted from PDF.")
            return None

        nombre_base = os.path.splitext(os.path.basename(archivo_pdf))[0]

        txt_path = os.path.join(ruta_txt, f"{nombre_base}.txt")

        Pdfatxt.save_to_txt(aligned_text, txt_path)

        for label, value in aligned_text:
            label = label.replace('_', '')
            value = value.replace('_', '')
            # print(f"{label}: {value}")

        return f"{nombre_base}.txt"
