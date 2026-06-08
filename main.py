import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origenes = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8081",
    "http://127.0.0.1:8081",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = "https://www.bcv.org.ve" # Sitio web objetivo

# Cache: Guarda el resultado por 2 hora (7200 segundos)
cache = TTLCache(maxsize=1, ttl=7200)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrap_bcv():
    # Si los datos están en caché, los devolvemos de una vez
    if "tasas" in cache:
        return cache["tasas"]
    
    try:
        response = requests.get(url, headers=HEADERS, verify="_.bcv.org.ve.crt", timeout=10) # Realizar la solicitud GET
        response.raise_for_status() # Verificar que la solicitud fue exitosa

        html = response.text # Obtener el contenido HTML de la respuesta
        soup = BeautifulSoup(html, "html.parser") # Parsear el HTML con BeautifulSoup
        ids = ["euro", "yuan", "lira", "rublo", "dolar"] # IDs de las monedas a extraer
        tasas = {} # Diccionario para almacenar el vaor de las monedas

        # Recorrer los IDs y extraer el valor de cada moneda
        for i in ids:
                container = soup.find("div", id=i)
                if container:
                    valor = container.find("strong").get_text()
                    tasas[i.capitalize()] = valor #limpiar_valor(valor)

        # Información adicional
        logo = url + soup.find("img", alt="logo_bcv-04.png")["src"]
        info = soup.find("div", class_="textp").get_text().strip()
        fecha = soup.find("div", class_="pull-right dinpro center").find("span").get_text()

        # Crear el diccionario final con toda la información
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

@app.get("/")
async def root():
    return {"mensaje": "API No oficial para obtener las monedas del BCV"}

@app.get("/tasas")
def get_tasas():
    prueba_api = scrap_bcv()
    status = 200 if "error" not in prueba_api else 500
    if status == 500:
        return {"error": "No se pudo obtener la información del BCV"}, status
    return  prueba_api
