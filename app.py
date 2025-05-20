from flask import Flask, render_template, request, send_file
from datetime import datetime
from fpdf import FPDF
import os
import base64
from io import BytesIO

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    datos = request.form
    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    pdf = FPDF()
    pdf.add_page()
    # Fondo con franjas horizontales alternas (azul claro y blanco)
    altura_fila = 12  # Altura de cada franja
    alto_pagina = 297  # A4 vertical
    ancho_pagina = 210

    y = 0
    color_on = True
    while y < alto_pagina:
        if color_on:
            pdf.set_fill_color(230, 240, 255)  # Azul claro
        else:
            pdf.set_fill_color(255, 255, 255)  # Blanco
        pdf.rect(0, y, ancho_pagina, altura_fila, 'F')
        y += altura_fila
        color_on = not color_on

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=10)

    # Logo
    pdf.image("static/logo.png", x=10, y=8, w=30)
    pdf.set_xy(150, 10)
    pdf.cell(0, 10, f"Fecha Contrato: {fecha_actual}", ln=True)

    # Título
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(0, 102, 204)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "DATOS DEL TITULAR DEL CONTRATO", ln=True, fill=True)

    # Datos del cliente
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)

    pdf.cell(50, 8, f"Nombre Completo: {datos['nombre_completo']}", 0, 0)
    pdf.cell(90, 8, "", 0, 0)
    pdf.cell(40, 8, f"DNI: {datos['dni']}", 0, 1)

    pdf.cell(0, 8, f"Correo: {datos['email']}", 0, 1)

    pdf.cell(50, 8, f"Dirección: {datos['direccion']}", 0, 0)
    pdf.cell(90, 8, "", 0, 0)
    pdf.cell(40, 8, f"Población: {datos['poblacion']}", 0, 1)

    pdf.cell(50, 8, f"CP: {datos['cp']}", 0, 0)
    pdf.cell(90, 8, "", 0, 0)
    pdf.cell(40, 8, f"Provincia: {datos['provincia']}", 0, 1)

    pdf.cell(0, 8, f"Tipo de Cliente: {datos['tipo_cliente']}", 0, 1)

   
    # Título detalles de contratación
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(0, 102, 204)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "DETALLES DE CONTRATACIÓN", ln=True, fill=True)

# Contenido de detalles
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)

# Primera línea: Tarifa contratada, Periodicidad y Precio
    pdf.cell(65, 8, f"Tarifa Contratada: {datos['tarifa']}", 0, 0)
    pdf.cell(65, 8, f"Periodicidad: {datos['periodicidad']}", 0, 0)
    pdf.cell(40, 8, f"Precio: {datos['precio']}", 0, 1)

# Segunda línea: Alta
    pdf.cell(0, 8, f"Alta: {datos['alta']}", 0, 1)

# Tercera línea: Equipos en Préstamo, Modelo y Cobertura
    pdf.cell(50, 8, f"Equipos en Préstamo: {datos['equipo']}", 0, 0)
    pdf.cell(60, 8, f"Modelo: {datos['modelo']}", 0, 0)
    pdf.cell(40, 8, f"Cobertura Total: {datos['cobertura']}", 0, 1)

# Cuarta línea: SSID
    pdf.cell(0, 8, f"SSID: {datos['ssid']}", 0, 1)

# Quinta línea: Total Instalación y Forma de Pago
    pdf.cell(70, 8, f"Total a Pagar en la Instalación: {datos['total_instalacion']}", 0, 0)
    pdf.cell(70, 8, f"Forma de Pago: {datos['forma_pago']}", 0, 1)

# Sexta línea: Pago al Instalador y Método de Pago
    pdf.cell(70, 8, f"Cliente Paga al Instalador: {datos['pago_instalador']}", 0, 0)
    pdf.cell(70, 8, f"Método: {datos['metodo_pago_instalador']}", 0, 1)

# Observaciones
    pdf.cell(0, 8, f"Observaciones: {datos['observaciones']}", 0, 1)


    # Título SEPA
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(0, 102, 204)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "ORDEN DE DOMICILIACIÓN DE ADEUDO DIRECTO SEPA", ln=True, fill=True)

    # Datos SEPA
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"IBAN: {datos['iban']}", 0, 1)
    
    # Insertar firma del cliente si existe
    # Insertar firma del cliente si existe
    firma_base64 = datos.get('firma')
    if firma_base64:
        firma_base64 = firma_base64.split(',')[1]
        firma_data = base64.b64decode(firma_base64)

        firma_path = os.path.join("static", "firma_temp.png")
        with open(firma_path, "wb") as f:
            f.write(firma_data)

    # Título de firmas
        pdf.ln(15)
        pdf.cell(80, 8, "Firma del Cliente:", 0, 0, 'L')
        pdf.cell(80, 8, "Firma de la Empresa:", 0, 1, 'R')

    # Firmas
        pdf.image(firma_path, x=10, y=pdf.get_y(), w=60)
        pdf.set_xy(120, pdf.get_y() + 5)
        pdf.cell(60, 20, "________________________", 0, 1, 'R')

        os.remove(firma_path)
    else:
        pdf.ln(15)
        pdf.cell(80, 8, "Firma del Cliente:", 0, 0, 'L')
        pdf.cell(80, 8, "Firma de la Empresa:", 0, 1, 'R')
        pdf.cell(80, 20, "________________________", 0, 0, 'L')
        pdf.cell(80, 20, "________________________", 0, 1, 'R')
    if not os.path.exists("contratos"):
        os.makedirs("contratos")
    ruta = os.path.join("contratos", "contrato_holawifi.pdf")
    pdf.output(ruta)

    return send_file(ruta, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
