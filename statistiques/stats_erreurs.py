# coding: utf-8

import os


def stats(dossier,fichier):
	
	fichier_entree = open(dossier+fichier,encoding="utf8",mode="r")
	next(fichier_entree)
	
	base = 0
	genre = 0
	nb = 0
	baseNb = 0
	baseGenre = 0
	baseGenreNb = 0
	flex = 0
	
	totalAdj = 0
	totalErr = 0
	normes = 0
	
	for ligne in fichier_entree:
		ligne = ligne.strip()
		infos = ligne.split("\t")
		if len(infos) == 26 :
			totalAdj += 1
			errBase = int(infos[23])
			errFlexGenre = int(infos[24])
			errFlexNb = int(infos[25])
			
			if errBase == 1 and errFlexGenre == 1 and errFlexNb == 1:
				baseGenreNb +=1
			elif errBase == 1 and errFlexGenre == 1 :
				baseGenre +=1
			elif errBase == 1 and errFlexNb == 1 :
				baseNb +=1
			
			if errBase == 1 :
				base += 1
			if errFlexGenre == 1 :
				genre+=1
			if errFlexNb == 1 :
				nb += 1
			
			if errFlexGenre == 1 or errFlexNb == 1 :
				flex+=1
			
			if errBase == 0 and errFlexGenre == 0 and errFlexNb == 0:
				normes += 1
	
	baseFlex = baseGenre+baseNb+baseGenreNb
	baseUnique = base-baseFlex
	flexUnique = flex-baseFlex
	
	#Erreurs base, genre, nombre
	txErrBase=round(base*100/totalAdj,2)
	txErrGenre=round(genre*100/totalAdj,2)
	txErrNb=round(nb*100/totalAdj,2)
	
	#Erreurs Bases
	txErrBaseFlex=round(baseFlex*100/totalAdj,2)
	txNormeBase=100-txErrBase
	txErrBaseUnique=round(baseUnique*100/totalAdj,2)
	
	#Erreurs flexions
	txErrFlex=round(flex*100/totalAdj,2)
	txNormFlex=100-txErrFlex
	txErrFlexUnique=round(flexUnique*100/totalAdj,2)
	
	motsNormes=round(normes*100/totalAdj,2)
	
	err_base_genre_nombre = str(motsNormes)+"\t"+str(txErrBase)+"\t"+str(txErrGenre)+"\t"+str(txErrNb)+"\n"
	err_base_flex = str(motsNormes)+"\t"+str(txErrBaseUnique)+"\t"+str(txErrBaseFlex)+"\t"+str(txErrFlexUnique)+"\n"
	normes_base_flex = str(txNormeBase)+"\t"+str(txErrBase)+"\t"+str(txNormFlex)+"\t"+str(txErrFlex)+"\n"
	
	fichier_entree.close()
	
	infos_fichier=fichier.split(".")
	nom_fichier=infos_fichier[0]
	
	return(nom_fichier+"\t"+err_base_genre_nombre, nom_fichier+"\t"+err_base_flex, nom_fichier+"\t"+normes_base_flex,)

if __name__ == '__main__':
	
	dossier = "../module_decoupage/resultats/"
	fichiers = os.listdir(dossier)
	
	fichier_sortie = open("stats_erreurs.csv", encoding="utf8", mode="w")
	fichier_sortie.write("Niveau\tMots normes\tErreurs bases\tErreurs flexions genre\tErreurs flexions nombre\n")
	
	err_base_genre_nombre=[]
	err_base_flex=[]
	normes_base_flex=[]
	
	#calculs
	for fichier in fichiers:
		
		res1, res2, res3 = stats(dossier,fichier)
		
		err_base_genre_nombre.append(res1)
		err_base_flex.append(res2)
		normes_base_flex.append(res3)
	
	#ecriture
	for resultat in err_base_genre_nombre:
		fichier_sortie.write(resultat.replace(".",","))
	
	fichier_sortie.write("\nNiveau\tMots Normés\tErreurs bases\tErreurs bases + flexions\tErreurs flexions\n")
	
	for resultat in err_base_flex:
		fichier_sortie.write(resultat.replace(".",","))
	
	fichier_sortie.write("\nNiveau\tBases normées\tErreurs bases\tFlexions normées\tErreurs flexions\n")
	
	for resultat in normes_base_flex:
		fichier_sortie.write(resultat.replace(".",","))
	
	fichier_sortie.close()

