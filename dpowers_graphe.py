#!/usr/bin/python2.6
# modules python
from sys import argv
# modules dpowers
import dpowers_svg as dsvg
import dpowers_txt as txt

help ="""
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
"""


pasx =30.0
pasy =20.0
taille_texte = min (pasx, pasy)

class pattern (dsvg.group):
	""" j'utilise un pattern dans un dessin de graphe
	c'est la seule fois ou j'utilise un pattern, j'ai prefere mettre cette classe et non dans dpowers_svg
	"""
	def __init__(self):
		dsvg.group.__init__(self)
		self.nature = 'pattern'

	def to_str (self):
		""" action: ecrire un pattern
		retourne: un texte correspondant au pattern
		"""
#		ecrire les formes
		list_shapes = dsvg.group.to_str (self)
#		modification propres aux pattern
		list_shapes = '<defs>'+ list_shapes +'</defs>'
		chn = " width='%s' height='%s' x='%s' y='%s' patternUnits='userSpaceOnUse'" % (
			txt.float_to_str (self.width),
			txt.float_to_str (self.height),
			txt.float_to_str (self.px),
			txt.float_to_str (self.py))
#		placer list shapes apres les eventuels id et class
		d= list_shapes.find ('pattern')
		d= list_shapes.find ('>',d)
		list_shapes = list_shapes[:d] +chn+ list_shapes[d:]
		return list_shapes

class courbe():
	""" type
		c ligne brisee
		b histogramme
	couleur	code html
	liste de coordonnees x
	liste de coordonnees y
	forme, polyline ou groupe de rectangles """
	def __init__ (self):
		self.type = 'c'
		self.couleur = 'red'
		self.ptx =[]
		self.pty =[]
		self.objet = dsvg.poly()
		self.id = 'courbe'

	def to_obj (self):
		""" action: dessiner l'objet svg auquel la courbe correspond """
#		si ptx est vide, creer un range
		if not self.ptx: self.ptx = range (len (self.pty))
# ?		retrouver les limites des points de la figure
		xmin = min (self.ptx)
		xmax = max (self.ptx)
		ymin = min (self.pty)
		ymax = max (self.pty)
#		creer une ligne brisee, un polyline
		if self.type =='c':
			self.objet = dsvg.poly()
			self.objet.ptx.extend (self.ptx)
			self.objet.pty.extend (self.pty)
			self.objet.autre = "style='stroke:%s'" % self.couleur
			self.objet.nature = 'polyline'
			self.objet.normalisation()
#		creer un histogramme
		elif self.type =='b':
			self.objet = dsvg.group()
#			largeur des colonnes
			rptx= range (2, len (self.ptx))
			lcol = float (self.ptx[1]) - self.ptx[0]
			for i in rptx:
				n= self.ptx[i] - self.ptx [i-1]
				if n< lcol: lcol =n
			if lcol >1: lcol =1	# largeur max=1
#			dessiner les colonnes
			range_pt = range (len (self.ptx))
			for i in range_pt:
				self.objet.rectangle (self.ptx[i], 0, lcol, self.pty[i])
				self.objet.lst[-1].autre = "style='fill:%s'" % self.couleur
#		parametres de la figure
		if xmin <0: xmin =0
		if ymin <0: ymin =0
		self.objet.px = xmin
		self.objet.py = ymin
		self.objet.width =xmax -xmin
		self.objet.height =ymax -ymin
		self.objet.id = self.id

class graphe (dsvg.svg):
	""" nom
	nom des axes x et y
	nom des graduations
	dimension x et y
	fichier """

	def __init__ (self, file=None):
		dsvg.svg.__init__(self, file)
#		titre, nom des axes
		self.namex =""
		self.namey =""
#		style des graphes
		self.style ="""* {
	fill: none;
	stroke: black;
	stroke-width: 2;
	}
text {
	fill: black;
	stroke: none;
	font-size: %.0fpx;
	text-anchor: middle;
	}
text.titre { font-size: %.0fpx; }
rect.fond { fill: url(#dent); }
pattern line { stroke: lightgrey; }""" %( 0.6* taille_texte, taille_texte)

	def ajouter (self, courbe):
		""" action: ajouter la forme """
		self.lst.append (courbe.objet)
#		les limites du graphe
		self.width = max (self.px + self.width, courbe.objet.px + courbe.objet.width)
		self.height = max (self.py + self.height, courbe.objet.py + courbe.objet.height)
		if self.px > courbe.objet.px: self.px = courbe.objet.px
		if self.py > courbe.objet.py: self.py = courbe.objet.py
		self.width -= self.px
		self.height -= self.py

	def dessiner (self):
		""" action: dessine un graphe y= f(x) au format svg """
