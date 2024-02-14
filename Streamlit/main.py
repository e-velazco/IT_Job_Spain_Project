################ Librerias ################

from streamlit_option_menu import option_menu

################ Funciones #################
from funciones.config import PAGE_CONFIG
from tech_job_app import *
from eda import eda
from modelo import modelo
from comparador import compara

############################################
st.set_page_config(**PAGE_CONFIG)

def main():


    menu = ["Inicio", "Explora el mercado", "Comparador", "Predictor Salarial", "Acerca de"]
    default_index = 0

    # Crea el menú
    with st.sidebar:
        selected_option = option_menu("Menu", menu,
    icons=['rocket-takeoff', 'bar-chart-line-fill', "intersect","robot", 'heart-fill'],
    menu_icon="house", default_index=0, orientation="vertical",
    styles={
        "container": {"padding": "0!important", "background-color": "#39393D"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "grey"},
    })



    if selected_option == "Inicio":

        tech_app()

        pass

    elif selected_option == "Explora el mercado":

        eda()

        pass

    elif selected_option == "Comparador":

        compara()

        pass

    elif selected_option == "Predictor Salarial":

        modelo()

        pass

    else:

        #info()

        pass


if __name__ == "__main__":
    main()