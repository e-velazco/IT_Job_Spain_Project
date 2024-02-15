################ Librerias ################

import streamlit as st
import pandas as pd
import os
import utils as utl

################ Funciones #################
from funciones.config import PAGE_CONFIG

from tech_job_app import tech_app
from eda import eda
from modelo import modelo

################ Funciones #################

from funciones.funciones_modelo import load_css

############################################
st.set_page_config(**PAGE_CONFIG)
#load_css('styles.css')

def main():

    menu = ["Inicio", "Explora el mercado", "Predictor Salarial", "Acerca de"]

    # Mostrar el menú en la barra lateral
    st.sidebar.markdown("Menu")

    page = st.sidebar.selectbox(label='Sidebar', options= menu, label_visibility='hidden')

    if page == "Inicio":
        
        tech_app()

        pass

    elif page == "Explora el mercado":

        eda()

        pass

    elif page == "Predictor Salarial":

        modelo()

        pass

    else:

        #info()

        pass


if __name__ == "__main__":
    main()