from io import BytesIO
import re
import locale
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, Border, Side, Alignment
from openpyxl.utils import get_column_letter


from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF

from django.http import HttpResponse
from django.urls import reverse_lazy

from pesaje.templatetags.pesaje_tags import numero_decimal


class ReporteContabilidad:
    def __init__(self, carga):
        self.__carga = carga

    def reporte_boleta(self):
        today = datetime.now()
        response = HttpResponse(content_type='application/pdf')
        # se crea el nombre del archivo de la descarga pdf
        pdf_name = 'peso_bruto_{}.pdf'.format(today.strftime("%Y%m%d"))
        response['Content-Disposition'] = 'inline; filename={}'.format(
            pdf_name)
        # se crea el buffer de memoria para generar el documento
        buffer = BytesIO()

        pdftam = (8*cm, 12*cm)
        pdf = canvas.Canvas(buffer, pagesize=pdftam)

        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawCentredString(115, 300, "DATOS DE ENTREGA")
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawString(25, 286, "Nº Boleta:")
        pdf.drawString(25, 274, "Fecha:")
        pdf.drawString(25, 262, "Cotizacion:")
        pdf.drawCentredString(115, 234, 'Descripcion')
        pdf.drawString(25, 162, 'Valor reposicion')
        pdf.drawRightString(205, 162, '{}'.format(
            numero_decimal(self.__carga.valor_reposicion)))
        pdf.drawString(25, 66, 'Valor descuentos')
        pdf.drawRightString(205, 66, '{}'.format(
            numero_decimal(self.__carga.total_descuento)))

        pdf.drawString(25, 43, 'Valor neto s/descuentos')
        pdf.drawRightString(205, 43, '{}'.format(
            numero_decimal(self.__carga.liquido_pagable)))
        pdf.setFont('Helvetica', 6)
        pdf.drawString(25, 56, '{:.0f}'.format(self.__carga.regalia))
        pdf.setFont('Helvetica', 7)
        pdf.drawRightString(205, 286, 'P{}'.format(self.__carga.numero))
        pdf.drawRightString(205, 274, today.strftime("%d/%m/%Y"))
        pdf.drawRightString(205, 262, '{:.0f}'.format(self.__carga.cotizacion))
        pdf.drawCentredString(115, 250, '{} {}'.format(
            self.__carga.proveedor.apellidos, self.__carga.proveedor.nombres))
        pdf.drawString(25, 222, 'Ton Humeda')
        pdf.drawRightString(205, 222, '{}'.format(
            numero_decimal(self.__carga.peso_neto_tn)))
        pdf.drawString(25, 210, 'Humedad %')
        pdf.drawRightString(205, 210, '{:.0f}'.format(self.__carga.h2o))
        pdf.drawString(25, 198, 'Ton Seco')
        pdf.drawRightString(205, 198, '{}'.format(
            numero_decimal(self.__carga.tms_pagar)))
        pdf.drawString(25, 186, 'Ley')
        pdf.drawRightString(205, 186, '{}'.format(
            numero_decimal(self.__carga.au)))
        pdf.drawString(25, 174, 'Finos recuper. Gr. - 60')
        pdf.drawRightString(205, 174, '{}'.format(
            numero_decimal(self.__carga.finos_gr_recup)))
        pdf.drawString(25, 150, 'Cobre soluble')
        pdf.drawRightString(205, 150, '{}'.format(
            numero_decimal(self.__carga.penalizacion_cu_soluble)))
        pdf.drawString(25, 138, 'Anticipos')
        pdf.drawRightString(205, 138, '{}'.format(
            numero_decimal(self.__carga.anticipo)))
        pdf.drawString(25, 126, 'Pala (carguio)')
        pdf.drawRightString(205, 126, '{}'.format(
            numero_decimal(self.__carga.equipo_pesado)))
        pdf.drawString(25, 114, 'Balanza (peso)')
        pdf.drawRightString(205, 114, '{}'.format(
            numero_decimal(self.__carga.balanza)))
        pdf.drawString(25, 102, 'Volqueta (Acarreo)')
        pdf.drawRightString(205, 102, '{}'.format(
            numero_decimal(self.__carga.volqueta)))
        pdf.drawString(25, 90, 'Laboratorio (Analisis)')
        pdf.drawRightString(205, 90, '{}'.format(
            numero_decimal(self.__carga.analisis_laboratorio)))
        pdf.drawString(25, 78, 'Descuentos p/terceros')
        pdf.drawRightString(205, 78, '{}'.format(
            numero_decimal(self.__carga.otros_descuentos)))

        pdf.line(20, 243, 210, 243)
        pdf.line(20, 231, 210, 231)
        pdf.line(20, 243, 20, 231)
        pdf.line(210, 243, 210, 231)

        pdf.line(20, 52, 210, 52)
        pdf.line(20, 40, 210, 40)
        pdf.line(20, 52, 20, 40)
        pdf.line(210, 52, 210, 40)

        pdf.setDash(0.5, 1.5)

        pdf.line(20, 295, 210, 295)
        pdf.line(20, 283, 210, 283)
        pdf.line(20, 271, 210, 271)
        pdf.line(20, 259, 210, 259)
        pdf.line(20, 247, 210, 247)
        pdf.line(20, 247, 20, 295)
        pdf.line(210, 247, 210, 295)

        pdf.line(20, 219, 210, 219)
        pdf.line(20, 207, 210, 207)
        pdf.line(20, 195, 210, 195)
        pdf.line(20, 183, 210, 183)
        pdf.line(20, 171, 210, 171)
        pdf.line(20, 159, 210, 159)
        pdf.line(20, 147, 210, 147)
        pdf.line(20, 135, 210, 135)
        pdf.line(20, 123, 210, 123)
        pdf.line(20, 111, 210, 111)
        pdf.line(20, 99, 210, 99)
        pdf.line(20, 87, 210, 87)
        pdf.line(20, 75, 210, 75)
        pdf.line(20, 63, 210, 63)
        pdf.line(20, 231, 20, 63)
        pdf.line(210, 231, 210, 63)

        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


