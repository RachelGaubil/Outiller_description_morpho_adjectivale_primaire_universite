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
		variation = mots[2]
		genre = mots[3]
		nb = mots[4]
		indication = mots[5]
		modeles[(lemme,indication)] = [base,variation,genre,nb]
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
			
			mot_attendu = colonnes[8].lower()
			mot_produit = colonnes[9].lower()
			
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
					
					#a enlever !!!!!!!!!!!!!!
					if clef not in modeles.keys() and lemme=="vieux":
						clef=(modele,genre+",_")
					
					if clef not in modeles.keys():
						print(nom_fic,lemme,clef)
						rappErr.write(line+"\n")
						fichier_sortie.write(line+"\n")
					else:
						
						
						comparaison = modeles[clef]
						
						#informations données par le modèle
						base = comparaison[0]
						variation = comparaison[1]
						marque_genre = comparaison[2]
						marque_nb = comparaison[3]
						
						#variables intermédiaire modifiables (pour pouvoir découper les mots sans perdre de données)
						mot_compare = lemme
						mot_analyse = mot_produit
						
						#variables pour le découpage des mots
						decoupe_base=lemme
						decoupe_genre="_"
						decoupe_nombre="_"
						
						#on attend du pluriel
						if nombre == "p":
							
							#si le pluriel est marqué
							#cas d'une flexion contenant 2 caractères
							if mot_analyse[len(mot_analyse)-2:]==marque_nb:
								mot_analyse=mot_analyse[:-2]
								decoupe_nombre=marque_nb
							
							#marque trouvée, la suite de l'analyse se fait sur le même mot sans cette marque
							elif mot_analyse[len(mot_analyse)-1]==marque_nb:
								mot_analyse=mot_analyse[:-1]
								decoupe_nombre=marque_nb
							
							else:
								nombre_ok=False
						
						#on attend du singulier
						#cherche si le mot porte la marque du pluriel
						elif (modele,genre+",p") in modeles.keys() and mascSing == False:
							comparaison2=modeles[(modele,genre+",p")]
							
							#cas d'une flexion contenant 2 caractères
							if len(comparaison2[3])==2:
								if mot_analyse[len(mot_analyse)-2:]==comparaison2[3]:
									nombre_ok=False
									decoupe_nombre=mot_analyse[-2]
									mot_analyse=mot_analyse[:-2]
							
							#marque trouvée, la suite de l'analyse se fait sur le même mot sans cette marque
							elif mot_analyse[len(mot_analyse)-1]==comparaison2[3]:
								nombre_ok=False
								decoupe_nombre=mot_analyse[-1]
								mot_analyse=mot_analyse[:-1]
						
						#on attend du féminin
						if genre == "f":
							#s'il y a une marque
							if mot_analyse[len(mot_analyse)-1]==marque_genre:
								mot_analyse=mot_analyse[:-1]
								decoupe_genre=marque_genre
							else:
								genre_ok=False
						
						#on attend du masculin
						#cherche si le mot porte la marque du féminin
						elif (modele,"f,"+nombre) in modeles.keys():
							comparaison2=modeles[(modele,"f,"+nombre)]
							
							#marque trouvée, la suite de l'analyse se fait sur le même mot sans cette marque
							if mot_analyse[len(mot_analyse)-1]==comparaison2[2]:
								genre_ok=False
								decoupe_genre=mot_analyse[-1]
								mot_analyse=mot_analyse[:-1]
						
						
						#si la base ne varie pas
						if variation == "_":
							#le mot sans flexion doit être le même que le lemme
							if mot_analyse!=lemme:
								base_ok=False
								decoupe_base=mot_analyse
						
						#la base varie
						else:
							#parcours des variations à exécuter
							while variation != "":
								car=variation[0]
								#retirer le dernier caractère du lemme
								if car == "-":
									mot_compare=mot_compare[:-1]
								#dedoublement de la dernière lettre du lemme
								elif car == "+":
									mot_compare+=mot_compare[-1]
								elif car == ".":
									variation+=mot_compare[-1]
									mot_compare=mot_compare[:-2]
								#ou ajouter un caractère
								else:
									mot_compare+=car
								variation=variation[1:]
							
							#base modifiée précédemment doit correspondre à la base du mot
							if mot_analyse!=mot_compare:
								base_ok=False
							decoupe_base=mot_analyse
					
					
						#récupération du découpage des formes normées et produites
						res_attendu="\t"+mot_compare+"\t"+marque_genre+"\t"+marque_nb
						res_produit="\t"+decoupe_base+"\t"+decoupe_genre+"\t"+decoupe_nombre
						
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