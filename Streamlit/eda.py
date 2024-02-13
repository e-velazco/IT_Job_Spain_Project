################ Funciones #################

from funciones.funciones_eda import *
import plotly.express as px
############################################
def eda():
    ################ DATOS #########################
    _, df, df_comunidades = load_data()
    ################################################

    st.title("Una visión general")

    st.warning(""" INTRODUCCIÓN """)


    ########## Densidad de empleos por comunidad autónoma ##########
    df_comunidad_suma = df.groupby('comunidad').size().reset_index(name='tot_jobs')
    df_comunidades = df_comunidades.merge(df_comunidad_suma, on='comunidad', how='left')
    min_size = df_comunidades['tot_jobs'].min()
    max_size = df_comunidades['tot_jobs'].max()

    df_comunidades['normalized_size'] = np.interp(df_comunidades['tot_jobs'], (min_size, max_size), (10, 100))

    st.markdown(
        """
        <style>
            .full-width {
                width: 100%;
                display: flex;
                justify-content: center;
            }
        </style>
        """, unsafe_allow_html=True
    )
    ############################################## posibilidad de hacerlo con contorno en comunidades https://python-charts.com/es/espacial/mapa-coropletas-plotly/ ##############
    mapa_burbuja = px.scatter_mapbox(
        df_comunidades,
        lat='latitude',
        lon='longitude',
        size='normalized_size',
        zoom=5,
        mapbox_style='open-street-map',
        color='tot_jobs',  # Agregar color según el tamaño de las burbujas
        color_continuous_scale=px.colors.sequential.Plasma,  # Puedes ajustar la escala de color
        labels={'tot_jobs': 'Total de Trabajos'},  # Etiqueta para la leyenda
        hover_data={'latitude': False, 'longitude': False, "normalized_size": False}
    )

    mapa_burbuja.update_traces(marker=dict(sizemode='diameter', sizeref= 1))
    mapa_burbuja.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    mapa_burbuja.update_layout(
        autosize=True,
        width=5000,  # Ajusta el ancho según tus preferencias
        height=700  # Ajusta la altura según tus preferencias
    )
    st.plotly_chart(mapa_burbuja, use_container_width=True)
    ############################################################################################


    ########## GRAFICO CATEGORIA TREEMAP ##########

    mask_cat = (df["categoria_empleo"] == "otros")
    df_titulos = df[~mask_cat].groupby(by="categoria_empleo")["titulo"].value_counts().to_frame().reset_index()
    df_titulos = df_titulos.groupby(by="categoria_empleo")[["categoria_empleo", "titulo", "count"]].head(3)

    min_size_cat = df_titulos['count'].min()
    max_size_cat = df_titulos['count'].max()
    df_titulos['normalized_size'] = np.interp(df_titulos['count'], (min_size_cat, max_size_cat), (10, 100))

    titulos = px.treemap(data_frame=df_titulos, values="count", path=["categoria_empleo", "titulo"],
                         color="categoria_empleo",
                         hover_data={"count": True, 'categoria_empleo': False, "normalized_size": False})

    titulos.update_layout(width= 1100,  # Ajusta el ancho según tus preferencias
                          height=700,  # Ajusta la altura según tus preferencias
                          uniformtext={"minsize": 12, "mode": 'hide'},
                          font={"color": "black"})

    titulos.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    st.plotly_chart(titulos)

    ########## GRAFICO PRESENCIALIDAD SUNBURST ##########
    cat_1, cat_2 = st.columns([1, 1])

    mask_pres = ((df["presencialidad"] == "no especificado") | (df["categoria_empleo"] == "otros"))
    df_pres = df[~mask_pres].groupby(by="presencialidad")["categoria_empleo"].value_counts().to_frame().reset_index()
    df_pres = df_pres.groupby(by="presencialidad")[["presencialidad", "categoria_empleo", "count"]].head(7)

    presencialidad = px.sunburst(df_pres,
                      path=["presencialidad", "categoria_empleo"],
                      values='count',
                      branchvalues='total')
    presencialidad.update_layout(
        width=650,  # Ajusta el ancho según tus preferencias
        height=650,  # Ajusta la altura según tus preferencias
        uniformtext={"minsize": 15, "mode": 'hide'},
        font={"color": "blue"})

    ########## GRAFICO HERRAMIENTAS TOP ESPAÑA ###########





    cat_1.plotly_chart(presencialidad)
    ############################################################################################





    ########## Distribucion de salarios(min y max en columnas diferentes) españa ##########
    sal_1, sal_2 = st.columns([1, 1])






    ########## Distribución de experiencia requerida ##########
    # Generar filtro en titulo para tener experiencia #





    ########## empresas con mayor numero de puestos ofertados GRAFICO CAJAS ##########



















