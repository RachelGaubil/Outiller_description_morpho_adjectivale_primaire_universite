# coding: utf-8

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
		indication = mots[4]
		modeles[(lemme,indication)] = [base,genre,nb]
	fic_modeles.close()
	return(modeles)

def analyse_corpus(lexique, modeles, nom_fic):

	#parcours du fichier des productions
	fichier = open("../corpus/corpus_entier/adj/"+nom_fic+".csv",encoding="utf8",mode="r")
	
	fichier_sortie=open("resultats/"+nom_fic+".csv",encoding="utf8",mode="w")
	fichier_sortie.write(fichier.readline().strip()+"\tbaseAtt\tflexGenreAtt"+\
	"\tflexNbAtt\tbaseProd\tflexGenreProd\tflexNbProd\tErrBase\tErrFlexGenre"+\
	"\tErrFlexNb\n")
	
	rappErr = open("rapportErreur.txt",encoding="utf8",mode="a")
	
	for line in fichier :
		
		mot_ok = False
		line=line.strip()
		colonnes = line.split("\t")
		categorie = colonnes[7]
		
		#faire un cas particulier pour les erreurs de catégorisation ?
		resultat=""
		
		if categorie == "ADJ" :
			
			mot_ok = False
			mot_attendu = colonnes[8].lower()
			mot_produit = colonnes[9].lower()
			
			if mot_attendu == mot_produit :
				mot_ok = True
			
			lemme = colonnes[6].lower()
			statutSegm = colonnes[13]
			exceptions = ["02-HyperSeg","03-HypoSeg","05-Non pertinent","06-Omis"]
			
			mascSing = False
			
			#pour ne pas tester un pluriel sur "gros" si "grosse" attendu
			if mot_produit ==  lemme :
				mascSing = True
			
			#si le mot est correctement catégorisé comme adjectif et qu'il
			#n'est ni hyper-segmenté ni hypo-segmenté
			if lemme != "<unknown>" and statutSegm not in exceptions :
				
				#récupération du modèle que suit le mot
				if lemme in lexique.keys():
					modele=lexique[lemme]
					casParticulier=False
					
					#variables de vérification du type d'erreur
					base_ok=True
					genre_ok=True
					nombre_ok=True
					
					genre = colonnes[14]
					nombre = colonnes[15]
					
					#cas d'un invariable qui ne l'est pas forcément dans
					#le Lexique 383 (ex : "mal")
					if modele == "furax":
						genre = "_"
						nombre = "_"
						
					clef=(modele,genre+","+nombre)
					
					#cas particuliers
					if mot_attendu =="vieil" or mot_attendu == "fol" or mot_attendu=="nouvel" or mot_attendu=="bel":
						catParticulier =True
						base = mot_attendu
						marque_genre="_"
						marque_nb="_"
						if lemme=="vieux":
							clef=(modele,genre+",_")
					
					#remplissage du fichier d'erreurs avec les cas non traitables
					if clef not in modeles.keys():
						print(nom_fic,mot_attendu, mot_produit,lemme,clef)
						rappErr.write(line+"\n")
						fichier_sortie.write(line+"\n")
					else:
						
						comparaison = modeles[clef]
						
						#informations données par le modèle
						if casParticulier ==False:
							base = comparaison[0]
							marque_genre = comparaison[1]
							marque_nb = comparaison[2]
						
						#variables pour le découpage des mots
						base_prod=lemme
						genre_prod="_"
						nombre_prod="_"
						
						#on attend marque pluriel
						if nombre == "p":
							
							mot_attendu=mot_attendu[:-len(marque_nb)]
							
							#si le pluriel est marqué
							if mot_produit[-len(marque_nb):]==marque_nb:
								mot_produit=mot_produit[:-len(marque_nb)]
								nombre_prod=marque_nb
							
							else:
								nombre_ok=False
						
						#on attend du singulier
						#cherche si le mot porte la marque du pluriel
						elif (modele,genre+",p") in modeles.keys() and mascSing == False:
							
							comparaison2=modeles[(modele,genre+",p")]
							
							if mot_produit[-len(marque_genre):]==comparaison2[2]:
								nombre_ok=False
								nombre_prod=mot_produit[-len(marque_genre)]
								mot_produit=mot_produit[:-len(marque_genre)]
						
						#on attend marque féminin
						if genre == "f":
							
							mot_attendu=mot_attendu[:-len(marque_nb)]
							
							#s'il y a une marque
							if mot_produit[-len(marque_nb):]==marque_genre:
								mot_produit=mot_produit[:-len(marque_nb)]
								genre_prod=marque_genre
							else:
								genre_ok=False
						
						#on attend du masculin
						#cherche si le mot porte la marque du féminin
						elif (modele,"f,"+nombre) in modeles.keys():
							
							comparaison2=modeles[(modele,"f,"+nombre)]
							
							#marque trouvée, la suite de l'analyse se fait sur le même mot sans cette marque
							if mot_produit[-len(marque_nb):]==comparaison2[1]:
								genre_ok=False
								genre_prod=mot_produit[-len(marque_nb)]
								mot_produit=mot_produit[:-len(marque_nb)]
						
						if mot_attendu==mot_produit:
							base_ok=True
						else:
							base_ok=False
						
						#récupération du découpage des formes normées et produites
						res_attendu="\t"+mot_attendu+"\t"+marque_genre+"\t"+marque_nb
						res_produit="\t"+mot_produit+"\t"+genre_prod+"\t"+nombre_prod
						
						resultat+=res_attendu+res_produit
						
						#classification des erreurs s'il y en a
						if base_ok==False:
							resultat+="\t"+str(1)
						else:
							resultat+="\t"+str(0)
						if genre_ok==False:
							resultat+="\t"+str(1)
						else:
							resultat+="\t"+str(0)
						if nombre_ok==False:
							resultat+="\t"+str(1)
						else:
							resultat+="\t"+str(0)
						
						#écriture du résultat
						fichier_sortie.write(line+resultat+"\n")
				
				#cas d'un lemme non trouvé dans le lexique
				else:
					rappErr.write(line+"\n")
					fichier_sortie.write(line+"\n")
	
	rappErr.close()
	fichier_sortie.close()
	fichier.close()

if __name__ == '__main__':
	
	lexique = recup_lexique("lexique.txt")
	modeles = recup_modeles("modeles.txt")
	
	niveaux = ["CP","CE1","CE2","CM1","3eme","licence1"]
	
	for niveau in niveaux :
		analyse_corpus(lexique, modeles, niveau)
