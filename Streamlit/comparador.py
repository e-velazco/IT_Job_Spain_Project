################ Funciones #################

from funciones.funciones_eda import *

############################################
def compara():
    ################ DATOS #########################

    _, df, df_ccaa = load_data()

    ################################################
    st.title("Explora cada rincón del mercado Tech español")

    st.warning(""" INTRODUCCIÓN Y DEFINICIÓN DE VARIABLES """)

    col1, col2 = st.columns([1, 1])

    #columns = [""]
    #selector_columnas = st.multiselect("Selecciona las columnas a comparar:", options= columns)

    #if selector_columnas:
        #st.table(df[selector_columnas])