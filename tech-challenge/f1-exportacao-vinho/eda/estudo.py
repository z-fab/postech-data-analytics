# %% Imports

import polars as pl
import plotly.express as px

# %% #################
# Lendo CSV
######################

df_raw = pl.read_csv("../data/ExpVinho.csv", separator=";", truncate_ragged_lines=True)
df_raw.head()

# %% CSV com código e info dos países

df_pais = pl.read_csv("../data/info_paises.csv", separator=",")

df_wwp = (
    pl.read_csv(
        "../data/WPP2022_Demographic_Indicators_Medium.csv", infer_schema_length=10000
    )
    .select(
        pl.col("Time").alias("year"),
        pl.col("ISO3_code").alias("iso_code"),
        pl.col("TPopulation1Jan").alias("population"),
        pl.col("MedianAgePop").alias("median_age"),
        pl.col("PopDensity").alias("pop_density"),
        pl.col("PopSexRatio").alias("sex_ratio"),
    )
    .filter((pl.col("iso_code").is_not_null()) & (pl.col("year") < 2023))
    .sort("year")
)

# %% #################
# Trantando CSV
######################
df_cleaned = (
    df_raw.melt(
        id_vars=["Id", "País"],
    )
    .with_columns(
        pl.col("variable")
        .str.extract(r"(\d{4})(_duplicated)?")
        .alias("year")
        .cast(pl.Int64)
    )
    .select(
        pl.col("País").alias("country"),
        pl.col(["year", "value"]),
        pl.when(pl.col("variable").str.contains("_duplicated"))
        .then(pl.lit("value"))
        .otherwise(pl.lit("liters"))
        .alias("type"),
    )
    .pivot(values="value", columns="type", index=["country", "year"])
    .join(df_pais, on="country", how="left")
    .join(df_wwp, on=["iso_code", "year"], how="left")
    .with_columns(
        (pl.col("liters") / pl.col("population")).alias("liters_per_capita"),
        (pl.col("value") / pl.col("liters")).alias("price_per_liter"),
    )
    .fill_nan(0)
    .fill_null(0)
)

df_cleaned.write_csv("../data/dataframe_final.csv")

# %%


# %% #################
# Gerando Tabela contendo as informações solicitadas
######################
df_cleaned.select(
    pl.lit("Brasil").alias("País de Origem"),
    pl.col("country").alias("País de Destino"),
    pl.col("year").alias("Ano de Referência"),
    pl.col("liters").alias("Quantidade de Vinho Exportado (Litros)"),
    pl.col("value").alias("Valor Total Exportado (US$)"),
)

# %% #################
# Grafico de Linha - Valor Exportado (US$) no Ano por País
######################
fig = px.line(df_cleaned, x="year", y="value", color="country")
fig.show()

# %% #################
# Scatterplot - Valor Exportado (US$) vs Litros Exportados
######################

fig = px.scatter(df_cleaned, x="liters", y="value", color="year")
fig.show()


# %% #################
# Grafico de barra - Valor total Exportado (US$) por Ano
######################
df_aux = df_cleaned.groupby("year").agg(pl.sum("value").alias("value"))
fig = px.bar(df_aux, x="year", y="value")
fig.show()


