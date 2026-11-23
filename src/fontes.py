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
        pass

    def obter(self):
        if self._dados is None:             # se ainda não leu nada...
            self._dados = self.carregar()   # ...lê agora e guarda
        return self._dados                  # devolve o que está guardado


class FonteCSV(FonteDados):
    """Lê um ou vários arquivos CSV de uma pasta e junta tudo em uma tabela."""

    def __init__(self, nome, pasta, nome_arquivo, tipos=str):
        super().__init__(nome)         
        self.pasta = pasta                  
        self.nome_arquivo = nome_arquivo    
        self.tipos = tipos                 

    def carregar(self):
        arquivos = sorted(self.pasta.glob(self.nome_arquivo))  
        if len(arquivos) == 0:                                 
            raise FileNotFoundError(f"{self.nome}: nenhum arquivo {self.nome_arquivo} em {self.pasta}")

        tabelas = []                                   
        
        for arquivo in arquivos:                               
            tabelas.append(pd.read_csv(arquivo, dtype=self.tipos))  
        return pd.concat(tabelas, ignore_index=True)           


class FonteAPI(FonteDados):
    """Busca dados de uma API na internet (usada para o IPCA) e guarda uma cópia local."""

    def __init__(self, nome, url, arquivo_copia):
        super().__init__(nome)              
        self.url = url                      
        self.arquivo_copia = arquivo_copia  

    def carregar(self):
        if self.arquivo_copia.exists():                 
            return pd.read_csv(self.arquivo_copia, dtype=str)  

        for tentativa in range(3):                  
            try:
                resposta = requests.get(self.url, timeout=60)  
                resposta.raise_for_status()                    
                tabela = pd.DataFrame(resposta.json())         
                self.arquivo_copia.parent.mkdir(parents=True, exist_ok=True)  
                tabela.to_csv(self.arquivo_copia, index=False) 
                return tabela                                  
            except requests.RequestException:                
                time.sleep(5)                                  

        raise RuntimeError(f"{self.nome}: a API não respondeu depois de 3 tentativas")
