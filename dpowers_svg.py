#!/usr/bin/python2.6
# modules python
from sys import argv
# modules dpowers
import dpowers_txt as txt


help ="""
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
"""



""" ____________________________________ fonctions hors classes ____________________________________ """

def extraire (objet, attribut):
	""" action: extraire la valeur d'un attribut
	arguments:
		l'objet svg, sous forme de texte "<rect x='20' y='5' width='60' height='30'/>"
		l'attribut, "width"
	retourne: la valeur de l'attribut, 60. si l'attribut correspond a un nombre, il est converti en float
	"""
#	attributs a ne pas transformer en float
	str_attributes = ('class', 'id', 'style', 'fill', 'stroke', 'points', 'd', 'viewBox')
#	l'attribut n'est pas ds la chaine
	if attribut +"='" not in objet and attribut in str_attributes: return ""
#	l'attribut n'est pas ds la chaine, il devait contenir un nb
	elif attribut +"='" not in objet: return 0.0
#	position du debut de la valeur de l'attribut
	d= objet.find (attribut +"='") + len (attribut) +2
#	position de la fin
	f= objet.find ("'", d)
#	extraire la valeur
	contenu = objet[d:f]
#	attribut numerique
	if attribut not in str_attributes: contenu = float (contenu)
	return contenu


""" ____________________________________ les classes d'objets svg simples ____________________________________ """

class obj():
	""" organisation, fonctions communes a tous les objets svg """
	def __init__ (self):
		self.width =0
		self.height =0
		self.px =0
		self.py =0
		self.nature =""
#		id et classe
		self.id =""
		self.classe =""
		self.autre =""

	def afficher (self):
		""" action: afficher l'objet en indiquant ses caracteristiques simples """
		print '--- %s svg ---' % self.nature
		print 'position:', self.px, self.py
		print 'dimension:', self.width, '*', self.height

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'un objet a partir d'une chaine de caracteres
		arguments:
			un objet vide
			la chaine ne contient qu'un seul objet, avec ses coins ouvrant et fermants <rect x='20' y='5' width='60' height='30'/>
		retourne: la sous-chaine contenant les caracteristiques de l'objet. elles seront estraites par des fonctions specifiques
		"""
#		nettoyer la forme afin de la rendre plus facile a traiter
		chn = chn.strip()
#		id et classe
		if 'id=' in chn: self.id = extraire (chn, 'id')
		if 'class=' in chn: self.classe = extraire (chn, 'class')
#		trouver la nature de la forme
		fspace = chn.find (' ')		# <rect x='10'/>
		if fspace <0: fspace =1000	# au cas ou f=-1
		fbracket = chn.find ('>')	# <rect>
		if fbracket <0: fbracket =1000
		fendbracket = chn.find ('/>')	# <rect/>
		if fendbracket <0: fendbracket =1000
		f= min (fspace, fbracket, fendbracket)
		self.nature = chn[1:f]		# 1 pour sauter le <

	def to_str (self, chn):
		""" action: transforme l'objet en texte
		arguments:
			l'objet
			la chaine creee par une fonction specifique
		retourne: une chaine contenant les classe et id de l'objet
		"""
#		ecrire la classe et l'identifiant
		chn_tmp =""
		if self.classe: chn_tmp = " class='%s'"% self.classe
		if self.id: chn_tmp = " id='%s'"% self.id + chn_tmp
		if self.autre: chn_tmp = chn_tmp +' '+ self.autre
#		trouver ou inclure chn_tmp
		fspace = chn.find (' ')		# <rect x='10'/>
		if fspace <0: fspace =1000	# au cas ou f=-1
		fbracket = chn.find ('>')	# <rect>
		if fbracket <0: fbracket =1000
		fendbracket = chn.find ('/>')	# <rect/>
		if fendbracket <0: fendbracket =1000
		d= min (fspace, fbracket, fendbracket)
		chn= chn[:d] + chn_tmp + chn[d:]
		return chn

	def translate (self,x,y):
		""" action: deplace une forme
		arguments:
			la forme
			le facteur de deplacement selon l'axe des x
			le facteur de deplacement selon l'axe des y
		retourne: la forme modifiee
		"""
		self.px +=x
		self.py +=y

	def scale (self,x,y):
		""" action: agrandit une forme. elle est deplacee
		arguments:
			la forme
			le facteur d'agrandissement selon l'axe des x
			le facteur d'agrandissement selon l'axe des y
			x et y >0
		retourne: la forme modifiee
		"""
		self.width *=x
		self.height *=y
		self.px *=x
		self.py *=y

	def min (self, x,y):
		""" action: compare px, py avec les coordonnees x,y
		arguments:
			l'objet
			une coordonnee x
			une coordonnee y
		retourne: les plus petites valeurs
		"""
		if self.px <x: x= self.px
		if self.py <y: y= self.py
		return x,y

	def max (self, x,y):
		""" action: compare px, py avec les coordonnees x,y
		arguments:
			l'objet
			une coordonnee x
			une coordonnee y
		retourne: les plus grande valeurs
		"""
		if self.px + self.width >x: x= self.px + self.width
		if self.py + self.height >y: y= self.py + self.height
		return x,y

class rect (obj):
	""" les rectangles """
	def __init__ (self):
		obj.__init__ (self)
		self.nature = 'rect'

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'un rectangle a partir d'une chaine
		arguments:
			un rect vide
			la chaine
		retourne: le rect avec ses nouvelles caracteristiques
		"""