# %% #################
# Grafico de barra - Valor total Exportado (US$) por Década
######################
df_aux = (
    df_cleaned.select((pl.col("year") // 10 * 10).alias("cut"), pl.col("*"))
    .group_by("cut")
    .agg(pl.sum("value").alias("value"))
)
fig = px.bar(df_aux, x="cut", y="value")
fig.show()


# %% #################
# Grafico de barra - Valor total Exportado (US$) por Continente
#######################

df_aux = (
    df_cleaned.group_by("continent").agg(pl.sum("value")).sort("value", descending=True)
)
fig = px.bar(df_aux, x="continent", y="value")
fig.show()


# %% #################
# Mapa - Valor total Exportado (US$) por Pais
#######################
df_aux = df_cleaned.group_by(["continent", "iso_code"]).agg(pl.sum("value"))
fig = px.scatter_geo(
    df_aux,
    locations="iso_code",
    size="value",
    color="continent",
    projection="orthographic",
)

fig.show()
# %% #################
# Mapa - Valor total Exportado (US$) por Pais por ano
#######################
df_aux = df_cleaned.group_by(["continent", "iso_code", "year"]).agg(pl.sum("value"))
fig = px.scatter_geo(
    df_aux,
    locations="iso_code",
    size="value",
    color="continent",
    projection="natural earth",
    animation_frame="year",
)
fig.show()

# %% #################
# Mapa 2 - Valor total Exportado (US$) por Pais por ano
#######################
df_aux = df_cleaned.group_by(["continent", "iso_code"]).agg(pl.sum("value"))
fig = px.choropleth(
    df_aux,
    locations="iso_code",
    color="value",
    color_continuous_scale=px.colors.sequential.Plasma,
)
fig.show()


# %% #################
# Grafico de Linha - Valor por litro (US$) no Ano por País
######################
fig = px.line(df_cleaned, x="year", y="price_per_liter", color="country")
fig.show()

# %% #################
# Grafico de barra - Valor total Exportado (US$) por Continente
#######################

df_aux = (
    df_cleaned.filter(pl.col("price_per_liter") > 0)
    .group_by("continent")
    .agg(pl.mean("price_per_liter"))
    .sort("price_per_liter", descending=True)
)
fig = px.bar(df_aux, x="continent", y="price_per_liter")
fig.show()
# %% #################
# Grafico de barra - Valor total Exportado (US$) por Continente
#######################

df_aux = (
    df_cleaned.filter(pl.col("liters") > 1000)
    .group_by("continent")
    .agg(pl.mean("liters"))
    .sort("liters", descending=True)
)
fig = px.bar(df_aux, x="continent", y="liters", barmode="group", text_auto=True)
fig.show()
# %% #################
# Scatterplot - Litros Exportados vs Idade Média
######################

fig = px.scatter(
    df_cleaned.filter(pl.col("liters") > 1000000),
    x="liters",
    y="median_age",
    color="year",
)
fig.show()
# %% #################
# Scatterplot - Litros Exportados vs Sex Ratio
######################

fig = px.scatter(
    df_cleaned.filter((pl.col("liters") > 1_000)),
    x="liters",
    y="sex_ratio",
    color="continent",
)
fig.show()

# %% #################
# Scatterplot - Litros Exportados vs Population Density
######################

fig = px.scatter(
    df_cleaned.filter((pl.col("liters") > 10_000) & (pl.col("liters") < 100_000)),
    y="liters",
    x="pop_density",
    color="continent",
)
fig.show()

# %% #################
# Scatterplot - Valor do Litro Exportado vs Média de Idade
######################

fig = px.scatter(
    df_cleaned.filter(pl.col("liters") > 1000),
    y="price_per_liter",
    x="median_age",
    color="year",
)
fig.show()

# %% Calculando Correlação
df_cleaned.filter(pl.col("liters") > 1000).select(
    pl.corr("price_per_liter", "median_age")
)
# %% #################
# Scatterplot - Valor Médio do Litro Exportado vs Média de Idade por Ano
######################

df_aux = (
    df_cleaned.filter(pl.col("liters") > 1000)
    .group_by("year")
    .agg(pl.mean("price_per_liter"), pl.mean("median_age"))
)

fig = px.scatter(df_aux, y="price_per_liter", x="median_age", color="year")
fig.show()

# %% #################
# Scatterplot - Valor Médio do Litro Exportado vs Ano de Exportação
######################

df_aux = (
    df_cleaned.filter(pl.col("liters") > 1000)
    .group_by(["continent", "year"])
    .agg(pl.mean("price_per_liter"))
)

fig = px.scatter(df_aux, y="price_per_liter", x="year", color="continent")
fig.show()

# %% Calculando a correlação
df_cleaned.filter(pl.col("liters") > 1000).select(pl.corr("price_per_liter", "year"))


# O Valor médio do litro exportado vem aumentando com o passar do tempo (correlação positiva entre ano e valor do litro)

# %% #################
# Verificando outras possíveis correlações
######################

df_cleaned.filter(pl.col("liters") > 1000).to_pandas().corr(
    numeric_only=True
).style.background_gradient(cmap="coolwarm")

# %% #################
# Função de agrupar Top N paises
######################


def agrupar_topn(df, n=5, var="value"):
    df_aux = (
        df.filter(pl.col("liters") > 1000)
        .select(pl.col(var, "country"))
        .group_by("country")
        .agg(pl.sum(var))
        .sort(var, descending=True)
        .limit(n)
    )

    list_topn = df_aux.select(pl.col("country")).to_series().to_list()

    df_aux2 = (
        df_cleaned.filter(pl.col("liters") > 1000)
        .select(pl.col(var, "country", "year"))
        .with_columns(
            pl.when(pl.col("country").is_in(list_topn))
            .then(pl.col("country"))
            .otherwise(pl.lit("Outros"))
            .alias("group")
        )
        .group_by("year", "group")
        .agg(pl.sum(var))
        .sort("year")
    )

    fig = px.line(
        df_aux2,
        x="year",
        y=var,
        color="group",
        color_discrete_map={"Outros": "#ccc"},
        markers=True,
    )
    fig.show()


# %%
agrupar_topn(df_cleaned, n=5, var="value")
# %%
px.histogram(df_cleaned.filter(pl.col("year") > 0), x="year", nbins=100)
# %%
