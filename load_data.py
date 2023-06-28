import movies.datasets as datasets
from config.models import Base
from config.database import engine

from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
print("Data Base Creation ... OK" + "\n" + "Starting Loading Process...")

session = Session(engine)

credits, crew, cast = datasets.load_credits()
movies, genders, production_companies, production_countires, spoken_languages = datasets.load_movies()

def load_data():

    movies.to_sql('Peliculas', con=engine, if_exists='append', index=False, chunksize=1000)
    crew.to_sql('Elenco', con=engine, if_exists='append', index=False, chunksize=1000)
    cast.to_sql('Actores', con=engine, if_exists='append', index=False, chunksize=1000)
    genders.to_sql('Generos', con=engine, if_exists='append', index=False, chunksize=1000)
    production_companies.to_sql('Companias', con=engine, if_exists='append', index=False, chunksize=1000)
    production_countires.to_sql('Paises', con=engine, if_exists='append', index=False, chunksize=1000)
    spoken_languages.to_sql('Idiomas', con=engine, if_exists='append', index=False, chunksize=1000)

    print('Data Loading Process ... OK')

session.close()
