# coding: utf-8

'''
Ce script a pour but de calculer le nombre de productions, de tokens et 
d'adjectifs que contient le corpus, tout ceci en fonction du niveau scolaire.
'''

import os

'''
But : calcul de nombre de production de tokens et d'adjectifs de chaque
		niveau scolaire présent dans le corpus.*
Entrée : fichier (.csv) à traiter
Sortie : chaîne de caractère contenant le nombre de productions, de
		tokens, d'adjectifs et le pourcentage d'adjectifs du fichier traité.
'''
def nb_adj(fichier):
	
	fic = open(fichier, encoding="utf8", mode="r")
	next(fic)
	
	ids_prods = {}
	ids_toks = []
	adjs = {}
	a=0
	for ligne in fic :
		a+=1
		if ligne != "\n" and ligne !="": #pas les lignes vides
			elements = ligne.split("\t")
			
			id_prod = elements[0]
			if id_prod not in ids_prods:
				ids_prods[id_prod]=1
				
			id_tok = elements[5]
			tok = elements[6]
			cat = elements[7]
			adj = elements[8]
			if tok != "" and str(tok)[0] != "<" and str(tok)[0] != ">" or tok =="<unknown>": #chiffres possibles comme tokens
				ids_toks.append([id_tok,cat,tok])
	
	fic.close()
	
	#vérification des identifiants attendus et comptage
	nb_tok = 1
	nb_adj = 0
	
	if len(ids_toks)>1 and ids_toks[0][1] == "ADJ" :
		nb_adj += 1
		adjs[ids_toks[0][2]]=1
	i = 1
	while i < len(ids_toks):
		id_precedent = ids_toks[i-1][0]
		if ids_toks[i][0] != id_precedent :
			nb_tok += 1
		if ids_toks[i][1] == "ADJ" :
			nb_adj += 1
			if ids_toks[i][2] not in adjs.keys():
				adjs[ids_toks[i][2]]=1
			else:
				adjs[ids_toks[i][2]]+=1
		i += 1
	
	infos_fichier = fichier.split("/")
	nom_fichier = infos_fichier[2]
	niveau = infos_fichier[3].split(".")
	
	tx_adj = round(nb_adj*100/nb_tok,2)
	
	return(niveau[0]+"\t"+str(len(ids_prods))+"\t"+str(nb_tok)+"\t"+str(nb_adj)+"\t"+str(tx_adj)+"%\n")

'''
Main : Récupération de tous les fichiers du corpus, lancement de nb_adj
		sur chacun d'entre eux puis récupération des chiffres donnés par
		cette fonction et mise en forme des résultats dans un fichier
		nommé "stats_corpus.csv"
'''
if __name__ == '__main__':
	
	resultat = ""
	chemin = "../corpus/"
	fichiers = os.listdir(chemin)
	
	#calculs
	for fichier in fichiers:
		if fichier[-4:]==".csv":
			resultat += nb_adj(chemin+"/"+fichier)
	
	#écriture des résultats
	fichier_resultat = open("stats_corpus.csv",encoding="utf8",mode="w")
	fichier_resultat.write("Niveau\tNbProd\tNbTok\tNbAdj\tTxAdj\n")
	fichier_resultat.write(resultat)
	fichier_resultat.close()
