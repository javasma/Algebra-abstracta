import groups as G

grupo = G.U(19)

potencia = G.power_set(grupo.elements)

subgrupos = G.Subgrupos(grupo)
print(G.superconjuntos(subgrupos[1],grupo))
indice = {i : subgrupos[i] for i in range(len(subgrupos))}
grafo = {i : G.superconjuntos(subgrupos[i],grupo) for i in range(len(subgrupos))}
print(indice)
print(grafo)