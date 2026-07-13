from dataclasses import dataclass

from model.artista import Artista


@dataclass
class Arco:
    artista1: Artista
    artista2: Artista
    peso: int