class ReporteExcel():

    def __init__(self, carga):
        self.__carga = carga

    def reporte_por_pagar(self):
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', )
        response['Content-Disposition'] = 'attachment; filename={date}-porpagar.xlsx'.format(
            date=datetime.now().strftime('%Y%m%d'), )

        titulo = NamedStyle(name="titulo")
        titulo.font = Font(bold=True, size=14,)
        titulo.alignment = Alignment(horizontal="center", vertical="center")

        monto = NamedStyle(name="monto")
        monto.font = Font(bold=True, size=14,)
        monto.alignment = Alignment(horizontal="right", vertical="center")
        wb = Workbook()

        wb.add_named_style(titulo)

        sheet = wb.active

        sheet['A1'] = "Numero"
        sheet['A1'].style = titulo
        sheet['B1'] = "Fecha"
        sheet['B1'].style = titulo
        sheet['C1'] = "Proveedor"
        sheet['C1'].style = titulo
        sheet['D1'] = "Monto"
        sheet['D1'].style = titulo

        liquido_pagable = 0

        for row in self.__carga:
            if row.liquido_pagable > 0:
                liquido_pagable = liquido_pagable + row.liquido_pagable
                sheet.append((row.numero, row.created.strftime("%d/%m/%Y"), '{} {}'.format(
                    row.proveedor.apellidos, row.proveedor.nombres), row.liquido_pagable))

        max_row = sheet.max_row

        total_liquido_pagable_descr_cell = sheet.cell(
            row=max_row + 2, column=sheet.max_column - 1)
        total_liquido_pagable_descr_cell.value = "Total"

        total_liquido_pagable = sheet.cell(
            row=max_row + 2, column=sheet.max_column)
        total_liquido_pagable.value = liquido_pagable

        total_liquido_pagable_descr_cell.style = titulo
        total_liquido_pagable.style = monto

        for i in range(1, sheet.max_column+1):
            sheet.column_dimensions[get_column_letter(i)].bestFit = True
            sheet.column_dimensions[get_column_letter(i)].auto_size = True

        wb.save(response)

        return response
