"""VegetIA - Chatbot por reglas para inspección de calidad en empaque de hortalizas.

Avance de proyecto 1. Python >= 3.10 + NLTK.
"""
import json
import random
import re
import unicodedata
from pathlib import Path

import nltk
from nltk.tokenize import word_tokenize

RUTA_INTENTS = Path(__file__).with_name("intents.json")
# Orden de prioridad para desempatar cuando dos intenciones tienen el mismo puntaje
PRIORIDAD = ["saludo", "despedida", "producto_dañado", "reportar_falla",
             "uso_mesa_inspeccion", "criterios_calidad", "especificacion_empaque"]


def cargar_intents(ruta: Path = RUTA_INTENTS) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def preprocesar(texto: str) -> list[str]:
    """Minúsculas, sin acentos ni signos, y tokenización con NLTK."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")  # quita acentos
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)  # quita ¿?¡!,.
    return word_tokenize(texto, language="spanish")


def detectar_producto(tokens: list[str], intents: dict) -> str:
    for producto, variantes in intents["productos"].items():
        if any(t in variantes for t in tokens):
            return producto
    return "general"


def detectar_intencion(tokens: list[str], intents: dict) -> str:
    """Cuenta coincidencias de palabras clave; gana la de mayor puntaje o 'respaldo'."""
    puntajes = {}
    for nombre in PRIORIDAD:
        claves = intents[nombre]["palabras_clave"]
        puntajes[nombre] = sum(1 for t in tokens if t in claves)
    mejor = max(PRIORIDAD, key=lambda n: puntajes[n])  # en empate gana el primero
    return mejor if puntajes[mejor] > 0 else "respaldo"


def responder(intencion: str, tokens: list[str], intents: dict) -> str:
    respuestas = intents[intencion]["respuestas"]
    if isinstance(respuestas, dict):  # respuestas que dependen del producto
        return respuestas[detectar_producto(tokens, intents)]
    return random.choice(respuestas)


def procesar(mensaje: str, intents: dict) -> tuple[str, str]:
    """Devuelve (intención detectada, respuesta). Útil para pruebas."""
    tokens = preprocesar(mensaje)
    intencion = detectar_intencion(tokens, intents)
    return intencion, responder(intencion, tokens, intents)


def main() -> None:
    nltk.download("punkt_tab", quiet=True)
    intents = cargar_intents()
    print("VegetIA: Hola, soy VegetIA. Escribe tu duda (o 'adiós' para salir).")
    while True:
        mensaje = input("Operador: ")
        intencion, respuesta = procesar(mensaje, intents)
        print(f"VegetIA: {respuesta}   [intención: {intencion}]")
        if intencion == "despedida":
            break


if __name__ == "__main__":
    main()
