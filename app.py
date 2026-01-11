import requests

from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_cors import CORS
from cachetools import TTLCache

# Crear la aplicación
app = Flask(__name__)
CORS(app) 


# Cache: Guarda el resultado por 1 hora (3600 segundos)
cache = TTLCache(maxsize=1, ttl=7200)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def limpiar_valor(texto):
    try:
        # Quitar espacios y símbolos
        limpio = texto.strip().replace("Bs.", "").replace(" ", "")
        # Cambiar coma por punto
        limpio = limpio.replace(",", ".")
        return float(limpio)
    except (ValueError, AttributeError):
        return None

def scrape_bcv():
    # Si los datos están en caché, los devolvemos de una vez
    if "tasas" in cache:
        return cache["tasas"]
    url = "https://www.bcv.org.ve" # Sitio web objetivo

    try:
    
        response = requests.get(url, HEADERS, verify="_.bcv.org.ve.crt", timeout=10) # Realizar la solicitud GET
        response.raise_for_status() # Verificar que la solicitud fue exitosa
        
        html = response.text # Obtener el contenido HTML de la respuesta
        soup = BeautifulSoup(html, "html.parser") # Parsear el HTML con BeautifulSoup

        # Diccionario para mapear los IDs del BCV
        ids = ["euro", "yuan", "lira", "rublo", "dolar"]
        tasas = {}

        for i in ids:
            container = soup.find("div", id=i)
            if container:
                valor = container.find("strong").get_text()
                tasas[i.capitalize()] = limpiar_valor(valor)

        # Información adicional
        logo = url + soup.find("img", alt="logo_bcv-04.png")["src"]
        info = soup.find("div", class_="textp").get_text().strip()
        fecha = soup.find("div", class_="pull-right dinpro center").find("span").get_text()


        monedas = {
            "tasas": tasas,
            "fecha_valor": fecha if fecha else "No disponible",
            "fuente": url,
            "info_adicional": info if info else "No disponible",
            "logo": logo if logo else "No disponible",
        }

        # Guardar en caché
        cache["tasas"] = monedas
        return monedas
    

    except Exception as e:
        return {"error": f"No se pudo obtener la informacion: {str(e)}"}


# Definir una ruta
@app.route("/api/v1/tasas")
def get_tasas():
    datos = scrape_bcv()
    status = 200 if "error" not in datos else 500
    return jsonify(datos), status


# Ejecutar la app
if __name__ == "__main__":
    app.run(debug=True, port=5000)