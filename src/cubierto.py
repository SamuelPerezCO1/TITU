class Cubierto:
    @staticmethod
    def imprimir_resultado_saldo(resultado, actual, tamano):
        try:
            if isinstance(resultado[0], int):
                if actual[0] == '-':
                    porcentaje = 100
                elif isinstance(actual[0], int):
                    porcentaje = (resultado[0] / actual[0]) * 100
                else:
                    raise ValueError("El valor de 'actual' no es válido.")
                lista_nueva = [f"{porcentaje:.2f}%"]
            else:
                lista_nueva = ["-"]
            
            # Rellenar el resto de la lista con '-'
            while len(lista_nueva) < len(tamano):
                lista_nueva.append("-")

            return lista_nueva
        except Exception as e:
            print(f"Error Exception en Cubierto: {e}")
            return ["-"] * len(tamano)