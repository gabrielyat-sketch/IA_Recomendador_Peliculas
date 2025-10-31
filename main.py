from logic.recomendador import recomendar

print("🎬 Bienvenido al Agente de IA Recomendador de Películas y Series 🎬\n")


tipo = input("¿Qué deseas ver? (pelicula/serie/nada): ").lower()
genero = input("¿Qué género te gustaría? (accion, comedia, drama, romance, ciencia ficcion, terror, animacion, fantasia, nada): ").lower()
estado_animo = input("¿Cuál es tu estado de ánimo? (feliz, motivado, pensativo, curioso, valiente, emocionado, nada): ").lower()
anio_input = input("¿Deseas filtrar por año mínimo? (Ejemplo: 2015, o 'no'): ").lower()

anio = int(anio_input) if anio_input != "no" else None


recomendaciones = recomendar(tipo=tipo, genero=genero, año=anio, estado_animo=estado_animo, cantidad=3)


print("\n✨ Aquí tienes tus recomendaciones:")
if recomendaciones:
    for r in recomendaciones:
        print(f"🎥 {r['titulo']} ({r['tipo'].capitalize()} - {r['genero'].capitalize()} - {r['año']} - Estado de ánimo: {r['estado_animo']})")
else:
    print("Lo sentimos, no encontramos recomendaciones con esos filtros.")

print("\nGracias por usar el Agente de IA Recomendador ❤️")
