import csv
import bs4
import os
import time
from selenium import webdriver

########################
# FUNCTIONS
########################
def complete_webpage(url_num):
    """
    Returns the source of the page with all the links opened.
    ---
    Parameters:
        url_num: Integer, contains the number of the link of the website to be extracted.
    """
    web = webdriver.Firefox()
    web.get(global_url + str(url_num))
    try:
        elements = web.find_elements_by_class_name('zoomable')
        for e in elements:
            e.click()
            time.sleep(0.5)
    except(Exception):  # In case of error we try it again
        web.close()
        main(url_num)
    return web

def store_points(total_points, team_name, jornada):
    """
    Stores the points of the team on the file points.csv
    ---
    Parameters:
        total_points: List of BeautifulSoup elements
        team_name: List of BeautifulSoup elements
        jornada: Integer
    """
    with open('points.csv', 'a') as csv_file:
        fieldNames = ('JORNADA', 'TEAM', 'POINTS')
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldNames, dialect='excel')
        if os.stat("points.csv").st_size == 0:
            csv_writer.writeheader()
        for tp, tn in zip(total_points, team_name):
            csv_writer.writerow({'JORNADA': jornada, 'TEAM': tn.getText(),
                                'POINTS': tp.next_element.getText()})

def main(ini):
    for y in range(ini, match):
        try:  # In case the webdriver is closed
            content = complete_webpage(y)
            page = bs4.BeautifulSoup(content.page_source, 'html.parser')
            content.close()
            total_points = page.findAll(text='Puntos totales')
            team_name = page.select('.clubname')
            store_points(total_points, team_name[1::2], y)  # The team names are repeated
        except(Exception):
            print(Exception)


########################
# VARIABLES
########################
global_url = 'https://stats.comunio.es/matchday/2018/'
match = 39


if __name__ == '__main__':
    main(1)
