from ast import literal_eval
import pandas as pd
import movies.transformaciones as tf
import datetime

def load_credits():

    data = pd.read_csv('raw_data/credits.csv', converters={'cast': literal_eval, 'crew': literal_eval})
    crew = tf.desanidar_diccionario(data, 'crew').drop(columns=['credit_id', 'profile_path', 'gender', 'id'])
    cast = tf.desanidar_diccionario(data, 'cast').drop(columns=['credit_id', 'profile_path','cast_id', 'order', 'id', 'gender'])

    return data, crew, cast

def load_movies():

    data = pd.read_csv('raw_data/movies_dataset.csv',low_memory=False, 
                       converters={'genres': literal_eval})
    
    data.drop_duplicates(inplace=True, subset=['id'])
    data['id'] = tf.convertir_entero(data, 'id')
    data = data[data.id != 0]
    data.dropna(subset=['title', 'production_companies', 'revenue'], inplace=True)

    data['production_companies'] = data['production_companies'].apply(lambda x: literal_eval(x))
    data['production_countries'] = data['production_countries'].apply(lambda x: literal_eval(x))
    data['spoken_languages'] = data['spoken_languages'].apply(lambda x: literal_eval(x))
    genders = tf.desanidar_diccionario(data[['genres','id']], 'genres').drop(columns=['id'])
    production_companies = tf.desanidar_diccionario(data[['production_companies','id']], 'production_companies').drop(columns=['id']).rename(columns={'name': 'company'})
    production_countires = tf.desanidar_diccionario(data[['production_countries','id']], 'production_countries').drop(columns=['iso_3166_1']).rename(columns={'name': 'country'})
    spoken_languages = tf.desanidar_diccionario(data[['spoken_languages','id']], 'spoken_languages').drop(columns=['iso_639_1']).rename(columns={'name': 'language'})
   
    data['budget'] = pd.to_numeric(data['budget'])
    data['popularity'] = pd.to_numeric(data['popularity'])

    data['original_language'].fillna('', inplace = True)
    data['overview'].fillna(' ', inplace = True)
    data['release_date'].fillna(str(datetime.datetime(1,1,1).date()), inplace = True)
    data['runtime'].fillna(0, inplace = True)
    data['tagline'].fillna(' ', inplace = True)

    data['day'] = data['release_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').weekday())
    data['year'] = data['release_date'].astype(str).str.extract('(\d\d\d\d).').astype(int)
    data['month'] = data['release_date'].astype(str).str.extract('.[-](\d\d).')

    month_dictionary = {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo',
            '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', 
            '11': 'Noviembre', '12': 'Diciembre'}
    day_dictionary = {'0': 'Lunes', '1': 'Martes', '2': 'Miercoles', '3': 'Jueves', '4': 'Viernes',
            '5': 'Sabado', '6': 'Domingo'}
    data['month'] = data['month'].apply(lambda x: month_dictionary[x])
    data['day'] = data['day'].apply(lambda x: day_dictionary[str(x)])

    data = data.drop(columns=['belongs_to_collection','video', 'imdb_id', 'adult', 'poster_path', 
                              'homepage', 'genres', 'production_companies', 'production_countries', 
                              'spoken_languages', 'status']).rename(columns={'id': 'movie_id'})

    return data, genders, production_companies, production_countires, spoken_languages




