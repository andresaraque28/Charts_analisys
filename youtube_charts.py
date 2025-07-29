# importar librerias
from playwright.sync_api import sync_playwright
import pandas as pd

#iniciar playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) # lanzar el navegador chrome en modo no aculto
    page = browser.new_page()

    #definimos url a scrapar
    url = "https://charts.youtube.com/charts/TopSongs/co/weekly"
    page.goto(url)

    # Esperar a que cargue el contenido de la seccion que queremos scrapear
    page.wait_for_selector('ytmc-chart-table-v2 div')

    #extraer las canciones que estan todas en lista con ytmc...
    songs = page.query_selector_all('ytmc-entry-row')
    print(f"Total de canciones encontradas: {len(songs)}")

    #creamos una lista vaacia para almacenar el top
    top_colombia_weekly =[]

    #iteramos sobre songs y extraemos la informacion de cada cancion
    for i, song in enumerate(songs, start=1): # iteramos pero usamos i para la posicion de casda una empezando en 1

        title= song.query_selector('#entity-title') # extraer titulo
        artist= song.query_selector('#artist-names') #extraer artista
        # aqui vamos a extraer vistas pero vemos que al usar el selector, 
        # no nos devuelve el nimero de visatas devuelve antes las semanas en top y luego vistas
        metrics = song.query_selector_all('.metric.content.center.tablet-non-displayed-metric')

        titlef= title.inner_text() if title else "N/A" #  usamos inner_text para extraer el texto
        artistf= artist.inner_text() if artist else "N/A"
        viewsf= metrics[1].inner_text() if len(metrics) > 1 else "N/A" # usamos el segundo elemento de metrics
        top_song = i # enumera las canciones para la posicion
        top_colombia_weekly.append({ # creamos un diccionario con la informacion de cada cancion
            'position': top_song,
            'title': titlef,
            'artist': artistf,
            'views': viewsf
        })

    print('top_colombia_weekly:')

    for song in top_colombia_weekly: # imprimimos resultados
        print(f"Posición: {song['position']} - Título: {song['title']} - Artista: {song['artist']} - Vistas: {song['views']}")

    # Convertir la lista de diccionarios a un DataFrame de pandas
    df= pd.DataFrame(top_colombia_weekly)

    #convertimos a csv
    df.to_csv("top_colombia_weekly.csv", index=False)
    input("Presiona Enter para continuar...")

    browser.close()


