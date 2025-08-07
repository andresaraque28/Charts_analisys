from playwright.sync_api import sync_playwright
import pandas as pd
import re
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Lanzar el navegador en modo  oculto
    page = browser.new_page()

    url = "https://charts.youtube.com/artist/%2Fg%2F11fm400jbf" # URL del artista
    page.goto(url) 
    page.wait_for_timeout(15000)
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

    

    # Convertir la columna de vistas a números
    df["Vistas"] = df["Vistas"].str.replace(".", "", regex=False).str.replace(",", "", regex=False).astype(int) 

    print(df)

    if os.path.exists("oyentes_diarios.csv"):
        # Si el archivo ya existe, cargarlo
        df_existente = pd.read_csv("oyentes_diarios.csv")
        # Concatenar los nuevos datos con los existentes
        df = pd.concat([df_existente, df], ignore_index=True)
        # Eliminar duplicados basados en la columna "Fecha"
        df = df.drop_duplicates(subset=["Fecha"], keep="last")
        # guardar los cambios en el archivo CSV
        df.to_csv("oyentes_diarios.csv", index=False)
        print("Datos actualizados y guardados en 'oyentes_diarios.csv'")
    # Guardar el DataFrame en un archivo CSV
    else:
        df.to_csv("oyentes_diarios.csv", index=False)
        print("Datos guardados en 'oyentes_diarios.csv'")

    browser.close()  # Cerrar el navegador