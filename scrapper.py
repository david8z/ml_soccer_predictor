from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re, requests
import pickle
import time



#how are you doin mate

# Código necesario para usar múltiples IP's en las requests.
#
# payload = {'api_key': '0fda2c72fd7ba1e7d7f013e51070ea27', 'url':'https://httpbin.org/ip'}
#
# r = requests.get('http://api.scraperapi.com', params=payload)

# Reset gecko log file
with open('geckodriver.log', 'w'):
    pass


url = 'https://es.whoscored.com/Matches/1316345/'

####################
## Preview
####################
def preview(url):
    """
    No necesitamos usar selenium
    """
    page = urlopen(url + "Preview")
    webpage = BeautifulSoup(page, 'html.parser')

    stats_11_probable = re.findall(r'\d*\,\d+|\d+',"".join([x.get_text() for x in webpage.find_all('div',attrs={'class':'stat-group'})]))

    rating_jug_ausentes_local = re.findall(r'\d*\,\d+|\d+',webpage.find('div',attrs={'id':'missing-players'}).find_next("div",attrs={'class':'home'}).get_text())

    rating_jug_ausentes_visitante = re.findall(r'\d*\,\d+|\d+',webpage.find('div',attrs={'id':'missing-players'}).find_next("div",attrs={'class':'away'}).get_text())

    return stats_11_probable, rating_jug_ausentes_local, rating_jug_ausentes_visitante


####################
## Show
####################
def show(url):
    # Obtenemos la página con selenium webdriver
    driver = webdriver.Firefox(executable_path=r'/home/david/Downloads/geckodriver')
    driver.get(url+ "Show")

    # Clickamos en Amplio
    driver.execute_script("document.querySelector('#standings-form > dl > dd:nth-child(5) > a').click()")
    webpage = BeautifulSoup(driver.page_source, 'html.parser')
    # Clasificaciones, Global, Local, Visitante
    clasificaciones = re.findall(r'\d*\,\d+|\d+',webpage.select('#standings-wide-grid > tbody')[0].get_text(" "))

    # Clickamos en Forma
    driver.execute_script("document.querySelector('#tables > li:nth-child(2) > a').click()")
    webpage = BeautifulSoup(driver.page_source, 'html.parser')
    # Forma respecto a últimos seis partidos
    forma_6_partidos = re.findall(r'\d*\,\d+|\d+|\-\d',webpage.select('#forms-grid > tbody')[0].get_text(" "))
    print(forma_6_partidos)

    # [Local_ganados, Empates, Local_ganados]
    enfrentamientos_previos = re.findall(r'\d*\,\d+|\d+',webpage.find('table',attrs={'class':'grid summary'}).find_next("thead").get_text())

    return enfrentamientos_previos, forma_6_partidos, clasificaciones

####################
## TeamStatistics
####################


####################
## MatchReport
####################



show(url)
