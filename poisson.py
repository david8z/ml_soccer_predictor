# Fuerza atacante
# Media egoles marcado equipo / Media goles marcados liga

# Fuerza defensiva
# Media goles encajados equipo / Media goles encajados liga

# Num probables goles A en partido Avs B
# Fuerza Atacante Local A * Fuerza Defensiva Vistante B * Media Goles En Casa Liga
# Num probables goles A
# Fuerza Atacante Visitante B * Fuerza Defensiva Local A * Media Goles Fuera Liga
from scipy.stats import poisson
import pandas as pd
import numpy as np
# poisson.pmf(actual value, mean)
file_variable = "ES"
nombre_equipos= {'Alavés':0, 'Athletic':1,
                'Atlético':2, 'Barcelona':3,
                'Betis':4, 'Celta':5,
                'Eibar':6, 'Espanyol':7,
                'Getafe':8, 'Girona':9,
                'Huesca':10, 'Leganés':11,
                'Levante':12, 'Rayo Vallecano':13,
                'Real Madrid':14, 'Real Sociedad':15,
                'Sevilla':16, 'Valencia':17,
                'Valladolid':18, 'Villarreal':19}

points = pd.read_pickle("points_2019_"+file_variable+".pickle")
results = pd.read_pickle("results_2019_"+file_variable+".pickle")

equipos = len(points.index)
jornadas = len(points.columns)



goles_local =np.zeros((equipos,jornadas+1))
goles_visitante = np.zeros((equipos,jornadas+1))



encajados_local = np.zeros((equipos,jornadas+1))
encajados_visitante = np.zeros((equipos,jornadas+1))

for j in results:
    for pos_i, i in enumerate(results.index):
        if results[j][i][0] == 0:
            # print(results[j][i])
            # Actualizamos número de jornadas
            goles_local[pos_i,0] += 1
            encajados_local[pos_i,0] += 1

            goles_local[pos_i,j] += results[j][i][1]
            encajados_local[pos_i,j] += results[j][i][2]
        else:
            # Actualizamos número de jornadas
            goles_visitante[pos_i,0] += 1
            encajados_visitante[pos_i,0] += 1

            goles_visitante[pos_i,j] += results[j][i][2]
            encajados_visitante[pos_i,j] += results[j][i][1]


def poisson_func(local, visitante, jornada):
    points_loc = points[jornada][local]**2
    points_vis = points[jornada][visitante]**2
    points_tot = points_loc+points_vis

    local = nombre_equipos[local.strip()]
    visitante = nombre_equipos[visitante.strip()]

    # BUG: Funciionan todos mal porque el acumulativo en pos 0 no indica realmente las jornadas que llevan

    media_goles_loc = np.sum(np.sum(goles_local[:,1:jornada+1], axis=1) / goles_local[:,0]) / len(nombre_equipos.keys())
    media_goles_vis = np.sum(np.sum(goles_visitante[:,1:jornada+1], axis=1) / goles_visitante[:,0])/ len(nombre_equipos.keys())

    media_encajados_loc = np.sum(np.sum(encajados_local[:,1:jornada+1], axis=1) / encajados_local[:,0])/ len(nombre_equipos.keys())
    media_encajados_vis = np.sum(np.sum(encajados_visitante[:,1:jornada+1], axis=1) / encajados_visitante[:,0])/ len(nombre_equipos.keys())

    ataLoc = np.sum(goles_local[local,1:jornada+1]) / goles_local[local,0] / media_goles_loc
    defLoc = np.sum(encajados_local[local,1:jornada+1]) / encajados_local[local,0] / media_encajados_loc

    ataVis = np.sum(goles_visitante[visitante,1:jornada+1]) / goles_visitante[visitante,0] / media_goles_vis
    defVis = np.sum(encajados_visitante[visitante,1:jornada+1]) / encajados_visitante[visitante,0] / media_encajados_vis

    goles_loc = ataLoc * defVis * media_goles_loc
    goles_vis = ataVis * defLoc * media_encajados_vis

    print(points_loc, points_vis)
    print(goles_loc,goles_vis)

    poisson_loc = poisson.pmf(np.arange(0,8), goles_loc*np.ones(8))# * points_loc/points_tot
    poisson_vis = poisson.pmf(np.arange(0,8), goles_vis*np.ones(8)) #* points_vis/points_loc
    return poisson_loc, poisson_vis

if __name__ == '__main__':
    print(poisson_func("Rayo Vallecano","Real Madrid",35))
