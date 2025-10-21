# Agente IA Recomendador de Películas y Series

## Descripción

Este proyecto implementa un **agente de Inteligencia Artificial** capaz de recomendar películas y series según el **género**, **estado de ánimo** y **año mínimo** indicado por el usuario.  
El agente se desarrolló como parte del curso de **Aseguramiento de la Calidad del Software** en la **Universidad Mariano Gálvez de Guatemala**.

Se implementaron tres versiones:

- **Terminal** (`main.py`)
- **Interfaz gráfica con Tkinter** (`main_gui.py`)
- **Aplicación web local con Flask** (`app.py`)

La lógica central de recomendaciones se encuentra en `logic/recomendador.py`, y los datos en `data/peliculas.json`.

## Requisitos

- Python 3.x
- Flask (para la versión web)
- Tkinter (incluido en Python estándar)

Instalar dependencias (solo para Flask):

```bash
pip install -r requirements.txt
```
