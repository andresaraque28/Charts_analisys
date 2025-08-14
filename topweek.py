# importar librerias
from playwright.sync_api import sync_playwright
import pandas as pd

#iniciar playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # lanzar el navegador chrome en modo oculto
    page = browser.new_page()

    #definimos url a scrapar
    url = "https://charts.youtube.com/charts/TopArtists/co/weekly"
    page.goto(url)

    # Esperar a que cargue el contenido de la seccion que queremos scrapear
    page.wait_for_selector('ytmc-chart-table-v2 div')

    #extraer los artistas que estan todos en lista con ytmc...
    artists = page.query_selector_all('ytmc-entry-row')
    print(f"Total de artistas encontrados: {len(artists)}")

    #creamos una lista vaacia para almacenar el top
    top_colombia_weekly =[]

    for artist in artists:
        name = artist.query_selector('span.artistName')
        top = artist.query_selector_all('div.metric.content.center')
        link = name.get_attribute('endpoint')

        # extraer nombre, posicion, semanas en el top y vistas
        namef = name.inner_text() if name else "N/A"  # usamos inner_text para extraer el texto
        top_position = top[1].inner_text() if len(top) > 1 else "N/A"
        weeks_in_top = top[2].inner_text() if len(top) > 2 else "N/A"
        weekly_views = top[3].inner_text() if len(top) > 3 else "N/A"

        print(link)
        # agregamos la informacion a la lista
        top_colombia_weekly.append({
            "top_position": top_position,
            "name": namef,
            "weeks_in_top": weeks_in_top,
            "weekly_views": weekly_views
        })

    
    #print(top_colombia_weekly)
    #convertir a dataframe
    df_top_artists = pd.DataFrame(top_colombia_weekly)
    print(df_top_artists.head())
    df_top_artists.to_csv("top_colombia_weekly_artists.csv", index=False)

    browser.close()  # Cerrar el navegador