#		recuperer la sous-chaine avec les caracteristiques
		obj.from_str (self, chn)
#		recuperer les caracteristiques
		self.width = extraire (chn, 'width')
		self.height = extraire (chn, 'height')
		self.px = extraire (chn, 'x')
		self.py = extraire (chn, 'y')

	def to_str (self):
		""" action: transforme le rect en texte
		argument: le rect
		retourne: une chaine contenant les caracteristiques de l'objet
		"""
#		creer la chaine contenant les caracteristiques des rectangles
		chn = "<rect x='%s' y='%s' width='%s' height='%s'/>"
#		ajouter les caracteristiques dans la chaine
		chn = chn %(
			txt.float_to_str (self.px),
			txt.float_to_str (self.py),
			txt.float_to_str (self.width),
			txt.float_to_str (self.height) )
#		id, classe
		chn= obj.to_str (self, chn)
		return chn

class circle (obj):
	""" les cercles """
	def __init__ (self):
		obj.__init__ (self)
		self.nature = 'circle'

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'un cercle a partir d'une chaine
		arguments:
			un circle vide
			la chaine
		retourne: le circle avec ses nouvelles caracteristiques
		"""
#		recuperer la sous-chaine avec les caracteristiques
		obj.from_str (self, chn)
#		recuperer les caracteristiques
		self.width = extraire (chn, 'r')
		self.px = extraire (chn, 'cx')
		self.py = extraire (chn, 'cy')
#		cx correspond au centre du cercle, pas au bord droit
		self.px -= self.width
		self.py -= self.width
#		r correspond au rayon, je dois obtenir le diametre
		self.width *=2
#		pour un cercle width = height
		self.height = self.width

	def to_str (self):
		""" action: transforme le circle en texte
		argument: le circle
		retourne: une chaine contenant les caracteristiques de l'objet
		"""
#		width correspond au diametre, je veux le rayon
		rayon = self.width /2
#		retrouver la position du centre
		posx = self.px + rayon
		posy = self.py + rayon
#		creer la chaine contenant les caracteristiques
		chn = "<circle cx='%s' cy='%s' r='%s'/>"
#		ecrire les caracteristiques de la forme
		chn = chn %(
			txt.float_to_str (posx),
			txt.float_to_str (posy),
			txt.float_to_str (rayon) )
#		id, classe
		chn= obj.to_str (self, chn)
		return chn

class ellipse (obj):
	""" les ellipses """
	def __init__ (self):
		obj.__init__ (self)
		self.nature = 'ellipse'

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'une ellipse a partir d'une chaine
		arguments:
			une ellipse vide
			la chaine
		retourne: l'ellipse avec ses nouvelles caracteristiques
		"""
#		recuperer la sous-chaine avec les caracteristiques
		obj.from_str (self, chn)
#		recuperer les caracteristiques
		self.width = extraire (chn, 'rx')
		self.height = extraire (chn, 'ry')
		self.px = extraire (chn, 'cx')
		self.py = extraire (chn, 'cy')
#		cx correspond au centre du cercle, pas au bord droit
		self.px -= self.width
		self.py -= self.width
