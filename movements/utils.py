from io import BytesIO
from django.http import FileResponse
from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.units import mm


def generar_comprobante_pdf(movimiento):
    """
    Genera un PDF (FileResponse) con el comprobante del movimiento pasado.
    - movimiento: instancia del modelo Movimiento con .detalles.all() (DetalleMovimiento)

    Devuelve: django.http.FileResponse con el PDF listo para descarga.
    """
    # Colores y estilos corporativos (modo claro para impresión)
    NAVY = HexColor('#1E293B')        # texto / encabezados
    LIGHT_BG = HexColor('#F1F5F9')    # filas alternadas
    DIVIDER = HexColor('#CBD5E1')     # líneas sutiles

    filename = f"comprobante_{(movimiento.numero_planilla or 'mov')}.pdf"

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=18*mm,
        bottomMargin=18*mm,
    )

    styles = getSampleStyleSheet()
    # Title style (Helvetica-Bold, 20pt)
    title_style = ParagraphStyle(
        'TitleCustom',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY,
        spaceAfter=15,
        alignment=1,  # centered
    )
    meta_value_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontSize=10,
        textColor=NAVY,
    )
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=NAVY,
    )
    table_par_style = ParagraphStyle(
        'TablePara',
        parent=styles['Normal'],
        fontSize=10,
        textColor=NAVY,
    )
    header_para_style = ParagraphStyle(
        'HeaderPara',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.white,
    )

    usable_width = A4[0] - (doc.leftMargin + doc.rightMargin)

    elements = []

    # Encabezado
    elements.append(Paragraph("COMPROBANTE DE MOVIMIENTO DE INVENTARIO", title_style))
    elements.append(Paragraph("ElectroTech - Sistema de Inventario", ParagraphStyle('Subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=14, textColor=NAVY, alignment=1, spaceAfter=4)))
    elements.append(Paragraph("Documento oficial de control de ingresos y egresos", ParagraphStyle('SubtitleNote', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=HexColor('#475569'), alignment=1, spaceAfter=10)))
    elements.append(HRFlowable(width="100%", thickness=1, color=DIVIDER, spaceBefore=2, spaceAfter=14))

    # Metadatos
    fecha = getattr(movimiento, 'fecha_hora', None)
    if not fecha:
        fecha = timezone.now()
    fecha_str = timezone.localtime(fecha).strftime("%d/%m/%Y %H:%M:%S")

    tipo_display = movimiento.get_tipo_display() if hasattr(movimiento, 'get_tipo_display') else getattr(movimiento, 'tipo', '')
    usuario_text = getattr(movimiento.usuario, 'email', None) or getattr(movimiento.usuario, 'username', str(movimiento.usuario))
    persona_text = movimiento.nombre_persona or 'N/D'
    cedula_text = movimiento.cedula or 'N/D'
    departamento_text = movimiento.departamento or 'N/D'
    cargo_text = movimiento.cargo or 'N/D'

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.white,
        alignment=1,
        leading=13,
    )
    badge = Paragraph(tipo_display, badge_style)

    left_meta = Table([
        [Paragraph('<b>Código de Operación</b>', label_style), Paragraph(movimiento.numero_planilla or '', meta_value_style)],
        [Paragraph('<b>Fecha / Hora</b>', label_style), Paragraph(fecha_str, meta_value_style)],
        [Paragraph('<b>Usuario</b>', label_style), Paragraph(usuario_text, meta_value_style)],
    ], colWidths=[usable_width * 0.20, usable_width * 0.30])
    left_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))

    right_meta = Table([
        [Paragraph('<b>Persona</b>', label_style), Paragraph(persona_text, meta_value_style)],
        [Paragraph('<b>Cédula / ID</b>', label_style), Paragraph(cedula_text, meta_value_style)],
        [Paragraph('<b>Departamento</b>', label_style), Paragraph(departamento_text, meta_value_style)],
        [Paragraph('<b>Cargo</b>', label_style), Paragraph(cargo_text, meta_value_style)],
    ], colWidths=[usable_width * 0.20, usable_width * 0.30])
    right_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))

    badge_table = Table([[badge]], colWidths=[usable_width * 0.24], hAlign='RIGHT')
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#16A34A') if movimiento.es_ingreso else HexColor('#DC2626')),
        ('BOX', (0,0), (-1,-1), 1.2, HexColor('#0F172A') if movimiento.es_ingreso else HexColor('#991B1B')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))

    elements.append(badge_table)
    elements.append(Spacer(1, 10))

    meta_container = Table(
        [[left_meta, right_meta]],
        colWidths=[usable_width * 0.46, usable_width * 0.46]
    )
    meta_container.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ]))
    elements.append(meta_container)
    elements.append(Spacer(1, 12))

    # Detalle de hardware: Tabla con encabezado + filas (usa Paragraph para auto wrap)
    header = [
        Paragraph("Nombre", header_para_style),
        Paragraph("Categoría", header_para_style),
        Paragraph("Cantidad", header_para_style),
    ]

    detalles_qs = list(getattr(movimiento, 'detalles').all()) if hasattr(movimiento, 'detalles') else []
    data_rows = []
    if detalles_qs:
        for det in detalles_qs:
            nombre = getattr(det, 'snapshot_nombre', getattr(det.componente, 'nombre', '—'))
            categoria = getattr(det, 'snapshot_categoria', getattr(getattr(det, 'componente', None).categoria, 'nombre', '—') if getattr(det, 'componente', None) else '—')
            cantidad_val = det.cantidad
            data_rows.append([
                Paragraph(str(nombre), table_par_style),
                Paragraph(str(categoria), table_par_style),
                Paragraph(str(cantidad_val), table_par_style),
            ])
    else:
        data_rows.append([
            Paragraph('-', table_par_style),
            Paragraph('-', table_par_style),
            Paragraph('-', table_par_style),
        ])

    table_data = [header] + data_rows

    # Column widths: distribuir en el ancho usable
    col_widths = [usable_width * 0.55, usable_width * 0.30, usable_width * 0.15]

    tbl = Table(table_data, colWidths=col_widths, hAlign='LEFT', repeatRows=1)

    tbl_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEABOVE', (0,0), (-1,0), 1, DIVIDER),
        ('LINEBELOW', (0,0), (-1,0), 1, DIVIDER),
        ('BOX', (0,0), (-1,-1), 0.8, DIVIDER),
        ('GRID', (0,0), (-1,-1), 0.25, DIVIDER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ])

    # Alternar fondo en las filas de datos
    for i in range(1, len(table_data)):
        if i % 2 == 1:
            tbl_style.add('BACKGROUND', (0,i), (-1,i), LIGHT_BG)
        tbl_style.add('LINEBELOW', (0,i), (-1,i), 0.25, DIVIDER)

    tbl.setStyle(tbl_style)
    elements.append(tbl)
    elements.append(Spacer(1, 18))

    # Sección de firmas
    signature_line = HRFlowable(width=120, thickness=0.7, color=DIVIDER, spaceBefore=6, spaceAfter=6)
    sig_table = Table(
        [
            [signature_line, signature_line],
            [Paragraph("Firma de Operador", meta_value_style), Paragraph("Firma de Almacén/Recepción", meta_value_style)]
        ],
        colWidths=[usable_width*0.48, usable_width*0.48],
        hAlign='CENTER'
    )
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(sig_table)

    def draw_footer(canvas, doc):
        footer_text = "ElectroTech - Comprobante de Movimiento"
        page_text = f"Página {doc.page}"
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#475569'))
        canvas.drawString(doc.leftMargin, 15 * mm, footer_text)
        canvas.drawRightString(A4[0] - doc.rightMargin, 15 * mm, page_text)
        canvas.restoreState()

    def draw_border(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(DIVIDER)
        canvas.setLineWidth(0.8)
        canvas.rect(doc.leftMargin - 6, doc.bottomMargin - 6, A4[0] - doc.leftMargin - doc.rightMargin + 12, A4[1] - doc.topMargin - doc.bottomMargin + 12, stroke=1, fill=0)
        canvas.restoreState()

    # Construir documento
    doc.build(elements, onFirstPage=lambda canvas, doc: (draw_border(canvas, doc), draw_footer(canvas, doc)), onLaterPages=lambda canvas, doc: (draw_border(canvas, doc), draw_footer(canvas, doc)))

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename, content_type='application/pdf' )