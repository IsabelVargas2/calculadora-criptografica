# -*- coding: utf-8 -*-
"""
Calculadora Criptográfica - Taller de Ciberseguridad
Autora: María Isabel Vargas Mendoza (Isa)
UNAB - Ingeniería de Sistemas

Ejecutar con:  streamlit run calculadora_criptografica.py
"""

import streamlit as st
import pandas as pd
import crypto_logic as cl

st.set_page_config(page_title="Calculadora Criptográfica", page_icon="🔐", layout="centered")

st.title("🔐 Calculadora Criptográfica")
st.caption("Taller de Ciberseguridad — Matemática modular, criptografía clásica y moderna, hash, codificación y SALT")

MENU_PRINCIPAL = {
    "1. Operaciones matemáticas modulares": [
        "1.1 Calcular el módulo de dos números (a mod n = b)",
        "1.2 Calcular inverso aditivo",
        "1.3 Calcular inverso de XOR",
        "1.4 Calcular MCD (Euclides) e indicar si existe inverso multiplicativo",
        "1.5 Calcular inverso multiplicativo (método tradicional)",
        "1.6 Calcular inverso multiplicativo (Algoritmo Extendido de Euclides - AEE)",
    ],
    "2. Criptografía Clásica": [
        "2.1 Cifrado Módulo 27",
        "2.2 Cifrado César",
        "2.3 Cifrado Vernam",
        "2.4 Cifrado ATBASH",
        "2.5 Cifrador de transposición columnar simple",
        "2.6 Cifrado Afín",
        "2.7 Cifra de Sustitución Simple",
    ],
    "3. Criptografía Moderna": [
        "3.1 Diffie-Hellman",
        "3.2 RSA",
        "3.3 Algoritmo de exponenciación rápida",
    ],
    "4. Algoritmos Hash": [
        "4.1 MD5",
        "4.2 SHA256",
        "4.3 SHA512",
    ],
    "5. Codificación": [
        "5.1 Codificar / decodificar ASCII",
        "5.2 Codificar / decodificar Hexadecimal",
        "5.3 Codificar / decodificar Binario",
        "5.4 Codificar / decodificar Base64",
    ],
    "6. Uso de SALT": [
        "6.1 Hash de claves con MD5 y SALT diferentes",
        "6.2 Hash de claves con SHA256 y SALT diferentes",
        "6.3 Hash de claves con SHA512 y SALT diferentes",
    ],
}

with st.sidebar:
    st.header("Menú")
    menu = st.selectbox("Selecciona el menú principal", list(MENU_PRINCIPAL.keys()))
    submenu = st.selectbox("Selecciona la opción", MENU_PRINCIPAL[menu])

st.divider()
st.subheader(submenu)


def mostrar(resultado, campos_resumen=None):
    """Muestra la tabla de pasos y un resumen de campos clave."""
    if campos_resumen:
        cols = st.columns(len(campos_resumen))
        for c, (etiqueta, valor) in zip(cols, campos_resumen.items()):
            c.metric(etiqueta, valor)
    if "explicacion" in resultado:
        st.info(resultado["explicacion"])
    if resultado.get("tabla"):
        st.write("**Tabla de resultados / pasos:**")
        st.dataframe(pd.DataFrame(resultado["tabla"]), use_container_width=True)


# ------------------------------------------------------------------
# 1. MATEMÁTICA MODULAR
# ------------------------------------------------------------------
if submenu.startswith("1.1"):
    a = st.number_input("a", value=27, step=1)
    n = st.number_input("n", value=5, step=1, min_value=1)
    if st.button("Calcular"):
        r = cl.calcular_modulo(int(a), int(n))
        mostrar(r, {"a mod n": r["b"]})

elif submenu.startswith("1.2"):
    a = st.number_input("a", value=7, step=1)
    n = st.number_input("n (módulo)", value=12, step=1, min_value=1)
    if st.button("Calcular"):
        r = cl.inverso_aditivo(int(a), int(n))
        mostrar(r, {"Inverso aditivo": r["inverso_aditivo"]})

