# -*- coding: utf-8 -*-
"""
crypto_logic.py
Lógica pura (sin interfaz) de la Calculadora Criptográfica.
Cada función retorna un diccionario con los resultados y, cuando aplica,
una lista de filas (pasos) para construir una tabla en la interfaz.

Autora: Isa Vargas
Taller: Calculadora Criptográfica - Ciberseguridad
"""

import hashlib
import base64
import random
import string

# =========================================================
# 1. OPERACIONES MATEMÁTICAS MODULARES
# =========================================================

def calcular_modulo(a: int, n: int):
    """1.1 a mod n = b"""
    if n == 0:
        raise ValueError("n no puede ser 0")
    b = a % n
    cociente = a // n
    return {
        "a": a, "n": n, "b": b,
        "explicacion": f"{a} = ({n} x {cociente}) + {b}  ->  {a} mod {n} = {b}",
        "tabla": [{"a": a, "n": n, "cociente (q)": cociente, "resto (a mod n)": b}]
    }


def inverso_aditivo(a: int, n: int):
    """1.2 Inverso aditivo de a mod n: x tal que (a + x) mod n = 0"""
    a_mod = a % n
    x = (n - a_mod) % n
    return {
        "a": a, "n": n, "a_mod_n": a_mod, "inverso_aditivo": x,
        "explicacion": f"({a} + {x}) mod {n} = {(a_mod + x) % n}",
        "tabla": [{"a mod n": a_mod, "n - (a mod n)": n - a_mod if a_mod != 0 else 0,
                   "Inverso aditivo": x, "Comprobación (a+x) mod n": (a_mod + x) % n}]
    }


def inverso_xor(a: int, n: int):
    """
    1.3 Inverso de XOR.
    El XOR es autoinverso: dado a y una "llave"/objetivo n, el valor x que cumple
    a XOR x = n es x = a XOR n (y también x XOR a = n, x XOR n = a).
    """
    x = a ^ n
    comprobacion = a ^ x
    return {
        "a": a, "n": n, "x": x,
        "bin_a": format(a, "08b"), "bin_n": format(n, "08b"), "bin_x": format(x, "08b"),
        "explicacion": f"x = a XOR n = {a} XOR {n} = {x}  (comprobación: a XOR x = {comprobacion})",
        "tabla": [{"a": a, "n (objetivo)": n, "x = a XOR n": x,
                   "bin(a)": format(a, "08b"), "bin(n)": format(n, "08b"), "bin(x)": format(x, "08b"),
                   "Comprobación": comprobacion}]
    }


def mcd_euclides(a: int, b: int):
    """1.4 MCD por algoritmo de Euclides + indica si existe inverso multiplicativo"""
    filas = []
    x, y = a, b
    ronda = 0
    while y != 0:
        q = x // y
        r = x % y
        filas.append({"Ronda": ronda, "x": x, "y": y, "cociente (q)": q, "residuo (r)": r})
        x, y = y, r
        ronda += 1
    mcd = x
    existe_inverso = (mcd == 1)
    return {
        "a": a, "b": b, "mcd": mcd, "existe_inverso_multiplicativo": existe_inverso,
        "explicacion": f"mcd({a},{b}) = {mcd}. "
                       + ("Como mcd = 1, SÍ existe inverso multiplicativo."
                          if existe_inverso else
                          "Como mcd != 1, NO existe inverso multiplicativo."),
        "tabla": filas
    }


def inverso_multiplicativo_tradicional(a: int, n: int):
    """1.5 Método tradicional: probar x = 1..n-1 hasta que (a*x) mod n == 1"""
    filas = []
    resultado = None
    for x in range(1, n):
        producto = (a * x) % n
        filas.append({"x probado": x, "(a*x) mod n": producto,
                       "¿Es 1?": "SÍ ✅" if producto == 1 else "No"})
        if producto == 1 and resultado is None:
            resultado = x
    return {
        "a": a, "n": n, "inverso": resultado,
        "existe": resultado is not None,
        "explicacion": (f"El inverso multiplicativo de {a} mod {n} es {resultado}"
                         if resultado is not None else
                         f"No existe inverso multiplicativo de {a} mod {n} (mcd(a,n) != 1)"),
        "tabla": filas
    }


