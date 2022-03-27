import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

## Creando la función para abrir el archivo

data_url = "data/ifood_df_eda.csv"
@st.cache
def load_data(data_url):
    data = pd.read_csv(data_url)
    data["IncomeOrder"] = pd.cut(data["Income"], bins = 4)
    return data

# abriendo el dataset

data_report = load_data(data_url)

st.title('Reporte de análisis exploratorio de datos')


image = Image.open('data/ifood.png')

st.image(image)

st.markdown("""iFood es la aplicación de entrega de alimentos líder en Brasil, presente en más de mil ciudades.
Actualmente tienen alrededor de cientos de miles de clientes registrados, además de que atienden a casi un millón
consumidores al año. Por lo que, siempre están buscando nuevas estrategias para invertir y mejorar
el desempeño de las actividades.""")

st.markdown("Se cuenta con una muestra de datos de una campaña piloto y en este informe se muestra los principales datos encontradas y la relevancia que pueden tener en una campaña.")

if st.checkbox('Mostrar datos crudos'):
    st.subheader('Datos crudos')
    st.write(data_report.head())


##  Primer grupo
st.header("Características del cliente")

## primera pregunta de exploración 

data_group_age = data_report.groupby("groupAge").agg( 
    frecuency_purchases_web = ("NumWebPurchases","mean"),
    frecuency_purchases_catalog = ("NumCatalogPurchases","mean"),
    frecuency_purchases_store = ("NumStorePurchases","mean"),
    ).reset_index().melt(id_vars =["groupAge"],
var_name='type', value_name='frecuency purchases')

data_group_age = data_group_age.replace({"type" : {"frecuency_purchases_web" : "Frec. compras por web",
                                "frecuency_purchases_catalog" : "Frec. compras por catálogo",
                                "frecuency_purchases_store" : "Frec. compras por tienda"
                                }})

plot1 = px.bar(data_group_age, x = "groupAge", 
y = "frecuency purchases", color = "type",
title = "Frecuencia de compras por grupo de edad",
category_orders= {"groupAge" : ["Young Adults", "Middle-Aged Adults", "Old Adults"]},
color_discrete_sequence=px.colors.qualitative.G10)

st.plotly_chart(plot1)

st.markdown("La gráfica nos muestra 2 puntos importantes")
st.markdown("* Los clientes compran con más frecuencias en tiendas físicas en comparación con los otros medios que cuenta la empresa.")
st.markdown("* Las personas adultas en promedio son las personas que más frecuente compran si lo comparamos por grupos de edad, esta tendencia se va mostrar en diferentes aspectos.")

## segunda pregunta de exploración 

plot2 = px.scatter(data_report, x = "Age",
    y = "MntProducts",
    facet_col = "Education", facet_col_wrap= 3,
    opacity = 0.5,
    title = "Relación entre la edad y el monto gastado por clientes según nivel de educación"
   )

st.plotly_chart(plot2)

st.markdown("La edad es un factor importante en el monto gastado por la persona, principalmente, con las personas que tienen un nivel de educación alcanzado alto. ")
st.markdown("Por otro lado, las personas con educación básica su evolución de gasto es casi nulo con más años alcanzados.")

## tercera pregunta de exploración

data_group_kid =  data_report.groupby("Kidhome").agg( MntWines = ("MntWines","mean"),
MntFruits = ('MntFruits',"mean"),
MntMeatProducts= ('MntMeatProducts',"mean"),
MntFishProducts = ('MntFishProducts',"mean"),
MntSweetProducts = ('MntSweetProducts',"mean")) / 24

data_group_kid = data_group_kid.reset_index()

plot3 = px.bar(data_group_kid, x = "Kidhome", 
y = ["MntWines","MntMeatProducts",'MntFishProducts','MntSweetProducts',"MntFruits"],
barmode= "group", title = "Gasto promedio mensual según tipo de producto",
color_discrete_sequence=px.colors.qualitative.G10)

plot3.update_xaxes(type='category')

st.plotly_chart(plot3)

