![logo Henry](https://www.soyhenry.com/_next/image?url=https%3A%2F%2Fassets.soyhenry.com%2Fhenry-landing%2Fassets%2FHenry%2Flogo.png&w=128&q=75)

# **PROYECTO MOVIES** - Henry

## **¿Por qué existe este proyecto?**

Este proyecto tiene como objetivo transformar un dataset de películas para su posterior análisis y utilización en un modelo de Machine Learning que puede ser aplicado para recomendar películas. 

Todo el backend se desarrolló como un trabajo práctico para aplicar los conocimientos adquiridos en el bootcamp de [@soyhenry_ok](https://twitter.com/soyhenry_ok).

### **Requerimientos**

* Python 3.7+
* uvicorn
* FastAPI
* SQLAlchemy

---

## 1. Paquete 'movies'

Este paquete contiene los módulos necesarios para la extracción, limpieza y tranformación de los datos (ETL), y está compuesto por:

* datasets.py

    Este módulo realiza el cargue y transformación (ETL) de los archivos CSV que se encuentran en la carpeta `raw_data`. Todo el proceso utiliza las librerías `pandas` y `ast`.

    El modulo contiene 3 clases, las cuales retornan dataframes de pandas como se observa acontinuación:

    ```python
    def load_movies():
        ...
        return movie_data, movie_genders, movie_production_companies, movie_production_countires, spoken_languages

    def load_credits():
        ...
        return credits_data, crew_data, cast_data

    load_ml_data()
        ...
        return machie_learning_data
    ```

* transformaciones.py

    Este módulo contiene las funciones utilizadas en el módulo `datasets.py` para acceder a las lístas de diccionarios, transformar tipos de datos y hallar la raíz de las palabras (para el modelo ML).

## 2. Paquete 'config'

Este paquete contiene los módulos necesarios para la creación de la base de datos sqlite y ORM mediante SQLAlquemy.

* database.py:

    Este módulo contiene la configuración de la base de datos sqlite, que se crea en el root con el nombre:

    ```python
    db_file = "../database.sqlite"
    ```

* modelos.py

    Este módulo crea las instancias ORM utilizadas en el proyecto, dividas de la siguiente manera:

    1. Clase Movies: Es la instancia principal de toda la base de datos, almacena los datos generales de las películas. Se compone de los siguientes atributos:

        Información General:

            movie_id: Entero - Llave Primaria
            original_title: String
            title: String
            tagline: String
            overview: String
            runtime: Float
            original_language: String

        Estreno:

            release_date: Datetime
            year: Integer
            month: String
            day: String

        Finanzas:

            budget: Float
            revenue: Float

        Popularidad:

            popularity: Float
            vote_average: Float
            vote_count: Float

    2. Clase Crew: Esta instancia almacena los datos del personal que apoyó la realización de la película, incluyendo directores, productores ejecutivos, directores de fotografía, entre otros. Se compone de los siguientes atributos:

            department: String
            job: String
            name: String

    3. Clase Cast: Esta instancia almaena los datos de los actores que participaron en la película. Se compone de los siguientes atributos:

            character: String
            name: String
    
## 3. API

La aplicación corre en `Fastapi` gracias a un servvidor un servidor `Uvicorn`, y contiene los siguientes endpoints:

1. cantidad_filmaciones_mes (String):
    Devuelve la cantidad de filmaciones estrenadas en un mes específico, ingresado como texto en español.

2. cantidad_filmaciones_dia (String):
    Devulve la cantidad de filmaciones estrenadas en un día de la semana específico, ingresado como texto en español.

3. score_titulo (String):
    Devulelve la popularidad de una película (al momento en que se exportó el archivo CSV) ingresando su título en ingles.

4. votos_titulo (String): 
    Devuelve la cantidad de votos y el promedio de los mismos únicamente si la película cuenta con 2.000 o más votos. Se ingresa el título de la película en ingles.

5. get_actor (String):
    Devuelve la cantidad de filmaciones realizadas por un actor, además de los ingresos totales generados, el ingreso promedio por película y una lísta con todas las películas en las que ha participado (Incluyendo el personaje y el año de estreno). Se ingresa el nombre del actor.

6. get_director (String):
    Devuelve el retorno total generado por el director, entendido como el número de dolares generados por cada dolar invertido. Además, devuelve una lista con cada una de las películas que ha dirigido, incluyendo el año de estreno, el persupuesto, los ingresos generador y el retorno de la mísma.

7. recomendacion (String):
    Devuelve una lista con 5 películas (incluye el título, el año de estreno y el resumen) recomendadas basas en una película previamente ingresada.
