import os

class CapitalCartera:
    @staticmethod
    def leer_desde_meses_hasta_tasa(archivo, palabras_adicionales=10):
        lineas = []
        dentro_del_rango = False
        palabras_acumuladas = 0

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    if "saldo" in linea:
                        dentro_del_rango = True
                        lineas.append(linea.strip())
                        palabras_acumuladas = len(linea.split())
                    elif dentro_del_rango:
                        lineas.append(linea.strip())
                        palabras_acumuladas += len(linea.split())
                        if palabras_acumuladas > palabras_adicionales:
                            dentro_del_rango = False
                            break
        except Exception as e:
            print(f"Error reading file {archivo}: {e}")

        return lineas

    @staticmethod
    def extraer_despues_del_dolar_o_dos_puntos(linea):
        if '$' in linea:
            partes = linea.split('$')
            resultado = partes[1].strip()
            resultado = resultado.replace("millones", "").strip()
            resultado = resultado.replace(",", "").strip()
            return resultado.replace(" ", "")  # Eliminar espacios adicionales
        elif ':' in linea:
            partes = linea.split(':')
            resultado = partes[1].strip()
            resultado = resultado.replace(",", "").strip()
            return resultado.replace(" ", "")  # Eliminar espacios adicionales
        return None

    @staticmethod
    def milesuvr(linea):
        partes = linea.split(':')
        if len(partes) > 1:
            resultado = partes[1].strip()
            resultado = resultado.replace(",", "").strip()
            return resultado.replace(" ", "")  # Eliminar espacios adicionales
        return None

    @staticmethod
    def recorrer_archivos_txt(nombre_archivo):

        lineas_desde_meses_hasta_tasa = CapitalCartera.leer_desde_meses_hasta_tasa(nombre_archivo, palabras_adicionales=5)

        patrones_excluir = ['a-2', 'a1-', 'a2-', 'b-', 'b1-', 'b2-', 'c-', 'c1-', 'c2-', 'mz-', 'til', 'tips', 'saldos y cobertura avalúo de brp:', 'tis', '15']

        lista_filtrada = []

        for elemento in lineas_desde_meses_hasta_tasa:
            if not any(elemento.startswith(patron) for patron in patrones_excluir):
                lista_filtrada.append(elemento)

        lista_final = [
            CapitalCartera.extraer_despues_del_dolar_o_dos_puntos(elemento) if ('$' in elemento or ':' in elemento) else CapitalCartera.milesuvr(elemento)
            for elemento in lista_filtrada
        ]

        if len(lista_final) >= 2:
            try:
                primer_valor = int(lista_final[0])

                return [primer_valor]  # Retornar una lista
            except ValueError as e:
                print(f'Error de conversión en archivo se esperaba un numero y se recibio un caracter , se supone que capital cartera esta en ceros {nombre_archivo}: {e}')
        else:
            print(f'No se encontraron suficientes datos en archivo {nombre_archivo}')
        return []

    @staticmethod
    def sacar_resultado(nombre_txt, tamano, ruta_txt):
        nombre_txt2 = os.path.join(ruta_txt, nombre_txt)
        resultado_lista = CapitalCartera.recorrer_archivos_txt(nombre_archivo=nombre_txt2)
        largo_especies = len(tamano)
        resultadosym = resultado_lista * largo_especies
        return resultadosym