import os
import re  # Importamos el módulo de expresiones regulares

class Mora:
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
        elif ':' in linea:
            partes = linea.split(':')
            resultado = partes[1].strip()
        else:
            return None

        # Usamos una expresión regular para extraer solo los dígitos
        resultado = re.sub(r'\D', '', resultado)
        return resultado

    @staticmethod
    def milesuvr(linea):
        partes = linea.split(':')
        if len(partes) > 1:
            resultado = partes[1].strip()
            # Usamos una expresión regular para extraer solo los dígitos
            resultado = re.sub(r'\D', '', resultado)
            return resultado
        return None

    @staticmethod
    def recorrer_archivos_txt(nombre_archivo):

        lineas_desde_meses_hasta_tasa = Mora.leer_desde_meses_hasta_tasa(nombre_archivo, palabras_adicionales=5)

        patrones_excluir = ['a-2', 'a1-', 'a2-', 'b-', 'b1-', 'b2-', 'c-', 'c1-', 'c2-', 'mz-', 'til', 'tips', 'saldos y cobertura avalúo de brp:', 'tis', '15']

        lista_filtrada = []

        for elemento in lineas_desde_meses_hasta_tasa:
            if not any(elemento.startswith(patron) for patron in patrones_excluir):
                lista_filtrada.append(elemento)

        lista_final = [
            Mora.extraer_despues_del_dolar_o_dos_puntos(elemento) if ('$' in elemento or ':' in elemento) else Mora.milesuvr(elemento)
            for elemento in lista_filtrada
        ]

        if len(lista_final) >= 2:
            try:
                segundo_valor = int(lista_final[1])

                print(f"MORA contenido {segundo_valor} y tipo es {type(segundo_valor)}")
                return [segundo_valor]  # Retornar una lista
            except ValueError as e:
                print(f'MORA Error de conversión en archivo se esperaba recibir un digito pero se recibio un caracter , se supone que estan en ceros {nombre_archivo}: {e}')
        else:
            print(f'No se encontraron suficientes datos en archivo {nombre_archivo}')
        return []

    @staticmethod
    def sacar_resultado(nombre_txt, tamano, ruta_txt):
        try:
            nombre_txt2 = os.path.join(ruta_txt, nombre_txt)
            resultado_lista = Mora.recorrer_archivos_txt(nombre_archivo=nombre_txt2)
            largo_especies = len(tamano)
            resultadosym = resultado_lista * largo_especies

            while len(resultadosym) < len(tamano):
                resultadosym.insert(0,'-')
                
            return resultadosym
        except Exception as e:
            print(f"Error exception en sacar_resultado mora {e}")
