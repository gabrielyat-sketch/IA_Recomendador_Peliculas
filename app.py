from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Cargar base de datos
def cargar_peliculas():
    with open("data/peliculas.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# Variables de conversación (para el chat IA)
conversaciones = {}

@app.route("/")
def index():
    return render_template("index.html")

# 🧠 CHAT LIBRE PROFESIONAL (Cinéa)
@app.route("/mensaje", methods=["POST"])
def mensaje():
    datos = request.get_json()
    mensaje_usuario = datos.get("mensaje", "").lower()
    user_id = "usuario"

    peliculas = cargar_peliculas()

    if user_id not in conversaciones:
        conversaciones[user_id] = {
            "fase": "inicio",
            "tipo": "",
            "genero": "",
            "estado_animo": "",
            "año": ""
        }

    contexto = conversaciones[user_id]
    respuesta = ""
    peliculas_encontradas = []
    sugeridas = []

    # --- Fase 1: saludo profesional ---
    if contexto["fase"] == "inicio":
        if any(x in mensaje_usuario for x in ["hola", "buenas", "hey", "saludos"]):
            respuesta = (
                "👋 Hola, soy **Cinéa**, tu asistente IA profesional en recomendaciones audiovisuales. "
                "¿Deseas que te recomiende una **película** o una **serie**?"
            )
            contexto["fase"] = "esperando_tipo"
        else:
            respuesta = (
                "Soy **Cinéa**, tu agente de inteligencia artificial especializado en entretenimiento. "
                "Puedo sugerirte películas o series según tu estado de ánimo y preferencias. "
                "¿Quieres que te recomiende algo?"
            )
            contexto["fase"] = "esperando_tipo"

    elif contexto["fase"] == "esperando_tipo":
        if "pelicula" in mensaje_usuario or "película" in mensaje_usuario:
            contexto["tipo"] = "pelicula"
            contexto["fase"] = "esperando_estado"
            respuesta = (
                "🎬 Excelente elección. Te recomendaré películas. "
                "¿Cómo te sientes hoy? (feliz, triste, motivado, pensativo, aburrido...)"
            )
        elif "serie" in mensaje_usuario:
            contexto["tipo"] = "serie"
            contexto["fase"] = "esperando_estado"
            respuesta = (
                "📺 Muy bien. Te recomendaré series. "
                "¿Cuál es tu estado de ánimo actualmente? (feliz, triste, motivado, pensativo, aburrido...)"
            )
        else:
            respuesta = "¿Podrías confirmarme si deseas una **película** o una **serie**?"

    elif contexto["fase"] == "esperando_estado":
        emociones = ["feliz", "triste", "motivado", "pensativo", "aburrido", "curioso", "valiente"]
        for emo in emociones:
            if emo in mensaje_usuario:
                contexto["estado_animo"] = emo
                break
        if contexto["estado_animo"]:
            contexto["fase"] = "esperando_genero"
            respuesta = (
                f"Perfecto 😊. Cuando te sientes **{contexto['estado_animo']}**, "
                "¿qué género prefieres? (acción, comedia, romance, terror, drama, ciencia ficción)"
            )
        else:
            respuesta = (
                "No entendí muy bien tu estado de ánimo 🤔. "
                "¿Podrías decirme si estás feliz, triste, motivado, pensativo o aburrido?"
            )

    elif contexto["fase"] == "esperando_genero":
        generos = ["accion", "comedia", "romance", "terror", "drama", "ciencia ficcion"]
        for g in generos:
            if g in mensaje_usuario:
                contexto["genero"] = g
                break
        if contexto["genero"]:
            contexto["fase"] = "esperando_año"
            respuesta = (
                "Perfecto 👍. ¿Deseas que te recomiende algo **reciente** o de algún **año específico**?"
            )
        else:
            respuesta = "¿Qué género te gustaría ver? (acción, comedia, romance, terror, drama, ciencia ficción)"

    elif contexto["fase"] == "esperando_año":
        if "reciente" in mensaje_usuario or "nuevo" in mensaje_usuario:
            contexto["año"] = "reciente"
        elif any(str(año) in mensaje_usuario for año in range(1990, 2026)):
            for año in range(1990, 2026):
                if str(año) in mensaje_usuario:
                    contexto["año"] = str(año)
                    break

        peliculas_encontradas = [
            p for p in peliculas
            if (p["tipo"] == contexto["tipo"])
            and (not contexto["genero"] or p["genero"] == contexto["genero"])
            and (not contexto["estado_animo"] or p["estado_animo"] == contexto["estado_animo"])
        ]

        if not peliculas_encontradas:
            respuesta = (
                "No encontré coincidencias exactas 😔, pero te dejo algunas sugerencias populares:"
            )
            sugeridas = random.sample(peliculas, min(3, len(peliculas)))
        else:
            sugeridas = random.sample(peliculas_encontradas, min(3, len(peliculas_encontradas)))
            respuesta = "✨ Aquí tienes mis recomendaciones personalizadas según tu preferencia:"

        contexto["fase"] = "inicio"

        return jsonify({
            "respuesta": respuesta,
            "peliculas": sugeridas
        })

    else:
        respuesta = "¿Podrías repetirlo, por favor? 🤔"

    return jsonify({
        "respuesta": respuesta,
        "peliculas": peliculas_encontradas
    })


# 🎬 SISTEMA DE RECOMENDACIONES (cuadro derecho)
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
        return jsonify({
            "respuesta": "😔 No encontré coincidencias exactas, pero te dejo algo popular:",
            "peliculas": random.sample(peliculas, min(3, len(peliculas)))
        })

    sugeridas = random.sample(recomendaciones, min(3, len(recomendaciones)))
    return jsonify({
        "respuesta": "✨ Aquí tienes tus recomendaciones:",
        "peliculas": sugeridas
    })


if __name__ == "__main__":
    app.run(debug=True)