data_group_teen =  data_report.groupby("Teenhome").agg( MntWines = ("MntWines","mean"),
MntFruits = ('MntFruits',"mean"),
MntMeatProducts= ('MntMeatProducts',"mean"),
MntFishProducts = ('MntFishProducts',"mean"),
MntSweetProducts = ('MntSweetProducts',"mean")) / 24

data_group_teen = data_group_teen.reset_index()

plot4 = px.bar(data_group_teen, x = "Teenhome", 
y = ["MntWines","MntMeatProducts",'MntFishProducts','MntSweetProducts',"MntFruits"],
barmode= "group", title = "Gasto promedio mensual según tipo de producto",
color_discrete_sequence=px.colors.qualitative.G10)

plot4.update_xaxes(type='category')

st.plotly_chart(plot4)

st.markdown("2 cosas importantes nos muestra esta gráficas:")
st.markdown("Primero, las personas que no tienen hijos menores o hijos adolecentes en promedio gastan más que las personas que tiene hijos menores ")
st.markdown("Segundo, El gasto promedio en vinos es mayor que los otros productos que ofrece Ifood.")


## Segundo grupo

st.header("Efectividad de la campaña piloto")

## primera pregunta de exploración

data_group_acc_1 = data_report[data_report["Accmost1"] == 1 ].groupby("Response").size().reset_index().rename(columns = {0: "total"})
data_group_acc_0 = data_report[data_report["Accmost1"] == 0 ].groupby("Response").size().reset_index().rename(columns = {0: "total"})


plot6 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])


plot6.add_trace(go.Pie( labels = data_group_acc_1["Response"] ,
 values = data_group_acc_1["total"], name = "AcceptCamp",
 title = "Aceptaron\n Anteriormente"),1,1)

plot6.add_trace(go.Pie( labels = data_group_acc_0["Response"] ,
 values = data_group_acc_0["total"], name = "AcceptCamp",
 title = "No aceptaron Anteriormente"),1,2)


plot6.update_traces(hole=.4,
 hoverinfo="label+percent+name",
 marker=dict(colors=['#f56a59','#398ef5']) )

plot6.update_layout(
    title_text="% de aceptación de la campaña piloto de las personas que aceptaron o no una campaña anteriormente",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text=' ', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text=' ', x=0.82, y=0.5, font_size=20, showarrow=False)])

st.plotly_chart(plot6)

st.markdown("""Podemos observar que las personas que aceptaron una campaña anteriormente
 tienen un mayor porcentaje de aceptación de la campaña piloto. Por otro lado, las personas que no
 aceptaron una campaña anteriormente son más propensos a no aceptar la campaña piloto.""")

## Segunda pregunta de exploración

tabla1 = data_report.groupby("IncomeOrder").agg(AcceptedCmp1 = ('AcceptedCmp1',"sum"),
AcceptedCmp2 = ('AcceptedCmp2',"sum"),
AcceptedCmp3 = ('AcceptedCmp3',"sum"),
AcceptedCmp4 = ('AcceptedCmp4',"sum"),
AcceptedCmp5 = ('AcceptedCmp5',"sum")
).sort_index().style.background_gradient(cmap='PuBu')

st.text("¿cuantas campañas en promedio se aceptaron según nivel de ingreso?")
st.table(tabla1)

st.markdown("""Las personas con ingresos medios altos son las personas 
que más dispuestos están de aceptar una oferta de una campaña de IFood, es decir, son los principales grupo
de clientes que cuenta la empresa.""")

## Tercera pregunta de exploración

data_group_income =  pd.crosstab(data_report["IncomeOrder"],data_report["Response"], normalize='index').rename(columns = {0 : "Rechazan", 1: "Aceptan"}).reset_index()
data_group_income.IncomeOrder = data_group_income.IncomeOrder.astype(str)

plot7 = px.line(data_group_income, x = "IncomeOrder",y = ["Aceptan","Rechazan"],
markers=True, title = " % Aceptación de la campaña según nivel de ingreso")

st.plotly_chart(plot7)


st.markdown("""La gráfica muestra que la proporción de personas que aceptan la campaña piloto
va en aumento cuando las personas cuentan con un nivel de ingreso mayor.""")


