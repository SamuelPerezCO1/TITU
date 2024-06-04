import fitz

class Titulo:
    def extraer_titulo(archivo_pdf):
        try:
            titulo = []
            documento = fitz.open(archivo_pdf)
            for pagina_numero in range(len(documento)):
                pagina = documento.load_page(pagina_numero)
                titulos = pagina.search_for("Informe de Riesgo")
                for palabra_titulo in titulos:
                    x0, y0, x1, y1 = palabra_titulo
                    area_debajo_titulo = fitz.Rect(x0, y1, x1 + 150, y1 + 20)
                    texto_debajo_titulo = pagina.get_text("text", clip=area_debajo_titulo)
                    titulo.append(texto_debajo_titulo)

            lista_info = []
            for info in titulo:
                info_lines = info.strip().splitlines()
                info_stripped = [line.strip().replace("__", "") for line in info_lines if line.strip()]
                lista_info.extend(info_stripped)

            patrones_excluir = ["$"]
            titulo_filtrado = []
            for elemento in lista_info:
                if any(elemento.startswith(patron) for patron in patrones_excluir):
                    continue
                titulo_filtrado.append(elemento)

            if titulo_filtrado:
                return titulo_filtrado[0]
        except Exception as e:
            print(f"Error Exception {e}")
        return None