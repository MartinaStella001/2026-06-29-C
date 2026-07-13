from model.model import Model

mdl = Model()
mdl.creaGrafo()
nodi, archi = mdl.getDettagliGrafo()
print(f"nodi: {nodi}, archi: {archi}")