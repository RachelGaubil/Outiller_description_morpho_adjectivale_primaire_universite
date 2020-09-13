# Outiller_description_morpho_adjectivale_primaire_universite

**TRAITEMENT GENERAL**

S'il y a de nouveaux fichiers à traiter :
  - Ajouter les nouveaux adjectifs s'il y en a et leur modèle de comportement flexionnel dans **AliAdj** > **modelisation** > *lexique.txt*
  - Ajouter les nouveaux fichiers (ou mettre à jour les anciens) dans **module_enrichissement** > **sorties_AliScol**
  - Lancer **module_enrichissement** > *module_enrichissement.py* (les résultats apparaîtront dans **module_enrichissement** > **corpus_enrichi**)
  - Remplacer le contenu de **corpus** par le contenu de **module_enrichissement** > **corpus_enrichi**

Si l'on veut des statistiques sur le corpus :
  - Relancer **statistiques** > *stats_corpus.py* (les résultats apparaîtront dans **statistiques** > *stats_corpus.csv*)

Si l'on veut effectuer le traitement des adjectifs (découpage + identification du type d'erreur)
  - Relancer **AliAdj** > *AliAdj.py* (les résultats apparaîtront dans **AliAdj** > **resultats**)

Si l'on veut des statistiques sur les erreurs :
  - Relancer **statistiques** > *stats_erreurs.py* (les résultats apparaîtront dans **statistiques** > *stats_erreurs.csv*)

**HIERARCHIE ET NOMINATION**

La hiérarchie et la nomination de certains documents est importante si l'on veut pouvoir lancer les scripts sans avoir à les modifier.
C'est pourquoi je vais les présenter ici. Les dossiers sont en gras et les fichiers en italique.

* **AliAdj**
  * *AliAdj.py*
  * *rapportErreurs.txt*
  * **modelisation** 
    * *lexique.txt*
    * *modeles.txt*
  * **resultats**
    * *CP.csv*
    * *CE1.csv*
    * ... 

* **corpus**
  * *CP.csv*
  * *CE1.csv*
  * ...
  * **adj**
    * *CP.csv*
    * *CE1.csv*
    * ...

* **guides**
  * *guide_de_transcription_v1.6.pdf*
  * *guide_normalisation_6mai2019.pdf*

* **module_enrichissement**
  * *module_enrichissement.py*
  * *Lexique383.tsv*
  * **sorties_AliScol**
    * *CP.csv*
    * *CE1.csv*
    * ...
  * **corpus_enrichi**
    * *CP.csv*
    * *CE1.csv*
    * ...

* **statistiques**
  * *stats_corpus.py*
  * *stats_corpus.csv*
  * *stats_erreurs.py*
  * *stats_erreurs.csv*