#		rx correspond au rayon, je dois obtenir le diametre
		self.width *=2
		self.height *=2

	def to_str (self):
		""" action: transforme l'ellipse en texte
		argument: l'ellipse
		retourne: une chaine contenant les caracteristiques de l'objet
		"""
#		width correspond au diametre, je veux le rayon
		rayonx = self.width /2
		rayony = self.height /2
#		retrouver la position du centre
		posx = self.px + rayonx
		posy = self.py + rayony
#		creer la chaine contenant les caracteristiques
		chn = "<circle cx='%s' cy='%s' rx='%s' ry='%s'/>"
#		ecrire les caracteristiques de la forme
		chn = chn %(
			txt.float_to_str (posx),
			txt.float_to_str (posy),
			txt.float_to_str (rayonx),
			txt.float_to_str (rayony) )
#		id, classe
		chn= obj.to_str (self, chn)
		return chn

class line (obj):
	""" lignes simples """
	def __init__ (self):
		obj.__init__ (self)
		self.nature = 'line'

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'une ellipse a partir d'une chaine
		arguments:
			un text vide
			la chaine
		retourne: le text avec ses nouvelles caracteristiques
		"""
#		recuperer la sous-chaine avec les caracteristiques
		obj.from_str (self, chn)
#		recuperer les caracteristiques
		x1 = extraire (chn, 'x1')
		x2 = extraire (chn, 'x2')
		y1 = extraire (chn, 'y1')
		y2 = extraire (chn, 'y2')
#		trouver px, py
		self.px = min (x1,x2)
		self.py = min (y1,y2)
#		trouver width, height
		self.width = max (x1,x2) - self.px
		self.height = max (y1,y2) - self.py

	def to_str (self):
		""" action: transforme la ligne en texte
		argument: la ligne
		retourne: une chaine contenant les caracteristiques de l'objet
		"""
#		modifier width et height pour qu'ils correspondent a des coordonnees
		x2= self.width + self.px
		y2= self.height + self.py
#		creer la chaine contenant les caracteristiques
		chn = "<line x1='%s' y1='%s' x2='%s' y2='%s'/>"
#		ajouter les caracteristiques dans la chaine
		chn = chn %(
			txt.float_to_str (self.px),
			txt.float_to_str (self.py),
			txt.float_to_str (x2),
			txt.float_to_str (y2) )
#		id, classe
		chn= obj.to_str (self, chn)
		return chn


""" ____________________________________ les classes d'objets svg complexes ____________________________________ """

class text (obj):
	""" le texte, <text/> """
	def __init__ (self):
		obj.__init__ (self)
		self.nature = 'text'
		self.text =""

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'une ellipse a partir d'une chaine
		arguments:
			un text vide
			la chaine
		retourne: le text avec ses nouvelles caracteristiques
		"""
#		recuperer la sous-chaine avec les caracteristiques
		obj.from_str (self, chn)
#		recuperer les caracteristiques
		self.px = extraire (chn, 'x')
		self.py = extraire (chn, 'y')
#		trouver le texte
		d= chn.find ('>') +1
		f= chn.find ('<',d)
		self.text = chn[d:f]
#		longueur du texte
		self.width = len (self.text)

	def to_str (self):
		""" action: transforme le text en texte
		argument: le text
		retourne: une chaine contenant les caracteristiques de l'objet
		"""
#		creer la chaine contenant les caracteristiques
		chn = "<text x='%s' y='%s'>%s</text>"
#		ecrire les caracteristiques de la forme
		chn = chn %(
			txt.float_to_str (self.px),
			txt.float_to_str (self.py),
			txt.float_to_str (self.text) )
#		id, classe
		chn= obj.to_str (self, chn)
		return chn

class poly (obj):
	""" polygones et polylines """
	def __init__ (self):
		""" les x et y sont stocques dans des listes separees """
		obj.__init__ (self)
		self.nature = 'polygon'
		self.ptx =[]
		self.pty =[]

	def from_list (self, listx, listy):
		""" action: extraire les caracteristiques d'un polygone a partir d'une chaine
		arguments:
			un poly vide
			deux listes, de points x et y
		retourne: le poly avec ses nouvelles caracteristiques
		"""
#		trouver les coordonnees, les dimensions
		self.px = min (listx)
		self.py = min (listy)
		self.width = max (listx) - self.px
		self.height = max (listy) - self.py
#		modifier les coordonnees des points pour qu'ils tiennent entre 0 et 1
		range_points = range (len (listx))
		for i in range_points:
			listx[i] -= self.px
			listy[i] -= self.py
		if self.width >1:
			for i in range_points: listx[i] /= self.width
		if self.height >1:
			for i in range_points: listy[i] /= self.height
#		ajouter les points
		self.ptx.extend (listx)
		self.pty.extend (listy)

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'un polygone a partir d'une chaine
		arguments:
			un poly vide
			la chaine
		retourne: le poly avec ses nouvelles caracteristiques
		"""
