import pandas as pd
import yaml
import uproot



def read_data(datasets: list, variables: list, carpeta: str = '../Samples/'):
    """
    Leer archivos root y convertirlos en un dataframe de pandas. Además, crea una columna donde categoriza por vbf o ggf de acuerdo al nombre del archivo.
    datasets: lista de nombres de archivos root.
    config: archivo de configuración yaml.
    carpeta: carpeta donde se encuentran los archivos root.
    """
    df_all = pd.DataFrame()
    # df_signal = pd.DataFrame()
    # df_background = pd.DataFrame()
    
    for data in datasets:
        file = uproot.open(carpeta+data+".root") 
        tree = file["miniT"]
        array = tree.arrays(variables, library="pd") # was ak - nLJmus20 and LJjet1_timing don't work with pd (but yes ak)
        df = pd.DataFrame(array)
        
        df['weights'] = df['intLumi'] * df['scale1fb']
        print(data)
        if 'vbf' in data:
            df['tipo'] = 'vbf'
        elif 'ggf' in data:
            df['tipo'] = 'ggf'
        
        df_all = pd.concat([df_all, df], axis=0)
        df_all = df_all.reset_index(drop=True)
        
    return df_all

def read_config(config_file):
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


        
        