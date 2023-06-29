import pandas as pd
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def desanidar_diccionario (df: pd.DataFrame, columna_desanidar: str):
    lista = list()
    for i, row in enumerate(df[f'{columna_desanidar}']):
        id_movie = df['id'].iloc[i]
        for item in row:
            item['movie_id'] = id_movie
            lista.append(item)

    lista = pd.DataFrame(lista)

    return lista

def convertir_diccionario(data, columna_desanidar: str, campo_extraer: str):
    lista = list()
    if columna_desanidar == 'crew':
        for row in data:
            if row['job'] == 'Director' or row['job'] == 'Executive Producer':
                lista.append(row[f'{campo_extraer}'])
                break
            else:
                continue
    else:
        for row in data:
            if len(lista) <= 6:
                lista.append(row[f'{campo_extraer}'])
            else:
                break
    return lista

def convertir_entero (df: pd.DataFrame, columna_convertir: int):
    lista = list()
    for i, row in df.iterrows():
        try:
            lista.append(int(row[f'{columna_convertir}']))
        except:
            lista.append(0)
    
    return pd.to_numeric(lista, downcast='integer')

def raiz_palabra(text):
    lista = list()

    for i in text.split():
        lista.append(ps.stem(i))

    return " ".join(lista)