#		recuperer la sous-chaine avec les caracteristiques
		obj.from_str (self, chn)
#		recuperer la chaine de points
		str_points = extraire (chn, 'points')
#		obtenir les positions x,y. stocquer les x et y dans des listes separees
		list_points = str_points.split (' ')
		for p in list_points:
			pl= p.split (',')
			self.ptx.append (float (pl[0]))
			self.pty.append (float (pl[1]))
#		trouver les coordonnees, les dimensions
		self.px = min (self.ptx)
		self.py = min (self.pty)
		self.width = max (self.ptx) - self.px
		self.height = max (self.pty) - self.py
#		modifier les coordonnees des points pour qu'ils tiennent entre 0 et 1
		range_points = range (len (self.ptx))
		for i in range_points:
			self.ptx[i] -= self.px
			self.pty[i] -= self.py
		if self.width >1:
			for i in range_points: self.ptx[i] /= self.width
		if self.height >1:
			for i in range_points: self.pty[i] /= self.height

	def to_str (self):
		""" action: transforme le poly en texte
		argument: le poly
		retourne: une chaine contenant les caracteristiques de l'objet
		"""
#		modifier les coordonnees des points pour qu'ils sortent de l'intervalle 0-1
		range_points = range (len (self.ptx))
		if self.width >1:
			for i in range_points: self.ptx[i] *= self.width
		if self.height >1:
			for i in range_points: self.pty[i] *= self.height
		for i in range_points:
			self.ptx[i] += self.px
			self.pty[i] += self.py
#		transformer les float en str
		list_points =[]
		for i in range_points:
			ptx = txt.float_to_str (self.ptx[i])
			pty = txt.float_to_str (self.pty[i])
			list_points.append (ptx +','+ pty)
		str_points =' '.join (list_points)
		str_points = '<'+ self.nature +" points='" + str_points +"'/>"
#		id, classe
		str_points = obj.to_str (self, str_points)
		return str_points

	def hexagon (self):
		""" action: creer un polygone en forme d'hegagone """
		ptx = [0.0, 0.25, 0.75, 1.0, 0.75, 0.25]
		pty = [0.5, 1.0, 1.0, 0.5, 0.0, 0.0]
		self.from_list (ptx, pty)
	def losange (self):
		""" action: creer un polygone en forme de losange """
		ptx = [0.5, 1, 0.5, 0]
		pty = [0.0, 0.5, 1.0, 0.5]
		self.from_list (ptx, pty)
	def triangle (self):
		""" action: creer un polygone en forme de triangle """
		ptx = [0.0, 1.0, 0.5]
		pty = [0.0, 0.0, 1.0]
		self.from_list (ptx, pty)

class group (obj):
	""" group """
	def __init__ (self):
		obj.__init__ (self)
		self.nature = 'g'
#		liste des objets contenus
		self.lst =[]

	def min (self):
		""" action: trouver les coordonnees minimales parmis les objets d'une liste
		arguments: le groupe
		retourne: xmin, ymin les coordonnees minimales
		"""
#		valeurs de depart
		xmin = self.lst[0].px
		ymin = self.lst[0].py
#		rechercher les coordonnees minimales
		for shape in self.lst: xmin, ymin = shape.min (xmin, ymin)
		return xmin, ymin

	def max (self):
		""" action: trouver les coordonnees maximales parmis les objets d'une liste
		arguments: le groupe
		retourne: xmax, ymax les coordonnees maximales
		"""
#		valeurs de depart
		xmax = self.lst[0].px + self.lst[0].width
		ymax = self.lst[0].py + self.lst[0].height
