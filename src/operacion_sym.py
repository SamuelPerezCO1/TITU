import os
import re  # Importamos el módulo de expresiones regulares

class Resultado:
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
        lineas_desde_meses_hasta_tasa = Resultado.leer_desde_meses_hasta_tasa(nombre_archivo, palabras_adicionales=5)

        patrones_excluir = ['a-2', 'a1-', 'a2-', 'b-', 'b1-', 'b2-', 'c-', 'c1-', 'c2-', 'mz-', 'til', 'tips', 'saldos y cobertura avalúo de brp:', 'tis', '15']

        lista_filtrada = []

        for elemento in lineas_desde_meses_hasta_tasa:
            if not any(elemento.startswith(patron) for patron in patrones_excluir):
                lista_filtrada.append(elemento)

        lista_final = [
            Resultado.extraer_despues_del_dolar_o_dos_puntos(elemento) if ('$' in elemento or ':' in elemento) else Resultado.milesuvr(elemento)
            for elemento in lista_filtrada
        ]

        if len(lista_final) >= 2:
            try:
                valor_primero = lista_final[0]
                primer_valor = int(valor_primero)
                segundo_valor = lista_final[1]
                
                # Verificar si el segundo valor es un número
                try:
                    segundo_valor = int(segundo_valor)
                    operacion = primer_valor - segundo_valor
                except ValueError:
                    operacion = primer_valor

                print(f"OPERACION_SYM contenido {operacion} y tipo es {type(operacion)}")

                return [operacion]  # Retornar una lista
            except Exception as e:
                print(f'OPERACION_SYM Error de conversión en archivo en el resultado de saldo y mora se esperaba hacer una operacion entre digito y digito pero en alguno de los dos campos se recibio un caracter , se supone que alguno de los dos caracteres esta en ceros {nombre_archivo}: {e}')
        else:
            print(f'No se encontraron suficientes datos en archivo {nombre_archivo}')
        return []

    @staticmethod
    def sacar_resultado(nombre_txt, tamano, ruta_txt):
        try:
            nombre_txt2 = os.path.join(ruta_txt, nombre_txt)
            resultado_lista = Resultado.recorrer_archivos_txt(nombre_archivo=nombre_txt2)
            largo_especies = len(tamano)
            resultadosym = resultado_lista * largo_especies

            # Formatear los resultados como números con separadores de coma para los miles
            resultadosym = [format(resultado, ",") if resultado is not None else None for resultado in resultadosym]

            # Si la longitud de resultadosym es menor que la de tamano, insertar '-' en los lugares faltantes
            while len(resultadosym) < len(tamano):
                resultadosym.insert(0, '-')

            return resultadosym

        except Exception as e:
            print(f"Error Exception en sacar_resultado en operacion_sym {e}")
