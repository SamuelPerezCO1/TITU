class Cubierto:
    def imprimir_resultado_saldo(resultado, actual, tamano):
        try:
            valor_resultado = float(resultado[0])
            valor_actual = float(actual[0])

            lista_nueva = [valor_resultado / valor_actual]

            while len(lista_nueva) < len(tamano):
                lista_nueva.insert(1,None)

            print(lista_nueva)
        except Exception as e:
            print(f"error Exception en cubierto {e}")
        