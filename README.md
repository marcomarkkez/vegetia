# VegetIA — Avance de proyecto 1

Chatbot por reglas (Python + NLTK) que orienta a operadores de una línea de empaque de hortalizas sobre criterios de calidad, producto dañado, piezas por caja, uso de la mesa de inspección y reporte de fallas.

> Las cifras de empaque y los criterios de calidad de `intents.json` son **ficticios**, creados para el ejercicio.

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `intents.json` | Base de conocimiento: palabras clave y respuestas por intención |
| `chatbot.py` | Preprocesamiento (NLTK), detección de intención, respuesta y ciclo de conversación |
| `pruebas.py` | Ejecuta las 10 pruebas y genera la tabla de evidencias y las transcripciones |
| `VegetIA_Avance1.ipynb` | Notebook de Colab con instalación, conversación interactiva y pruebas |

## Requisitos

- Python 3.10 o superior
- NLTK (`pip install nltk`)

## Cómo ejecutar

```bash
pip install nltk
python chatbot.py     # conversación interactiva; escribe "adiós" para salir
python pruebas.py     # 10 pruebas + tabla de evidencias
```

En Google Colab: sube `intents.json`, `chatbot.py` y `pruebas.py`, o abre el notebook y ejecuta las celdas en orden.

## Intenciones

`saludo`, `criterios_calidad`, `producto_dañado`, `especificacion_empaque`, `reportar_falla`, `uso_mesa_inspeccion`, `despedida` y `respaldo`.
