CALCULADORA CRIPTOGRÁFICA - Taller de Ciberseguridad


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

PENDIENTE POR HACER TÚ (no se puede generar desde aquí):
- Pantallazo de un ejemplo funcionando: corre la app localmente (o en Streamlit
  Cloud, como hiciste con tus otros proyectos) y toma una captura de cualquier
  submenú con un resultado calculado.
- Video de 10 minutos explicando el funcionamiento y cómo se hizo: grábalo
  mostrando la app en vivo (un par de submenús de cada categoría) y comentando
  brevemente crypto_logic.py (una función por categoría basta, no hace falta
  leer todo el código).
- Si el profesor pide notebook de Jupyter en vez de .py: las funciones de
  crypto_logic.py se pueden importar tal cual en un notebook (import crypto_logic
  as cl) y llamarlas en celdas separadas por submenú.

NOTAS DE CONTENIDO:
- 1.6 (AEE) muestra el número de rondas y la tabla completa (q, r, s, t) en
  cada iteración, tal como pidió el profesor.
- 1.4 y 1.6 indican explícitamente si existe o no el inverso multiplicativo.
- Todos los resultados se presentan en tabla, como se solicitó.