#		preparer les graduations des axes
		width = int (self.width) +2
		rangeX = range (width)
		graduationX =[]
		for i in rangeX: graduationX.append (str (i))
		height = int (self.height) +2
		rangeY = range (height)
		graduationY =[]
		for i in rangeY: graduationY.append (str(i))
		self.scale (pasx, pasy)
		self.translate (taille_texte, taille_texte)
		self.width = pasx*max (rangeX) +pasx
		self.height = pasy*max (rangeY) +pasy
# 1)		pattern, dessiner les graduations
		self.lst.append (pattern())
		self.lst[-1].width =pasx
		self.lst[-1].height =pasy
		self.lst[-1].px= taille_texte
		self.lst[-1].py= taille_texte
		self.lst[-1].ligne (pasx, 0,0,0)
		self.lst[-1].ligne (0, pasy, 0,0)
		self.lst[-1].id= 'dent'
# 2)		dessiner un rectangle encadrant le graphe
		width -=1 ; height -=1
		self.rectangle (taille_texte, taille_texte, width*pasx, height*pasy)
		self.lst[-1].classe ='fond'
# 3)		dessiner l'abcisse
		self.lst.append (dsvg.group())
		self.lst[-1].id = 'graduationX'
		py= 0.6* taille_texte
		for i in rangeX:
			px= taille_texte +i* pasx
			self.lst[-1].texte (px, py, graduationX[i])
# 4)		dessiner l'ordonnee
		self.lst.append (dsvg.group())
		self.lst[-1].id = 'graduationY'
		px= 0.5* taille_texte
		for i in rangeY:
			py= taille_texte +i* pasy
			self.lst[-1].texte (px, py, graduationY[i])
# 5)		nom de l'abcisse
		if self.namex:
#			decaler le graphe afin de faire une place pour le titre. on ne touche pas au pattern
			for shape in self.lst:
				if shape.nature == 'pattern': shape.py +=taille_texte
				else: shape.translate (0, taille_texte)
			px= self.width /2.0
			py= taille_texte -0.2*pasx
			self.height += taille_texte
			self.texte (px,py, self.namex)
			self.lst[-1].classe ='titre'
			self.lst[-1].id ='axeX'
# 6)		titre
		if self.id:
#			decaler le graphe afin de faire une place pour le titre. on ne touche pas au pattern
			for shape in self.lst:
				if shape.nature == 'pattern': shape.py +=taille_texte
				else: shape.translate (0, taille_texte)
			px= self.width /2.0
			py= taille_texte -0.2*pasx
			self.height += taille_texte
			self.texte (px,py, self.id)
			self.lst[-1].classe ='titre'
			self.lst[-1].id ='titre'
# 7)		nom de l'ordonnee
		if self.namey:
#			decaler le graphe afin de faire une place pour le titre. on ne touche pas au pattern
			for shape in self.lst:
				if shape.nature == 'pattern': shape.px +=taille_texte
				else: shape.translate (taille_texte, 0)
			px= taille_texte *0.8
			py= self.height /2
			self.width += taille_texte
			self.texte (px,py, self.namey)
			self.lst[-1].classe ='titre'
			self.lst[-1].id ='axeY'
#			faire retourner le nom de l'ordonnee
			self.lst[-1].autre ="transform='rotate(270,%.1f,%.1f)'" %( self.lst[-1].px, self.lst[-1].py)
		self.to_file()



""" ____________________________________ les actions ____________________________________ """



# si ce script est appeler dans un autre fichier
if argv[0] != 'dpowers_graphe.py': pass
# si l'utilisateur a entrer une commande inconnue
elif len (argv) <3: print help
else:
#	variables
	gph = graphe()
	gph.file = argv[1]
	crb = courbe()
	crb.couleur = 'red'
	if len (argv) >3: crb.couleur = argv[3]
	crb.type = 'l'
	if len (argv) >5: crb.type = argv[5]
#	recuperer les points de la liste Y
	str_points = argv[2].strip ('[]()')
	str_points = str_points.replace (', ',',')
	list_points = str_points.split (',')
	rang = range (len (list_points))
	for i in rang: crb.pty.append (float (list_points[i]))
#	recuperer les points de la liste X
	if len (argv) >4:
		str_points = argv[4].strip ('[]()')
		str_points = str_points.replace (', ',',')
		list_points = str_points.split (',')
		rang = range (len (list_points))
		for i in rang: crb.ptx.append (float (list_points[i]))
#	appeler la fonction de creation de graphe
	crb.to_obj()
	gph.ajouter (crb)
	gph.dessiner()



