class Cubierto:
    @staticmethod
    def imprimir_resultado_saldo(resultado, actual, tamano):
        try:
            lista_nueva = []
            suma_actual = 0

            for i in range(len(actual)):
                try:
                    actual_i = 0 if actual[i] == '-' else actual[i]

                    if actual_i == 0:
                        porcentaje = 100
                    else:
                        if i == 0:
                            porcentaje = (resultado[0] / actual_i) * 100
                        else:
                            suma_actual += 0 if actual[i - 1] == '-' else actual[i - 1]
                            porcentaje = ((resultado[0] - suma_actual) / actual_i) * 100

                    lista_nueva.append(porcentaje)
                except ZeroDivisionError:
                    lista_nueva.append(100)

            return lista_nueva
        except Exception as e:
            print(e)
            return []

#__________________