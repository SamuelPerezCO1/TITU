class DevolverNumeros:
    @staticmethod
    def devolver_numeros(lista):    
        numeros_actual = []
        for i in lista:
            if i == '-':
                numeros_actual.append(i)
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
                numeros_actual.append(numero)
            except ValueError:
                print(f"El valor '{i}' no es un número válido y será omitido.")

        return numeros_actual
