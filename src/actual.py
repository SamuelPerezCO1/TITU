import fitz

class Actual:
    def extraer_actual(archivo_pdf , tamano):
        try:
            actual = []
            documento = fitz.open(archivo_pdf)
            for pagina_numero in range(len(documento)):
                pagina = documento.load_page(pagina_numero)
                palabras_actual = pagina.search_for("Actual")
                for palabra_actual in palabras_actual:
                    x0, y0, x1, y1 = palabra_actual
                    area_debajo_actual = fitz.Rect(x0 - 10, y1, x1 + 35, y1 + 55)
                    texto_debajo_actual = pagina.get_text("text", clip=area_debajo_actual)
                    actual.append(texto_debajo_actual)

            """
            Mejorar como trae el actual
            """
            lista_info = []
            for info in actual:
                info_lines = info.strip().splitlines()
                info_stripped = [line.strip() for line in info_lines if line.strip()]
                lista_info.extend(info_stripped)

            porcentajes = [f"{i / 10:.1f}%" for i in range(10, 1001)]
            patrones_excluir = ["_", "P", "L", "a", "Escenario", "valoración", 'Actual',
                                "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
                                ".", "p", "i", "ó", "Inicial", "Participación", "n", "l", "tal", "era", "t", "c", "o", "m", "s", "E", "v", 'A', 'B', 'C', 'A1', 'A2', 'A3',
                                'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'MZ', 'T', 'S', 'd', 'i', 'c', 'e', 'é', 'h', 'r', 'c', 'Ãº', 'ú', ' ', 'E', 'u', ':' ,'0.0%']
            patrones_excluir.extend(porcentajes)

            actual_filtrados = []
            for elemento in lista_info:
                if any(elemento.startswith(patron) for patron in patrones_excluir):
                    continue
                if len(elemento) > 4 or '-' in elemento:
                    actual_filtrados.append(elemento)
            
            while len(actual_filtrados) < tamano:
                actual_filtrados.insert(0,'-')

            return actual_filtrados
        except Exception as e:
            print(f"(extraccion_actual) extraer_actual error Exception {e}")
            return []