"""Pacote responsável pela obtenção dos dados (Etapa 2)."""

from fontes.fonte_dados import FonteDados
from fontes.fonte_csv import FonteCSV
from fontes.fonte_api import FonteAPI

__all__ = ["FonteDados", "FonteCSV", "FonteAPI"]