#		rechercher les coordonnees maximales
		for shape in self.lst: xmax, ymax = shape.max (xmax, ymax)
		return xmax, ymax

	def from_str (self, chn):
		""" action: extraire les caracteristiques d'un groupe a partir d'une chaine
		arguments:
			un group vide
			la chaine
		retourne: le group avec ses nouvelles caracteristiques
		"""
#		recuperer la sous-chaine avec les caracteristiques
		obj.from_str (self, chn)
#		nettoyer le texte pour faciliter sa manipulation
		chn= chn.strip()
		chn= chn.replace ('"', "'")
		while '  ' in chn: chn= chn.replace ('  ',' ')
		chn= chn.replace (' <', '<')
		chn= chn.replace ('\n ', ' ')
#		eliminer les bornes <g>...</g>
		d= chn.find ('>') +1
		f= chn.rfind ('</'+ self.nature +'>')
		chn= chn[d:f]
#		extraire les differents objets
		d=0 ; f=0
		while '/>' in chn:
#			reperer le premier objet
			d= chn.find ('<')
			if chn[d:d+2] == '<g':
				self.lst.append (group())
				f= chn.find ('</g>', d) +4
			elif chn[d:d+5] == '<text':
				self.lst.append (text())
				f= chn.find ('</text>', d) +7
			elif chn[d:d+5] == '<rect':
				self.lst.append (rect())
				f= chn.find ('/>',d) +2
			elif chn[d:d+5] == '<elli':
				self.lst.append (ellipse())
				f= chn.find ('/>',d) +2
			elif chn[d:d+5] == '<circ':
				self.lst.append (circle())
				f= chn.find ('/>',d) +2
			elif chn[d:d+5] == '<poly':
				self.lst.append (poly())
				f= chn.find ('/>',d) +2
			elif chn[d:d+5] == '<line':
				self.lst.append (line())
				f= chn.find ('/>',d) +2
			else:
				f=d+1
				chn = chn[f:]
				continue
#			creer l'objet
			self.lst[-1].from_str (chn[d:f])
			chn = chn[f:]
#		recuperer les caracteristiques
		self.px, self.py = self.min()
		self.width, self.height = self.max()
		self.width -= self.px
		self.height -= self.py

	def to_str (self):
		""" action: transforme le group en texte
		argument: le groupe
		retourne: une chaine contenant l'objet
		"""
#		mettre toutes les formes contenues sous forme de texte
		list_shapes =""
		for shape in self.lst:
			list_shapes= list_shapes+ shape.to_str()
#		rajouter les balises du groupes
		list_shapes = '<'+ self.nature +'>'+ list_shapes + '</'+ self.nature +'>'
		list_shapes = list_shapes.replace ('><', '>\n<')
#		id, classe
		list_shapes= obj.to_str (self, list_shapes)
		return list_shapes

	def afficher (self):
		""" action: afficher l'objet en indiquant ses caracteristiques simples """
#		affichage basique
		obj.afficher (self)
