import json
import random
import os

def cargar_peliculas():
    base = os.path.join(os.path.dirname(__file__), "..", "data", "peliculas.json")
    with open(base, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def recomendar(tipo=None, genero=None, año=None, estado_animo=None, cantidad=3):
    peliculas = cargar_peliculas()
    recomendaciones = []

    for p in peliculas:
        # Normaliza keys si vienen con mayúsculas o distintos nombres
        p_tipo = p.get("tipo", "").lower()
        p_genero = p.get("genero", "").lower()
        p_año = p.get("año") or p.get("anio") or 0
        p_estado = p.get("estado_animo", "").lower()

        # Comprobar combinaciones (se sigue tu estilo original)
        if tipo and genero and año and estado_animo:
            if (p_tipo == tipo.lower() and
                p_genero == genero.lower() and
                p_año >= año and
                p_estado == estado_animo.lower()):
                recomendaciones.append(p)
        elif tipo and genero and estado_animo:
            if (p_tipo == tipo.lower() and
                p_genero == genero.lower() and
                p_estado == estado_animo.lower()):
                recomendaciones.append(p)
        elif tipo and genero and año:
            if (p_tipo == tipo.lower() and
                p_genero == genero.lower() and
                p_año >= año):
                recomendaciones.append(p)
        elif tipo and estado_animo:
            if p_tipo == tipo.lower() and p_estado == estado_animo.lower():
                recomendaciones.append(p)
        elif genero and estado_animo:
            if p_genero == genero.lower() and p_estado == estado_animo.lower():
                recomendaciones.append(p)
        elif tipo and genero:
            if p_tipo == tipo.lower() and p_genero == genero.lower():
                recomendaciones.append(p)
        elif tipo and año:
            if p_tipo == tipo.lower() and p_año >= año:
                recomendaciones.append(p)
        elif genero and año:
            if p_genero == genero.lower() and p_año >= año:
                recomendaciones.append(p)
        elif estado_animo and tipo:
            if p_estado == estado_animo.lower() and p_tipo == tipo.lower():
                recomendaciones.append(p)
        elif estado_animo and genero:
            if p_estado == estado_animo.lower() and p_genero == genero.lower():
                recomendaciones.append(p)
        elif tipo:
            if p_tipo == tipo.lower():
                recomendaciones.append(p)
        elif genero:
            if p_genero == genero.lower():
                recomendaciones.append(p)
        elif estado_animo:
            if p_estado == estado_animo.lower():
                recomendaciones.append(p)
        else:
            recomendaciones.append(p)

    if not recomendaciones:
        recomendaciones = peliculas  # fallback

    # Elegir al azar la cantidad solicitada (o las que existan)
    return random.sample(recomendaciones, min(cantidad, len(recomendaciones)))
