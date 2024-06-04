import fitz

class Porcentajes:
    def extraer_porcentajes(archivo_pdf, tamano):
        try:
            porcentajes = []

            documento = fitz.open(archivo_pdf)

            for pagina_numero in range(len(documento)):
                pagina = documento.load_page(pagina_numero)

                x0 = 370
                x1 = 550
                y0 = 117
                y1 = 180

                area_debajo_tips = fitz.Rect(x0, y0, x1, y1)

                texto_debajo_tips = pagina.get_text("text", clip=area_debajo_tips)
                porcentajes.append(texto_debajo_tips)

            lista_info = []

            for info in porcentajes:
                info_lines = info.strip().splitlines()
                info_stripped = [line.strip() for line in info_lines if line.strip()]

                lista_info.extend(info_stripped)

            patrones_excluir = ["MZ", "B", "A", "C", "T", "+", "_", "$", "Z", "o", "E", "l", "d", "ió", 'g', 'a', 'V', 'A', 'A +', 'A1',
                                'A2', 'A3', 'B1', 'B2', 'B3', 'B', 'C', 'C1', 'C2', 'C3', 'MZ', '+', '2 + B', '1 +']

            lista_filtrada = []
            for elemento in lista_info:
                if any(elemento.startswith(patron) for patron in patrones_excluir):
                    continue
                if elemento.endswith('%'):
                    lista_filtrada.append(elemento)

            while len(lista_filtrada) < tamano:
                lista_filtrada.insert(0, '-')

            return lista_filtrada

        except Exception as e:
            print(f"(extraccion_porcentajes) extraer_porcentajes Error Exception {e}")
            return []