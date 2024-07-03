import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._teams = []
        self._allYears=DAO.getAllYears()
        self._grafo = nx.Graph()
        self._idMapTeams = {}

        self._bestPath=[]
        self._bestObjVal=0



    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._teams}
        return self._teams
    def buildGraph(self, year):
        self._grafo.clear()
        if len(self._teams) == 0:
            print("empty list")
            return
        self._grafo.add_nodes_from(self._teams)
        edges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(edges)
        salariesOfTeams = DAO.getTeamsSalaries(year, self._idMapTeams)
        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]
    def printGraphDetails(self):
        print(f"Grafo creato con {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi.")
    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
    def getViciniOrdinati(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append( (v, self._grafo[v0][v]["weight"]))
        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple
    def getPercorso(self, v0):
        self._bestPath = []
        self._bestObjVal = 0
        parziale=[v0]
        listaVicini=[]
        for v in self._grafo.neighbors(v0):
            edgeV = self._grafo[v0][v]["weight"]
            listaVicini.append((v, edgeV))
        listaVicini.sort(key=lambda x: x[1], reverse=True)
        parziale.append(listaVicini[0][0])
        self.ricorsione(parziale)
        parziale.pop()
    def ricorsione(self, parziale):
        if self.getScore(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self.getScore(parziale)
    def getScore(self, listOfNodes):
        if len(listOfNodes) == 1:
            return 0
        score = 0
        for i in range(0, len(listOfNodes) - 1):
            score += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return score