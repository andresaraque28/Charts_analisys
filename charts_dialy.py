from playwright.sync_api import sync_playwright
import pandas as pd
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Lanzar el navegador en modo no aculto
    page = browser.new_page()

    url = "https://charts.youtube.com/artist/%2Fg%2F11fm400jbf" # URL del artista
    page.goto(url) 
    page.wait_for_timeout(5000)
    page.wait_for_selector('ytmc-views-card-v2')  # Esperar a que cargue el contenido

    # Extraer el número de oyentes diarios
    oyentes = page.query_selector('ytmc-views-card-v2')
    texto = oyentes.inner_text()
    # Filtrar solo las líneas que tienen el patrón "fecha    vistas"
    patron = r"(\d{1,2} \w+\.? \d{4})\s+([\d,.]+)"
    datos = re.findall(patron, texto)
    datos = datos[1:]  # Elimina el primer elemento que es el encabezado
    print(datos)

    # Convertir a DataFrame
    df = pd.DataFrame(datos, columns=["Fecha", "Vistas"])

    print(df)

    input("Presiona Enter para cerrar...")
    browser.close()  # Cerrar el navegador