🔗 APP (Streamlit Cloud):
https://calculadora-criptografica-n9eucrfmexylsbhmq2e8sr.streamlit.app

Nota: Streamlit Community Cloud pone la app "a dormir" tras un tiempo sin
visitas. Si al entrar ves un mensaje tipo "Zzz... your app is waking up",
espera 30-60 segundos y se activa sola — no está rota, solo estaba en reposo.

ESTRUCTURA DEL REPOSITORIO:
calculadora-criptografica/
├── app/
│   ├── calculadora_criptografica.py   -> interfaz Streamlit (los 6 menús y submenús)
│   └── crypto_logic.py                -> toda la lógica matemática/criptográfica
├── docs/
│   ├── Calculadora_Criptografica_Ejemplos.pdf -> un ejemplo resuelto de cada submenú, en tablas
│   └── generar_pdf_ejemplos.py        -> script que generó el PDF de ejemplos
└── README.md

CÓMO USAR LA APP:
En la barra lateral se elige el menú principal (1-6) y luego el submenú;
se llenan los campos y se presiona "Calcular". Los resultados y la tabla
de pasos aparecen debajo.
=======
ARCHIVOS:
- calculadora_criptografica.py -> interfaz Streamlit (los 6 menús y submenús)
- crypto_logic.py               -> toda la lógica matemática/criptográfica (probada por separado)
- generar_pdf_ejemplos.py       -> script que generó el PDF de ejemplos
- Calculadora_Criptografica_Ejemplos.pdf -> un ejemplo resuelto de cada submenú, en tablas

CÓMO EJECUTARLA:
1) Instalar dependencias (una sola vez):
   pip install streamlit pandas

2) Ejecutar:
   streamlit run calculadora_criptografica.py

3) Se abre en el navegador (http://localhost:8501). En la barra lateral se elige
   el menú principal (1-6) y luego el submenú; se llenan los campos y se
   presiona "Calcular". Los resultados y la tabla de pasos aparecen debajo.

NOTAS DE CONTENIDO:
- 1.6 (AEE) muestra el número de rondas y la tabla completa (q, r, s, t) en
  cada iteración, tal como pidió el profesor.
- 1.4 y 1.6 indican explícitamente si existe o no el inverso multiplicativo.
- Todos los resultados se presentan en tabla, como se solicitó.
