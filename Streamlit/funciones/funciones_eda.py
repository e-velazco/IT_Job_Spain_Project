################ Librerias ################
import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import pydeck as pdk


############################################################################################################
#################################### Función de carga de datos #############################################

@st.cache_data
def load_data():
    ruta_datos = os.getcwd().replace("Streamlit", "Datos/Procesados/")
    geo_spain = pd.read_csv(ruta_datos + 'coordenadas_empleos.csv')
    df = pd.read_csv(ruta_datos + "datos_jobs_finales.csv")
    df_comunidades = pd.read_csv(ruta_datos + 'comunidades_esp.csv')
    return geo_spain, df, df_comunidades


############################################################################################################
