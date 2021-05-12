from io import BytesIO
import re
import locale
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF

from django.http import HttpResponse
from django.urls import reverse_lazy

from .templatetags.pesaje_tags import numero_decimal


class ReporteCarga:
    def __init__(self, carga):
        self.__carga = carga

    def reporte_peso_bruto(self):
        today = datetime.now()
        response = HttpResponse(content_type='application/pdf')
        # se crea el nombre del archivo de la descarga pdf
        pdf_name = 'peso_bruto_{}.pdf'.format(today.strftime("%Y%m%d"))
        response['Content-Disposition'] = 'inline; filename={}'.format(
            pdf_name)
        # se crea el buffer de memoria para generar el documento
        buffer = BytesIO()

        pdftam = (9*cm, 10*cm)
        pdf = canvas.Canvas(buffer, pagesize=pdftam)

        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawCentredString(125, 265, "DATOS PESAJE")
        pdf.line(80, 263, 170, 263)
        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawString(5, 250, "==========================================")
        pdf.drawString(5, 90, "==========================================")
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawCentredString(160, 230, self.__carga.numero)
        pdf.setFont('Helvetica', 6)
        pdf.drawString(15, 85, self.__carga.usuario.username)
        pdf.drawRightString(235, 85, today.strftime("%I:%M:%S"))
        pdf.setFont('Helvetica', 7)
        pdf.drawString(15, 230, "Nº PESAJE:")
        pdf.drawString(15, 210, "FECHA:")
        pdf.drawString(15, 190, "CONDUCTOR:")
        pdf.drawString(15, 170, "N PLACA:")
        pdf.drawString(15, 150, "PESO BRUTO:")
        pdf.drawString(15, 130, "ORIGEN:")
        pdf.drawString(15, 110, "UBICACION:")
        locale.setlocale(locale.LC_TIME, "es_ES.utf-8")
        pdf.drawString(75, 210, self.__carga.created.strftime("%A, %d %B %Y"))
        pdf.drawString(75, 190, '{} {}'.format(
            self.__carga.conductor_vehiculo.apellidos, self.__carga.conductor_vehiculo.nombres))
        pdf.drawString(75, 170, self.__carga.vehiculo.placa)
        pdf.drawString(75, 150, str(self.__carga.peso_bruto))
        pdf.drawString(75, 130, str(self.__carga.origen))
        pdf.drawString(75, 110, str(self.__carga.destino))
        pdf.setDash(1, 2)
        pdf.line(15, 223, 235, 223)
        pdf.line(15, 203, 235, 203)
        pdf.line(15, 183, 235, 183)
        pdf.line(15, 163, 235, 163)
        pdf.line(15, 143, 235, 143)
        pdf.line(15, 123, 235, 123)
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def reporte_peso_neto(self):
        today = datetime.now()
        response = HttpResponse(content_type='application/pdf')
        # se crea el nombre del archivo de la descarga pdf
        pdf_name = 'peso_neto_{}.pdf'.format(today.strftime("%Y%m%d"))
        response['Content-Disposition'] = 'inline; filename={}'.format(
            pdf_name)
        # se crea el buffer de memoria para generar el documento
        buffer = BytesIO()

        pdftam = (9*cm, 21*cm)
        pdf = canvas.Canvas(buffer, pagesize=pdftam)

        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawCentredString(125, 575, "BOLETA DE PESAJE")
        pdf.line(65, 573, 185, 573)
        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawString(5, 545, "==========================================")
        pdf.drawString(5, 425, "==========================================")
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawRightString(185, 560, self.__carga.numero)
        pdf.drawRightString(242, 365, self.__carga.numero)
        pdf.drawRightString(242, 160, self.__carga.numero)
        pdf.setFont('Helvetica', 6)
        pdf.drawString(15, 420, self.__carga.usuario.username)
        pdf.drawRightString(235, 420, today.strftime("%H:%M:%S"))
        pdf.setFont('Helvetica', 7)
        pdf.drawString(65, 560, "Nº PESAJE:")
        pdf.drawString(15, 530, "FECHA:")
        pdf.drawString(15, 520, "Nº PLACA VEHIC.:")
        pdf.drawString(15, 510, "CONDUCTOR:")
        pdf.drawString(15, 500, "CARGUIO:")
        pdf.drawString(15, 490, "PROVEEDOR:")
        pdf.drawString(15, 480, "ORIGEN CARGA:")
        pdf.drawString(15, 470, "DESTINO CARGA:")
        pdf.drawString(15, 460, "PESO BRUTO (Kg):")
        pdf.drawString(15, 450, "PESO TARA  (Kg):")
        pdf.drawString(15, 440, "PESO NETO  (Tn):")
        locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')
        pdf.drawString(85, 530, self.__carga.created.strftime(
            "%d/%m/%Y  %H:%M:%S"))
        pdf.drawString(85, 520, self.__carga.vehiculo.placa)
        pdf.drawString(85, 510, '{} {}'.format(
            self.__carga.conductor_vehiculo.apellidos, self.__carga.conductor_vehiculo.nombres))
        if self.__carga.equipo_carguio:
            pdf.drawString(85, 500, '{} {}'.format(
                self.__carga.equipo_carguio.apellidos, self.__carga.equipo_carguio.nombres))
        else:
            pdf.drawString(85, 500, '')
        pdf.drawString(85, 490, str(self.__carga.proveedor))
        pdf.drawString(85, 480, str(self.__carga.origen))
        pdf.drawString(85, 470, str(self.__carga.destino))
        pdf.drawRightString(180, 460, numero_decimal(self.__carga.peso_bruto))
        pdf.drawRightString(180, 450, numero_decimal(self.__carga.peso_tara))
        pdf.drawRightString(180, 440, numero_decimal(
            self.__carga.peso_neto_tn))
        pdf.setFont('Helvetica-Bold', 24)
        pdf.drawString(15, 365, "A")
        pdf.drawString(15, 160, "B")

        qrw = QrCodeWidget('{}{}'.format('http://192.168.0.1',
                                         reverse_lazy('pesaje-detail', kwargs={'pk': self.__carga.id})))
        b = qrw.getBounds()

        w = b[2]-b[0]
        h = b[3]-b[1]

        d = Drawing(80, 80, transform=[80./w, 0, 0, 80./h, 0, 0])
        d.add(qrw)

        renderPDF.draw(d, pdf, 165.5, 50)
        renderPDF.draw(d, pdf, 165.5, 255)

        pdf.rect(15, 320, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 280, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 240, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(170, 260, 2.5*cm, 2.5*cm, stroke=1, fill=0)
        pdf.rect(15, 115, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 75, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 35, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(170, 55, 2.5*cm, 2.5*cm, stroke=1, fill=0)
        pdf.setDash(1, 2)
        pdf.line(5, 400, 250, 400)
        pdf.line(5, 203, 250, 203)
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
