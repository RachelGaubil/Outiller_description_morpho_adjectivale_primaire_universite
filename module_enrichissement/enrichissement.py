# coding: utf-8


'''
Ce script a pour but de compléter les sorties de l'aligneur avec les
informations de genre et de nombre des mots ainsi qu'avec la catégorie
nommée "infover" pour les verbes et qui contient les informations de mode,
de temps et de personne.
'''


import os
import shelve


'''
Extraction des données qui nous intéressent dans le lexique 383 :
le mot, son lemme, sa catégorie, son genre, son nombre et son infover

Si relancement de cette fonction, bien penser à supprimer le dossier
"donnees_temporaires" avant
'''
def extract_lexique():
	
	lexique_complet = open("entrees/Lexique383.tsv", encoding="UTF8", mode="r")
	next(lexique_complet)
	
	if not os.path.exists("entrees/donnees_temporaires"):
		os.mkdir("entrees/donnees_temporaires")
	
	#Création d'un dico associatif (shelve) pour stocker les données
	#clef : "mot cat", valeur : "lemme genre nombre infover"
	with shelve.open("entrees/donnees_temporaires/lexique.dat") as lexique :
		
		i=0
		
		for ligne in lexique_complet :
			
			#indicateur exécution code
			i+=1
			if i%1000==0:
				print(str(i)+"/"+str(142000))
			
			cols=ligne.split("\t")
			nouv_ligne=""
			lemme=cols[2]
			cat=cols[3]
			
			#normalisation des catégories
			if cat[:3]=="ART" or cat[-3:]=="pos" :
				mot_cat = cols[0]+" DET"
			elif cat[-3:]=="dem":
				mot_cat = cols[0]+" PRO"
			elif cat!="ADJ:num" :
				mot_cat=cols[0]+" "+cat[:3]
			
			#ajout du genre
			if len(cols[4])==0:
				nouv_ligne+="_\t"
			else :
				nouv_ligne+=cols[4]+"\t"
			
			#ajout du nombre
			if len(cols[5])==0:
				nouv_ligne+="_\t"
			else :
				nouv_ligne+=cols[5]+"\t"
			
			#ajout du temps des verbes
			if len(cols[10])==0:
				nouv_ligne+="_"
			else :
				nouv_ligne+=cols[10]
			
			lexique[mot_cat]=lemme+"\t"+nouv_ligne
	
	lexique_complet.close()

 
'''
But : fonction qui recherche dans le lexique les informations (si existantes)
      genre, nombre et infover d'un mot donné associé à une catégorie donnée
Entrées : le mot (chaîne), sa catégorie (chaîne) et le lexique (shelve)
Sortie : genre, nombre et infover (dans une seule chaîne avec tabulation
         comme séparateur)
'''
def recherche_infos(mot, cat, lexique):
	
	clef=mot+" "+cat
	clef_min=mot.lower()+" "+cat
	
	if clef in lexique.keys():
		return lexique[clef]
	elif clef_min in lexique.keys():
		return lexique[clef_min]
	else:
		return ""

