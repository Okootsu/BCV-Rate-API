# BCV Rate API

API REST construida con **Python** y **Flask** para obtener las tasas oficiales de cambio del **Banco Central de Venezuela (BCV)** mediante técnicas de web scraping.

## 🚀 Características

* **Scraping en tiempo real:** Extrae valores de Dólar, Euro, Yuan, Lira y Rublo.
* **Caché de alto rendimiento:** Usa `cachetools` con un TTL de 2 horas (7200 seg) para optimizar la velocidad y no saturar el servidor del BCV.
* **Manejo estricto de SSL:** Configurado para validar la conexión de forma segura.
* **CORS:** Habilitado para integración inmediata con aplicaciones web (React, Vue, Angular, etc.).

---

## 🔐 Solución al Certificado SSL

El portal del BCV suele presentar problemas con las entidades certificadoras estándar que utiliza Python. Para que la API funcione correctamente y de forma segura:

1.  Se debe incluir el archivo de certificado `_.bcv.org.ve.crt` en la raíz del proyecto.
2.  La API utiliza este archivo explícitamente en cada solicitud para verificar la identidad del sitio oficial sin desactivar la seguridad SSL.

---

## 🛠️ Instalación

1.  **Clona este repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/nombre-de-tu-repo.git](https://github.com/tu-usuario/nombre-de-tu-repo.git)
    cd nombre-de-tu-repo
    ```

2.  **Instala las dependencias necesarias:**
    ```bash
    pip install flask flask-cors requests beautifulsoup4 cachetools
    ```

3.  **Ejecución:**
    ```bash
    python app.py
    ```

La API estará disponible en: `http://localhost:5000/api/v1/tasas`

---

## 📊 Estructura de la Respuesta

```json
{
  "tasas": {
    "Dolar": 36.50,
    "Euro": 39.20,
    "Yuan": 5.05,
    "Lira": 1.12,
    "Rublo": 0.39
  },
  "fecha_valor": "12-05-2024",
  "fuente": "[https://www.bcv.org.ve](https://www.bcv.org.ve)",
  "info_adicional": "Tipo de Cambio de Referencia..."
}