def inverso_multiplicativo_aee(a: int, n: int):
    """
    1.6 Algoritmo Extendido de Euclides (AEE).
    Calcula el inverso multiplicativo de a mod n, mostrando la tabla de rondas
    (cociente, residuos, y los coeficientes de Bézout) y la cantidad de rondas usadas.
    """
    filas = []
    old_r, r = a % n, n
    old_s, s = 1, 0
    old_t, t = 0, 1
    ronda = 0
    while r != 0:
        q = old_r // r
        filas.append({
            "Ronda": ronda, "q (cociente)": q,
            "r": old_r, "r_sig": r, "nuevo r": old_r - q * r,
            "s": old_s, "t": old_t
        })
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        ronda += 1
    mcd = old_r
    inverso = old_s % n if mcd == 1 else None
    return {
        "a": a, "n": n, "mcd": mcd, "inverso": inverso,
        "rondas": ronda,
        "existe": mcd == 1,
        "explicacion": (f"AEE usó {ronda} rondas. mcd({a},{n})={mcd}. "
                         f"Inverso multiplicativo de {a} mod {n} = {inverso}"
                         if mcd == 1 else
                         f"AEE usó {ronda} rondas. mcd({a},{n})={mcd} != 1, no existe inverso."),
        "tabla": filas
    }


# =========================================================
# 2. CRIPTOGRAFÍA CLÁSICA
# =========================================================

ALFABETO_27 = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"  # 27 letras (incluye Ñ), sin espacio


def _limpiar_texto(texto: str, alfabeto: str):
    texto = texto.upper()
    return "".join(c for c in texto if c in alfabeto)


def cifrado_modulo27(texto: str, k: int, modo: str = "cifrar"):
    """2.1 Cifrado por desplazamiento en módulo 27 (alfabeto español con Ñ, sin espacios)"""
    texto_limpio = _limpiar_texto(texto, ALFABETO_27)
    resultado = []
    filas = []
    for c in texto_limpio:
        p = ALFABETO_27.index(c)
        if modo == "cifrar":
            c_out = (p + k) % 27
        else:
            c_out = (p - k) % 27
        letra_out = ALFABETO_27[c_out]
        resultado.append(letra_out)
        filas.append({"Letra": c, "Posición (0-26)": p, "Operación": f"({p} {'+' if modo=='cifrar' else '-'} {k}) mod 27",
                       "Resultado": c_out, "Letra resultante": letra_out})
    return {"texto_entrada": texto_limpio, "k": k, "modo": modo,
            "resultado": "".join(resultado), "tabla": filas}


def cifrado_cesar(texto: str, k: int, modo: str = "cifrar"):
    """2.2 Cifrado César clásico, alfabeto de 26 letras A-Z"""
    alfabeto = string.ascii_uppercase
    texto_limpio = _limpiar_texto(texto, alfabeto)
    resultado = []
    filas = []
    for c in texto_limpio:
        p = alfabeto.index(c)
        c_out = (p + k) % 26 if modo == "cifrar" else (p - k) % 26
        letra_out = alfabeto[c_out]
        resultado.append(letra_out)
        filas.append({"Letra": c, "Posición": p, "Desplazamiento (k)": k, "Letra resultante": letra_out})
    return {"texto_entrada": texto_limpio, "k": k, "modo": modo,
            "resultado": "".join(resultado), "tabla": filas}


def cifrado_vernam(texto: str, clave: str, modo: str = "cifrar"):
    """
    2.3 Cifrado Vernam (XOR bit a bit / one-time pad).
    La clave debe tener al menos la longitud del texto (se repite si es más corta,
    como variante didáctica del Vernam puro).
    """
    datos = texto.encode("utf-8") if modo == "cifrar" else bytes.fromhex(texto)
    clave_bytes = clave.encode("utf-8")
    filas = []
    salida = bytearray()
    for i, b in enumerate(datos):
        k = clave_bytes[i % len(clave_bytes)]
        r = b ^ k
        salida.append(r)
        filas.append({"i": i, "Byte texto": b, "Byte clave": k, "XOR (resultado)": r})
    if modo == "cifrar":
        resultado = salida.hex()
    else:
        resultado = salida.decode("utf-8", errors="replace")
    return {"clave": clave, "modo": modo, "resultado": resultado, "tabla": filas}


ALFABETO_ATBASH = string.ascii_uppercase


