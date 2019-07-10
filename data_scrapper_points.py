from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import pandas as pd

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
    url = re.split("([0-9]+)",url)
    url[1], url[3] = url_num, url_num

    page = urlopen("".join([str(x) for x in url]))

    return BeautifulSoup(page, 'html.parser')

def store_points(team_points, jornada):
    """
    Stores the points of the team on the file points.csv
    ---
    Parameters:

        jornada: Integer
    """
    # SO it reference the global variable
    global results
    if jornada == 1:
        results = pd.DataFrame([int(y) for x,y in team_points], index=[x for x, y in team_points],columns=[1])
    else:
        results[jornada] = [int(y) for x,y in team_points]


def main(url):
    for y in range(1, match):
        soup = complete_webpage(y, url)
        table=soup.find('div',attrs={'class':'tableContainer'})
        table_data = re.split('[|]', table.get_text('|', strip=True))[7:]
        team_points = sorted(zip(table_data[1::7],table_data[3::7]))
        store_points(team_points, y)



if __name__ == '__main__':
    url = 'https://stats.comunio.es/club_pts_history.php?matchday_start=1&matchday_end=1&place=ha'
    match = 36
    results = pd.DataFrame()
    main(url)
    results.to_pickle("points_2019_ES.pickle")
