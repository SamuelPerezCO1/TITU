from datetime import datetime as dt
import json
import os
import glob
import pandas as pd
import convertir_pdf_txt
import titulo
import especie
import fecha
import actual
import operacion_sym
import capital_cartera
import mora
import porcentajes
import escenariosestres
import pdfatxt
import cubierto
import devolver_numeros_actual
import devolver_numeros_resultado

fecha_actual = dt.now().strftime("%Y%m")

with open("static/main.json", "r") as f:
    data = json.load(f)
    ruta_pdfs = os.path.abspath(data["rutas"]["ruta_pdfs"])
    ruta_txt = os.path.abspath(data["rutas"]["ruta_txt"])

extraer_titulo = titulo.Titulo
extraer_especie = especie.Especie
extraer_fecha = fecha.Fecha
extraer_actual = actual.Actual
conversion = convertir_pdf_txt.Pdfatxt
extraer_operacion = operacion_sym.Resultado
extraer_cc = capital_cartera.CapitalCartera
extraer_mora = mora.Mora
extraer_porcentajes = porcentajes.Porcentajes
extraer_estres = escenariosestres.EscenariosEstres
conversion2 = pdfatxt.Pdfatxt
operacion = cubierto.Cubierto
devolver_lista = devolver_numeros_actual.DevolverNumeros
devolver_lista_resultado = devolver_numeros_resultado.DevolverNumerosResultado


def eliminar_archivos_en_carpeta(carpeta):
    archivos = glob.glob(os.path.join(carpeta, '*'))
    
    for archivo in archivos:
        if os.path.isfile(archivo):
            os.remove(archivo)
contador = 0

def recorrer_archivos_pdf(archivos_pdf):
    try:
        directorio_txt = ruta_txt
        for archivo_pdf in archivos_pdf:
            print(f"convirtiendo el archivo {archivo_pdf}")
            titulo_principal = extraer_titulo.extraer_titulo(archivo_pdf)
            if titulo_principal:
                tamano = extraer_especie.extraer_especie(archivo_pdf, titulo_principal)
                fecha = extraer_fecha.extraer_fecha(archivo_pdf, tamano)
                actual = extraer_actual.extraer_actual(archivo_pdf , len(tamano))
                lista_actual_nueva = devolver_lista.devolver_numeros(actual)
                nombre_txt = conversion.convertir_pdf_txt(archivo_pdf, directorio_txt)

                if nombre_txt is None:
                    nombre_txt = conversion2.convertir_pdf_txt(archivo_pdf=archivo_pdf ,ruta_txt=directorio_txt )
                
                resultado = extraer_operacion.sacar_resultado(nombre_txt, tamano, directorio_txt)
                resultado_numeros = devolver_lista_resultado.devolver_numeros_resultado(resultado)
                saldo_cc = extraer_cc.sacar_resultado(nombre_txt , tamano , directorio_txt)
                saldo_mora = extraer_mora.sacar_resultado(nombre_txt , tamano , directorio_txt)
                porcentaje = extraer_porcentajes.extraer_porcentajes(archivo_pdf , len(tamano))
                df_escenarios_estres = extraer_estres.extraer_escenariosestres(archivo_pdf)
                eliminar_archivos_en_carpeta(directorio_txt)


                primera_operacion = operacion.imprimir_resultado_saldo(resultado_numeros,lista_actual_nueva , tamano)

                print(f"Resultado numero es {resultado_numeros}")
                tamano.append('------')
                fecha.append('------')
                lista_actual_nueva.append('------')
                resultado.append('------')
                saldo_cc.append('------')
                saldo_mora.append('------')
                porcentaje.append('------')
                resultado_numeros.append('------')
                primera_operacion.append('------')

                print(f"lista division nueva es {primera_operacion}")

                if tamano and fecha and lista_actual_nueva and resultado and saldo_cc and saldo_mora and porcentaje  and resultado_numeros and primera_operacion and\
                    len(tamano) == len(fecha) == len(lista_actual_nueva) == len(resultado) == len(saldo_cc) == len(saldo_mora) == len(porcentaje) == len(resultado_numeros) == len(primera_operacion):
                    df_nuevo = pd.DataFrame({
                        "Especie": tamano,
                        "Fecha": fecha,
                        "Saldo_CC": saldo_cc,
                        "Saldo_mora": saldo_mora,
                        "Cobertura": porcentaje,
                        "Resultado":resultado,
                        "R_Numeros": resultado_numeros,
                        "Actual": lista_actual_nueva,
                        "P_Operacion": primera_operacion
                    })


                    if not df_escenarios_estres.empty:
                        df_nuevo = pd.concat([df_nuevo , df_escenarios_estres] , axis = 1)
                        
                    archivo_csv = f'{fecha_actual}.csv'

                    if os.path.exists(archivo_csv):
                        df_existente = pd.read_csv(archivo_csv)
                        df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
                    else:
                        df_actualizado = df_nuevo

                    df_actualizado.to_csv(archivo_csv, index=False)
                else:
                    print(f"Error: Las listas de especies, fechas, saldos actuales y resultados no coinciden en la longitud para el archivo {archivo_pdf}")

            else:
                print(f"No se pudo extraer el titulo principal del archivo {archivo_pdf}")
        eliminar_archivos_en_carpeta(directorio_txt)
    except Exception as e:
        print(f"Error Exception en recorrer_archivos_pdf main {e}")


archivos_pdf = glob.glob(os.path.join(ruta_pdfs, '*.pdf'))
recorrer_archivos_pdf(archivos_pdf)
