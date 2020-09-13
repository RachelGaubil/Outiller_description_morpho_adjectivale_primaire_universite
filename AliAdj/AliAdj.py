# coding: utf-8

'''
AliAdj est un module de traitement des adjectifs qui permet de découper
ces derniers en trois partie : base - flexion de genre - flexion de nombre.
Il fait se découpage à la fois sur la forme attendue (donc normée) et sur
la forme produite de l'adjectif.
Il compare au fur et à mesure ces découpage afin de pouvoir relever la
localisation de l'erreur sur l'adjectif s'il y en a une.

Pour cela il a besoin :
	des fichiers à traiter (.csv),
	d'un lexique (.txt),
	d'une liste de modèles de comportements flexionnels (.txt)

Il produit des fichiers (.csv) contenant les informations des fichiers à
traiter plus les découpages et les types d'erreur.
'''

import os



'''
But : extraire des fichiers à traiter les lignes décrivant les adjectifs
Entrée : fichier (.csv) à traiter
Sortie : fichier (.csv) ne contenant que les adjectifs et la ligne 
		 d'en-têtes du fichier à traiter
'''
def extraction_adj(fichier):
	
	chemin_adj = "../corpus/adj/"
	
	if not os.path.exists(chemin_adj):
		os.mkdir(chemin_adj)
	
	entree = open("../corpus/"+fichier,encoding="utf8",mode="r")
	sortie = open(chemin_adj+fichier,encoding="utf8",mode="w")
	
	#extraction + écriture de la ligne d'en-têtes
	sortie.write(entree.readline())
	
	for ligne in entree:
		elements = ligne.split("\t")
		#extraction + écriture des lignes contenant des adjectifs
		if elements[7]=="ADJ":
			sortie.write(ligne)
	
	sortie.close()
	entree.close()

'''
But : fonction qui récupère le contenu du lexique
Entrée : fichier lexique.txt
Sortie : dictionnaire associatif
		 clef (chaîne) = lemme
		 valeur (chaîne) = modèle de comportement
		 flexionnel correspondant au lemme
'''
def recup_lexique(nom_fic):
	
	#Extraction du lexique (lemme -> modèle)
	fic_lexique = open(nom_fic,encoding="utf8",mode="r")
	lexique = {}
	
	for ligne in fic_lexique :
		ligne=ligne.strip()
		mots = ligne.split("\t")
		lexique[mots[0]] = mots[1]
	
	fic_lexique.close()
	
	return(lexique)



'''
But : fonction qui récupère le contenu des modèles de comportements flexionnels
Entrée : fichier modeles.txt
Sortie : dictionnaire associatif :
		 clef (tuple de chaînes) = lemme, genre et nombre :
			format : ("lemme", "genre,nombre")
		 valeur (liste de chaînes) = base du mot, marques de genre et de nombre
			format : [base, marque_genre, marque_nb]
'''
def recup_modeles(nom_fic):
	
	#extraction des modèles (lemme -> base -> variation -> flex_genre -> flex_nb -> indication)
	fic_modeles = open(nom_fic,encoding="utf8",mode="r")
	modeles = {}
	
	for ligne in fic_modeles :
		ligne=ligne.strip()
		mots = ligne.split("\t")
		
		lemme = mots[0]
		base = mots[1]
		genre = mots[2]
		nb = mots[3]
		genre_nombre = mots[4]
		
		modeles[(lemme,genre_nombre)] = [base,genre,nb]
	
	fic_modeles.close()
	return(modeles)



