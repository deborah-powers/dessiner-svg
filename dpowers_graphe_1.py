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

ce script permet de dessiner des graphes, une seule courbe par graphe.
je trouvais matplotlib complexe, recherchais un script plus simple pour dessiner des graphes

il contient:

les variables globales pasx, pasy
	elles servent a definir le nombre de pixels entre deux unites du graphe, selon les axes x et y

la classe pattern
	j'utilise un pattern dans un dessin de graphe
	c'est la seule fois ou j'utilise un pattern, j'ai prefere mettre cette classe et non dans dpowers_svg

la classe graphe


"""


pasx =80.0
pasy =40.0
TailleTexte = min (pasx, pasy)

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

class graphe (dsvg.svg):
	def __init__ (self, file=None):
		dsvg.svg.__init__(self, file)
#		titre, nom des axes
		self.title =""
		self.namex =""
		self.namey =""
#		labels des graduations
		self.idx =[]
		self.idy =[]
#		liste des corrdonnees x,y
		self.ptx =[]
		self.pty =[]
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
polyline { stroke: #000000; }
rect { fill: #000000; }
rect.fond { fill: url(#dent); }
pattern line { stroke: lightgrey; }""" %( 0.6* TailleTexte, TailleTexte)

	def dessiner (self, couleur='red', mode='l'):
		""" action: dessine un graphe y= f(x) au format svg.
		le dessin comprend:
			le titre
			le nom des axes
			la numerotation des graduations des axes x et y
			un rectangle de fond
			une courbe ou un histogramme
		cette fonction ne peut tracer qu'une courbe par graphe
		arguments:
			mode la forme sous laquelle la courbe doit etre representee
				b un histogramme
				l une ligne brisee
			sa couleur
		"""
#		si ptx n'a pas ete indique, creer un range de la longueur de pty
		if not self.ptx: self.ptx = range (1, len (self.pty) +1)
# 1)		pattern, dessiner les graduations
		self.lst.append (pattern())
		self.lst[-1].width =pasx
		self.lst[-1].height =pasy
		self.lst[-1].ligne (pasx, 0,0,0)
		self.lst[-1].ligne (0, pasy, 0,0)
		self.lst[-1].id= 'dent'
#		preparer les idx, graduations des axes
		xmax = int (max (self.ptx))
		ymax = int (max (self.pty))
		xmax +=1 ; ymax +=1
# 2)		dessiner un rectangle encadrant le graphe
		xmax *= pasx ; ymax *= pasy
		self.rectangle (TailleTexte, TailleTexte, xmax, ymax)
		self.lst[-1].classe ='fond'
# 3)		dessiner l'abcisse
		if not self.idx:		# si aucun nom (idx) n'a ete indique
			rang = range (int (xmax /pasx) +1)
			for i in rang: self.idx.append (str (rang[i]))
		self.lst.append (dsvg.group())
		py= TailleTexte -0.2*pasx
		rang = range (len (self.idx))
		for i in rang:
			px= (i)* pasx + TailleTexte
			self.lst[-1].texte (px, py, self.idx[i])
		self.lst[-1].id = 'graduationX'
# 3)		dessiner l'ordonnee
		if not self.idy:		# si aucun nom (idy) n'a ete indique
			rang = range (int (ymax /pasy) +1)
			for i in rang: self.idy.append (str (rang[i]))
		self.lst.append (dsvg.group())
		px= TailleTexte /2.0
		rang = range (len (self.idy))
		for i in rang:
			py= (i+1)* pasy
			self.lst[-1].texte (px, py, self.idy[i])
		self.lst[-1].id = 'graduationY'
#		limites de la figure
		xmin = float (min (self.ptx))
		xmax = float (max (self.ptx)) -xmin
		ymin = float (min (self.pty))
		ymax = float (max (self.pty)) -ymin
# 4)		dessiner le graphe
# 4a)		transformer les points en polyline
		if mode =='l':
			"""
			la fonction de dessin de polygone considere que les points sont dans l'intervalle (0,1).
			je dois convertir mes listes de coordonnees de facon a ce qu'elles rentrent dans cet intervalle
			"""
			rang = range (len (self.ptx))
			for i in rang:
				self.ptx[i] -= xmin
				self.ptx[i] /= xmax
			rang = range (len (self.pty))
			for i in rang:
				self.pty[i] -= ymin
				self.pty[i] /= ymax
