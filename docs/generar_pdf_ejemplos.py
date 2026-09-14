# -*- coding: utf-8 -*-
"""Genera el PDF con un ejemplo resuelto de cada submenú de la calculadora."""

import crypto_logic as cl
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Sub", fontSize=13, spaceAfter=6, spaceBefore=14,
                           textColor=colors.HexColor("#1a3d6d"), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="MenuTitle", fontSize=16, spaceAfter=10, spaceBefore=18,
                           textColor=colors.white, backColor=colors.HexColor("#1a3d6d"),
                           fontName="Helvetica-Bold", leftIndent=6, borderPadding=6))
styles.add(ParagraphStyle(name="Body", fontSize=10, spaceAfter=6, leading=14))
styles.add(ParagraphStyle(name="Mono", fontSize=9, fontName="Courier", spaceAfter=6, leading=12,
                           backColor=colors.HexColor("#f0f0f0")))
styles.add(ParagraphStyle(name="CellMono", fontSize=7, fontName="Courier", leading=9, wordWrap="CJK"))
styles.add(ParagraphStyle(name="CellNormal", fontSize=7.5, fontName="Helvetica", leading=9, wordWrap="CJK"))
styles.add(ParagraphStyle(name="CellHeader", fontSize=7.5, fontName="Helvetica-Bold", leading=9,
                           textColor=colors.white, wordWrap="CJK"))

story = []


def titulo_menu(txt):
    story.append(Paragraph(txt, styles["MenuTitle"]))


def subtitulo(txt):
    story.append(Paragraph(txt, styles["Sub"]))


def texto(txt):
    story.append(Paragraph(txt, styles["Body"]))


def tabla_dict(filas, max_col_width=None):
    if not filas:
        return
    headers = list(filas[0].keys())
    data = [headers] + [[str(f.get(h, "")) for h in headers] for f in filas]
    n = len(headers)
    ancho_disp = 17 * cm
    col_w = ancho_disp / n
    t = Table(data, colWidths=[col_w] * n, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3d6d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


def tabla_salt(filas):
    """Tabla especial para SALT: la columna Hash es larga, se envuelve en varias líneas."""
    if not filas:
        return
    headers = list(filas[0].keys())
    widths_cm = {"Salt": 2.2, "Clave": 3.0, "Salt+Clave": 3.5}
    n = len(headers)
    anchos = []
    for h in headers:
        anchos.append(widths_cm.get(h, None))
    fijo = sum(w for w in anchos if w is not None) * cm
    restante = (17 * cm) - fijo
    n_flex = sum(1 for w in anchos if w is None)
    anchos = [w * cm if w is not None else restante / max(n_flex, 1) for w in anchos]

    data = [[Paragraph(h, styles["CellHeader"]) for h in headers]]
    for f in filas:
        fila = []
        for h in headers:
            val = str(f.get(h, ""))
            estilo = styles["CellMono"] if h in ("Salt+Clave", "Hash") else styles["CellNormal"]
            fila.append(Paragraph(val, estilo))
        data.append(fila)

    t = Table(data, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3d6d")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


# ============================================================
# PORTADA
# ============================================================
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Calculadora Criptográfica", ParagraphStyle(
    name="Portada", fontSize=26, alignment=1, fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1a3d6d"))))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("Ejemplos resueltos por submenú", ParagraphStyle(
    name="Portada2", fontSize=16, alignment=1, textColor=colors.HexColor("#444444"))))
story.append(Spacer(1, 2 * cm))
story.append(Paragraph("Taller de Ciberseguridad", ParagraphStyle(
    name="Portada3", fontSize=13, alignment=1)))
story.append(Paragraph("María Isabel Vargas Mendoza — Ingeniería de Sistemas, UNAB",
                        ParagraphStyle(name="Portada4", fontSize=12, alignment=1, spaceBefore=6)))
story.append(Paragraph("Script: calculadora_criptografica.py (Streamlit) + crypto_logic.py",
                        ParagraphStyle(name="Portada5", fontSize=11, alignment=1, spaceBefore=20,
                                       textColor=colors.HexColor("#666666"))))
story.append(PageBreak())

# ============================================================
# 1. MATEMÁTICA MODULAR
# ============================================================
titulo_menu("1. Operaciones matemáticas modulares")

subtitulo("1.1 Módulo de dos números (a mod n = b)")
r = cl.calcular_modulo(27, 5)
texto(f"Entrada: a = {r['a']}, n = {r['n']}")
texto(r["explicacion"])
tabla_dict(r["tabla"])