#		afficher chaque elements contenu
		print 'nature\tpx\tpy\twidth\theight'
		for shape in self.lst:
			print '%s\t%.1f\t%.1f\t%.1f\t%.1f' %( shape.nature, shape.px, shape.py, shape.width, shape.height)

	def translate (self, x,y):
		""" action: deplace les elements d'un groupe selon les coordonnees x et y
		arguments: les coordonnees x et y, float ou int
		"""
		for shape in self.lst: shape.translate (x,y)

	def scale (self, x,y):
		""" action: change la taille des elements d'un groupe selon les facteurs x et y
		arguments: les facteurs x et y, float ou int
		"""
		for shape in self.lst:
			shape.width *=x
			shape.height *=y
			shape.px *=x
			shape.py *=y

	def append (self, shape):
		""" action: ajouter une forme a la fin de la liste des formes d'un groupe
		arguments:
			le groupe
			la forme
		"""
		self.lst.append (shape)

	def objet (self, nature, x,y,w,h):
		""" action: dessine une forme dans le svg
		arguments:
			nature la nature de l'objet a rajouter, representee par une lettre
			x la position x la plus a gauche
			y la position y la plus haute
			w width, la longueur de la ligne selon l'axe des x
			h height, la longueur de la ligne selon l'axe des y
		"""
		if nature =='l': self.lst.append (line())
		if nature =='e': self.lst.append (ellipse())
		elif nature =='r': self.lst.append (rect())
		elif nature =='c': self.lst.append (circle())
		elif nature =='t': self.lst.append (text())
		elif nature =='p': self.lst.append (poly())
		self.lst[-1].px =x
		self.lst[-1].py =y
		self.lst[-1].width =w
		self.lst[-1].height =h

	def ligne (self, x1,y1,x2,y2):
		""" action: dessine une ligne dans le svg
		arguments:
			x1 la position x la plus a gauche
			y1 la position y de ce point
			x2 la position x la plus a droite
			y2 la position y de ce point
		certaines hauteurs peuvent etre negatives
		"""
		width = x2-x1
		height =y2-y1
		self.objet ('l', x1,y1, width, height)

	def rectangle (self, x,y,w,h):
		""" action: dessine un carre dans le svg
		arguments:
			x la position x
			y la position y
			w width, la longueur du rectangle
			h height, la hauteur du rectangle
		"""
		self.objet ('r', x,y,w,h)

	def carre (self, x,y,w):
		""" action: dessine un carre dans le svg
		arguments:
			x la position x
			y la position y
			w width, la largeur du carre
		"""
		self.objet ('r', x,y,w,w)

	def cercle (self, x,y,d):
		""" action: dessine un cercle dans le svg
		arguments:
			x la position x du centre
			y la position y du centre
			d le diametre du cercle
		"""
		rayon = d/2.0
		px= x- rayon
		py= y- rayon
		self.objet('c', x,y,d,d)

	def ellipse (self, px,py,dx,dy):
		""" action: dessine une ellipse dans le svg
		arguments:
			x la position x du centre
			y la position y du centre
			dx le diametre du cercle selon l'abcisse
			dy le diametre du cercle selon l'ordonnee
		"""
		rayon = dx/2.0
		px= x- rayon
		rayon = dy/2.0
		py= y- rayon
		self.objet('e', px,py,dx,dy)

	def polyligne (self, x,y,w,h, lstx, lsty):
		""" action: dessine un polyligne dans le svg
		arguments:
			x la position x
			y la position y
			w width, la longueur du polyligne
			h height, la hauteur du polyligne
			lstx la liste des coordonnees x
			lsty la liste des coordonnees y
		"""
		self.objet ('p', x,y,w,h)
		self.lst[-1].nature = 'polyline'
		self.lst[-1].ptx.extend (lstx)
		self.lst[-1].pty.extend (lsty)

	def polygone (self, x,y,w,h, lstx, lsty):
		""" action: dessine un polygone dans le svg
		arguments:
			x la position x
			y la position y
			w width, la longueur du polygone
			h height, la hauteur du polygone
			lstx la liste des coordonnees x
			lsty la liste des coordonnees y
		"""
		self.objet ('p', x,y,w,h)
		self.lst[-1].nature = 'polygon'
		self.lst[-1].ptx.extend (lstx)
		self.lst[-1].pty.extend (lsty)

	def hexagone (self, x,y,w,h):
		""" action: dessine un hexagone dans le svg
		arguments:
			x la position x
			y la position y
			w width, la longueur du polyligne
			h height, la hauteur du polyligne
		"""
		self.objet ('p', x,y,w,h)
		self.lst[-1].nature = 'polygon'
		self[-1].hexagon()

	def losange (self, x,y,w,h):
		""" action: dessine un losange dans le svg
		arguments:
			x la position x
			y la position y
			w width, la longueur du polyligne
			h height, la hauteur du polyligne
		"""
		self.objet ('p', x,y,w,h)
		self.lst[-1].nature = 'polygon'
		self[-1].losange()

	def triangle (self, x,y,w,h):
		""" action: dessine un triangle dans le svg
		arguments:
			x la position x
			y la position y
			w width, la longueur du polyligne
			h height, la hauteur du polyligne
		"""
		self.objet ('p', x,y,w,h)
		self.lst[-1].nature = 'polygon'
		self[-1].triangle()

	def texte (self, x,y, txt):
		""" action: dessine un texte dans le svg
		arguments:
			x la position x
			y la position y
			txt le texte
		"""
		width = 6* len (txt)
		height =20
		self.objet ('t', x,y, width, height)
		self.lst[-1].text = txt

	def action (self, tag, x=None, y=None):
		""" action: modifie une image svg
		arguments:
			tag l'action a accomplir
			x,y les facteurs selon lesquels l'image devra etre modifiee. ce sont des nombre sous forme str "10.3"
		"""
		nbx=None ; nby=None
		if x!= None:
			nbx= float (x)
			nby= float (y)