'''
But : fonction qui  complète les sorties de l'aligneur en y ajoutant les
      informations (si existantes) genre, nombre et infover aux mots.
      Pour cela elle part des sorties de l'aligneur (.csv) et recompose 
      le corpus dans un autre dossier (corpus_enrichis)
Entrée : nom du fichier à compléter (chaîne)
'''
def ajout_infos(nom_fic):
	
	entree = open("entrees/sorties_aligneur/"+nom_fic, encoding="UTF8", mode="r")
	sortie = open("corpus_enrichi/"+nom_fic, encoding="UTF8", mode="w")
	
	#ligne d'en-têtes
	sortie.write(entree.readline().strip()+"\tGenre\tNombre\tInfover\n")
	
	
	with shelve.open("entrees/donnees_temporaires/lexique.dat") as lexique :
		
		for ligne in entree :
			
			lemme_modif=False
			
			ligne=ligne.strip()
			
			if ligne!="" and ligne != "\n":
				
				donnees=ligne.split("\t")
				
				lemme=donnees[6]
				mot=donnees[8]
				id_tok_norme=donnees[5]
				cat=donnees[7][:3]
				
				#pour un adjectif si on a deux lemmes pour un seul mot
				#on choisit le masculin (ex : "favori|favorite")
				if cat == "ADJ" and "|" in lemme:
					lemme_modif = True
					lemmes = lemme.split("|")
					
					#les deux lemmes entre lesquels on doit choisir
					lemme1, lemme2 = lemmes[0], lemmes[1]
					
					res_lemme1 = recherche_infos(lemme1,cat,lexique)
					res_lemme2 = recherche_infos(lemme2,cat,lexique)
					infos = res_lemme1.split("\t")
					
					#récupération du lemme qui est au masculin
					if infos[1]=="m":
						lemme=lemme1
					else:
						lemme=lemme2
				
				#recherche des infos voulues
				resultat = recherche_infos(mot,cat,lexique)
				
				#Si la recherche des infos échoue on ré-essaye avec le
				#même mot en tant que verbe (ex : cas d'un participe passé)
				#si l'erreur se reproduit on cherche le mot en tant que
				#nom (ex : "mécanicien")
				if resultat =="" and cat=="ADJ":
					resultat = recherche_infos(mot,"VER",lexique)
					infos = resultat.split("\t")
					if len(infos)>2:
						infover = infos[3]
						#si le mot trouvé n'est pas participe (passé ou
						#présent) alors ce n'est pas le bon
						if infover[:3]!="par":
							resultat = ""
					if resultat=="":
						resultat = recherche_infos(mot,"NOM",lexique)
				
				
				infosResultat = resultat.split("\t")
				
				
				if resultat != "":
					genre = infosResultat[1]
					lemmeLexique=infosResultat[0]
					
					#si le lemme est au féminin (pluriel ou singulier)
					#on le modifie et prend le masculin
					if cat == "ADJ" and genre == "f":
						if mot == lemme: 
							lemme_modif = True
							lemme=lemmeLexique
						elif mot == lemme+"s": 
							lemme_modif = True
							lemme=lemmeLexique
				
				
				#si le mot ne correspond pas au lemme indiqué : cas d'un
				#mot composé morcelé en plusieurs(ex : "soi-disant" :
				#"soi", "-" et "disant" alors #on fait la recherche avec
				#le lemme du lexique et non le mot
				if cat == "ADJ" and infosResultat[0] != lemme and lemme!="<unknown>":
					if "-" in lemme:
						resultat = recherche_infos(lemme,"ADJ",lexique)
				
				infosResultat = resultat.split("\t")
				
				
				#si on a modifié le lemme alors la ligne originelle de la 
				#sortie doit être modifiée
				if lemme_modif:
					sortie.write("\t".join(donnees[0:6])+"\t"+lemme+"\t"+"\t".join(donnees[7:]))
				else:
					sortie.write(ligne)
				
				#ajout des données genre, nombre et infover
				if resultat=="":
					sortie.write("\t_\t_\t_\n")
				else:
					sortie.write("\t"+"\t".join(infosResultat[1:])+"\n")
	
	entree.close()
	sortie.close()
	
	#indicateur execution code
	print(nom_fic+" traité")




if __name__ == '__main__':
	
	'''Décommenter la ligne ci-dessous s'il y a eu modification manuelle
	de "Lexique383.tsv" + supprimer le dossier "donnees_temporaires"
	s'il existe avant de lancer cette fonction'''
	extract_lexique()
	
	if not os.path.exists("corpus_enrichi"):
		os.mkdir("corpus_enrichi")
	
	sorties_aligneur = os.listdir("entrees/sorties_aligneur")
	
	for fichier in sorties_aligneur:
		ajout_infos(fichier)