subtitulo("1.2 Inverso aditivo")
r = cl.inverso_aditivo(7, 12)
texto(f"Entrada: a = {r['a']}, n = {r['n']}")
texto(r["explicacion"])
tabla_dict(r["tabla"])

subtitulo("1.3 Inverso de XOR")
r = cl.inverso_xor(173, 201)
texto(f"Entrada: a = {r['a']}, n (objetivo) = {r['n']}")
texto(r["explicacion"])
tabla_dict(r["tabla"])

subtitulo("1.4 MCD (Algoritmo de Euclides) e inverso multiplicativo")
r = cl.mcd_euclides(25, 9)
texto(f"Entrada: a = {r['a']}, b = {r['b']}")
texto(r["explicacion"])
tabla_dict(r["tabla"])
texto("Contraejemplo (no existe inverso, mcd ≠ 1):")
r2 = cl.mcd_euclides(24, 9)
texto(r2["explicacion"])
tabla_dict(r2["tabla"])

subtitulo("1.5 Inverso multiplicativo — método tradicional")
r = cl.inverso_multiplicativo_tradicional(7, 26)
texto(f"Entrada: a = {r['a']}, n = {r['n']}")
texto(r["explicacion"])
tabla_dict(r["tabla"])

subtitulo("1.6 Inverso multiplicativo — Algoritmo Extendido de Euclides (AEE)")
r = cl.inverso_multiplicativo_aee(7, 26)
texto(f"Entrada: a = {r['a']}, n = {r['n']}")
texto(r["explicacion"])
tabla_dict(r["tabla"])
story.append(PageBreak())

# ============================================================
# 2. CRIPTOGRAFÍA CLÁSICA
# ============================================================
titulo_menu("2. Criptografía Clásica")

