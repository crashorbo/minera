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

        pdftam = (8*cm, 10*cm)
        pdf = canvas.Canvas(buffer, pagesize=pdftam)

        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawCentredString(115, 265, "DATOS PESAJE")
        pdf.line(70, 263, 160, 263)
        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawString(5, 250, "=====================================")
        pdf.drawString(5, 90, "=====================================")
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawCentredString(140, 230, self.__carga.numero)
        pdf.setFont('Helvetica', 6)
        pdf.drawString(10, 85, self.__carga.usuario.username)
        pdf.drawRightString(215, 85, today.strftime("%I:%M:%S"))
        pdf.setFont('Helvetica', 7)
        pdf.drawString(10, 230, "Nº PESAJE:")
        pdf.drawString(10, 210, "FECHA:")
        pdf.drawString(10, 190, "CONDUCTOR:")
        pdf.drawString(10, 170, "N PLACA:")
        pdf.drawString(10, 150, "PESO BRUTO:")
        pdf.drawString(10, 130, "ORIGEN:")
        pdf.drawString(10, 110, "UBICACION:")
        locale.setlocale(locale.LC_TIME, "es_ES.utf-8")
        pdf.drawString(65, 210, self.__carga.created.strftime("%A, %d %B %Y"))
        pdf.drawString(65, 190, '{} {}'.format(
            self.__carga.conductor_vehiculo.apellidos, self.__carga.conductor_vehiculo.nombres))
        pdf.drawString(65, 170, self.__carga.vehiculo.placa)
        pdf.drawString(65, 150, str(self.__carga.peso_bruto))
        pdf.drawString(65, 130, str(self.__carga.origen))
        pdf.drawString(65, 110, str(self.__carga.destino))
        pdf.setDash(1, 2)
        pdf.line(10, 223, 220, 223)
        pdf.line(10, 203, 220, 203)
        pdf.line(10, 183, 220, 183)
        pdf.line(10, 163, 220, 163)
        pdf.line(10, 143, 220, 143)
        pdf.line(10, 123, 220, 123)
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

        pdftam = (8*cm, 21*cm)
        pdf = canvas.Canvas(buffer, pagesize=pdftam)

        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawCentredString(115, 575, "BOLETA DE PESAJE")
        pdf.line(55, 573, 175, 573)
        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawString(5, 545, "=====================================")
        pdf.drawString(5, 425, "=====================================")
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawRightString(175, 560, self.__carga.numero)
        pdf.drawRightString(207, 365, self.__carga.numero)
        pdf.drawRightString(207, 160, self.__carga.numero)
        pdf.setFont('Helvetica', 6)
        pdf.drawString(15, 420, self.__carga.usuario.username)
        pdf.drawRightString(215, 420, today.strftime("%H:%M:%S"))
        pdf.setFont('Helvetica', 7)
        pdf.drawString(55, 560, "Nº PESAJE:")
        pdf.drawString(10, 530, "FECHA:")
        pdf.drawString(10, 520, "Nº PLACA VEHIC.:")
        pdf.drawString(10, 510, "CONDUCTOR:")
        pdf.drawString(10, 500, "CARGUIO:")
        pdf.drawString(10, 490, "PROVEEDOR:")
        pdf.drawString(10, 480, "ORIGEN CARGA:")
        pdf.drawString(10, 470, "DESTINO CARGA:")
        pdf.drawString(10, 460, "PESO BRUTO (Kg):")
        pdf.drawString(10, 450, "PESO TARA  (Kg):")
        pdf.drawString(10, 440, "PESO NETO  (Tn):")
        locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')
        pdf.drawString(75, 530, self.__carga.created.strftime(
            "%d/%m/%Y  %H:%M:%S"))
        pdf.drawString(75, 520, self.__carga.vehiculo.placa)
        pdf.drawString(75, 510, '{} {}'.format(
            self.__carga.conductor_vehiculo.apellidos, self.__carga.conductor_vehiculo.nombres))
        if self.__carga.equipo_carguio:
            pdf.drawString(75, 500, '{} {}'.format(
                self.__carga.equipo_carguio.apellidos, self.__carga.equipo_carguio.nombres))
        else:
            pdf.drawString(75, 500, '')
        pdf.drawString(75, 490, str(self.__carga.proveedor))
        pdf.drawString(75, 480, str(self.__carga.origen))
        pdf.drawString(75, 470, str(self.__carga.destino))
        pdf.drawRightString(215, 460, numero_decimal(self.__carga.peso_bruto))
        pdf.drawRightString(215, 450, numero_decimal(self.__carga.peso_tara))
        pdf.drawRightString(215, 440, numero_decimal(
            self.__carga.peso_neto_tn))
        pdf.setFont('Helvetica-Bold', 24)
        pdf.drawString(15, 365, "A")
        pdf.drawString(15, 160, "B")

        qrw = QrCodeWidget('{}{}'.format('http://190.104.10.157',
                                         reverse_lazy('pesaje-detail', kwargs={'pk': self.__carga.id})))
        b = qrw.getBounds()

        w = b[2]-b[0]
        h = b[3]-b[1]

        d = Drawing(60, 60, transform=[60./w, 0, 0, 60./h, 0, 0])
        d.add(qrw)

        renderPDF.draw(d, pdf, 161.5, 60)
        renderPDF.draw(d, pdf, 161.5, 265)

        pdf.rect(15, 320, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 280, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 240, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(164, 268, 1.9*cm, 1.9*cm, stroke=1, fill=0)
        pdf.rect(15, 115, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 75, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(15, 35, 5*cm, 1*cm, stroke=1, fill=0)
        pdf.rect(164, 63, 1.9*cm, 1.9*cm, stroke=1, fill=0)
        pdf.setDash(1, 2)
        pdf.line(5, 400, 222, 400)
        pdf.line(5, 203, 222, 203)
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
