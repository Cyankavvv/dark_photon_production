import pandas as pd
import yaml
import uproot
import math



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


# Function that returns the number of MC events
def get_number_of_mc_events(array):
    number_of_mc_events = ak.count(array["weight"])
    return number_of_mc_events

# Function that returns the number of real events
def get_number_of_real_events(config:dict, array):
    lum = config['lhc']['lum']
    number_of_real_events = ak.sum(array["weight"]*lum)
    return number_of_real_events

# Function that calculates de significance (Gaussian)
def get_significance_gauss(s, b):
    significance = s / (s + b)**(1/2)
    return significance

# Function that calculates de significance (Poisson)
def get_significance_poisson(s, b):
    significance = math.sqrt(2 * abs( (s+b) * math.log(1 + ( s / b )) - s))
    return significance



def get_mincut_significance(config:dict, array_sgn, array_bkg, variable, n_bins, min_value, max_value):
    array_masked_sgn = array_sgn
    array_masked_bkg = array_bkg
    best_significance = 0
    best_cut = 0
    table = [["Cut", "Signal", "Background", "Significance", "Best cut"]]
    for i in range(n_bins):
        cut_value = min_value + (max_value - min_value) / n_bins * i
        array_masked_sgn = ak.mask(array_masked_sgn, array_masked_sgn[variable] > cut_value)
        array_masked_bkg = ak.mask(array_masked_bkg, array_masked_bkg[variable] > cut_value)
        signal = get_number_of_real_events(config, array_masked_sgn)
        background = get_number_of_real_events(config, array_masked_bkg)
        significance = get_significance_poisson(signal, background)
        if significance > best_significance:
            best_significance = significance
            best_cut = cut_value
        table.append([cut_value, signal, background, significance, best_cut])
    return table



        
        