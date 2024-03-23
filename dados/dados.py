import os
import subprocess
from sklearn.model_selection import train_test_split

from pandas import ExcelFile, read_excel, read_csv


def carregar_dados_planilha(guia="Importar_Ciclo"):
    """
    Importando os dados da planilha, gerando o dataframe da base de dados.

    :return: a base de dados.
    """
    caminho = "./base/base_dados.xlsx"
    planilha = ExcelFile(caminho)
    dados = read_excel(planilha, guia)

    print(f"\033[94m{dados[:1]}\033[0m")
    # exit()

    return dados


def preparar_dados(base_dados):
    """
    Prepara os dados para gerar o modelo.

    :param base_dados: DataFrame da base de dados.

    :return: os dados de atributos (bolas = x) e os dados
    de classificação (ganhadores = y).
    """

    # Carrega a base de dados
    dados = base_dados.copy()

    # Reajustando a columa de ganhadores para:
    # 1 - concurso com ganhadores | 0 - concurso sem ganhadores
    dados.loc[dados["Ganhou"] > 1, "Ganhou"] = 1

    # Seleciona todas as linhas mais as colunas das dezenas sorteadas
    # e a coluna de ganhadores
    dados = dados.iloc[:, 2:18]
    # print(f"\033[92m{dados[:10]}\033[0m\n")

    # Separando atributos (bolas = x) e classe (ganhadores = y)
    atributos = dados.iloc[:, 0:15].values
    # print(f"\033[93m{dados[:10]}\033[0m\n")

    classe = dados.iloc[:, 15].values
    # print(f"\033[95m{dados[:10]}\033[0m")

    # exit()

    return atributos, classe


def dividir_dados(base_dados, tm_teste=0.1, seed=12):
    """
    Divide a base de dados em treino e teste.
    Default: 90% dos dados para treino e 10% dos dados para teste.

    :param base_dados: DataFrame da base de dados.
    :param tm_teste: define o percentual de dados para teste.
    :param seed: padroniza a randomização dos dados para replicação do modelo.
    :return: os dados de treino, teste e o total de atributos contido na base de dados.
    """

    atributos, classe = preparar_dados(base_dados)
    total_atributos = atributos.shape[1]

    # Dividindo os dados em treino e teste
    x_treino, x_teste, y_treino, y_teste = train_test_split(
        atributos, classe, test_size=tm_teste, random_state=seed
    )

    return x_treino, x_teste, y_treino, y_teste, total_atributos


def carregar_dados_csv():
    """
    Importando os dados do csv, gerando o dataframe da base de dados.

    :return: a base de dados.
    """
    # csv = "./base/resultados.csv"
    # Obtém o caminho absoluto do arquivo resultados.csv
    csv = os.path.abspath("./base/resultados.csv")

    # Verificar se o arquivo existe
    if not os.path.exists(csv):
        print(f"Arquivo: {csv} não existe.\nTentando criar e carregar este arquivo...")

        # Chama o script Python para criar o CSV
        subprocess.run(["python3", "./dados/obter_resultados.py"])

        # exit()

    dados = read_csv(csv, sep=";", thousands=".", decimal=",", encoding="utf-8")
    print("\033[91m{dados}\033[0m")
    exit()
    return dados

    # dados = read_csv(
    #     csv,
    #     sep=";",
    #     thousands=".",
    #     decimal=",",
    #     header=0,
    #     names=[
    #         "Concurso",
    #         "Data Sorteio",
    #         "B1",
    #         "B2",
    #         "B3",
    #         "B4",
    #         "B5",
    #         "B6",
    #         "B7",
    #         "B8",
    #         "B9",
    #         "B10",
    #         "B11",
    #         "B12",
    #         "B13",
    #         "B14",
    #         "B15",
    #         "Ganhadores 15 acertos",
    #         "Cidade / UF",
    #         "Rateio 15 acertos",
    #         "Ganhadores 14 acertos",
    #         "Rateio 14 acertos",
    #         "Ganhadores 13 acertos",
    #         "Rateio 13 acertos",
    #         "Ganhadores 12 acertos",
    #         "Rateio 12 acertos",
    #         "Ganhadores 11 acertos",
    #         "Rateio 11 acertos",
    #         "Acumulado 15 acertos",
    #         "Arrecadacao Total",
    #         "Estimativa Prêmio",
    #         "Acumulado sorteio especial Lotofácil da Independência",
    #         "Observação",
    #     ],
    # )
