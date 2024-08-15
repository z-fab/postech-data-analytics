from datetime import datetime
import polars as pl
import streamlit as st
import spacy


@st.cache_data()
def create_dataframe():
    df_diarioFreq = pl.read_csv("backend/data/TbDiarioFrequencia.csv").select(
        pl.col("IdDiarioAula").alias("id_diario_aula"),
        pl.col("IdAluno").alias("id_aluno"),
        pl.when(pl.col("StPresencaFalta") == "P")
        .then(1)
        .otherwise(0)
        .alias("presente"),
    )

    df_diarioAula = (
        pl.read_csv(
            "backend/data/TbDiarioAula.csv",
            ignore_errors=True,
        )
        .select(
            pl.col("IdDiarioAula").alias("id_diario_aula"),
            pl.col("IdDiario").alias("id_diario"),
            pl.col("DataAula")
            .str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S")
            .alias("data_aula"),
            pl.col("NumeroAula").alias("num_aula"),
            pl.col("ConteudoMinistrado").alias("conteudo_ministrado"),
            pl.col("IdProfessor").alias("id_professor"),
        )
        .with_columns(pl.col("data_aula").dt.weekday().alias("dia_semana"))
        .to_dummies("dia_semana")
        .sort(["data_aula", "num_aula"])
    )

    df_diario = pl.read_csv("backend/data/TbDiario.csv", ignore_errors=True).select(
        pl.col("IdDiario").alias("id_diario"),
        pl.col("IdTurma").alias("id_turma"),
        pl.col("IdDisciplina").alias("id_disciplina"),
    )

    df_turma = pl.read_csv("backend/data/TbTurma.csv", ignore_errors=True).select(
        pl.col("IdTurma").alias("id_turma"),
        pl.col("IdSerie").alias("id_serie"),
        pl.col("IdPeriodo").alias("id_periodo"),
        pl.col("TurnoPrincipal")
        .replace_strict({"M": 0, "T": 1, "N": 2, "Z": 3}, default=4)
        .alias("turno_turma"),
    )

    df_aluno = (
        pl.read_csv("backend/data/TbAluno.csv", ignore_errors=True)
        .select(
            pl.col("IdAluno").alias("id_aluno"),
            pl.col("DataNascimento")
            .str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S", strict=False)
            .alias("data_nascimento_aluno"),
            pl.col("Sexo").replace_strict({"M": 0, "F": 1}).alias("sexo_aluno"),
            pl.when(pl.col("IdPai").is_null()).then(0).otherwise(1).alias("tem_pai"),
            pl.when(pl.col("IdMae").is_null()).then(0).otherwise(1).alias("tem_mae"),
            pl.col("CorRaca").fill_null("None").alias("raca_aluno"),
        )
        .with_columns(
            (datetime.now().year - pl.col("data_nascimento_aluno").dt.year()).alias(
                "idade_aluno"
            )
        )
        .to_dummies(["raca_aluno"])
    )

    df_professor = (
        pl.read_csv(
            "backend/data/TbProfessor.csv",
            ignore_errors=True,
        )
        .select(
            pl.col("IdProfessor").alias("id_professor"),
            pl.col("DataNascimento")
            .str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S", strict=False)
            .alias("data_nascimento_professor"),
            pl.col("Sexo").replace_strict({"M": 0, "F": 1}).alias("sexo_professor"),
            pl.col("CorRaca").alias("raca_professor"),
            pl.col("Cargo").fill_null("Nenhum").alias("cargo_professor"),
        )
        .with_columns(
            (datetime.now().year - pl.col("data_nascimento_professor").dt.year()).alias(
                "idade_professor"
            )
        )
        .to_dummies(["raca_professor", "cargo_professor"])
    )

    # merge
    df_raw = df_diarioFreq.join(df_aluno, on="id_aluno", how="left")
    df_raw = df_raw.join(df_diarioAula, on="id_diario_aula", how="left")
    df_raw = df_raw.join(df_professor, on="id_professor", how="left")
    df_raw = df_raw.join(df_diario, on="id_diario", how="left")
    df_raw = df_raw.join(df_turma, on="id_turma", how="left")

    df_seq = df_raw.sort("id_aluno", "data_aula").with_columns(
        pl.col("data_aula").rank("ordinal").over("id_aluno").alias("seq_presenca")
    )

    return df_seq


