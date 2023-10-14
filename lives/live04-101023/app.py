import polars as pl
import streamlit as st
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Análise do dataset StudentsPerformance",
    page_icon="📊",
    menu_items={
        'About': 'https://github.com/z-fab/postech-data-analytics',
    }
)

@st.cache_data
def load_data():
    df = pl.read_csv('data/StudentsPerformance.csv', separator=';')
    return df


def plot_pie(col: str, title: str, df: pl.DataFrame) -> None:
    df_aux = df.select(col).to_series().value_counts()
    fig = px.pie(df_aux, values='counts', names=col, title=title)
    return st.plotly_chart(fig, use_container_width=True)


st.write("# Análise do dataset StudentsPerformance")

t1, t2, t3 = st.tabs(["🌎 Visão Geral", "Análise Etnia", "Análise Gênero"])

df_raw = load_data()

with t1:
    
    st.dataframe(df_raw, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        plot_pie(col='gender', title='Distribuição por Gênero', df=df_raw)
    with c2:
        plot_pie(col='race/ethnicity', title='Distribuição por Etnia', df=df_raw)
        
    c1, c2 = st.columns(2)
    with c1:
        plot_pie(col='lunch', title='Distribuição por Refeição', df=df_raw)
    with c2:
        plot_pie(col='parental level of education', title='Distribuição por Educação dos pais', df=df_raw)
        
with t2:
    #Frequencia de etnias
    df_aux = df_raw.select('race/ethnicity').to_series().value_counts().sort(by='race/ethnicity')
    fig = px.bar(df_aux, x='race/ethnicity', y='counts', text_auto=True, title='Freq. Etnias')
    fig.update_traces(textfont_size=16, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)
    
    #Aviso maior proporção
    maior_prop = df_aux.sort(by='counts', descending=True).row(0)
    st.info(f"Analisando o grupo de etnias dos estudantes o **{maior_prop[0]}** representa a maior proporção dos estudantes, representando {maior_prop[1]/df_raw.shape[0]*100:.1f}% do total.", icon='📊')
    
    #Média de notas por etnia
    df_aux = df_raw.group_by(['race/ethnicity']).agg(
            pl.col(['math score', 'reading score', 'writing score']).mean().round(2),
        ).sort(by='race/ethnicity', descending=False)
    
    fig = px.bar(
        df_aux.melt(id_vars='race/ethnicity'), 
        x='race/ethnicity', 
        y='value', 
        color='variable', 
        text_auto=True, 
        title='Média de Notas por Etnia', 
        barmode='group')
    
    fig.update_traces(
        textfont_size=16,
        textposition="outside",
        cliponaxis=False
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df_aux, use_container_width=True)
    
with t3:
    #Frequencia de Genero
    df_aux = df_raw.select('gender').to_series().value_counts().sort(by='gender')
    fig = px.pie(df_aux, names='gender', values='counts', title='Freq. Gênero')
    st.plotly_chart(fig, use_container_width=True)
    
    #Aviso maior proporção
    maior_prop = df_aux.sort(by='counts', descending=True).row(0)
    st.info(f"Analisando a distribuição de gênero dos estudantes, **{maior_prop[0]}** representa a maior proporção dos estudantes, representando {maior_prop[1]/df_raw.shape[0]*100:.1f}% do total.", icon='📊')
    
    #Média de notas por etnia
    df_aux = df_raw.group_by(['gender']).agg(
            pl.col(['math score', 'reading score', 'writing score']).mean().round(2),
        ).sort(by='gender', descending=False)
    
    fig = px.bar(
        df_aux.melt(id_vars='gender'), 
        x='gender', 
        y='value', 
        color='variable', 
        text_auto=True, 
        title='Média de Notas por Genero', 
        barmode='group')
    
    fig.update_traces(
        textfont_size=16,
        textposition="outside",
        cliponaxis=False
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df_aux, use_container_width=True)