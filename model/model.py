import copy

import networkx as nx
from networkx.classes import neighbors

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapArtisti = {}
        self._idMapTrackArtist = {}
        self._idMapPlaylistArtist = {}
        self._artisti = []
        self._edges = []
        self._bestPath = []
        self._bestCost = 0

    def creaGrafo(self):
        self._grafo.clear()
        self._artisti = DAO.getAllNodes()
        for a in self._artisti:
            self._idMapArtisti[a.ArtistId] = a
            self._idMapTrackArtist[a.ArtistId] = DAO.getTracksFromArtistId(a.ArtistId)
            self._idMapPlaylistArtist[a.ArtistId] = DAO.getTracksFromArtistId(a.ArtistId)

        self._grafo.add_nodes_from(self._artisti)
        self._edges = DAO.getAllEdges(self._idMapArtisti)
        for e in self._edges:
            self._grafo.add_edge(e.artista1, e.artista2, weight=e.peso)

    def getDettagliGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getArtistaGradoMax(self):
        maxArtista = max(self._grafo.nodes, key= lambda x:self._grafo.degree(x))
        return maxArtista, self._grafo.degree(maxArtista)
    def getArtistaPesiMax(self):
        artistiPesi = []
        for n in self._grafo.nodes:
            sommaPesi =  0
            vicini = self._grafo.neighbors(n)
            for v in vicini:
                sommaPesi += self._grafo[v][n]["weight"]
            artistiPesi.append((n, sommaPesi))
        artistiPesi.sort(key=lambda x: x[1], reverse=True)
        return artistiPesi[0]

    def best10archi(self):
        best10archi = []
        for u,v,data in self._grafo.edges(data=True):
            # metto sempre prima il nodo alfabeticamente che viene prima
            if v.Name > u.Name:
                best10archi.append((u,v,data["weight"]))
            else:
                best10archi.append((v, u, data["weight"]))
        best10archi.sort(key=lambda x: (-x[2] ,x[0].Name ,x[1].Name))
        return best10archi[:10]

    def getAllArtisti(self):
        return self._artisti

    def getPath(self,N, source):
        self._bestPath =[]
        self._bestCost = 0
        parziale = [source]

        self._ricorsione(parziale,N)


        listaArtistiOrd = []
        for a in self._bestPath:
            listaArtistiOrd.append((a.Name, len(self._idMapTrackArtist[a.ArtistId]), len(self._idMapPlaylistArtist[a.ArtistId])))
        listaArtistiOrd.sort(key=lambda x: x[0])
        return listaArtistiOrd, len(listaArtistiOrd), self._bestCost

    def _ricorsione(self, parziale,N):

        if len(parziale) == N:
            totBrani = self._getTotBrani(parziale)
            if totBrani > self._bestCost:
                self._bestCost = totBrani
                self._bestPath = copy.deepcopy(parziale)
            return
        #   INSIEME DI ARTISTI -> set() NON HA DUPLICATI
        for candidato in self._grafo.nodes:
                if self.hasCollegamento(candidato, parziale) and not self.hasPeso1(candidato, parziale) and candidato not in parziale:
                    parziale.append(candidato)
                    self._ricorsione(parziale,N)
                    parziale.pop()

    def hasCollegamento(self,candidato,parziale):
        for n in parziale:
            if self._grafo.has_edge(candidato,n):
                return True

        return False

    def hasPeso1(self,candidato,parziale):
        for n in parziale:
            if self._grafo.has_edge(candidato,n):
                if self._grafo[candidato][n]["weight"] == 1:
                    return True
        return False

    def _getTotBrani(self,parziale):
        totBrani = 0
        for n in parziale:
            totBrani += len(self._idMapTrackArtist[n.ArtistId])
        return totBrani