elif submenu.startswith("1.3"):
    a = st.number_input("a", value=173, step=1, min_value=0)
    n = st.number_input("n (valor objetivo)", value=201, step=1, min_value=0)
    if st.button("Calcular"):
        r = cl.inverso_xor(int(a), int(n))
        mostrar(r, {"x = a XOR n": r["x"]})

elif submenu.startswith("1.4"):
    a = st.number_input("a", value=25, step=1, min_value=1)
    b = st.number_input("b (n)", value=9, step=1, min_value=1)
    if st.button("Calcular"):
        r = cl.mcd_euclides(int(a), int(b))
        mostrar(r, {"MCD": r["mcd"], "¿Existe inverso?": "Sí" if r["existe_inverso_multiplicativo"] else "No"})

elif submenu.startswith("1.5"):
    a = st.number_input("a", value=7, step=1, min_value=1)
    n = st.number_input("n (módulo)", value=26, step=1, min_value=2)
    if st.button("Calcular"):
        r = cl.inverso_multiplicativo_tradicional(int(a), int(n))
        mostrar(r, {"Inverso": r["inverso"] if r["inverso"] is not None else "No existe"})

elif submenu.startswith("1.6"):
    a = st.number_input("a", value=7, step=1, min_value=1)
    n = st.number_input("n (módulo)", value=26, step=1, min_value=2)
    if st.button("Calcular"):
        r = cl.inverso_multiplicativo_aee(int(a), int(n))
        mostrar(r, {"Inverso": r["inverso"] if r["existe"] else "No existe", "Rondas": r["rondas"]})

# ------------------------------------------------------------------
# 2. CRIPTOGRAFÍA CLÁSICA
# ------------------------------------------------------------------
elif submenu.startswith("2.1"):
    texto = st.text_input("Texto", value="HOLA MUNDO")
    k = st.number_input("Clave k", value=3, step=1)
    modo = st.radio("Modo", ["cifrar", "descifrar"], horizontal=True)
    if st.button("Calcular"):
        r = cl.cifrado_modulo27(texto, int(k), modo)
        mostrar(r, {"Resultado": r["resultado"]})

elif submenu.startswith("2.2"):
    texto = st.text_input("Texto", value="HOLA MUNDO")
    k = st.number_input("Clave k (desplazamiento)", value=3, step=1)
    modo = st.radio("Modo", ["cifrar", "descifrar"], horizontal=True)
    if st.button("Calcular"):
        r = cl.cifrado_cesar(texto, int(k), modo)
        mostrar(r, {"Resultado": r["resultado"]})

elif submenu.startswith("2.3"):
    modo = st.radio("Modo", ["cifrar", "descifrar"], horizontal=True)
    if modo == "cifrar":
        texto = st.text_input("Texto plano", value="HOLA")
    else:
        texto = st.text_input("Texto cifrado (hex)", value="")
    clave = st.text_input("Clave", value="CLAVE")
    if st.button("Calcular"):
        r = cl.cifrado_vernam(texto, clave, modo)
        mostrar(r, {"Resultado": r["resultado"]})

elif submenu.startswith("2.4"):
    texto = st.text_input("Texto", value="HOLA MUNDO")
    if st.button("Calcular"):
        r = cl.cifrado_atbash(texto)
        mostrar(r, {"Resultado": r["resultado"]})

elif submenu.startswith("2.5"):
    texto = st.text_input("Texto", value="ATACARALAMANECER")
    clave = st.text_input("Clave (palabra clave)", value="ZORRO")
    modo = st.radio("Modo", ["cifrar", "descifrar"], horizontal=True)
    if st.button("Calcular"):
        r = cl.cifrado_transposicion_columnar(texto, clave.upper(), modo)
        mostrar(r, {"Resultado": r["resultado"], "Orden columnas": str(r["orden_columnas"])})

