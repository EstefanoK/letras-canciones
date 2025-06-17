from flask import Flask, render_template, request
import requests

app = Flask(__name__)

import os
GENIUS_TOKEN = os.environ.get("GENIUS_TOKEN")

@app.route("/", methods=["GET", "POST"])
def home():
    resultados = []
    if request.method == "POST":
        cancion = request.form["cancion"]
        artista = request.form.get("artista", "")
        busqueda = f"{cancion} {artista}"

        headers = {
            "Authorization": f"Bearer {GENIUS_TOKEN}"
        }
        url = f"https://api.genius.com/search?q={busqueda}"
        respuesta = requests.get(url, headers=headers)

        if respuesta.status_code == 200:
            data = respuesta.json()
            hits = data["response"]["hits"]
            if hits:
                for hit in hits[:5]:  # Mostrar hasta 5 resultados
                    titulo = hit["result"]["full_title"]
                    url_letra = hit["result"]["url"]
                    resultados.append({"titulo": titulo, "url": url_letra})
            else:
                resultados.append({"titulo": "No se encontraron resultados para esa canción.", "url": ""})
        else:
            resultados.append({"titulo": "Error al consultar la API de Genius.", "url": ""})

    return render_template("index.html", resultados=resultados)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