def cifrado_atbash(texto: str):
    """2.4 Cifrado Atbash: invierte el alfabeto (A<->Z, B<->Y, ...). Es simétrico."""
    texto_limpio = _limpiar_texto(texto, ALFABETO_ATBASH)
    filas = []
    resultado = []
    for c in texto_limpio:
        p = ALFABETO_ATBASH.index(c)
        c_out = 25 - p
        letra_out = ALFABETO_ATBASH[c_out]
        resultado.append(letra_out)
        filas.append({"Letra": c, "Posición": p, "25 - posición": c_out, "Letra resultante": letra_out})
    return {"texto_entrada": texto_limpio, "resultado": "".join(resultado), "tabla": filas}


def cifrado_transposicion_columnar(texto: str, clave: str, modo: str = "cifrar"):
    """2.5 Cifrador de transposición columnar simple, usando el orden alfabético de la clave."""
    texto = texto.upper().replace(" ", "")
    n_cols = len(clave)
    orden = sorted(range(n_cols), key=lambda i: clave[i])  # orden de lectura de columnas

    if modo == "cifrar":
        filas_grid = [texto[i:i + n_cols] for i in range(0, len(texto), n_cols)]
        # rellenar la última fila
        if filas_grid and len(filas_grid[-1]) < n_cols:
            filas_grid[-1] = filas_grid[-1] + "X" * (n_cols - len(filas_grid[-1]))
        columnas = []
        for c in range(n_cols):
            columnas.append("".join(fila[c] for fila in filas_grid))
        resultado = "".join(columnas[i] for i in orden)
        tabla = [{"Fila": idx, **{f"Col {c+1} ({clave[c]})": (filas_grid[idx][c] if c < len(filas_grid[idx]) else "")
                                   for c in range(n_cols)}} for idx in range(len(filas_grid))]
    else:
        n_filas = -(-len(texto) // n_cols)  # techo
        largo_col = n_filas
        # última columna puede estar incompleta si el texto no llena la grilla
        total = len(texto)
        cols_completas = total - n_cols * (largo_col - 1)
        columnas_texto = [""] * n_cols
        pos = 0
        long_col_real = [largo_col if orden.index(i) < cols_completas else largo_col for i in range(n_cols)]
        for i in orden:
            columnas_texto[i] = texto[pos:pos + largo_col]
            pos += largo_col
        filas_grid = []
        for f in range(largo_col):
            fila = "".join(columnas_texto[c][f] if f < len(columnas_texto[c]) else "" for c in range(n_cols))
            filas_grid.append(fila)
        resultado = "".join(filas_grid)
        tabla = [{"Fila": idx, **{f"Col {c+1} ({clave[c]})": (filas_grid[idx][c] if c < len(filas_grid[idx]) else "")
                                   for c in range(n_cols)}} for idx in range(len(filas_grid))]

    return {"texto_entrada": texto, "clave": clave, "modo": modo, "orden_columnas": orden,
            "resultado": resultado, "tabla": tabla}


def cifrado_afin(texto: str, a: int, b: int, modo: str = "cifrar", m: int = 26):
    """2.6 Cifrado afín: E(x) = (a*x + b) mod m ; requiere mcd(a,m) = 1"""
    def mcd(x, y):
        while y:
            x, y = y, x % y
        return x

    if mcd(a, m) != 1:
        raise ValueError(f"'a'={a} no es coprimo con m={m}; el cifrado afín no es válido (no invertible).")

    alfabeto = string.ascii_uppercase[:m] if m <= 26 else ALFABETO_27
    texto_limpio = _limpiar_texto(texto, alfabeto)

    # inverso de a mod m (AEE)
    a_inv = None
    for x in range(1, m):
        if (a * x) % m == 1:
            a_inv = x
            break

    filas = []
    resultado = []
    for c in texto_limpio:
        p = alfabeto.index(c)
        if modo == "cifrar":
            c_out = (a * p + b) % m
            op = f"({a}*{p} + {b}) mod {m}"
        else:
            c_out = (a_inv * (p - b)) % m
            op = f"{a_inv}*({p} - {b}) mod {m}"
        letra_out = alfabeto[c_out]
        resultado.append(letra_out)
        filas.append({"Letra": c, "Posición": p, "Operación": op, "Letra resultante": letra_out})

    return {"texto_entrada": texto_limpio, "a": a, "b": b, "m": m, "a_inverso": a_inv,
            "modo": modo, "resultado": "".join(resultado), "tabla": filas}


def cifrado_sustitucion_simple(texto: str, clave_sustitucion: str = None, modo: str = "cifrar", semilla: int = 42):
    """
    2.7 Cifra de sustitución simple (monoalfabética).
    Si no se da una clave de 26 letras, se genera un alfabeto barajado reproducible con 'semilla'.
    """
    alfabeto = string.ascii_uppercase
    if clave_sustitucion is None or len(clave_sustitucion.replace(" ", "")) != 26:
        letras = list(alfabeto)
        random.Random(semilla).shuffle(letras)
        clave_sustitucion = "".join(letras)
    else:
        clave_sustitucion = clave_sustitucion.upper().replace(" ", "")

    texto_limpio = _limpiar_texto(texto, alfabeto)
    mapa_cifrar = dict(zip(alfabeto, clave_sustitucion))
    mapa_descifrar = dict(zip(clave_sustitucion, alfabeto))

    filas = []
    resultado = []
    for c in texto_limpio:
        if modo == "cifrar":
            c_out = mapa_cifrar[c]
        else:
            c_out = mapa_descifrar[c]
        resultado.append(c_out)
        filas.append({"Letra original": c, "Letra sustituida": c_out})

    return {"texto_entrada": texto_limpio, "alfabeto_sustitucion": clave_sustitucion,
            "modo": modo, "resultado": "".join(resultado), "tabla": filas}


# =========================================================
# 3. CRIPTOGRAFÍA MODERNA
# =========================================================

def exponenciacion_rapida(base: int, exponente: int, modulo: int):
    """3.3 Exponenciación rápida (cuadrado y multiplicación / square-and-multiply)"""
    filas = []
    resultado = 1
    b = base % modulo
    e = exponente
    paso = 0
    while e > 0:
        bit = e & 1
        if bit == 1:
            resultado = (resultado * b) % modulo
        filas.append({"Paso": paso, "Exponente restante (bin)": bin(e), "Bit": bit,
                       "base^(2^paso) mod n": b, "Resultado acumulado": resultado})
        b = (b * b) % modulo
        e >>= 1
        paso += 1
    return {"base": base, "exponente": exponente, "modulo": modulo, "resultado": resultado,
            "tabla": filas}


def diffie_hellman(p: int, g: int, a_priv: int, b_priv: int):
    """3.1 Diffie-Hellman: p (primo), g (generador/raíz primitiva), claves privadas a y b"""
    A_pub = pow(g, a_priv, p)   # clave pública de A
    B_pub = pow(g, b_priv, p)   # clave pública de B
    secreto_A = pow(B_pub, a_priv, p)
    secreto_B = pow(A_pub, b_priv, p)
    return {
        "p": p, "g": g, "a_priv": a_priv, "b_priv": b_priv,
        "A_publica": A_pub, "B_publica": B_pub,
        "secreto_compartido_A": secreto_A, "secreto_compartido_B": secreto_B,
        "coinciden": secreto_A == secreto_B,
        "tabla": [
            {"Actor": "A (Alice)", "Clave privada": a_priv, "Clave pública (g^x mod p)": A_pub,
             "Secreto calculado": secreto_A},
            {"Actor": "B (Bob)", "Clave privada": b_priv, "Clave pública (g^x mod p)": B_pub,
             "Secreto calculado": secreto_B},
        ]
    }


def _es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def rsa(p: int, q: int, e: int = None, mensaje: int = None):
    """3.2 RSA: genera n, phi(n), e, d; opcionalmente cifra/descifra un mensaje numérico"""
    if not (_es_primo(p) and _es_primo(q)):
        raise ValueError("p y q deben ser números primos")
    n = p * q
    phi = (p - 1) * (q - 1)

    def mcd(x, y):
        while y:
            x, y = y, x % y
        return x

    if e is None:
        e = 3
        while mcd(e, phi) != 1:
            e += 2

    if mcd(e, phi) != 1:
        raise ValueError(f"e={e} no es coprimo con phi(n)={phi}")

    # inverso modular de e mod phi con AEE
    old_r, r = e, phi
    old_s, s = 1, 0
    while r != 0:
        q_ = old_r // r
        old_r, r = r, old_r - q_ * r
        old_s, s = s, old_s - q_ * s
    d = old_s % phi

    resultado = {
        "p": p, "q": q, "n": n, "phi_n": phi, "e": e, "d": d,
        "clave_publica": (e, n), "clave_privada": (d, n),
        "tabla": [{"n = p*q": n, "phi(n) = (p-1)(q-1)": phi,
                   "e (exponente público)": e, "d (exponente privado)": d}],
        "tabla_mensaje": []
    }

    if mensaje is not None:
        if mensaje >= n:
            raise ValueError(f"El mensaje debe ser menor que n={n}")
        c = pow(mensaje, e, n)
        m_recuperado = pow(c, d, n)
        resultado["mensaje"] = mensaje
        resultado["cifrado"] = c
        resultado["descifrado"] = m_recuperado
        resultado["tabla_mensaje"] = [
            {"Mensaje (M)": mensaje, "Cifrado C = M^e mod n": c, "Descifrado M' = C^d mod n": m_recuperado}
        ]
    return resultado


# =========================================================
# 4. ALGORITMOS HASH
# =========================================================

def calcular_hash(texto: str, algoritmo: str):
    """4.1 / 4.2 / 4.3 MD5, SHA256, SHA512"""
    datos = texto.encode("utf-8")
    if algoritmo == "md5":
        h = hashlib.md5(datos).hexdigest()
    elif algoritmo == "sha256":
        h = hashlib.sha256(datos).hexdigest()
    elif algoritmo == "sha512":
        h = hashlib.sha512(datos).hexdigest()
    else:
        raise ValueError("Algoritmo no soportado")
    return {"texto": texto, "algoritmo": algoritmo, "hash": h, "longitud_bits": len(h) * 4,
            "tabla": [{"Texto": texto, "Algoritmo": algoritmo.upper(), "Hash (hex)": h}]}


# =========================================================
# 5. CODIFICACIÓN
# =========================================================

def codificar_ascii(texto: str, modo: str = "codificar"):
    if modo == "codificar":
        codigos = [ord(c) for c in texto]
        resultado = " ".join(str(c) for c in codigos)
        filas = [{"Carácter": c, "Código ASCII": ord(c)} for c in texto]
    else:
        codigos = [int(x) for x in texto.split()]
        resultado = "".join(chr(c) for c in codigos)
        filas = [{"Código ASCII": c, "Carácter": chr(c)} for c in codigos]
    return {"entrada": texto, "modo": modo, "resultado": resultado, "tabla": filas}


def codificar_hexa(texto: str, modo: str = "codificar"):
    if modo == "codificar":
        resultado = texto.encode("utf-8").hex()
        filas = [{"Carácter": c, "Hex": format(ord(c), "02x")} for c in texto]
    else:
        b = bytes.fromhex(texto.replace(" ", ""))
        resultado = b.decode("utf-8", errors="replace")
        filas = [{"Byte hex": texto[i:i+2], "Carácter": bytes.fromhex(texto[i:i+2]).decode("utf-8", errors="replace")}
                  for i in range(0, len(texto.replace(" ", "")), 2)]
    return {"entrada": texto, "modo": modo, "resultado": resultado, "tabla": filas}


def codificar_binario(texto: str, modo: str = "codificar"):
    if modo == "codificar":
        resultado = " ".join(format(ord(c), "08b") for c in texto)
        filas = [{"Carácter": c, "Binario (8 bits)": format(ord(c), "08b")} for c in texto]
    else:
        grupos = texto.split()
        resultado = "".join(chr(int(g, 2)) for g in grupos)
        filas = [{"Binario": g, "Carácter": chr(int(g, 2))} for g in grupos]
    return {"entrada": texto, "modo": modo, "resultado": resultado, "tabla": filas}


def codificar_base64(texto: str, modo: str = "codificar"):
    if modo == "codificar":
        resultado = base64.b64encode(texto.encode("utf-8")).decode("ascii")
    else:
        resultado = base64.b64decode(texto.encode("ascii")).decode("utf-8", errors="replace")
    return {"entrada": texto, "modo": modo, "resultado": resultado,
            "tabla": [{"Entrada": texto, "Modo": modo, "Resultado": resultado}]}


# =========================================================
# 6. USO DE SALT
# =========================================================

def hash_con_salts(clave: str, algoritmo: str, salts=None):
    """
    6.1 / 6.2 / 6.3 Genera el hash de una misma clave con distintos SALT,
    demostrando que el resultado cambia aunque la clave sea la misma.
    """
    if salts is None:
        salts = ["a1B9", "z7Kq", "Xy02", "salt_2026"]

    func = {"md5": hashlib.md5, "sha256": hashlib.sha256, "sha512": hashlib.sha512}[algoritmo]
    filas = []
    for s in salts:
        combinado = (s + clave).encode("utf-8")
        h = func(combinado).hexdigest()
        filas.append({"Salt": s, "Clave": clave, "Salt+Clave": s + clave, "Hash": h})
    return {"clave": clave, "algoritmo": algoritmo, "salts": salts, "tabla": filas}