elif submenu.startswith("2.6"):
    texto = st.text_input("Texto", value="HOLA MUNDO")
    a = st.number_input("a (coprimo con 26)", value=5, step=1)
    b = st.number_input("b", value=8, step=1)
    modo = st.radio("Modo", ["cifrar", "descifrar"], horizontal=True)
    if st.button("Calcular"):
        try:
            r = cl.cifrado_afin(texto, int(a), int(b), modo)
            mostrar(r, {"Resultado": r["resultado"], "Inverso de a": r["a_inverso"]})
        except ValueError as e:
            st.error(str(e))

elif submenu.startswith("2.7"):
    texto = st.text_input("Texto", value="HOLA MUNDO")
    clave_sust = st.text_input("Alfabeto de sustitución (26 letras, opcional)", value="")
    modo = st.radio("Modo", ["cifrar", "descifrar"], horizontal=True)
    if st.button("Calcular"):
        r = cl.cifrado_sustitucion_simple(texto, clave_sust or None, modo)
        mostrar(r, {"Resultado": r["resultado"]})
        st.caption(f"Alfabeto de sustitución usado (A..Z ->): {r['alfabeto_sustitucion']}")

# ------------------------------------------------------------------
# 3. CRIPTOGRAFÍA MODERNA
# ------------------------------------------------------------------
elif submenu.startswith("3.1"):
    p = st.number_input("p (número primo)", value=23, step=1, min_value=2)
    g = st.number_input("g (raíz primitiva / generador)", value=5, step=1, min_value=2)
    a_priv = st.number_input("Clave privada de A", value=6, step=1, min_value=1)
    b_priv = st.number_input("Clave privada de B", value=15, step=1, min_value=1)
    if st.button("Calcular"):
        r = cl.diffie_hellman(int(p), int(g), int(a_priv), int(b_priv))
        mostrar(r, {"Secreto compartido": r["secreto_compartido_A"],
                     "¿Coinciden?": "Sí ✅" if r["coinciden"] else "No"})

elif submenu.startswith("3.2"):
    p = st.number_input("p (primo)", value=61, step=1, min_value=2)
    q = st.number_input("q (primo)", value=53, step=1, min_value=2)
    e_manual = st.text_input("e (dejar vacío para autoseleccionar)", value="17")
    mensaje = st.text_input("Mensaje numérico M (opcional, M < n)", value="65")
    if st.button("Calcular"):
        try:
            e_val = int(e_manual) if e_manual.strip() else None
            m_val = int(mensaje) if mensaje.strip() else None
            r = cl.rsa(int(p), int(q), e_val, m_val)
            resumen = {"n": r["n"], "e": r["e"], "d": r["d"]}
            if "cifrado" in r:
                resumen["Cifrado"] = r["cifrado"]
            mostrar(r, resumen)
            if r.get("tabla_mensaje"):
                st.write("**Cifrado / descifrado del mensaje:**")
                st.dataframe(pd.DataFrame(r["tabla_mensaje"]), use_container_width=True)
        except ValueError as e:
            st.error(str(e))

elif submenu.startswith("3.3"):
    base = st.number_input("Base", value=7, step=1)
    exp = st.number_input("Exponente", value=560, step=1, min_value=0)
    mod = st.number_input("Módulo", value=561, step=1, min_value=1)
    if st.button("Calcular"):
        r = cl.exponenciacion_rapida(int(base), int(exp), int(mod))
        mostrar(r, {"Resultado": r["resultado"]})

# ------------------------------------------------------------------
# 4. ALGORITMOS HASH
# ------------------------------------------------------------------
elif submenu.startswith("4.1"):
    texto = st.text_input("Texto a hashear", value="ciberseguridad2026")
    if st.button("Calcular"):
        r = cl.calcular_hash(texto, "md5")
        mostrar(r, {"MD5": r["hash"]})

