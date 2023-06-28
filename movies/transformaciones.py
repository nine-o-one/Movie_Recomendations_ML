import pandas as pd

def desanidar_diccionario (df: pd.DataFrame, columna_desanidar: str):
    lista = list()
    for i, row in enumerate(df[f'{columna_desanidar}']):
        id_movie = df['id'].iloc[i]
        for item in row:
            item['movie_id'] = id_movie
            lista.append(item)

    lista = pd.DataFrame(lista)

    return lista

def convertir_entero (df: pd.DataFrame, columna_convertir: int):
    lista = list()
    for i, row in df.iterrows():
        try:
            lista.append(int(row[f'{columna_convertir}']))
        except:
            lista.append(0)
    
    return pd.to_numeric(lista, downcast='integer')