subtitulo("2.1 Cifrado Módulo 27")
texto_plano = "HOLA MUNDO"
r = cl.cifrado_modulo27(texto_plano, 3, "cifrar")
texto(f"Texto plano: {texto_plano}   |   Clave k = 3")
texto(f"Texto cifrado: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])
rd = cl.cifrado_modulo27(r["resultado"], 3, "descifrar")
texto(f"Verificación — texto descifrado: <b>{rd['resultado']}</b>")

subtitulo("2.2 Cifrado César")
r = cl.cifrado_cesar(texto_plano, 3, "cifrar")
texto(f"Texto plano: {texto_plano}   |   Clave k = 3")
texto(f"Texto cifrado: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])

subtitulo("2.3 Cifrado Vernam (XOR)")
r = cl.cifrado_vernam("HOLA", "CLAVE", "cifrar")
texto(f"Texto plano: HOLA   |   Clave: CLAVE")
texto(f"Texto cifrado (hex): <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])
rd = cl.cifrado_vernam(r["resultado"], "CLAVE", "descifrar")
texto(f"Verificación — texto descifrado: <b>{rd['resultado']}</b>")

subtitulo("2.4 Cifrado ATBASH")
r = cl.cifrado_atbash(texto_plano)
texto(f"Texto plano: {texto_plano}")
texto(f"Texto cifrado: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])

subtitulo("2.5 Cifrador de transposición columnar simple")
r = cl.cifrado_transposicion_columnar("ATACARALAMANECER", "ZORRO", "cifrar")
texto(f"Texto plano: ATACARALAMANECER   |   Clave: ZORRO")
texto(f"Orden de lectura de columnas (según orden alfabético de la clave): {r['orden_columnas']}")
texto(f"Texto cifrado: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])

subtitulo("2.6 Cifrado Afín")
r = cl.cifrado_afin(texto_plano, 5, 8, "cifrar")
texto(f"Texto plano: {texto_plano}   |   a = 5, b = 8, m = 26 (inverso de a = {r['a_inverso']})")
texto(f"Texto cifrado: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])

subtitulo("2.7 Cifra de Sustitución Simple")
r = cl.cifrado_sustitucion_simple(texto_plano, None, "cifrar")
texto(f"Texto plano: {texto_plano}")
texto(f"Alfabeto de sustitución generado (A..Z →): {r['alfabeto_sustitucion']}")
texto(f"Texto cifrado: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])
story.append(PageBreak())

# ============================================================
# 3. CRIPTOGRAFÍA MODERNA
# ============================================================
titulo_menu("3. Criptografía Moderna")

subtitulo("3.1 Diffie-Hellman")
r = cl.diffie_hellman(23, 5, 6, 15)
texto(f"Parámetros públicos: p = {r['p']} (primo), g = {r['g']} (generador)")
texto(f"Clave privada de A = {r['a_priv']}  |  Clave privada de B = {r['b_priv']}")
texto(f"Secreto compartido calculado por ambos: <b>{r['secreto_compartido_A']}</b> "
      f"(coinciden: {'Sí' if r['coinciden'] else 'No'})")
tabla_dict(r["tabla"])

subtitulo("3.2 RSA")
r = cl.rsa(61, 53, 17, 65)
texto(f"Primos: p = {r['p']}, q = {r['q']}  →  n = {r['n']}, φ(n) = {r['phi_n']}")
texto(f"Clave pública (e, n) = ({r['e']}, {r['n']})   |   Clave privada (d, n) = ({r['d']}, {r['n']})")
texto(f"Mensaje M = {r['mensaje']}  →  Cifrado C = {r['cifrado']}  →  Descifrado M' = {r['descifrado']}")
tabla_dict(r["tabla"])
tabla_dict(r["tabla_mensaje"])

subtitulo("3.3 Algoritmo de exponenciación rápida (cuadrado y multiplicación)")
r = cl.exponenciacion_rapida(3, 13, 7)
texto(f"Calcular {r['base']}^{r['exponente']} mod {r['modulo']} → Resultado: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])
story.append(PageBreak())

# ============================================================
# 4. ALGORITMOS HASH
# ============================================================
titulo_menu("4. Algoritmos Hash")
texto_hash = "ciberseguridad2026"

subtitulo("4.1 MD5")
r = cl.calcular_hash(texto_hash, "md5")
texto(f"Texto: {texto_hash}")
story.append(Paragraph(f"Hash MD5: {r['hash']}", styles["Mono"]))

subtitulo("4.2 SHA256")
r = cl.calcular_hash(texto_hash, "sha256")
story.append(Paragraph(f"Hash SHA256: {r['hash']}", styles["Mono"]))

subtitulo("4.3 SHA512")
r = cl.calcular_hash(texto_hash, "sha512")
story.append(Paragraph(f"Hash SHA512: {r['hash']}", styles["Mono"]))
story.append(Spacer(1, 10))

# ============================================================
# 5. CODIFICACIÓN
# ============================================================
titulo_menu("5. Codificación")
texto_cod = "HOLA"

subtitulo("5.1 ASCII")
r = cl.codificar_ascii(texto_cod)
texto(f"Texto: {texto_cod}  →  Códigos ASCII: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])

subtitulo("5.2 Hexadecimal")
r = cl.codificar_hexa(texto_cod)
texto(f"Texto: {texto_cod}  →  Hexadecimal: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])

subtitulo("5.3 Binario")
r = cl.codificar_binario(texto_cod)
texto(f"Texto: {texto_cod}  →  Binario: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])

subtitulo("5.4 Base64")
r = cl.codificar_base64(texto_cod)
texto(f"Texto: {texto_cod}  →  Base64: <b>{r['resultado']}</b>")
tabla_dict(r["tabla"])
story.append(PageBreak())

# ============================================================
# 6. USO DE SALT
# ============================================================
titulo_menu("6. Uso de SALT")
clave_salt = "MiClave123"
salts_demo = ["a1B9", "z7Kq", "Xy02", "salt_2026"]
texto(f"Clave/contraseña usada en los tres ejemplos: <b>{clave_salt}</b>. "
      "Nótese que, aunque la clave es la misma, el hash resultante cambia por completo "
      "al variar el SALT — esto evita ataques de diccionario/rainbow tables.")

subtitulo("6.1 MD5 con SALT diferentes")
r = cl.hash_con_salts(clave_salt, "md5", salts_demo)
tabla_salt(r["tabla"])

subtitulo("6.2 SHA256 con SALT diferentes")
r = cl.hash_con_salts(clave_salt, "sha256", salts_demo)
tabla_salt(r["tabla"])

subtitulo("6.3 SHA512 con SALT diferentes")
r = cl.hash_con_salts(clave_salt, "sha512", salts_demo)
tabla_salt(r["tabla"])

# ============================================================
doc = SimpleDocTemplate("Calculadora_Criptografica_Ejemplos.pdf", pagesize=letter,
                         topMargin=1.5 * cm, bottomMargin=1.5 * cm,
                         leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                         title="Calculadora Criptográfica - Ejemplos")
doc.build(story)
print("PDF generado correctamente.")
