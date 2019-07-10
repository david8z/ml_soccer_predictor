from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import pandas as pd
import numpy as np

# https://www.marca.com/estadisticas/futbol/primera/2018_19/jornada_22/
# https://game.laligafantasymarca.com/matches
# https://www.marca.com/eventos/marcador/futbol/2018_19/primera/jornada_13/
# https://es.whoscored.com/Matches/1316841/LiveStream/Espa%C3%B1a-La-Liga-2018-2019-Real-Betis-Espanyol
########################
# VARIABLES
########################
LOCAL = [0]
VISITANT = [1]
LOOSE = [0]
DRAFT = [1]
WIN = [3]
########################
# FUNCTIONS
########################
def complete_webpage(url_num, url):
    """
    Returns the source of the page.
    ---
    Parameters:
        url_num: Integer, contains the number of the link of the website to be extracted.
    """


    page = urlopen(url + str(url_num))

    return BeautifulSoup(page, 'html.parser')

def store_points(matches, jornada):
    """
    Stores the points of the team on the file points.csv
    ---
    Parameters:

        jornada: Integer
    """
    # So it reference the global variable
    global results
    if jornada == 1:
        teams = sorted([x for x, y, z in matches] + [y for x, y, z in matches])
        results = pd.DataFrame( index=teams, columns=[x for x in range(1,total_match)])
        # results = results.astype('numpy.dtype')

    # Fila, Columna -> (LOCAL or VISITANT, Goles LOCAL, Goles VISITANTS, POINTS)
    for i in [(x,z) for x, y, z in matches]:
        aux = DRAFT if i[1][0] == i[1][1] else LOOSE if i[1][0] < i[1][1] else WIN
        aux = np.array(LOCAL+i[1]+aux)
        results.loc[i[0], jornada] = aux
    for i in [(y,z) for x, y, z in matches]:
        aux = DRAFT if i[1][0] == i[1][1] else WIN if i[1][0] < i[1][1] else LOOSE
        aux = np.array(VISITANT + i[1]+ aux)
        results.loc[i[0], jornada] = aux

def main(url):
    for y in range(1, total_match+1):
        soup = complete_webpage(y, url)

        local_teams = soup.find_all('td',attrs={'class':'left clubname leftClub'})
        visitant_teams = soup.find_all('td',attrs={'right clubname rightClub'})
        game_results = soup.find_all('td',attrs={'class':'matchdayResult'})

        # List of games (local_team, visitant_team, match result)
        store_points([(l.get_text(), v.get_text(), list(map(int,re.split(':',r.get_text())))) for l, v, r in zip(local_teams, visitant_teams, game_results)], y)

if __name__ == '__main__':
    url = 'https://stats.comunio.es/matchday/2018-19/'
    total_match = 36
    main(url)
    results.to_pickle("results_2019_ES.pickle")
