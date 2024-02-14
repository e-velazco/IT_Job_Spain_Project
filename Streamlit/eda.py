################ Funciones #################
import streamlit_folium

from funciones.funciones_eda import *
############################################
def eda():
    ################ DATOS #########################
    _, df, df_comunidades, df_herramientas, provincias_geojson = load_data()
    ################################################

    st.title("Una visión general")

    st.warning(""" INTRODUCCIÓN """)

    ################################################################
    ########## Densidad de empleos por comunidad autónoma ##########
    df_comunidad_suma = df.groupby('comunidad').size().reset_index(name='tot_jobs')
    df_comunidades = df_comunidades.merge(df_comunidad_suma, on='comunidad', how='left')
    df_comunidades["comunidad"] = df_comunidades["comunidad"].map(lambda x: re.sub(r'[áéíóúüàèìòùñ]', lambda m: unidecode(m.group()), str(x)))

    mapa_españa = folium.Map(location=[40.223611, -1.979444], zoom_start=5)

    folium.Choropleth(
        geo_data=provincias_geojson,
        name="choropleth",
        data=df_comunidades,
        columns=["comunidad", "tot_jobs"],
        key_on="properties.comunidad",
        fill_color="RdYlBu_r",
        bins=20,
        saturation=0.5,
        fill_opacity=0.6,
        line_opacity=.1,
        legend_name="Número de empleos",
    ).add_to(mapa_españa)

    folium.LayerControl().add_to(mapa_españa)

    # Mostrar el mapa en Streamlit
    streamlit_folium.folium_static(mapa_españa)


    ###############################################
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


    titulos.update_traces(marker=dict(cornerradius=5))

    st.plotly_chart(titulos)
    ######################################################
    ########## GRAFICO PRESENCIALIDAD ####################

    data = [{'id': 'Total', 'datum': 3945, 'children': [
        {'id': "presencial", 'datum': 420,
         'children': [
             {'id': "programador", 'datum': 262},
             {'id': "sistemas", 'datum': 98},
             {'id': "data driven", 'datum': 60}
         ]},
        {'id': "hibrido", 'datum': 1345,
         'children': [
             {'id': "programador", 'datum': 905},
             {'id': "sistemas", 'datum': 151},
             {'id': "data driven", 'datum': 299}
         ]},
        {'id': "remoto", 'datum': 2230,
         'children': [
             {'id': "programador", 'datum': 1421},
             {'id': "sistemas", 'datum': 283},
             {'id': "data driven", 'datum': 526}
         ]}
    ]}]

    circles = circlify.circlify(
        data,
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

    # Create just a figure and only one subplot
    grafico_presencialidad, ax = plt.subplots(figsize=(14, 14))

    # Title
    ax.set_title('Distribución de la presencialidad según categorías ')

    # Remove axes
    ax.axis('off')

    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)

    # Print circle the highest level (continents):
    presencialidad_labels = []
    for circle in circles:
        if circle.level != 2:
            continue
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=3, color="lightblue"))
        text = plt.annotate(circle.ex["id"], (x, y), va='bottom', ha='left',
                            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=.9))
        # Personalize label positions here
        if circle.ex["id"] == "Total":
            text.set_position((x - 0.1 + 0.2, y))  # Move up and right
        elif circle.ex["id"] == "presencial":
            text.set_position((x - 0.07, y - 0.2))  # Move down and left
        elif circle.ex["id"] == "hibrido":
            text.set_position((x - 0.1, y - 0.3))  # Move down and right
        elif circle.ex["id"] == "remoto":
            text.set_position((x, y + 0.4))  # Move up
        presencialidad_labels.append(text)

    # Print circle and labels for the highest level:
    for circle in circles:
        if circle.level != 3:
            continue
        x, y, r = circle
        label = circle.ex["id"]
        ax.add_patch(plt.Circle((x, y), r, alpha=0.5, linewidth=2, color="#69b3a2"))
        plt.annotate(label, (x, y), ha='center', color="black")

    # Print labels for the continents
    for circle in circles:
        if circle.level != 2:
            continue
        x, y, r = circle
        label = circle.ex["id"]

    col_1, col_2, col_3 = st.columns([1, 1, 1], gap="large")
    # Show the plot in Streamlit
    col_2.pyplot(grafico_presencialidad)

    ######################################################
    ########## GRAFICO HERRAMIENTAS TOP ESPAÑA ###########

    if st.checkbox(label="Sin Inglés"):
        mask = df_herramientas["herramienta"] == "ingles"
        top_30_herramientas = df_herramientas[~mask].sort_values(by="count", ascending=False).head(30)

    else:
        top_30_herramientas = df_herramientas.sort_values(by="count", ascending= False).head(30)

    grafico_herramientas = go.Figure(data=[go.Bar(
                                     x= top_30_herramientas['herramienta'], y= top_30_herramientas['count'],
                                     text= top_30_herramientas['herramienta'],
                                     textposition='auto',
                                     marker={"color": list(range(0, len(top_30_herramientas['herramienta']))), 'colorscale': 'blugrn'})])

    grafico_herramientas.update_layout(barmode='stack', xaxis_type='category',
                      title='<b></b><b>Herramientas más demandadas en el mercado laboral Tech español.</b>',
                      # "",
                      paper_bgcolor='rgb(17,17,17)',
                      plot_bgcolor='rgb(206, 220, 227)',
                      font=dict(
                          family="Courier New, monospace",
                          size=20,
                          color="#000000"
                      ),
                      width=1400,
                      height=600,
                      margin=dict(l=0, r=0, t=50, b=0),
                      autosize=True

                      )
    st.plotly_chart(grafico_herramientas)


    ########## Distribucion de salarios ##################
    ######################################################

    df_salarios = df.dropna(subset=['salario_min', 'salario_max'], how='all')
    df_salarios = df_salarios[df_salarios['salario_min'] > 15000]
    df_salarios = metodo_tukey(df_salarios, 'salario_min', 1.5)
    df_salarios = metodo_tukey(df_salarios, 'salario_max', 1.5)

    grafico_salarios = px.histogram(data_frame=df_salarios,
                       x=["salario_min", "salario_max"],
                       nbins=30,
                       marginal="box",
                       color_discrete_map={"salario_min": "#19F2BA", "salario_max": "#F29B19"})

    grafico_salarios.update_layout(title_text="Histogramas de Salarios en España", height=600, width=1000)

    st.plotly_chart(grafico_salarios)

    ########## Distribución de experiencia ###############
    ######################################################

    df_experiencia = df["experiencia"].value_counts().sort_index().to_frame().reset_index()

    col_1, col_2, col_3 = st.columns([1, 1, 1], gap="large")

    grafica_experiencia, ax = plt.subplots(figsize=(8, 8))
    ax.stem(df_experiencia["experiencia"], df_experiencia["count"])
    lineas = ax.get_lines()
    lineas[0].set_color("orange")
    lineas[0].set_linewidth(3)
    col_2.pyplot(grafica_experiencia, use_container_width=True)





    ########## empresa con número de puestos ofertados ##########
    #############################################################

    df_empresas = df.copy()
    top_15_empresas = df_empresas['empresa'].value_counts().head(15)
    df_empresas_top_15 = df_empresas[df_empresas['empresa'].isin(top_15_empresas.index)]
    df_empresas_top_15['total'] = 1

    if st.checkbox(label="Sin Otros"):
        mask_empleo = df_empresas_top_15['categoria_empleo'] != 'otros'
        df_empresas_top_15 = df_empresas_top_15[mask_empleo]

    graf_empresas_top = px.treemap(df_empresas_top_15,
                     values="total",
                     path=["empresa", "categoria_empleo"],
                     hover_name="categoria_empleo",
                     color="empresa",
                     title='Treemap: Suma de veces que aparece cada empresa')
    graf_empresas_top.update_traces(marker=dict(cornerradius=5))
    # Mostrar el gráfico
    st.plotly_chart(graf_empresas_top)


















