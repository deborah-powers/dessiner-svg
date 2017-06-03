# dessiner_svg
Je voulais un script simple qui me permette de dessiner en svg, et de tracer des graphes

________________________________________________ dpowers svg ________________________________________________

dependances:
	le module sys de python
	le module dpowers_txt de deborah-powers

ce script peut etre appele dans d'autres scripts
vous pouvez egalement modifier un fichier svg

nettoyer le fichier, transformer les x='10.00001' en x='10'. simplifier la mise en forme
	python dpowers_svg.py fichier.svg n
decaler l'image
	python dpowers_svg.py fichier.svg t x y
	x,y sont les coordonnees selon lesquelles l'image doit etre deplacer. elles peuvent etre en float ou en int
changer la taille de l'image
	python dpowers_svg.py fichier.svg s x y
	x,y sont les facteur selon lesquelles l'image doit etre agrandie. elles peuvent etre en float ou en int


__________________ les classes d'objets svg simples __________________

un objet se caracterise par
	la position de son coin haut gauche, px et py
	sa largeur et sa hauteur, width et height
	sa nature: rect, circle...

obj
	base a partir de laquelle les autres objets seront construits
	organisation, fonctions communes a tous les objets svg
rect
circle
ellipse
line

__________________ les classes d'objets svg complexes __________________

text	contient un champ pour stoquer le texte
group
	base a partir de laquelle les autres objets conteneurs seront construits
	objet groupe, avec un champ pour stocquer la liste des objets contenus
svg



________________________________________________ dpowers graphe 1 ________________________________________________


dependances:
	le module sys de python
	le module dpowers_svg de deborah-powers
	le module dpowers_txt de deborah-powers

fonctionnement:
python dpowers_graphe.py fichier.svg list_pointsY (couleur, list_pointsX, mode)

arguments:
	fichier le fichier svg ou le graphe sera dessiner. s'il existe son ancien contenu sera detruit
	list_pointsY la liste des ordonnees des points du graphe a dessiner. exemple: (5,4,6,4), [5, 2, 3, 6]
	list_pointsX la liste des abcisses des points du graphe a dessiner
	couleur la couleur de la courbe, en code html
	mode le type de courbe a dessiner
		l, dessiner une ligne brisee
		b, dessiner des barres, un histogramme

ce script permet de dessiner des graphes, une seule courbe par graphe.
je trouvais matplotlib complexe, recherchais un script plus simple pour dessiner des graphes

il contient:

les variables globales pasx, pasy
	elles servent a definir le nombre de pixels entre deux unites du graphe, selon les axes x et y

la classe pattern
	j'utilise un pattern dans un dessin de graphe
	c'est la seule fois ou j'utilise un pattern, j'ai prefere mettre cette classe et non dans dpowers_svg

la classe graphe


 ________________________________________________ dpowers graphe ________________________________________________


dependances:
	le module sys de python
	le module dpowers_svg de deborah-powers
	le module dpowers_txt de deborah-powers

fonctionnement:
python dpowers_graphe.py fichier.svg list_pointsY (couleur, list_pointsX, mode)

arguments:
	fichier le fichier svg ou le graphe sera dessiner. s'il existe son ancien contenu sera detruit
	list_pointsY la liste des ordonnees des points du graphe a dessiner. exemple: (5,4,6,4), [5, 2, 3, 6]
	list_pointsX la liste des abcisses des points du graphe a dessiner
	couleur la couleur de la courbe, en code html
	mode le type de courbe a dessiner
		l, dessiner une ligne brisee
		b, dessiner des barres, un histogramme

ce script permet de dessiner des graphes contenant plusieurs courbes dans un meme cadre.
je trouvais matplotlib complexe, recherchais un script plus simple pour dessiner des graphes

il contient:

les variables globales pasx, pasy
	elles servent a definir le nombre de pixels entre deux unites du graphe, selon les axes x et y

la classe pattern
	j'utilise un pattern dans un dessin de graphe
	c'est la seule fois ou j'utilise un pattern, j'ai prefere mettre cette classe et non dans dpowers_svg

la classe courbe
	type
		ligne brisee
		histogramme
	couleur	code html
	liste de coordonnees x
	liste de coordonnees y

la classe graphe (derive de svg)
	nom
	nom des axes x et y
	nom des graduations
	dimension x et y
	fichier