#		nettoyer l'image
		if tag =='n':
			for shape in img.lst:
				shape.classe =""
				shape.id =""
#		decaler l'image
		elif tag =='t' and nbx != None: img.translate (nbx, nby)
#		changer la taille de l'image
		elif tag =='s' and nbx != None: img.scale (nbx, nby)
#		le tag n'est pas reconnu
		else: print help

class svg (group):
	""" les fichiers svg peuvent etre traites comme des groupes
	file: fichier du svg
	style: feuille de style du svg
	"""
	def __init__(self, fichier=None):
		group.__init__(self)
		self.nature = 'svg'
		self.file =""
		self.style =""
		self.style_externe =""
		if fichier and fichier[-4:] =='.svg': self.file = fichier

	def from_file (self, fichier=None):
		""" action: recuperer le contenu d'un fichier svg
		arguments:
			l'objet svg vide
			le fichier
		retourne: l'objet svg
		"""
#		recuperer le texte
		if fichier: self.file = fichier
		chn = txt.lire (self.file)
#		nettoyer le texte pour faciliter sa manipulation
		chn= chn.replace ('"', "'")
		while '  ' in chn: chn= chn.replace ('  ',' ')
		chn= chn.replace (' <', '<')
		chn= chn.replace ('\n ', ' ')
#		feuille de style externe
		if '<?xml-stylesheet' in chn:
			d= chn.find ('<?xml-stylesheet')
			d= chn.find ("href='",d) +6
			f= chn.find ('.css',d)
			self.style_externe = chn[d:f]
#		feuille de style interne
		if '<style>' in chn:
			d= chn.find ('<style><![CDATA[') +16
			f= chn.find (']]></style>')
			self.style = chn[d:f]
#			eliminer la balise <style/> pour faciliter l'extraction des formes
			chn= '<svg>'+ chn[f+11:]
#		width, height
		self.px =0.0
		self.py =0.0
		self.width = extraire (chn, 'width')
		self.height = extraire (chn, 'height')
#		les formes
		d= chn.find ('<svg')
		chn= chn[d:]
		group.from_str (self, chn)

	def to_file (self):
		""" action: ecrire le contenu d'un svg dans son fichier """
#		creer le contenu svg, <svg>...</svg>
		self.px =0
		self.py =0
		text_svg = self.to_str()
#		rajouter des infos dans la balise <svg>
		text_svg = text_svg[:4] + """ width='%s' height='%s'
	xmlns:xlink='http://www.w3.org/1999/xlink'
	xmlns='http://www.w3.org/2000/svg'>
""" %( txt.float_to_str (self.width), txt.float_to_str (self.height) )+ text_svg[5:]
#		feuille de style interne
		if self.style:
			self.style = self.style.strip()
			style = '<style><![CDATA[\n' + self.style + '\n]]></style>\n'
			d= text_svg.find ('>\n') +2
			text_svg = text_svg[:d] + style + text_svg[d:]
#		feuille de style externe
		if self.style_externe: text_svg = "<?xml-stylesheet type='text/css' href='%s.css' ?>\n" % self.style_externe + text_svg
		text_svg = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" + text_svg
#		ecrire
		txt.ecrire (self.file, text_svg, 'w')



""" ____________________________________ les actions ____________________________________ """




# si ce script est appeler dans un autre fichier
if argv[0] != 'dpowers_svg.py': pass
# si l'utilisateur a entrer une commande inconnue
elif len (argv) <3: print help
else:
	img = svg()
#	on a envoyer un fichier, il faut l'ouvrir
	if argv[1][-4:] =='.svg': img.from_file (argv[1])
#	on a envoyer un texte contenant un groupe, il faut extraire les formes
	else: img.from_str (argv[1])
#	recuperer les facteurs x,y
	x=None ; y=None
	if len (argv) >3: x= argv[3]
	if len (argv) >4: y= argv[4]
	else: y=x
#	modifier l'image
	img.action (argv[2], x,y)
#	on a envoyer un fichier, il faut ecrire dedans
	if argv[1][-4:] =='.svg': img.to_file()
#	on a envoyer un texte contenant un groupe, il faut l'afficher
	else:
		chn= img.to_str()
		print chn

