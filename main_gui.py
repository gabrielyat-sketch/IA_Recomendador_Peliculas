import tkinter as tk
from tkinter import ttk
from logic.recomendador import recomendar


colores_genero = {
    "accion": "#FF6347",
    "comedia": "#FFD700",
    "drama": "#8A2BE2",
    "romance": "#FF69B4",
    "ciencia ficcion": "#00CED1",
    "terror": "#2F4F4F",
    "animacion": "#FFA500",
    "fantasia": "#ADFF2F"
}

emojis_estado = {
    "feliz": "😊",
    "motivado": "💪",
    "pensativo": "🤔",
    "curioso": "🧐",
    "valiente": "🦁",
    "emocionado": "🤩"
}


def obtener_recomendaciones():
    tipo = tipo_var.get().lower()
    genero = genero_var.get().lower()
    estado_animo = estado_var.get().lower()
    anio_input = anio_entry.get()
    anio = int(anio_input) if anio_input else None

    resultados = recomendar(tipo=tipo, genero=genero, año=anio, estado_animo=estado_animo, cantidad=200)

    
    resultados.sort(key=lambda x: x.get("popularidad", 0), reverse=True)

    resultados_texto.config(state="normal")
    resultados_texto.delete(1.0, tk.END)

    if resultados:
        for r in resultados:
            color = colores_genero.get(r['genero'].lower(), "black")
            emoji = emojis_estado.get(r['estado_animo'].lower(), "")
            texto = f"{emoji} {r['titulo']} ({r['tipo'].capitalize()} - {r['genero'].capitalize()} - {r['año']} - Estado de ánimo: {r['estado_animo']} - Popularidad: {r.get('popularidad',0)})\n"
            resultados_texto.insert(tk.END, texto)
            resultados_texto.tag_add(r['titulo'], "end-1l linestart", "end-1l lineend")
            resultados_texto.tag_config(r['titulo'], foreground=color)
    else:
        resultados_texto.insert(tk.END, "No se encontraron recomendaciones con esos filtros.")

    resultados_texto.config(state="disabled")


def reiniciar_filtros():
    tipo_var.set("")
    genero_var.set("")
    estado_var.set("")
    anio_entry.delete(0, tk.END)
    resultados_texto.config(state="normal")
    resultados_texto.delete(1.0, tk.END)
    resultados_texto.config(state="disabled")


ventana = tk.Tk()
ventana.title("Agente de IA Recomendador de Películas y Series")
ventana.geometry("700x500")
ventana.resizable(False, False)


tipo_var = tk.StringVar()
genero_var = tk.StringVar()
estado_var = tk.StringVar()


tk.Label(ventana, text="Tipo:").pack(pady=5)
tipo_combo = ttk.Combobox(ventana, textvariable=tipo_var, state="readonly")
tipo_combo['values'] = ("Pelicula", "Serie")
tipo_combo.pack()

tk.Label(ventana, text="Género:").pack(pady=5)
genero_combo = ttk.Combobox(ventana, textvariable=genero_var, state="readonly")
genero_combo['values'] = ("Accion", "Comedia", "Drama", "Romance", "Ciencia Ficcion", "Terror", "Animacion", "Fantasia")
genero_combo.pack()

tk.Label(ventana, text="Estado de ánimo:").pack(pady=5)
estado_combo = ttk.Combobox(ventana, textvariable=estado_var, state="readonly")
estado_combo['values'] = ("Feliz", "Motivado", "Pensativo", "Curioso", "Valiente", "Emocionado")
estado_combo.pack()

tk.Label(ventana, text="Año mínimo (opcional):").pack(pady=5)
anio_entry = tk.Entry(ventana)
anio_entry.pack()


tk.Button(ventana, text="Obtener Recomendaciones", command=obtener_recomendaciones).pack(pady=5)
tk.Button(ventana, text="Reiniciar Filtros", command=reiniciar_filtros).pack(pady=5)


frame_texto = tk.Frame(ventana)
frame_texto.pack(pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side="right", fill="y")

resultados_texto = tk.Text(frame_texto, height=20, width=90, yscrollcommand=scrollbar.set, state="disabled")
resultados_texto.pack(side="left", fill="both", expand=True)

scrollbar.config(command=resultados_texto.yview)


ventana.mainloop()