'''
But : Fonction qui parcours un fichier d'adjectifs, qui en découpe les
	  formes attendue et produites en 3 (base, flexions de genre et de
	  nombre) et les compare entre elles pour trouver s'il y a des erreurs
	  et si oui, où.
Entrées : dictionnaire associatif contenant les infos du lexique
		  dictionnaire associatifs des modèles de comportements flexionnels
		  fichier à traiter (.csv)
Sortie : produit un fichier .csv du même format que le fichier d'entrée
		 avec 9 colonnes supplémentaires : les 3 premières sont le découpage
		 de la forme attendue, les 3 suivantes le découpage de la forme
		 produite et les 3 dernière sont les types d'erreurs présentes 
		 ou non (erreur base, flexion de genre et flexion de nombre
'''
def analyse_corpus(lexique, modeles, nom_fic):
	
	"""Préparation des fichiers d'entrée et de sortie"""
	
	#ouverture fichier des productions
	fichier = open("../corpus/adj/"+nom_fic,encoding="utf8",mode="r")
	
	#ouverture du fichier de résultats + écriture de la ligne des en-têtes
	fichier_sortie=open("resultats/"+nom_fic,encoding="utf8",mode="w")
	fichier_sortie.write(fichier.readline().strip()+"\tbaseAtt\tflexGenreAtt"+\
	"\tflexNbAtt\tbaseProd\tflexGenreProd\tflexNbProd\tErrBase\tErrFlexGenre"+\
	"\tErrFlexNb\n")
	
	"""Parcours du fichier"""
	
	for line in fichier :
		
		#extraction de la catégorie syntaxique de l'adjectif
		line = line.strip()
		colonnes = line.split("\t")
		categorie = colonnes[7]
		
		"""Vérification que le mot lu est un adjectif"""
		if categorie == "ADJ" :
			
			#variable servant à écrire le résultat
			resultat=""
			
			#extraction des formes attendue et produite, du lemme et du
			#statut de segmentation
			mot_attendu = colonnes[8].lower()
			mot_produit = colonnes[9].lower()
			lemme = colonnes[6].lower()
			statutSegm = colonnes[13]
			
			#vérification de si le mot est au masculin singulier pour ne
			#pas tester un pluriel sur des formes telles que "gros" si
			#"grosse" est attendue
			mascSing = False
			if mot_produit ==  lemme :
				mascSing = True
			
			"""Vérification que l'adjectif est traitable"""
			
			#vérification que le lemmme est connu et que le mot n'est ni
			#hypo-segmenté, hyper-segmenté, non pertinent ou omis
			if lemme != "<unknown>" and statutSegm == "01-Normé" :
				
				#le lemme du mot doit être présent dans le lexique
				if lemme in lexique.keys():
					
					"""Déclaration des variables utiles"""
					
					#modèle que le lemme suit
					modele = lexique[lemme]
					
					#variables de vérification du type d'erreur
					base_normee = True
					genre_norme = True
					nombre_norme = True
					
					#genre et nombre attendus
					genre = colonnes[14]
					nombre = colonnes[15]
					
					#cas d'un invariable qui ne l'est pas forcément dans
					#le Lexique 383 (ex : "mal") -> suit le modèle "furax"
					if modele == "furax":
						genre = "_"
						nombre = "_"
					
					#infos nécessaires pour trouver le modèle de découpage
					clef = (modele,genre+","+nombre)
					
					#cas particuliers (vieil, fol, nouvel et bel)
					cas_particulier = False
					if mot_attendu =="vieil" or mot_attendu == "fol" or mot_attendu=="nouvel" or mot_attendu=="bel":
						cas_particulier =True
						base = mot_attendu
						marque_genre = "_"
						marque_nb = "_"
						if lemme == "vieux":
							clef=(modele,genre+",_")
					
					
					"""Découpage de l'adjectif"""
					
					#remplissage du fichier d'erreurs avec les cas non
					#traitables et écriture de la ligne lue dans le
					#fichier des résultats
					if clef not in modeles.keys():
						rappErr.write(line+"\n")
						fichier_sortie.write(line+"\n")
					
					else:
						
						#récup des infos de découpage données par le modèle
						comparaison = modeles[clef]
						if cas_particulier == False:
							base = comparaison[0]
							marque_genre = comparaison[1]
							marque_nb = comparaison[2]
						
						#variables pour le découpage du mot produit
						base_prod = lemme
						genre_prod = "_"
						nombre_prod = "_"
						
						"""Comparaison de la flexion de nombre"""
						
						#marque du pluriel attendue
						if nombre == "p":
							
							#retrait de la marque de nombre de la forme attendue
							mot_attendu=mot_attendu[:-len(marque_nb)]
							
							#pluriel marqué : retrait de la marque de nombre
							#de la forme produite + stockage de cette marque
							if mot_produit[-len(marque_nb):]==marque_nb:
								mot_produit = mot_produit[:-len(marque_nb)]
								nombre_prod = marque_nb
							
							#sinon erreur sur le nombre
							else:
								nombre_norme=False
						
						#singulier attendu :
						#cherche si le mot porte quand même la marque du pluriel
						elif (modele,genre+",p") in modeles.keys() and mascSing == False:
							
							#récup des infos de découpage pour le mot
							#attendu mais sous sa forme au pluriel
							comparaison2=modeles[(modele,genre+",p")]
							
							#marque du pluriel présente => stockage de cette
							#marque et retrait sur la forme produite +
							#indiquer que le nombre est erroné
							if mot_produit[-len(marque_nb):] == comparaison2[2]:
								nombre_prod = mot_produit[-len(marque_nb)]
								mot_produit = mot_produit[:-len(marque_nb)]
								nombre_norme = False
						
						"""Comparaison de la flexion de genre"""
						
						#marque du féminin attendue
						if genre == "f":
							
							#retrait de la marque de genre de la forme attendue
							mot_attendu=mot_attendu[:-len(marque_nb)]
							
							#féminin marqué : retrait de la marque de genre
							#de la forme produite + stockage de cette marque
							if mot_produit[-len(marque_nb):] == marque_genre:
								mot_produit = mot_produit[:-len(marque_nb)]
								genre_prod = marque_genre
							
							#sinon erreur sur le genre
							else:
								genre_norme = False
						
						#masculin attendu
						#cherche si le mot porte quand même la marque du féminin
						elif (modele,"f,"+nombre) in modeles.keys():
							
							#récup des infos de découpage pour le mot
							#attendu mais sous sa forme au féminin
							comparaison2 = modeles[(modele,"f,"+nombre)]
							
							#marque du féminin présente => stockage de cette
							#marque et retrait sur la forme produite +
							#indiquer que le genre est erroné
							if mot_produit[-len(marque_genre):]==comparaison2[1]:
								genre_prod = mot_produit[-len(marque_genre)]
								mot_produit = mot_produit[:-len(marque_genre)]
								genre_norme = False
						
						"""Comparaison des bases"""
						
						#comparaison des bases des formes produite et attendue
						if mot_attendu == mot_produit:
							base_normee = True
						else:
							base_normee = False
						
						"""Constitution du résultat"""
						
						#récupération du découpage des formes attendue et produite
						res_attendu="\t"+mot_attendu+"\t"+marque_genre+"\t"+marque_nb
						res_produit="\t"+mot_produit+"\t"+genre_prod+"\t"+nombre_prod
						
						resultat+=res_attendu+res_produit
						
						#classification des erreurs s'il y en a
						if base_normee==False:
							resultat+="\t"+str(1)
						else:
							resultat+="\t"+str(0)
						if genre_norme==False:
							resultat+="\t"+str(1)
						else:
							resultat+="\t"+str(0)
						if nombre_norme==False:
							resultat+="\t"+str(1)
						else:
							resultat+="\t"+str(0)
						
						#écriture du résultat
						fichier_sortie.write(line+resultat+"\n")
				
				#cas d'un lemme non trouvé dans le lexique : on l'écrit
				#dans le fichier rapportant les erreurs et on écrit la
				#ligne du ficheir d'entrée telle quelle dans le fichier
				#de sortie
				else:
					rappErr.write(line+"\n")
					fichier_sortie.write(line+"\n")
	
	fichier_sortie.close()
	fichier.close()

'''
Main : Récupération dans le corpus des données nécessaires soient uniquement
	   les adjectifs de chaque niveau, le lexique et la liste de modèles.
	   Lancement du traitement des adjectifs.
'''
if __name__ == '__main__':
	
	lexique = recup_lexique("lexique.txt")
	modeles = recup_modeles("modeles.txt")
	
	#ouverture du fichier rapportant les possibles erreurs du système
	rappErr = open("rapportErreur.txt",encoding="utf8",mode="w")
	
	fichiers = os.listdir("../corpus/")
	if not os.path.exists("resultats"):
		os.mkdir("resultats")
	
	for fichier in fichiers :
		#vérification du format des fichiers
		if fichier[-4:] == ".csv":
			
			#création de fichiers contenant uniquement les adjectifs
			extraction_adj(fichier)
			#lancement du traitement des adjectifs sur ces fichiers
			analyse_corpus(lexique, modeles, fichier)
	
	rappErr.close()
