import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedTeam=None

    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona un anno dal menu."))
            return
        self._model.buildGraph(self._view._ddAnno.value)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        n, a = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f" il grafo è costituito di {n} nodi e {a} archi."))
        self._view.update_page()


    def handleDettagli(self, e):
        vicini = self._model.getViciniOrdinati(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {self._selectedTeam} con relativo peso "
                                                       f"dell'arco"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        pass
    def fillDDYear(self):
        years = self._model._allYears
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options.extend(yearsDD)
        self._view.update_page()
    def handleDDYearSelection(self, e):
        self._teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(
            f"Ho trovato {len(self._teams)} squadre "
            f"che hanno giocato nel {self._view._ddAnno.value}."))
        for t in self._teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(
                data=t, text=t.teamCode, on_click=self.readDDTeams))
        self._view.update_page()
    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam=None
        else:
            self._selectedTeam = e.control.data
        print(f"readDDTeams called -- {self._selectedTeam}")