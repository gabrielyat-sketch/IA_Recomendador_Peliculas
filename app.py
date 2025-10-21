from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Cargar base de datos
def cargar_peliculas():
    with open("data/peliculas.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recomendar", methods=["POST"])
def recomendar():
    datos = request.get_json()
    tipo = datos.get("tipo", "").lower()
    genero = datos.get("genero", "").lower()
    estado_animo = datos.get("estado_animo", "").lower()

    peliculas = cargar_peliculas()
    recomendaciones = [
        p for p in peliculas
        if (not tipo or p["tipo"] == tipo)
        and (not genero or p["genero"] == genero)
        and (not estado_animo or p["estado_animo"] == estado_animo)
    ]

    if not recomendaciones:
        return jsonify({"respuesta": "😔 No encontré coincidencias exactas, pero te dejo algo popular:",
                        "peliculas": random.sample(peliculas, 3)})

    sugeridas = random.sample(recomendaciones, min(3, len(recomendaciones)))
    return jsonify({"respuesta": "✨ Aquí tienes tus recomendaciones:", "peliculas": sugeridas})

if __name__ == "__main__":
    app.run(debug=True)
