# coding: utf-8

'''
Script calculant des statistiques sur les différents types d'erreurs
repérés grâce à AliAdj.
'''


import os


def stats(dossier,fichier):
	
	fichier_entree = open(dossier+fichier,encoding="utf8",mode="r")
	next(fichier_entree)
	
	#types d'erreur possibles
	base = 0
	genre = 0
	nb = 0
	base_nb = 0
	base_genre = 0
	base_genre_nb = 0
	genre_nb = 0
	
	#totaux
	totalAdj = 0
	totalErr = 0
	normes = 0
	
	for ligne in fichier_entree:
		
		ligne = ligne.strip()
		infos = ligne.split("\t")
		
		#vérification que l'adjectif a bien pu être traité par AliAdj
		if len(infos) == 26 :
			
			totalAdj += 1
			
			#récup des infos sur les erreurs dans le fichier
			err_base = int(infos[23])
			err_genre = int(infos[24])
			err_nb = int(infos[25])
			
			#Comptage des erreurs en fonction de leur type
			
			if err_base == 1 and err_genre == 1 and err_nb == 1:
				base_genre_nb +=1
			elif err_base == 1 and err_genre == 1 :
				base_genre +=1
			elif err_base == 1 and err_nb == 1 :
				base_nb +=1
			
			if err_base == 1 :
				base += 1
			if err_genre == 1 :
				genre+=1
			if err_nb == 1 :
				nb += 1
			
			if err_genre == 1 or err_nb == 1 :
				genre_nb+=1
			
			#mots normés
			if err_base == 0 and err_genre == 0 and err_nb == 0:
				normes += 1
	
	total_base_genre_nb = base_genre+base_nb+base_genre_nb
	base_unique = base-total_base_genre_nb
	genre_nb_unique = genre_nb-total_base_genre_nb
	
	#Erreurs base, genre, nombre
	tx_err_base = round(base*100/totalAdj,2)
	tx_err_genre = round(genre*100/totalAdj,2)
	tx_err_nb = round(nb*100/totalAdj,2)
	
	#Erreurs Bases
	tx_err_total_base_genre_nb = round(total_base_genre_nb*100/totalAdj,2)
	tx_base_normee = 100-tx_err_base
	tx_err_base_unique = round(base_unique*100/totalAdj,2)
	
	#Erreurs genre_nbions
	tx_err_genre_nb = round(genre_nb*100/totalAdj,2)
	tx_genre_nb_normes = 100-tx_err_genre_nb
	tx_err_genre_nb_unique=round(genre_nb_unique*100/totalAdj,2)
	
	mots_normes=round(normes*100/totalAdj,2)
	
	#écriture des résultats
	err_base_genre_nombre = str(mots_normes)+"\t"+str(tx_err_base)+"\t"+str(tx_err_genre)+"\t"+str(tx_err_nb)+"\n"
	err_base_genre_nb = str(mots_normes)+"\t"+str(tx_err_base_unique)+"\t"+str(tx_err_total_base_genre_nb)+"\t"+str(tx_err_genre_nb_unique)+"\n"
	normes_base_genre_nb = str(tx_base_normee)+"\t"+str(tx_err_base)+"\t"+str(tx_genre_nb_normes)+"\t"+str(tx_err_genre_nb)+"\n"
	
	fichier_entree.close()
	
	infos_fichier=fichier.split(".")
	nom_fichier=infos_fichier[0]
	
	return(nom_fichier+"\t"+err_base_genre_nombre, nom_fichier+"\t"+err_base_genre_nb, nom_fichier+"\t"+normes_base_genre_nb,)

if __name__ == '__main__':
	
	dossier = "../AliAdj/resultats/"
	fichiers = os.listdir(dossier)
	
	fichier_sortie = open("stats_erreurs.csv", encoding="utf8", mode="w")
	fichier_sortie.write("Niveau\tMots normes\tErreurs bases\tErreurs flexions genre\tErreurs flexions nombre\n")
	
	#mots normésvs bases erronées vs genre_nb genre erronées vs genre_nb nb erronées
	err_base_genre_nombre = []
	#mots normés vs bases erronées vs base+genre_nbions erronées vs genre_nbons erronées
	err_base_genre_nb = []
	#bases normees vs bases erronées + genre_nbions normées vs genre_nbions erronées
	normes_base_genre_nb = []
	
	#calculs des comparaisons précédentes
	for fichier in fichiers:
		
		res1, res2, res3 = stats(dossier,fichier)
		
		err_base_genre_nombre.append(res1)
		err_base_genre_nb.append(res2)
		normes_base_genre_nb.append(res3)
	
	#ecriture des résultats
	for resultat in err_base_genre_nombre:
		fichier_sortie.write(resultat.replace(".",","))
	
	fichier_sortie.write("\nNiveau\tMots Normés\tErreurs bases\tErreurs bases + flexions\tErreurs flexions\n")
	
	for resultat in err_base_genre_nb:
		fichier_sortie.write(resultat.replace(".",","))
	
	fichier_sortie.write("\nNiveau\tBases normées\tErreurs bases\tflexions normées\tErreurs flexions\n")
	
	for resultat in normes_base_genre_nb:
		fichier_sortie.write(resultat.replace(".",","))
	
	fichier_sortie.close()

