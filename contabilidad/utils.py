from datetime import datetime


class NumeroLiteral():
    def unidades(self, x):
        if x == 0:
            unidad = "CERO"
        if x == 1:
            unidad = "UN"
        if x == 2:
            unidad = "DOS"
        if x == 3:
            unidad = "TRES"
        if x == 4:
            unidad = "CUATRO"
        if x == 5:
            unidad = "CINCO"
        if x == 6:
            unidad = "SEIS"
        if x == 7:
            unidad = "SIETE"
        if x == 8:
            unidad = "OCHO"
        if x == 9:
            unidad = "NUEVE"
        return unidad

    def teens(self, x):
        if x == 0:
            teenname = "DIEZ"
        if x == 1:
            teenname = "ONCE"
        if x == 2:
            teenname = "DOCE"
        if x == 3:
            teenname = "TRECE"
        if x == 4:
            teenname = "CATORCE"
        if x == 5:
            teenname = "QUINCE"
        return teenname

    def tens(self, x):
        if x == 1:
            tensname = "DIEZ"
        if x == 2:
            tensname = "VEINTE"
        if x == 3:
            tensname = "TREINTA"
        if x == 4:
            tensname = "CUARENTA"
        if x == 5:
            tensname = "CINCUENTA"
        if x == 6:
            tensname = "SESENTA"
        if x == 7:
            tensname = "SETENTA"
        if x == 8:
            tensname = "OCHENTA"
        if x == 9:
            tensname = "NOVENTA"
        return tensname

    def tercia(self, num):
        numero = str(num)
        if len(numero) == 1:
            numero = '00'+numero
        if len(numero) == 2:
            numero = '0'+numero
        a = int(numero[0])
        b = int(numero[1])
        c = int(numero[2])
    #       print a, b, c
        if a == 0:
            if b == 0:
                resultado = self.unidades(c)
                return resultado
            elif b == 1:
                if c >= 0 and c <= 5:
                    resultado = self.teens(c)
                    return resultado
                elif c >= 6 and c <= 9:
                    resultado = 'DIECI' + self.unidades(c)
                    return resultado
            elif b == 2:
                if c == 0:
                    resultado = 'VEINTE'
                    return resultado
                elif c > 0 and c <= 9:
                    resultado = 'VEINTI '+self.unidades(c)
                    return resultado
            elif b >= 3 and b <= 9:
                if c == 0:
                    resultado = self.tens(b)
                    return resultado
                if c >= 1 and c <= 9:
                    resultado = self.tens(b) + ' Y ' + self.unidades(c)
                    return resultado
        if a == 1:
            if b == 0:
                if c == 0:
                    resultado = 'CIEN'
                    return resultado
                elif c > 0 and c <= 9:
                    resultado = 'CIENTO ' + self.unidades(c)
                    return resultado
            elif b == 1:
                if c >= 0 and c <= 5:
                    resultado = 'CIENTO ' + self.teens(c)
                    return resultado
                elif c >= 6 and c <= 9:
                    resultado = 'CIENTO ' + \
                        self.tens(b)+' Y ' + self.unidades(c)
                    return resultado
            elif b == 2:
                if c == 0:
                    resultado = 'CIENTO VEINTE'
                    return resultado
                elif c > 0 and c <= 9:
                    resultado = 'CIENTO VEINTI '+self.unidades(c)
                    return resultado
            elif b >= 3 and b <= 9:
                if c == 0:
                    resultado = 'CIENTO '+self.tens(b)
                    return resultado
                elif c > 0 and c <= 9:
                    resultado = 'CIENTO ' + self.tens(b) + ' Y ' + self.unidades(c
                                                                                 )
                    return resultado

        elif a >= 2 and a <= 9:
            if a == 5:
                prefix = 'QUINIENTO '
            elif a == 7:
                prefix = 'SETECIENTOS '
            elif a == 9:
                prefix = 'NOVECIENTOS '
            else:
                prefix = self.unidades(a)+' CIENTOS '
            if b == 0:
                if c == 0:
                    resultado = prefix
                    return resultado
                elif c > 0 and c <= 9:
                    resultado = prefix + self.unidades(c)
                    return resultado
            elif b == 1:
                if c >= 0 and c <= 5:
                    resultado = prefix+self.teens(c)
                    return resultado
                elif c >= 6 and c <= 9:
                    resultado = prefix+self.tens(b) + ' Y ' + self.unidades(c)
                    return resultado
            elif b == 2:
                if c == 0:
                    resultado = prefix+' VEINTE'
                    return resultado
                elif c > 0 and c <= 9:
                    resultado = prefix+' VEINTI ' + self.unidades(c)
                    return resultado
            elif b >= 3 and b <= 9:
                if c == 0:
                    resultado = prefix + self.tens(b)
                    return resultado
                elif c > 0 and c <= 9:
                    resultado = prefix + \
                        self.tens(b) + ' Y ' + self.unidades(c)
                    return resultado

    def main(self, num):
        result = ''
        numero = str(num)
        if len(numero) == 1:
            numero = '00000000'+numero
        if len(numero) == 2:
            numero = '0000000'+numero
        if len(numero) == 3:
            numero = '000000'+numero
        if len(numero) == 4:
            numero = '00000'+numero
        if len(numero) == 5:
            numero = '0000'+numero
        if len(numero) == 6:
            numero = '000'+numero
        if len(numero) == 7:
            numero = '00'+numero
        if len(numero) == 8:
            numero = '0'+numero
        posicion = 1
        for i in [0, 3, 6]:
            var = numero[i]+numero[i+1]+numero[i+2]
            if int(var) != 0:
                res = self.tercia(var)
                if i == 0:
                    result = res+" MILLONES "
                elif i == 3:
                    result = result+res+" MIL "
                elif i == 6:
                    result = result+res
        return result


class FechaLiteral():
    LITERALES = {
        1: 'ENE',
        2: 'FEB',
        3: 'MAR',
        4: 'ABR',
        5: 'MAY',
        6: 'JUN',
        7: 'JUL',
        8: 'AGO',
        9: 'SEP',
        10: 'OCT',
        11: 'NOV',
        12: 'DIC',
    }

    def fecha_literal(self, fecha):
        return '{}/{}'.format(self.LITERALES[fecha.month], fecha.year)