data_group_marital =  pd.crosstab(data_report["marital_status"], data_report["Response"]).rename(columns = {0 : "Rechazan", 1: "Aceptan"}).reset_index()

plot8 = go.Figure()

plot8.add_trace(go.Bar(
y = data_group_marital["marital_status"],
x = data_group_marital["Rechazan"],
name = "Rechazan",
orientation = "h",
marker=dict(
        color='#d32f2f')
))

plot8.add_trace(go.Bar(
y = data_group_marital["marital_status"],
x = data_group_marital["Aceptan"],
name = "Aceptan",
orientation = "h",
marker=dict(
        color='#3f51b5')
))


plot8.update_layout(barmode='stack', title_text = "¿Qué situación civil estaban las personas que aceptaron la campaña piloto ?")


st.plotly_chart(plot8)

st.markdown("""Apesar de que el rechazo de la campaña piloto es mayor en todas las situaciones
civil de las personas, hay que comprender que hay grupos, como las personas solteras,
que muestran una mayor aceptación de la campaña piloto que está llevando la compañía.""")

## Tercer grupo

st.header("Producto y medio de compra")

## primera pregunta de exploración

data_group_num = data_report.loc[:,["NumWebPurchases","NumCatalogPurchases","NumStorePurchases"]].mean().sort_values().reset_index().rename(columns = {0 : "Frecuencia de compra"})

plot9 = px.bar(data_group_num, x = "index" , y = "Frecuencia de compra",
hover_data={"Frecuencia de compra":':.2f'},
title = "¿Cuántas compras en promedio se realizaron según medio de compra?",
color_discrete_sequence=px.colors.qualitative.G10)

st.plotly_chart(plot9)

st.markdown("""Los clientes realizan con mayor frecuencia compras en la tienda física de la empresa, además,
el segundo medio donde se realizan mayor número de compras en promedio es el sitio web de la empresa.
""")

## Segunda pregunta de exploración

data_group_mnt = data_report.loc[:,["MntWines","MntFruits","MntMeatProducts","MntFishProducts","MntSweetProducts","MntGoldProds"]].mean().sort_values().reset_index().rename(columns = {0 : "Mnt gastado"})

plot10 = go.Figure(go.Bar( x = data_group_mnt["index"],
 y = data_group_mnt["Mnt gastado"]))

plot10.update_layout(
    title_text="¿Que categoría de producto han gastado más los clientes?")

st.plotly_chart(plot10)

st.markdown("""Ifood ofrece 5 tipos de productos, los vinos son uno de los principales productos en las
que se gasta más en promedio, además de las carnes que tambien son más gastado por los clientes.""")
st.markdown("""*Hay que tomar en cuenta los productos Gold, son productos dentro de las categorías 
que maneja la empresa, pero que son productos más cotizados para ellos.*""")

## Tercera pregunta de exploración

data_tercer = data_report.groupby("marital_status").mean()[["MntWines","MntFruits","MntMeatProducts","MntFishProducts","MntSweetProducts","MntGoldProds"]] /24

data_tercer = data_tercer.T.style.background_gradient(cmap='PuBu')

data_cuarto = data_report.groupby("Education").mean()[["MntWines","MntFruits","MntMeatProducts","MntFishProducts","MntSweetProducts","MntGoldProds"]] /24

data_cuarto = data_cuarto.T.style.background_gradient(cmap='PuBu')

st.text("¿Qué producto gastan más los clientes según estado civil?")

st.table(data_tercer)
st.table(data_cuarto)

st.markdown("""Tal como se vio en la gráfica anterior, las preferencias por estado civil no varian, es decir,
las personas gastan más en vinos independiente de su estado civil. Pero si lo analizamos por nivel
de educación, se puede ver un patrón similar al cuadro 1, pero que se diferencia con las personas
de educación básica que tienen una preferencia a comprar los productos gold de la empresa y los productos de pescado. """)

st.markdown("""*Aunque las personas con educación básica tienen una preferencia por los productos gold, estás son en niveles bajos de gastos.*""")
