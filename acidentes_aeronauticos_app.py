import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import streamlit as st
import cenipa_library as cl
import plotly.express as px
from PIL import Image

#Loading Data
path = r'C://Users/BeneviBr/Downloads/acidentes_aeronauticos.csv'

@st.cache
def load_data(path):
    data = pd.read_csv(path)
    data['data'] = pd.to_datetime(data['data'])
    object_cols = [x for x, y in zip(data.dtypes.index, data.dtypes.values) if y == 'object']
    data[object_cols] = data[object_cols].astype(str)

    #Colocar as colunas em lowercase
    columns = ['classificacao','tipo','tipo_categoria','cidade','status']
    to_title = lambda x: x.title()
    data[columns] = data[columns].applymap(to_title)
    return data

df = load_data(path)

#Sidebar
st.sidebar.header("Parametros")

info_rows = st.sidebar.empty()

##Ano dos fatos
st.sidebar.subheader("Ano")
ano = st.sidebar.slider("Selecione o ano",min(df.data.dt.year),max(df.data.dt.year),max(df.data.dt.year) - 1)

##Classificação de Ocorrencia
st.sidebar.subheader("Classificação de Ocorrencia")
incidentes_tipo = st.sidebar.multiselect(label="Selecione as Ocorrências",
                                         options=df.classificacao.unique().tolist(),
                                         default= ["Incidente Grave"])

##Redes Sociais
linkedin = Image.open(r"C:\Users\BeneviBr\Downloads\linkedin1.jpg")
github = Image.open(r"C:\Users\BeneviBr\Downloads\github.jpg")
st.sidebar.subheader("Follow me")
st.sidebar.image([linkedin,github],width=50)
st.sidebar.markdown("[**breno benevides (LinkedIn)**](https://www.linkedin.com/in/breno-benevides-173665143/)")
st.sidebar.markdown("[**breno benevides (Github)**](https://github.com/BrenoBenevides/Data-Science)")

st.sidebar.markdown("*Developed by Breno Benevides*")

##Cabeçalho e outras informações
st.title("Cenipa - Incidentes Aeronáuticos")
st.markdown("""Essa aplicação disponibiliza relatórios anuais de acidentes aeronáuticos usando dados fornecidos
               pelo [Cenipa](https://www2.fab.mil.br/cenipa/).""")

image = Image.open(r"C:\Users\BeneviBr\Downloads\forca_aeria.jpg")
st.image(image,caption="Força Aéria Brasileira")

st.subheader("Parâmetros")
st.markdown("**Ano Selecionado**: {}".format(ano))
st.markdown(f"""**Tipos de Incidentes**: {", ".join(incidentes_tipo)}""")

##Filtragem do dataframe
df_filtered = df[(df.data.dt.year == int(ano)) & (df.classificacao.isin(incidentes_tipo))].reset_index(drop=True)
info_rows.info("Foram carregadas {} linhas".format(df_filtered.shape[0]))

##Grafico de cards
cl.card_chart(df_filtered,range(4))

##Insights abaixo do grafico

try:
    df_last_year = df.loc[df.data.dt.year== ano-1]
    df_this_year = df.loc[df.data.dt.year== ano]

    st.subheader("Insights Gerais")
    st.markdown("* {} acidentes comparado ao ano passado".format(cl.year_comparasion(df_this_year,df_last_year,"codigo_ocorrencia")))
    st.markdown("* {} aeronaves envolvidas comparado ao ano passado".format(str(int(df_this_year.aeronaves_envolvidas.sum()*100 / df_last_year.aeronaves_envolvidas.sum() -1))+"%"))
    st.markdown("* **Mês com mais acidentes:** {}".format(cl.get_month_name(df_this_year.data.dt.month.value_counts().index[0])))
    st.markdown("* **Estado com mais acidentes:** {}".format(df_this_year.ocorrencia_uf.value_counts().index[0]))
except:
    st.markdown("* **Mês com mais acidentes:** {}".format(cl.get_month_name(df_this_year.data.dt.month.value_counts().index[0])))
    st.markdown("* **Estado com mais acidentes:** {}".format(df_this_year.ocorrencia_uf.value_counts().index[0]))

st.subheader("Relatório referente {}".format(ano))

meses_mais_acidentes = df_filtered.groupby(df_filtered.data.dt.month)['codigo_ocorrencia'].count().sort_values()
estados_mais_acidentes = df_filtered.ocorrencia_uf.value_counts()[:10].sort_values()

fig,ax = plt.subplots(1,2,figsize=(24,8))

##Acidentes por mês

st.plotly_chart(px.bar(x=meses_mais_acidentes.index,
                       y=meses_mais_acidentes.values,
                       title="Acidentes por mes em {}".format(ano),
                       labels={"x":"Meses","y":"Acidentes"}))

##Acidentes por Estado

st.plotly_chart(px.bar(y=estados_mais_acidentes.index,
                       x=estados_mais_acidentes.values,
                       title="Acidentes por Estado",
                       orientation='h',
                       labels={"x":"Acidentes","y":"Estados"}))
#Acidentes por Categoria
categorias_grp = df_filtered.groupby("tipo_categoria")['tipo_categoria'].count()
st.plotly_chart(px.pie(categorias_grp,categorias_grp.index,categorias_grp.values,title="Acidentes por Categoria"))

#Acidentes por classificação
classificacao_grp = df.loc[df.data.dt.year==ano].groupby("classificacao")['classificacao'].count()
st.plotly_chart(px.pie(classificacao_grp,classificacao_grp.index,classificacao_grp.values,title="Classificacao de Acidentes"))

#Relatorio Geral
st.subheader("Relatório Geral dos Anos")

st.markdown('* Houveram {} acidentes entre 2008 e 2018'.format(df.count()[0]))
st.markdown('* {} foi responsavel por {} dos acidentes'.format(estados_mais_acidentes.index[-1],
                                                               str(int(estados_mais_acidentes.values[0] * 100 / estados_mais_acidentes.values.sum()))+"%"))

##Acidentes ao longo dos anos
acidentes_grp = df.groupby(df.data.dt.year)['codigo_ocorrencia'].count()
st.plotly_chart(px.line(acidentes_grp,
                        x= acidentes_grp.index,y= acidentes_grp.values,
                        title= "Acidentes ao longo dos anos",
                        labels= {"data":'Ano',"y":"Acidentes"}))

##Acidentes por Estado
estados_mais_acidentes_geral = df.ocorrencia_uf.value_counts()[:10].sort_values()
st.plotly_chart(px.bar(y=estados_mais_acidentes_geral.index,
                       x=estados_mais_acidentes_geral.values,
                       title="Acidentes por Estado",
                       orientation='h',
                       labels={"x":"Acidentes","y":"Estados"}))

##Acidentes por Categoria
categorias_grp_geral = df.groupby("tipo_categoria")['tipo_categoria'].count()
st.plotly_chart(px.pie(categorias_grp_geral,categorias_grp_geral.index,categorias_grp_geral.values,title="Acidentes por Categoria"))


##Mapa de Calor dos Acidentes

st.write("Mapa dos Acidentes")
st.map(df)






