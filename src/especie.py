import fitz

class Especie:
    def extraer_especie(archivo_pdf, titulo_principal):
        try:
            informacion_debajo_tips = []
            documento = fitz.open(archivo_pdf)
            for pagina_numero in range(len(documento)):
                pagina = documento.load_page(pagina_numero)
                palabras_tips = pagina.search_for("Saldos y cobertura _______________________________________")
                for palabra_tips in palabras_tips:
                    x0, y0, x1, y1 = palabra_tips
                    area_debajo_tips = fitz.Rect(x0, y1, x1 - 150, y1 + 55)
                    texto_debajo_tips = pagina.get_text("text", clip=area_debajo_tips)
                    informacion_debajo_tips.append(texto_debajo_tips)

            lista_info = []
            for info in informacion_debajo_tips:
                info_lines = info.strip().splitlines()
                info_stripped = [line.strip() for line in info_lines if line.strip()]
                lista_info.extend(info_stripped)

            patrones_excluir = ["Tasa", "%", "Prepago______", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Prepago", "$", "Saldo" , "S"]
            tips_filtrados = []
            for elemento in lista_info:
                if any(elemento.startswith(patron) for patron in patrones_excluir):
                    continue
                tips_filtrados.append(elemento)

            tips_filtrados.pop(0)
            tips_filtrados_prefijo = [f"{titulo_principal} {item}" for item in tips_filtrados]

            return tips_filtrados_prefijo
        except Exception as e:
            print(f"(extraer_informacion_debajo_tips) Error Exception {e}")
            return []