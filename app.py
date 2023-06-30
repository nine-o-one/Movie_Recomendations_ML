from config.models import Crew, Movies, Cast, Machine_Learning
from config.database import engine

import joblib
import datetime
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import uvicorn

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

print("App is Iniciating...")

session = Session(engine)
app = FastAPI() #application instance

def try_or(rev, but, default):
    try:
        return rev/but
    except:
        return default

cercania = joblib.load("model.joblib")

# some routing for displaying the home page
@app.get('/peliculas/{key_word}')
async def peliculas(key_word):

    res = session.query(Movies).where(or_(Movies.title.icontains(f"{key_word}"), Movies.overview.icontains(f"{key_word}")))
    
    lista = list()
    for movie in session.scalars(res):
        lista.append({'Pelicula': movie.title, 'Estreno': datetime.datetime.isoformat(movie.release_date), 'Resumen': movie.overview})

    return JSONResponse(status_code = status.HTTP_200_OK, content = lista)

@app.get('/cantidad_filmaciones_mes/{mes}')
async def cantidad_filmaciones_mes(mes:str):
    
    res = session.query(Movies).where(Movies.month.ilike(f'{mes}')).count()

    return JSONResponse(status_code = status.HTTP_200_OK, content={'mes': mes, 'cantidad':res})

@app.get('/cantidad_filmaciones_dia/{dia}')
async def cantidad_filmaciones_dia(dia:str):
    res = session.query(Movies).where(Movies.day.ilike(f'{dia}')).count()
    return JSONResponse(status_code = status.HTTP_200_OK, content={'dia':dia, 'cantidad':res})

@app.get('/score_titulo/{titulo}')
async def score_titulo(titulo: str ):
    res  = session.query(Movies).where(Movies.title.ilike(f'{titulo}')).first()
    return JSONResponse(status_code = status.HTTP_200_OK, content={'titulo':titulo, 'anio': res.year, 'popularidad': res.popularity})

@app.get('/votos_titulo/{titulo}')
async def votos_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
    res  = session.query(Movies).where(Movies.title.ilike(f'{titulo}')).first()

    respuesta_OK = {'Titulo':titulo.title(), 'Anio':res.year, 'Voto_Total':res.vote_count, 'Voto_Promedio':res.vote_average}
    respuesta_ALERT = {'Alerta': 'La pelicula consultada no cuenta con suficientes votos.', 'Info:': {'Titulo':titulo.title(), 'Numero_Votos':res.vote_count} }
    return JSONResponse(status_code = status.HTTP_200_OK, content = respuesta_OK) if res.vote_count >= 2000 else JSONResponse(status_code= status.HTTP_404_NOT_FOUND, content= respuesta_ALERT)

@app.get('/get_actor/{nombre_actor}')
async def get_actor(nombre_actor:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    actor = session.query(Cast).where(Cast.name.ilike(f'%{nombre_actor}%')).group_by(Cast.name).first()

    list_posibilidades = []
    if actor == None:
        query2 = session.query(Cast).where(Cast.name.ilike(f'%{nombre_actor[:2]}%{nombre_actor[-2:]}%')).group_by(Cast.name).limit(100)
        for row in query2:
            list_posibilidades.append(row.name)
        respuesta_ALERT = {'Error': 'No se encontraron registros, pruebe con alguna de las siguientes opciones', 'Nombres': list_posibilidades}
        
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content = respuesta_ALERT)

    else:
        list_peliculas = []
        ingresos = 0
        contador_peliculas = 0

        query = session.query(Movies, Cast).join(Cast).where(Cast.name == actor.name).order_by(Movies.release_date)
        for row in query:
            ingresos += row[0].revenue
            contador_peliculas += 1
            list_peliculas.append({'Titulo': row[0].title, 'Personaje': row[1].character, 'Anio_Estreno': row[0].year})
        retorno_promedio = try_or(ingresos, contador_peliculas, 0)        
        respuesta_OK = {'Actor':actor.name, 'Cantidad_Filmaciones':contador_peliculas, 'Retorno_Total':ingresos, 'Retorno_Promedio':retorno_promedio, 'Peliculas': list_peliculas}


        return JSONResponse(status_code = status.HTTP_200_OK, content = respuesta_OK)

@app.get('/get_director/{nombre_director}')
async def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    
    director = session.query(Crew).where(and_(Crew.name.ilike(f'%{nombre_director}%'), Crew.job == 'Director')).group_by(Crew.name).first()

    list_posibilidades = []

    if director == None:
        query2 = session.query(Crew).where(and_(Crew.name.ilike(f'%{nombre_director[:2]}%{nombre_director[-2:]}%'), Crew.job == 'Director')).group_by(Crew.name).limit(100)
        for row in query2:
            list_posibilidades.append(row.name)
        respuesta_ALERT = {'Error': 'No se encontraron registros, pruebe con alguna de las siguientes opciones', 'Nombres': list_posibilidades}
        
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content = respuesta_ALERT)

    else: 
        list_peliculas = []

        query = session.query(Movies, Crew).join(Crew).where(and_(Crew.name == director.name, Crew.job == 'Director')).order_by(Movies.release_date)
        presupuesto = 0
        ingresos = 0
        for row in query:
            presupuesto += row[0].budget
            ingresos += row[0].revenue
            list_peliculas.append({'Titulo': row[0].title, 'Anio_Estreno': row[0].year, 
            'Budget': row[0].budget, 'Revenue': row[0].revenue, 'Retorno': try_or(row[0].revenue, row[0].budget, 0)})
        retorno = try_or(ingresos, presupuesto, 0)
        respuesta_OK = {'Director': director.name,'Retorno_Total_Generado': retorno,'Peliculas': list_peliculas}  

        return JSONResponse(status_code = status.HTTP_200_OK, content = respuesta_OK)

# ML
@app.get('/recomendacion/{titulo}')
async def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''

    indice_consulta = session.query(Movies, Machine_Learning).join(Machine_Learning).where(Movies.title.ilike(f'%{titulo}%')).first()

    if indice_consulta == None:

        return {'Error': 'No se encontró la película consultada.'}
    
    else:
        recomendaciones = sorted(list(enumerate(cercania[indice_consulta[1].id_ml])), reverse = True, key = lambda x:x[1])[1:6]

        list_recomendaciones = []
        for index in recomendaciones:
            movie = session.query(Movies, Machine_Learning).join(Machine_Learning).where(Machine_Learning.id_ml == index[0]).first()
            crew = session.query(Movies, Crew).join(Crew).where(and_(Movies.movie_id == movie[0].movie_id, Crew.job == 'Director')).first()

            list_recomendaciones.append({'Pelicula': movie[0].title, 'Director': crew[1].name, 'Estreno': movie[0].year, 'Resumen': movie[0].overview})

        return {'Pelicula consultada': indice_consulta[0].title + ' - ' + str(indice_consulta[0].year),'lista recomendada': list_recomendaciones}

if __name__ == '__main__':
    uvicorn.run(app, port=8000)