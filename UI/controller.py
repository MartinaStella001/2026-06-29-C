import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceArtista = None


    def handleCreaGrafo(self, e):
        self._model.creaGrafo()
        nodi, archi = self._model.getDettagliGrafo()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato.", color="green")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di nodi: {nodi}")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {archi}")
        )
        self._fillDDArtista()
        self._view.update_page()

    def _fillDDArtista(self):
        artisti = self._model.getAllArtisti()
        for a in artisti:
            self._view._ddArtista.options.append(
                ft.dropdown.Option(data=a, text=a.Name, on_click=self._saveChoiceArtista)
            )
        self._view.update_page()

    def _saveChoiceArtista(self,e):
        self._choiceArtista = e.control.data
        print(f"Artista: {self._choiceArtista}")


    def handleStampaInfo(self,e):
        artistaGradoMax, grado = self._model.getArtistaGradoMax()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Artista con grado maggiore: {artistaGradoMax} (grado:{grado})")
        )
        artistaPesiMax = self._model.getArtistaPesiMax()
        self._view._txt_result.controls.append(
            ft.Text(f"Artista con somma pesi incidenti massima: {artistaPesiMax[0]} (somma:{artistaPesiMax[1]})")
        )
        top10archi = self._model.best10archi()
        self._view._txt_result.controls.append(
            ft.Text(f"Top 10 archi con peso maggiore:")
        )
        counter=1
        for e in top10archi:
            self._view._txt_result.controls.append(
                ft.Text(f"{counter}. {e[0]} -- {e[1]} (peso:{e[2]})")
            )
            counter+=1
        self._view.update_page()

    def handleSelezione(self,e):
        #controllo N num intero positivo
        if self._choiceArtista is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Selezionare un artista dal menu", color="red")
            )
            self._view.update_page()
            return
        txtN = self._view._txtInN.value
        try:
            intN = int(txtN)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Inserire un numero intero valido.", color="red")
            )
            self._view.update_page()
            return

        if intN < 0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Inserire un numero positivo.", color="red")
            )
            self._view.update_page()
            return
        pathArtisti, lenPath, bestCost = self._model.getPath(intN, self._choiceArtista)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Trovato cammino ottimo di lunghezza {lenPath} e num complessivo di brani uguale a {bestCost}. Di seguito i nodi che lo compongono: ",color="green")
        )
        for a in pathArtisti:
            self._view._txt_result.controls.append(
                ft.Text(f"{a[0]} -- brani: {a[1]} , playlist:{a[2]}")
            )

        self._view.update_page()