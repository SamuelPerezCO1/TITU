import fitz

class Fecha:
    def extraer_fecha(archivo_pdf, tamano):
        try:
            fecha = []
            documento = fitz.open(archivo_pdf)
            for pagina_numero in range(len(documento)):
                pagina = documento.load_page(pagina_numero)
                x0 = 360
                x1 = 470
                y0 = 20
                y1 = 80
                area_fecha = fitz.Rect(x0, y0, x1, y1)
                texto_fecha = pagina.get_text("text", clip=area_fecha)
                fecha.append(texto_fecha.strip())

            lista_info = []
            for info in fecha:
                info_lines = info.strip().splitlines()
                info_stripped = [line.strip() for line in info_lines if line.strip()]
                lista_info.extend(info_stripped)

            largo_especies = len(tamano)
            fecha_multiplicada = lista_info * largo_especies

            return fecha_multiplicada
        except Exception as e:
            print(f"(extraccion_fecha) extraer_fecha error Exception {e}")
            return []