#			creer le polyline
			px = xmin * pasx + TailleTexte
			py = ymin * pasy + TailleTexte
			width = xmax * pasx
			height = ymax * pasy
			self.polyligne (px,py, width, height, self.ptx, self.pty)
			self.lst[-1].id = 'info'
# 4b)		transformer les points en barres
		elif mode =='b':
#			largeur des colonnes
			rptx= range (2, len (self.ptx))
			lcol = self.ptx[1] - self.ptx[0]
			for i in rptx:
				n= self.ptx[i] - self.ptx [i-1]
				if n< lcol: lcol =n
			lcol *= pasx
			if lcol > pasx: lcol = pasx	# largeur max = pasx
#			dessiner les colonnes
			self.lst.append (dsvg.group())
			range_pt = range (len (self.ptx))
			for i in range_pt:
				px= self.ptx[i] *pasx -0.5*pasx + TailleTexte
				py= self.pty[i] *pasy
				self.lst[-1].rectangle (px, TailleTexte, lcol, py)
			self.lst[-1].id = 'info'
# 4c)		mode non reconnu
		else:
			print 'mode non reconnu', mode
			print 'modes reconnus:\n\tl- tracer une ligne\n\tb- tracer un histogramme'
			return
# 5)		nom de l'abcisse
		if self.namex:
#			decaler le graphe afin de faire une place pour le titre. on ne touche pas au pattern
			for shape in self.lst[1:]: shape.translate (0, TailleTexte)
			px= xmin + xmax /2.0
			px*= pasx
			px+= TailleTexte
			py= TailleTexte -0.2*pasx
			self.texte (px,py, self.namex)
			self.lst[-1].classe ='titre'
			self.lst[-1].id ='axeX'
# 6)		titre
		if self.title:
# 7)			decaler le graphe afin de faire une place pour le titre. on ne touche pas au pattern
			for shape in self.lst[1:]: shape.translate (0, TailleTexte)
			px= xmin + xmax /2.0
			px*= pasx
			px+= TailleTexte
			py= TailleTexte -0.2*pasx
			self.texte (px,py, self.title)
			self.lst[-1].classe ='titre'
			self.lst[-1].id ='titre'
# 8)		nom de l'ordonnee
		if self.namey:
#			decaler le graphe afin de faire une place pour le titre. on ne touche pas au pattern
			for shape in self.lst[1:]: shape.translate (TailleTexte, 0)
			px= TailleTexte *0.8
			py= ymin + ymax /2.0
			py*= pasy
			py+= TailleTexte
			self.texte (px,py, self.namey)
			self.lst[-1].classe ='titre'
			self.lst[-1].id ='axeY'
#			faire retourner le nom de l'ordonnee
			self.lst[-1].autre ="transform='rotate(270,%.1f,%.1f)'" %( self.lst[-1].px, self.lst[-1].py)
# 9)		tous dessiner
#		couleur du graphe
		self.style = self.style.replace ('#000000', couleur)
#		dimensions du graphe
		self.width = len (self.idx) *pasx + 2* TailleTexte
		self.height = len (self.idy) *pasy + 3* TailleTexte
		self.to_file()



""" ____________________________________ les actions ____________________________________ """




# si ce script est appeler dans un autre fichier
if argv[0] != 'dpowers_graphe_1.py': pass
# si l'utilisateur a entrer une commande inconnue
elif len (argv) <3: print help
else:
#	variables
	gph = graphe()
	gph.file = argv[1]
	couleur = 'red'
	if len (argv) >3: couleur = argv[3]
	mode = 'l'
	if len (argv) >5: mode = argv[5]
#	recuperer les points de la liste Y
	str_points = argv[2].strip ('[]()')
	str_points = str_points.replace (', ',',')
	list_points = str_points.split (',')
	rang = range (len (list_points))
	for i in rang: gph.pty.append (float (list_points[i]))
#	recuperer les points de la liste X
	if len (argv) >4:
		str_points = argv[4].strip ('[]()')
		str_points = str_points.replace (', ',',')
		list_points = str_points.split (',')
		rang = range (len (list_points))
		for i in rang: gph.ptx.append (float (list_points[i]))
#	appeler la fonction de creation de graphe
	gph.dessiner (couleur, mode)



