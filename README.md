# Calculadora Criptográfica

Aplicación web desarrollada en Python con Streamlit que implementa operaciones
de matemática modular, criptografía clásica y moderna, algoritmos hash,
codificación y uso de SALT — desarrollada como taller de la asignatura de
Ciberseguridad, Ingeniería de Sistemas, UNAB.

## Demo en vivo

**[calculadora-criptografica-n9eucrfmexylsbhmq2e8sr.streamlit.app](https://calculadora-criptografica-n9eucrfmexylsbhmq2e8sr.streamlit.app)**

> Nota: Streamlit Community Cloud pone la aplicación en reposo tras un
> periodo de inactividad. Si al ingresar aparece un mensaje de "waking up",
> espera unos segundos mientras se reactiva.

## Funcionalidades

**1. Operaciones matemáticas modulares**
Módulo, inverso aditivo, inverso de XOR, máximo común divisor (Algoritmo de
Euclides) e inverso multiplicativo (método tradicional y Algoritmo Extendido
de Euclides, con tabla de rondas).

**2. Criptografía clásica**
Cifrado módulo 27, César, Vernam, Atbash, transposición columnar simple,
cifrado afín y sustitución simple.

**3. Criptografía moderna**
Intercambio de claves Diffie-Hellman, cifrado y descifrado RSA, y algoritmo
de exponenciación rápida (cuadrado y multiplicación).

**4. Algoritmos hash**
MD5, SHA-256 y SHA-512.

**5. Codificación**
Conversión entre texto, ASCII, hexadecimal, binario y Base64.

**6. Uso de SALT**
Generación de hashes con distintos valores de SALT sobre una misma clave,
para ilustrar su efecto en la seguridad del hash resultante.

Cada operación muestra el resultado junto con una tabla del procedimiento
paso a paso.

## Estructura del proyecto

```
calculadora-criptografica/
├── app/
│   └── calculadora_criptografica.py   # Aplicación (lógica + interfaz Streamlit)
├── docs/
│   ├── Calculadora_Criptografica_Ejemplos.pdf   # Ejemplo resuelto por cada submenú
│   └── generar_pdf_ejemplos.py                  # Script generador del PDF
└── README.md
```

## Tecnologías

- Python 3
- Streamlit
- Pandas

## Ejecución local

```bash
pip install streamlit pandas
streamlit run app/calculadora_criptografica.py
```

La aplicación se abre automáticamente en `http://localhost:8501`.

## Autora

María Isabel Vargas Mendoza — Ingeniería de Sistemas, UNAB
