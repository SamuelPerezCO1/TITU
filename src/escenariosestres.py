from PyPDF2 import PdfReader
import pandas as pd
import re

class EscenariosEstres:
    def extraer_escenariosestres(archivo_pdf):
        """
        Extrae y procesa la información de los escenarios de estrés de un archivo PDF y la guarda en un archivo CSV.
        Args:
            archivo_pdf (str): Ruta del archivo PDF del cual se extraerá y procesará la información de los escenarios de estrés.
        Returns:
            pd.DataFrame: DataFrame con la información extraída y procesada.
        Raises:
            Exception: Si ocurre un error durante la extracción, el procesamiento o la escritura del archivo CSV.
        """
        try:
            with open(archivo_pdf, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

            pattern = r'Escenarios de Estrés\s*_{5,}\s*(.*?)\s*Tasa'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                extracted_text = match.group(1).strip()
            else:
                return pd.DataFrame()  # Retorna un DataFrame vacío si no se encuentra la información
            
            lines = extracted_text.split('\n')
            lines = [line for line in lines if line.strip()]
            
            data = []
            for line in lines:
                if line.startswith("MM"):
                    parts = line.split()
                    data.append(parts)

            # Determinar el número de columnas basándose en el máximo número de partes encontrado
            max_columns = max(len(parts) for parts in data)
            columns = [f"Columna{i+1}" for i in range(max_columns)]

            df = pd.DataFrame(data, columns=columns)
            return df

        except Exception as e:
            print(f"(extraccion_escenarios_estres) extract_and_process_info error Exception {e}")
            return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error