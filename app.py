from config.models import Crew, Movies, Cast
from config.database import engine

import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, and_

print("App is Iniciating...")

session = Session(engine)
app = FastAPI() #application instance

def try_or(rev, but, default):
    try:
        return rev/but
    except:
        return default

# some routing for displaying the home page
@app.get('/peliculas/{key_word}')
async def peliculas(key_word):

    res = select(Movies).where(or_(Movies.title.icontains(f"{key_word}"), Movies.overview.icontains(f"{key_word}")))
    res2 = session.query(Movies).filter(Movies.title.icontains(f'{key_word}')).first()

    lista = list()
    for movie in session.scalars(res):
        lista.append({'Pelicula': movie.title, 'Estreno': datetime.datetime.isoformat(movie.release_date), 'Resumen': movie.overview})

    return JSONResponse(lista)

@app.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes:str):
    
    res = session.query(Movies).filter(Movies.month.ilike(f'{mes}')).count()

    return {'mes':mes, 'cantidad':res}


@app.get('/cantidad_filmaciones_dia{dia}')
async def cantidad_filmaciones_dia(dia:str):
    res = session.query(Movies).filter(Movies.day.ilike(f'{dia}')).count()
    return {'dia':dia, 'cantidad':res}

@app.get('/score_titulo/{titulo}')
async def score_titulo(titulo: str ):
    res  = session.query(Movies).filter(Movies.title.ilike(f'{titulo}')).first()
    return {'titulo':titulo, 'anio': res.year, 'popularidad': res.popularity}

@app.get('/votos_titulo/{titulo}')
async def votos_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
    return {'titulo':titulo, 'anio':1, 'voto_total':1, 'voto_promedio':1}

@app.get('/get_actor/{nombre_actor}')
async def get_actor(nombre_actor:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    query = session.query(Movies, Cast).join(Cast).where(Cast.name.ilike(f'{nombre_actor}')).order_by(Movies.release_date)

    list_peliculas = []
    ingresos = 0
    contador_peliculas = 0
    for row in query:
        ingresos += row[0].revenue
        contador_peliculas += 1
        list_peliculas.append({'Titulo': row[0].title, 'Personaje': row[1].character, 'Anio_Estreno': row[0].year})
    
    retorno_promedio = try_or(ingresos, contador_peliculas, 0)

    if len(list_peliculas) == 0:
        list_posibilidades = []
        query2 = session.query(Crew).where(Crew.name.ilike(f'{nombre_actor[:2]}%{nombre_actor[-2:]}')).group_by(Crew.name)
        for row in query2:
            list_posibilidades.append(row.name)

    return {'Actor':nombre_actor.title(), 'Cantidad_Filmaciones':contador_peliculas, 'Retorno_Total':ingresos, 
            'Retorno_Promedio':retorno_promedio, 'Peliculas': list_peliculas} if len(list_peliculas) >= 1 else {'Error': 'No se encontraron registros, pruebe con alguna de las siguientes opciones', 
                                                              'Nombres': list_posibilidades}

@app.get('/get_director/{nombre_director}')
async def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    
    query = session.query(Movies, Crew).join(Crew).where(and_(Crew.name.ilike(f'{nombre_director}'), Crew.job == 'Director')).order_by(Movies.release_date)
    
    list_peliculas = []
    presupuesto = 0
    ingresos = 0
    for row in query:
        presupuesto += row[0].budget
        ingresos += row[0].revenue
        list_peliculas.append({'Titulo': row[0].title, 'Anio_Estreno': row[0].year, 
        'Budget': row[0].budget, 'Revenue': row[0].revenue, 'Retorno': try_or(row[0].revenue, row[0].budget, 0)})
    
    retorno = try_or(ingresos, presupuesto, 0)

    if len(list_peliculas) == 0:
        list_posibilidades = []
        query2 = session.query(Crew).where(Crew.name.ilike(f'{nombre_director[:2]}%{nombre_director[-2:]}')).group_by(Crew.name)
        for row in query2:
            list_posibilidades.append(row.name)

    return {'Director':nombre_director.title(),'Retorno_Total_Generado': retorno,
    'Peliculas': list_peliculas}  if len(list_peliculas)>=1 else {'Error': 'No se encontraron registros, pruebe con alguna de las siguientes opciones', 
                                                              'Nombres': list_posibilidades}

# ML
@app.get('/recomendacion/{titulo}')
async def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    return {'lista recomendada': 1}

if __name__ == '__main__':
    uvicorn.run(app, port=4000)