elif submenu.startswith("4.2"):
    texto = st.text_input("Texto a hashear", value="ciberseguridad2026")
    if st.button("Calcular"):
        r = cl.calcular_hash(texto, "sha256")
        mostrar(r, {"SHA256": r["hash"][:20] + "..."})

elif submenu.startswith("4.3"):
    texto = st.text_input("Texto a hashear", value="ciberseguridad2026")
    if st.button("Calcular"):
        r = cl.calcular_hash(texto, "sha512")
        mostrar(r, {"SHA512": r["hash"][:20] + "..."})

# ------------------------------------------------------------------
# 5. CODIFICACIÓN
# ------------------------------------------------------------------
elif submenu.startswith("5.1"):
    modo = st.radio("Modo", ["codificar", "decodificar"], horizontal=True)
    texto = st.text_input("Texto" if modo == "codificar" else "Códigos ASCII separados por espacio",
                           value="HOLA" if modo == "codificar" else "72 79 76 65")
    if st.button("Calcular"):
        r = cl.codificar_ascii(texto, modo)
        mostrar(r, {"Resultado": r["resultado"]})

elif submenu.startswith("5.2"):
    modo = st.radio("Modo", ["codificar", "decodificar"], horizontal=True)
    texto = st.text_input("Texto" if modo == "codificar" else "Hexadecimal",
                           value="HOLA" if modo == "codificar" else "486f6c61")
    if st.button("Calcular"):
        r = cl.codificar_hexa(texto, modo)
        mostrar(r, {"Resultado": r["resultado"]})

elif submenu.startswith("5.3"):
    modo = st.radio("Modo", ["codificar", "decodificar"], horizontal=True)
    texto = st.text_input("Texto" if modo == "codificar" else "Binario (grupos de 8 bits separados por espacio)",
                           value="HOLA" if modo == "codificar" else "01001000 01001111 01001100 01000001")
    if st.button("Calcular"):
        r = cl.codificar_binario(texto, modo)
        mostrar(r, {"Resultado": r["resultado"]})

elif submenu.startswith("5.4"):
    modo = st.radio("Modo", ["codificar", "decodificar"], horizontal=True)
    texto = st.text_input("Texto" if modo == "codificar" else "Base64",
                           value="HOLA" if modo == "codificar" else "SE9MQQ==")
    if st.button("Calcular"):
        r = cl.codificar_base64(texto, modo)
        mostrar(r, {"Resultado": r["resultado"]})

# ------------------------------------------------------------------
# 6. USO DE SALT
# ------------------------------------------------------------------
elif submenu.startswith("6.1"):
    clave = st.text_input("Clave / contraseña", value="MiClave123")
    salts_txt = st.text_input("Salts (separados por coma)", value="a1B9,z7Kq,Xy02,salt_2026")
    if st.button("Calcular"):
        r = cl.hash_con_salts(clave, "md5", [s.strip() for s in salts_txt.split(",")])
        mostrar(r)

elif submenu.startswith("6.2"):
    clave = st.text_input("Clave / contraseña", value="MiClave123")
    salts_txt = st.text_input("Salts (separados por coma)", value="a1B9,z7Kq,Xy02,salt_2026")
    if st.button("Calcular"):
        r = cl.hash_con_salts(clave, "sha256", [s.strip() for s in salts_txt.split(",")])
        mostrar(r)

elif submenu.startswith("6.3"):
    clave = st.text_input("Clave / contraseña", value="MiClave123")
    salts_txt = st.text_input("Salts (separados por coma)", value="a1B9,z7Kq,Xy02,salt_2026")
    if st.button("Calcular"):
        r = cl.hash_con_salts(clave, "sha512", [s.strip() for s in salts_txt.split(",")])
        mostrar(r)

st.divider()
st.caption("Taller de Ciberseguridad · Calculadora Criptográfica")
