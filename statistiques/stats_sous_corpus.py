# coding: utf-8

import os

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
	tx_adj_diff = round(len(adjs)*100/nb_adj,2)
	
	return(nom_fichier+"\t"+niveau[0]+"\t"+str(len(ids_prods))+"\t"+str(nb_tok)+"\t"+str(nb_adj)+"\t"+str(tx_adj)+"%\t"+str(tx_adj_diff)+"%\n")

if __name__ == '__main__':
	
	resultat=""
	chemins = ["../corpus/corpus_entier","../corpus/corpus_travail","../corpus/corpus_reference"]
	
	for chemin in chemins :
		fichiers = os.listdir(chemin)
		
		for fichier in fichiers:
			if fichier[-4:]==".csv":
				resultat += nb_adj(chemin+"/"+fichier)
	
	fichier_resultat = open("stats_corpus.csv",encoding="utf8",mode="w")
	fichier_resultat.write("NomCorpus\tNiveau\tNbProd\tNbTok\tNbAdj\tTxAdj\nTxAdjDiff")
	fichier_resultat.write(resultat)
	fichier_resultat.close()