@st.cache_data()
def get_alunos():
    df_aluno = (
        pl.read_csv("backend/data/TbAluno.csv", ignore_errors=True)
        .select(
            pl.col("IdAluno").alias("id_aluno"),
            pl.col("NomeAluno").alias("nome_aluno"),
            pl.col("DataNascimento")
            .str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S", strict=False)
            .alias("data_nascimento_aluno"),
            pl.col("Sexo").replace_strict({"M": 0, "F": 1}).alias("sexo_aluno"),
        )
        .with_columns(
            pl.concat_str(
                [pl.col("nome_aluno"), pl.col("id_aluno")], separator=" - ID: "
            ).alias("nome_id_aluno")
        )
    )
    return df_aluno


def prepare_data_to_predict(df, id_aluno):
    df_aluno = df.filter(pl.col("id_aluno") == id_aluno)

    inicio_janela = df_aluno["seq_presenca"].max() - 10
    fim_janela = df_aluno["seq_presenca"].max()

    nlp = spacy.load("pt_core_news_sm")

    def criar_embedding(texto):
        doc = nlp(texto)
        return doc.vector.tolist()

    df_janela = (
        df_aluno.sort("seq_presenca")
        .filter(
            (pl.col("seq_presenca") >= inicio_janela)
            & (pl.col("seq_presenca") <= fim_janela)
        )
        .group_by("id_aluno")
        .agg(
            # Coletando dados da aula
            pl.first("data_aula").alias("first_data_aula"),
            pl.last("data_aula").alias("last_data_aula"),
            pl.sum("dia_semana_1"),
            pl.sum("dia_semana_2"),
            pl.sum("dia_semana_3"),
            pl.sum("dia_semana_4"),
            pl.sum("dia_semana_5"),
            pl.sum("dia_semana_6"),
            pl.sum("dia_semana_7"),
            pl.col("conteudo_ministrado").str.concat(" ").alias("conteudo"),
            # Coletando dados do aluno
            pl.first("sexo_aluno").alias("sexo_aluno"),
            pl.first("tem_pai").alias("tem_pai"),
            pl.first("tem_mae").alias("tem_mae"),
            pl.first("raca_aluno_A"),
            pl.first("raca_aluno_B"),
            pl.first("raca_aluno_I"),
            pl.first("raca_aluno_N"),
            pl.first("raca_aluno_None"),
            pl.first("raca_aluno_P"),
            pl.first("raca_aluno_R"),
            pl.mean("idade_aluno").alias("idade_aluno_media"),
            # Coletando dados do professor
            pl.sum("sexo_professor"),
            pl.sum("raca_professor_A"),
            pl.sum("raca_professor_B"),
            pl.sum("raca_professor_N"),
            pl.sum("raca_professor_P"),
            pl.sum("raca_professor_R"),
            pl.sum("cargo_professor_Nenhum"),
            pl.sum("cargo_professor_Neuropsicóloga"),
            pl.sum("cargo_professor_Professor"),
            pl.sum("cargo_professor_Professor Inglês"),
            pl.sum("cargo_professor_Professor de Inglês"),
            pl.sum("cargo_professor_Professor de Matemática"),
            pl.sum("cargo_professor_Professora"),
            pl.sum("cargo_professor_Professora de Inglês"),
            pl.sum("cargo_professor_Professora de Matemática"),
            pl.sum("cargo_professor_Professora/Coordenadora"),
            pl.sum("cargo_professor_Psicóloga"),
            pl.sum("cargo_professor_Psicólogo"),
            pl.sum("cargo_professor_professora"),
            pl.mean("idade_professor"),
            # verificando quantos professores diferentes o aluno teve aula
            pl.n_unique("id_professor").alias("num_professores"),
            # verificando quantas disciplinas diferentes o aluno teve
            pl.n_unique("id_disciplina").alias("num_disciplinas"),
            # verificando quantas series diferentes o aluno esteve presente
            pl.n_unique("id_serie").alias("num_series"),
            # verificando quantas turmas diferentes o aluno esteve presente
            pl.n_unique("id_turma").alias("num_periodos"),
            # quantas presenças o aluno teve
            pl.sum("presente").alias("num_presencas"),
            # quantas presenças totais houve no período
            pl.count("presente").alias("num_aulas"),
            # na ordem de presenças, qual foi a última que o aluno esteve presente
            pl.when(pl.col("presente") == 1)
            .then(pl.col("seq_presenca"))
            .otherwise(0)
            .max()
            .alias("ultima_presenca"),
        )
        .with_columns(
            pl.lit(fim_janela).alias("last_seq"),
            pl.col("conteudo")
            .map_elements(criar_embedding, return_dtype=pl.List(pl.Float64()))
            .alias("conteudo_embedding"),
        )
        .select(
            pl.all().exclude("conteudo", "conteudo_embedding"),
            pl.col("conteudo_embedding").list.to_struct(),
        )
        .unnest("conteudo_embedding")
    )

    return df_janela


def load_data():
    return create_dataframe()
