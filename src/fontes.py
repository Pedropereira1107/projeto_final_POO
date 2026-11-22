"""Fontes de dados: as classes que buscam os dados (em arquivo CSV ou na internet).

Conceitos de POO usados aqui:
- CLASSE ABSTRATA: FonteDados é só um "molde". Não dá para criar um objeto dela.
- HERANÇA: FonteCSV e FonteAPI "herdam" de FonteDados e ganham o método obter().
- POLIMORFISMO: as duas têm o método carregar(), mas cada uma faz do seu jeito.
  Quem usa uma fonte só chama fonte.obter(), sem se importar com o tipo dela.
"""

import time                              # para esperar alguns segundos (time.sleep)
from abc import ABC, abstractmethod      # ferramentas para criar classes abstratas

import pandas as pd                      # biblioteca de tabelas (DataFrames)
import requests                          # biblioteca para acessar sites e APIs


class FonteDados(ABC):
    """Molde de qualquer fonte de dados. Toda fonte tem um nome e sabe carregar dados."""

    def __init__(self, nome):
        self.nome = nome        # atributo: nome da fonte (ex.: "PRODES")
        self._dados = None      # atributo interno (o _ indica "não mexa de fora"): guarda os dados lidos

    @abstractmethod             # obriga toda subclasse a escrever o seu próprio carregar()
    def carregar(self):
        """Lê os dados da origem. Cada subclasse faz do seu jeito."""

    def obter(self):
        """Devolve os dados. Só lê da origem na 1ª vez; depois reaproveita (cache)."""
        if self._dados is None:             # se ainda não leu nada...
            self._dados = self.carregar()   # ...lê agora e guarda
        return self._dados                  # devolve o que está guardado


class FonteCSV(FonteDados):
    """Lê um ou vários arquivos CSV de uma pasta e junta tudo em uma tabela."""

    def __init__(self, nome, pasta, nome_arquivo, tipos=str):
        super().__init__(nome)              # chama o __init__ da classe mãe (guarda o nome)
        self.pasta = pasta                  # pasta onde estão os arquivos
        self.nome_arquivo = nome_arquivo    # nome do arquivo, ou padrão com * (ex.: "mdcr_custeio_*.csv")
        self.tipos = tipos                  # tipo das colunas; str (texto) preserva zeros à esquerda ("01")

    def carregar(self):
        arquivos = sorted(self.pasta.glob(self.nome_arquivo))  # lista os arquivos que batem com o nome, em ordem
        if len(arquivos) == 0:                                  # se não achou nenhum, avisa com um erro claro
            raise FileNotFoundError(f"{self.nome}: nenhum arquivo {self.nome_arquivo} em {self.pasta}")

        tabelas = []                                            # lista vazia para guardar cada tabela lida
        for arquivo in arquivos:                                # para cada arquivo encontrado...
            tabelas.append(pd.read_csv(arquivo, dtype=self.tipos))  # ...lê o CSV e coloca na lista
        return pd.concat(tabelas, ignore_index=True)            # empilha todas as tabelas em uma só


class FonteAPI(FonteDados):
    """Busca dados de uma API na internet (usada para o IPCA) e guarda uma cópia local."""

    def __init__(self, nome, url, arquivo_copia):
        super().__init__(nome)              # chama o __init__ da classe mãe
        self.url = url                      # endereço da API
        self.arquivo_copia = arquivo_copia  # onde salvar a cópia, para não baixar toda vez

    def carregar(self):
        if self.arquivo_copia.exists():                 # se já baixou antes...
            return pd.read_csv(self.arquivo_copia, dtype=str)  # ...lê a cópia local e pronto

        for tentativa in range(3):                      # tenta até 3 vezes (a API do BCB às vezes falha)
            try:
                resposta = requests.get(self.url, timeout=60)  # faz o pedido à API (espera até 60 s)
                resposta.raise_for_status()                    # se a API respondeu com erro, vai para o except
                tabela = pd.DataFrame(resposta.json())         # transforma o JSON recebido em tabela
                self.arquivo_copia.parent.mkdir(parents=True, exist_ok=True)  # cria a pasta, se não existir
                tabela.to_csv(self.arquivo_copia, index=False)  # salva a cópia local
                return tabela                                  # devolve a tabela
            except requests.RequestException:                  # se deu erro de conexão ou erro da API...
                time.sleep(5)                                  # ...espera 5 segundos e tenta de novo

        raise RuntimeError(f"{self.nome}: a API não respondeu depois de 3 tentativas")
