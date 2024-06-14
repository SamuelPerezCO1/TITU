class DevolverNumerosResultado:
    @staticmethod
    def devolver_numeros_resultado(lista):
        numeros_resultado = []
        for i in lista:
            if i == '-':
                numeros_resultado.append(i)
                continue
            # Eliminar símbolo de moneda si existe
            i = i.replace('$', '').strip()

            try:
                # Identificar y manejar el formato del número
                if ',' in i and '.' in i:
                    # Si contiene ambos, asumimos que la coma es separador de miles y el punto es decimal
                    i = i.split('.')[0].replace(',', '')
                elif ',' in i:
                    # Si solo contiene coma, asumimos que es separador de miles
                    i = i.replace(',', '')
                elif '.' in i:
                    # Si solo contiene punto, asumimos que es separador de miles
                    i = i.replace('.', '')

                # Convertir a número entero
                numero = int(i)
                numeros_resultado.append(numero)
            except ValueError:
                print(f"El valor '{i}' no es un número válido y será omitido.")

        if numeros_resultado:
            # Mantener solo el primer número y rellenar el resto con '-'
            first_number = numeros_resultado[0]
            numeros_resultado = [first_number] + ['-'] * (len(lista) - 1)
        else:
            # Si no hay números válidos, rellenar todo con '-'
            numeros_resultado = ['-'] * len(lista)

        print(f"numeros_resultado es {numeros_resultado}")

        return numeros_resultado
