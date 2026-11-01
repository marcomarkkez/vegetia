"""Ejecuta las 10 pruebas del Avance 1 y genera la tabla de evidencias.

Uso: python pruebas.py
Compara la intención esperada contra la detectada y asigna el resultado
con un criterio fijo: correcta / incorrecta / respaldo activado.
"""
import nltk

from chatbot import cargar_intents, procesar

# (escenario, mensajes del operador, intención esperada para cada mensaje)
PRUEBAS = [
    ("Saludo inicial", ["Hola"], ["saludo"]),
    ("Piezas por caja de pimiento", ["¿Cuántas piezas lleva la caja de pimiento?"], ["especificacion_empaque"]),
    ("Mayúsculas y sin acentos", ["CUANTOS PEPINOS VAN EN LA CAJA"], ["especificacion_empaque"]),
    ("Producto con mancha", ["este tomate tiene una mancha"], ["producto_dañado"]),
    ("Variación de palabra (golpeado)", ["este pimiento viene golpeado"], ["producto_dañado"]),
    ("Sinónimo regional (jitomate)", ["¿Qué criterios de calidad tiene el jitomate?"], ["criterios_calidad"]),
    ("Falla de báscula", ["la báscula marca error"], ["reportar_falla"]),
    ("Uso de la mesa de inspección", ["¿cómo uso la mesa de inspección?"], ["uso_mesa_inspeccion"]),
    ("Palabras clave ambiguas", ["la báscula marca menos peso en la caja"], ["reportar_falla"]),
    ("Fuera de dominio y despedida", ["¿a qué hora es la comida?", "gracias, adiós"], ["respaldo", "despedida"]),
]

# Casos en que la intención es correcta, pero la respuesta no lo es
# (p. ej., no reconoce el producto). Se revisan a mano y se anotan aquí.
RESPUESTA_GENERICA = "¿De qué producto?"


def evaluar(esperada: str, detectada: str, respuesta: str) -> str:
    if detectada != esperada:
        return "incorrecta"
    if detectada == "respaldo":
        return "respaldo activado"
    if respuesta.startswith(RESPUESTA_GENERICA):
        return "incorrecta"  # intención bien, pero no identificó el producto
    return "correcta"


def main() -> None:
    nltk.download("punkt_tab", quiet=True)
    intents = cargar_intents()
    correctas = 0
    print("| # | Escenario | Intenciones probadas | Resultado | Captura |")
    print("|---|---|---|---|---|")
    transcripciones = []
    for i, (escenario, mensajes, esperadas) in enumerate(PRUEBAS, start=1):
        resultados, detectadas = [], []
        transcripcion = [f"--- Prueba {i}: {escenario} ---"]
        for mensaje, esperada in zip(mensajes, esperadas):
            detectada, respuesta = procesar(mensaje, intents)
            detectadas.append(detectada)
            resultados.append(evaluar(esperada, detectada, respuesta))
            transcripcion += [f"Operador: {mensaje}", f"VegetIA: {respuesta}   [intención: {detectada}]"]
        transcripciones.append("\n".join(transcripcion))
        if "incorrecta" not in resultados:
            correctas += 1
        probadas = ", ".join(esperadas)
        detalle = " + ".join(dict.fromkeys(resultados))
        if detectadas != esperadas:
            detalle += f" (detectó: {', '.join(detectadas)})"
        print(f"| {i} | {escenario} | {probadas} | {detalle} | Figura {i} |")
    print(f"\nPruebas correctas: {correctas} de {len(PRUEBAS)}\n")
    print("\n\n".join(transcripciones))


if __name__ == "__main__":
    main()
