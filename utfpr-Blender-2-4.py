from Blender import *
import math

k_counter = 0

flag_no_doors = True


def CreateDale (scn, x, y, z, sx, sy):

	global k_counter

	k_counter += 1
	name = 'p' + str(k_counter)

	tile     = Mesh.Primitives.Cube(1.0)
	ob       = scn.objects.new (tile, name)
	ob.SizeX = sx
	ob.SizeY = sy
	ob.SizeZ = 0.2
	ob.LocX  = x + (sx / 2.0)
	ob.LocY  = y + (sy / 2.0)
	ob.LocZ  = z-0.2
	
	Colorize(ob,238./255., 233./255., 233./255.)
	return ob


def CreateSphere (scn, x, y, z, radius):

	global k_counter

	k_counter += 1
	name = 'p' + str(k_counter)

	tile     = Mesh.Primitives.Icosphere(3.0, radius)
	ob       = scn.objects.new (tile, name)
	ob.LocX  = x
	ob.LocY  = y
	ob.LocZ  = z
	
	return ob


def CreateHemisphere (ox,oy,oz,ray): 


	global k_counter

	k_counter += 1
	name = 'p' + str(k_counter)
	smooth = 0
	type = 'UV'
	n = 16
	ray = ray / 5.0

	ME=Object.New('Mesh','jose') 
	Scene.getCurrent().link(ME) 
	me=ME.getData()  

	ME.LocX = ox
	ME.LocY = oy
	ME.LocZ = oz
	
	if type=='ico': 
	   icovert = [    [0.0,0.0,-2.0],  
		[1.4472, -1.05144,-0.89443], 
		[-0.55277, -1.70128,-0.89443],  
		[-1.78885,0.0,-0.89443], 
		[-0.55277,1.70128,-0.89443],  
		[1.4472,1.05144,-0.89443], 
		[0.55277,-1.70128,0.89443], 
		[-1.4472,-1.05144,0.89443], 
		[-1.4472,1.05144,0.89443], 
		[0.55277,1.70128,0.89443], 
		[1.78885,0.0,0.89443], 
		[0.0,0.0,2.0]]

	   icoface = [ 
		[1,0,2], 
		[1,0,5], 
		[2,0,3], 
		[3,0,4], 
		[4,0,5], 
		[1,5,10], 
		[2,1,6], 
		[3,2,7], 
		[4,3,8], 
		[5,4,9], 
		[10,1,6], 
		[6,2,7], 
		[7,3,8], 
		[8,4,9], 
		[9,5,10], 
		[6,10,11], 
		[7,6,11], 
		[8,7,11], 
		[9,8,11], 
		[10,9,11]]  
	   for v in icovert: 
			vn=NMesh.Vert(v[0],v[1],v[2]) 
			me.verts.append(vn)

	   for f in icoface: 
			f_=NMesh.Face() 
			for v in f:  
			   f_.append(me.verts[v]) 
			f_.smooth=smooth 
			me.faces.append(f_) 
	elif type=='UV':
		for i in range(0,n):
			for j in range(0,n): 
				x=math.sin(j*math.pi*2.0/(n-1))*math.cos(-math.pi/2.0+i*math.pi/(n-1))*2.0 
				y=math.cos(j*math.pi*2.0/(n-1))*(math.cos(-math.pi/2.0+i*math.pi/(n-1)))*2.0 
				z=math.sin(-math.pi/2.0+i*math.pi/(n-1))*2.0 
				if z >= 0:
					 v=NMesh.Vert(x*ray,y*ray,z*ray) 
					 me.verts.append(v) 
					 #k = k + 1
		n0=len(range(0,n)) 
		#n0 = len(me.verts)
		for i in range(0,n-1):  
			for j in range(0,n-1):
				if len(me.verts) >= (i+1)*n0+j+1:
					f=NMesh.Face()  
					f.v.append(me.verts[i*n0+j])  
					f.v.append(me.verts[i*n0+j+1])  
					f.v.append(me.verts[(i+1)*n0+j+1])  
					f.v.append(me.verts[(i+1)*n0+j])  
					me.faces.append(f) 
					f.smooth=smooth  
					me.faces.append(f) 
			#f.smooth=smooth

	me.update() 
	return ME


def CreateMarche (scn, x, y, z, sx, sy, sz):

	global k_counter

	k_counter += 1
	name = 'p' + str(k_counter)

	tile     = Mesh.Primitives.Cube(1.0)
	ob       = scn.objects.new (tile, name)
	ob.SizeX = sx
	ob.SizeY = sy
	ob.SizeZ = sz
	ob.LocX  = x + (sx / 2.0)
	ob.LocY  = y + (sy / 2.0)
	ob.LocZ  = z + (sz / 2.0)
	
	Colorize(ob,238./255., 233./255., 233./255.)
	return ob



def CreateEchelle (scn, x, y, z, x2, y2, z2, largeur, nmarches):

	global k_counter

	dx = x2-x
	dy = y2-y
	dz = z2-z
	
	sx = dx/nmarches
	sy = dy/nmarches
	sz = dz/nmarches
	
	print dx,dy,dz,sx,sy,sz
	
	if (0 == dx):
		for i in xrange (nmarches):
			CreateMarche (scn, x, y+(i*sy), z+(i*sz), largeur, sy, sz)
	else:
		for i in xrange (nmarches):
			CreateMarche (scn, x+(i*sx), y, z+(i*sz), sx, largeur, sz)
	

def CreerChaise (scn, x, y, z, direction):

	dx = 0.35
	dy = 0.40

	if (1 == direction):
		dx = -dx
	
	CreateMarche (scn, x     , y     , z, 0.05, 0.05, 0.50)
	CreateMarche (scn, x+dx  , y     , z, 0.05, 0.05, 0.50)
	
	CreateMarche (scn, x     , y+dy, z    , 0.05, 0.05, 1.10)
	CreateMarche (scn, x+dx  , y+dy, z    , 0.05, 0.05, 1.10)
	
	CreateMarche (scn, x     , y     , z+.50, abs(dx), dy, 0.05)
	
	CreateMarche (scn, x     , y+dy  , z+.50, dx, 0.05, 0.60)




	
def CreateParois (scn, x, y, z, sx, sy, sz):

	global k_counter

	k_counter += 1
	name = 'p' + str(k_counter)

	tile     = Mesh.Primitives.Cube(1.0)
	ob       = scn.objects.new (tile, name)
	ob.SizeX = sx
	ob.SizeY = sy
	ob.SizeZ = sz
	ob.LocX  = x + (sx / 2.0)
	ob.LocY  = y + (sy / 2.0)
	ob.LocZ  = z + (sz / 2.0)
	
	Colorize(ob,238./255., 233./255., 233./255.)
	return ob


def CreateParois2 (scn, x, y, z, sx, sy, sz):

	global k_counter

	k_counter += 1
	name = 'p' + str(k_counter)

	tile     = Mesh.Primitives.Plane(1.0)
	ob       = scn.objects.new (tile, name)	
	ob.SizeX = sz
	ob.SizeY = sy
	ob.SizeZ = 1
	ob.RotX = 0
	ob.RotY = 0
	ob.RotZ = 0
	ob.LocX  = x + sx#+ (sx / 2.0)
	ob.LocY  = y + (sy / 2.0)
	ob.LocZ  = z + (sz / 2.0)
	if sx > sy:
		ob.RotX  = 3.1415/2.0
	else:
		ob.RotY  = 3.1415/2.0
	
	tile2    = Mesh.Primitives.Plane(1.0)
	ob2       = scn.objects.new (tile2, name+'2')	
	ob2.SizeX = sz
	ob2.SizeY = sy
	ob2.SizeZ = 1
	ob2.RotX = 0
	ob2.RotY = 0
	ob2.RotZ = 0
	ob2.LocX = ob.LocX
	ob2.LocY = ob.LocY
	ob2.LocZ = ob.LocZ
	
	if sx > sy:
		ob2.RotX  = 3.1415/2.
		ob2.LocY  = y #- (sy / 2.0)
	else:
		ob2.RotY  = 3.1415/2.
		ob2.LocX  = x #- (sx / 2.0)
	

	return tile



def openHole (scn, obj1,x,y,z,sx,sy,sz): 


	if flag_no_doors:
		return obj1
	
	mexe	 = Mesh.Primitives.Cube(1.0)
	ob       = scn.objects.new (mexe, 'furo')
	ob.SizeX = sx
	ob.SizeY = sy
	ob.SizeZ = sz
	ob.LocX  = x + (sx / 2.0)
	ob.LocY  = y + (sy / 2.0)
	ob.LocZ  = z + (sz / 2.0)

	mod = obj1.modifiers.append (Modifier.Type.BOOLEAN) # add boolean modifier 
	mod[Modifier.Settings.OBJECT] = ob                        # defines the object to operate 
	mod[Modifier.Settings.OPERATION] = 2                        # defines the operation 
	
	obj1.makeDisplayList ()
	Window.RedrawAll ()
	
	oldmesh = obj1.getData(mesh=1)
	oldmena = oldmesh.name
	
	deformedmesh = Mesh.New()
	deformedmesh.getFromObject (obj1.name)
	
	obj2=scn.objects.new(deformedmesh,'utro')
	obj2.LocX = obj1.LocX
	obj2.LocY = obj1.LocY
	obj2.LocZ = obj1.LocZ
	obj2.SizeX = obj1.SizeX
	obj2.SizeY = obj1.SizeY
	obj2.SizeZ = obj1.SizeZ
	
	scn.unlink (ob)
	scn.unlink (obj1)
	return obj2


def openHole2 (scn, obj1,x,y,z,sx,sy,sz): 

	mexe	 = Mesh.Primitives.Cube(1.0)
	ob       = scn.objects.new (mexe, 'furo')
	ob.SizeX = sx
	ob.SizeY = sy
	ob.SizeZ = sz
	ob.LocX  = x + (sx / 2.0)
	ob.LocY  = y + (sy / 2.0)
	ob.LocZ  = z + (sz / 2.0)

	mod = obj1.modifiers.append (Modifier.Type.BOOLEAN) # add boolean modifier 
	mod[Modifier.Settings.OBJECT] = ob                        # defines the object to operate 
	mod[Modifier.Settings.OPERATION] = 1                        # defines the operation 

	Window.RedrawAll ()
	scn.unlink (ob)


def Colorize(ob,r,g,b):

	global k_counter
	k_counter += 1
	name = 'cl' + str(k_counter)

	mat = Material.New('newMat')          # create a new Material called 'newMat'
	mat.rgbCol = [0.8, 0.1, 0.2]          # change its color

	v = [r, g, b]
	mat.rgbCol = v
	
	mat.setAlpha(0.2)                     # mat.alpha = 0.2 -- almost transparent
	mat.emit = 0.0                        # equivalent to mat.setEmit(0.8)

	n=ob.getData()
	n.materials=[mat]
	n.update()

	

def Texturize (me, texpath):

	global k_counter
	k_counter += 1
	name = 't' + str(k_counter)

	newmat = Material.New('name') 
	newmat.mode = newmat.mode  | 2048 
	me.materials.append(newmat)  

	im=Image.Load(texpath) 

	tex = Texture.New()  
	tex.setType('Image')  
	tex.image = im  
	newmat.setTexture(0, tex)  
	mtex = newmat.getTextures() 
	mtex[0].texco=Texture.TexCo.UV 
	
	f = me.faces[0]
	#f = NMesh.Face() 
	#f.v.append(me.verts[0]) 
	#f.v.append(me.verts[1]) 
	#f.v.append(me.verts[2]) 
	#f.v.append(me.verts[3]) 

	uv = [] 

	print (dir(me))
	print ('===========')
	print(dir(f))
	print (f.uv)
	print ('===========')
	f.image = im 

	uv.append( (0.0,0.0)) 
	uv.append( (1.0,0.0)) 
	uv.append( (1.0,1.0)) 
	uv.append( (0.0,1.0)) 

	f.uv = [[2,4],[1,2]] 


	if Blender.Get('version')>=228: 
	     C = NMesh.FaceModes 
	else: 
	     C = NMesh.Const 

	f.mode=C['LIGHT'] 
	f.mode|=C['TEX'] 
	f.mode|=C['TWOSIDE'] 
	
	
editmode = Window.EditMode()    # are we in edit mode?  If so ...
if editmode: Window.EditMode(0) # leave edit mode before getting the mesh
scn = Scene.GetCurrent()          # link object to current scene

for x in scn.objects:
	scn.objects.unlink(x)


if editmode: Window.EditMode(1)  # optional, just being nice





#=====================================================
# sous sol
#=====================================================
scn.setLayers ([1])


da = CreateDale   (scn, 0,  39, -1.0, 62, 65)   # GRAMADO
Colorize (da, .3, .6, .3)



CreateDale   (scn,     0,  0, -3, 10.5, 29)
CreateDale   (scn,  66.5,  0, -3, 10.5, 29)
CreateDale   (scn,     0, 29, -3, 66.5, 10)

CreateParois (scn,    70,  0, -3,  0.3,  29, 3)
CreateParois (scn,  66.5,  0, -3,  0.5,  29, 3)
CreateParois (scn,  76.5,  0, -3,  0.5,  29, 3)
CreateParois (scn,   6.5,  0, -3,  0.3,  29, 3)
CreateParois (scn,     0,  0, -3,  0.5,  39, 3)
CreateParois (scn,  10.5,  0, -3,  0.5,  29, 3)

# fa\E7ade sousterraine
da=CreateParois (scn,     0, 39, -3, 66.5, 0.5, 3)
Colorize (da, 105./255., 105./255., 105./255.)


CreateParois (scn,  10.5, 29, -3, 66.5, 0.5, 3)
CreateParois (scn,  10.5, 35, -3, 66.5, 0.5, 3)
CreateParois (scn,     0,  0, -3, 10.5, 0.5, 3)

#Dalle Cours Interieure
CreateDale   (scn,  10.5, 0, -2,  10, 29)


#=====================================================
# chemin xerox
#=====================================================

#passarelle
CreateDale   (scn, 62,  39, 0.1, 3, 25)
CreateDale   (scn, 62,  39, 3.1, 3, 25)
CreateParois (scn,  65, 39, 0, 0.2, 25, 3)

da = CreateParois (scn,  62, 39, -1.0, 0.2, 25, 2.0)
#Colorize (da,.8, .1, .2)


#Texturize (da,'d:\\48.jpg')


#=====================================================
# rez de chausse
#=====================================================
scn.setLayers ([2])

CreateDale   (scn,     0,  0, 0, 10.5, 29) #sol D104
CreateDale   (scn,  66.5,  0, 0, 10.5, 29) #sol d'autre cote

CreateDale   (scn,     0, 29, 0, 10.5, 10) #sol devant mini-theatre
CreateDale   (scn,  10.5, 35, 0,  6.0, 4.5)  #sol devant echelles
CreateDale   (scn,  15.5, 29, 0, 60.0, 10) #sol couloir devant chapelle

CreateDale   (scn,    33,  5, 0,   12, 24)


# mini-theatre (z = 0)
CreateDale   (scn,     0, 39, 0, 10.5,  6.5)

# parois externes du mini-theatre
CreateParois (scn,  0.0,  45.0, -1.0, 10.5, 0.5, 6.0)
CreateParois (scn, 10.5,  39.0, -1.0,  0.2, 6.5, 6.0)
CreateParois (scn,  0.0,  39.0, -1.0,  0.2, 6.5, 6.0)


CreateParois (scn, 0,  0,  0,   1, 0.5, 5)


#parois salles D106, D105, D104
CreateParois (scn, 0, 28,  0, 6.5,  .3, 5)
CreateParois (scn, 0, 17,  0, 6.5,  .3, 5)
CreateParois (scn, 0,  9,  0, 6.5,  .3, 5)
CreateParois (scn, 0,  4,  0, 6.5,  .3, 5)


#parois portes D104 D105
da = CreateParois (scn,   6.5,  0, 0,  0.3,  39, 5)

#porte salle D106
da2 = openHole (scn, da , 6, 37, 0.0, 1.0, 1.5, 3.0)
da  = openHole (scn, da2, 6, 19, 0.0, 1.0, 1.5, 3.0)
da2 = openHole (scn, da , 6, 11, 0.0, 1.0, 1.5, 3.0)
da  = openHole (scn, da2, 6,  6, 0.0, 1.0, 1.5, 3.0)
da2 = openHole (scn, da , 6,  2, 0.0, 1.0, 1.5, 3.0)


#parois fenetres D104 D105, jusqu'au mini theatre
da = CreateParois (scn,   0.0,  0, 0,  0.5,  45, 5)

#fenetres salles D104...
for y in [2, 6, 10, 11, 12.5, 14, 15.5, 18, 19.5, 21, 22.5, 24, 25.5, \
	      29, 30.5, 32, 33.5, 35, 36.5]:
	da2 = openHole (scn, da, -0.6, y, 1.2,   1.5, 1.0, 2.0)
	da  = da2
	da2 = None



#paroi couloir Jesus
CreateParois (scn,  67,  0, 0,  0.5,  35, 5)


#paroi ou on a pendu Jesus
CreateParois (scn,    70,  0, 0,  0.3,  34, 5)

#paroi labos cote biblioteque
CreateParois (scn,  76.5,  0, 0,  0.5,  35, 5)


#parois fond GEREC
CreateParois (scn,  10.5, 29, 0,   22, 0.5, 5)
CreateParois (scn,    45, 29, 0,   22, 0.5, 5)

#paroi qui separe echelle/gerec
CreateParois (scn,  15.0, 29.0, 0, 0.5, 6.0, 5.0)


#paroi entree chapelle
#on laisse espace pour les echelles
CreateParois (scn,  10.5+4.5, 35, 0,   57-4.5, 0.5, 5)

# Vers l'informatique
CreateEchelle (scn, 10.5, 35.0, 0.0, 10.5, 30.0, 2.5, 2.0, 8.0)
CreateEchelle (scn, 12.5, 30.0, 2.0, 12.5, 35.0, 5.0, 2.0, 8.0)
CreateEchelle (scn, 12.5, 31.0,-3.0, 12.5, 35.0, 0.0, 2.0, 8.0)


#paroi salles D104 D105, fenetres vers la cours, 
da  = CreateParois (scn,  10.5,  0,  0, 0.5,  33, 5)
da2 = openHole (scn, da, 10.5, 18, 0.0, 1.0, 2.0, 3.0)

# Echelle vers la cours interieure
CreateEchelle (scn, 10.5, 18.0,  0, 13.0, 18.0, -2.0, 2, 12)




# chapelle----------------------------------------
CreateParois (scn,    33,  5, 0,  12, 0.5, 6.5)

da = CreateParois (scn,  32.5,  5, 0, 0.5, 24, 6.5)
openHole (scn, da, 32.5, 7, 0.0,   1.0, 3.0, 6.5)
CreateParois (scn,  32.5,  28, 0, 0.5, 7, 4.9)

da = CreateParois (scn,    45,  5, 0, 0.5,  24, 6.5)
openHole (scn, da, 45, 7, 0.0,   1.0, 3.0, 6.5)
CreateParois (scn,  45,  28, 0, 0.5, 7, 4.9)



# dalle, rampe d'access vers GEPPG juscqu a Kastner
CreateDale   (scn,   0.0, -10,  0,  15, 10)

#dalle, labo d'electronique juscqu'a biblioteque
CreateDale   (scn,  15.0, -10.0,  1.0,  62.0, 7.0)

#dalle, couloir fond (vers biblioteque)
CreateDale   (scn,  11.0,  -3.0,  1.0,  66.0-10.5-1.0,  3.0)
CreateDale   (scn,  66.0,  -3.0,  0.0,  10.0,  3.0)

#echelle pres de Kastner
CreateEchelle (scn, 10.,  -2.3,  0, 11.2, -2.3, 0.90, 2.2, 5)

#echelle pres de la biblioteque
CreateEchelle (scn, 66.0-1.0,  -3.0,  1.0, 66.0, -3.0, 0.0, 3.0, 5)


# paroi fond utfpr, fond salle Kastner
CreateParois (scn,     0, -10,  0,    77, 0.5, 5)


#paroi qui ferme salle Kastner et salles suivantes
CreateParois (scn,  10.5 - 3.5,  -10,  0,  0.3, 7, 5)
CreateParois (scn,  15.0,  -10,  0,  0.3, 7, 5)
CreateParois (scn,  30.0,  -10,  0,  0.3, 7, 5)
CreateParois (scn,  40.0,  -10,  0,  0.3, 7, 5)
CreateParois (scn,  50.0,  -10,  0,  0.3, 7, 5)


#paroi portes: salle Kastner, labos..
da = CreateParois (scn,  10.5 - 3.5,   -3,  0,  66.5+3.5, 0.5, 5)
da2 = openHole (scn, da, 8.0, -3.1, 0, 1.0, 1.0, 2.5)
da  = da2
da2 = None
for x in [16, 31, 41, 51]:
	da2 = openHole (scn, da, x, -3.1, 1.0,   1.0, 1.0, 2.0)
	da  = da2
	da2 = None



CreateParois (scn,     0,   0,  1,   6.5, 0.5, 5)
CreateParois (scn,  10.5,   0,  1,  66.5, 0.5, 5)

# paroi vers biblioteque
CreateParois (scn,  76.5, -10,  1,   0.5,  10, 5)


# dale, salles D103, D104
CreateDale   (scn,   0.0, 0,  0,  10.5, 29)


#-----------------------------------------------
#fa\E7ade et fen\EAtres  (rez de chausse)
#-----------------------------------------------

da = CreateParois (scn, 0, 39, 0.0,   66.0, 0.5, 5.0)
Colorize(da,238./255., 130./255., 98./255.)

centre = 56.0 / 2.0

#porte centrale
da2 = openHole (scn, da, 10.5 + centre, 39, 0.0,   2.0, 1.0, 3.0)  # porte
da = da2
da2 = None

CreateEchelle (scn, 10.5+centre, 41.4, -1.0, 10.5+centre, 39.0, 0.1, 2.0, 10.0)


#porte mini-theatre
da2 = openHole (scn, da, 8, 39, 0.0,   1.0, 1.0, 3.0)  # porte



centre = 10.5 + (56.0 / 2.0)

da = None
da = da2
da2= None

for n in xrange (9):
	da2 = openHole (scn, da, centre + 3.0 + (2.0 * n), 39, 1.2,   1.5, 1.0, 2.0)
	da  = da2
	da2 = None
	da2 = openHole (scn, da, centre - 3.0 - (2.0 * n), 39, 1.2,   1.5, 1.0, 2.0)
	da  = da2
	da2 = None



#Echelle Tour
CreateEchelle (scn, 68.0, 39.0, 0.0, 68.0, 42.0, 2.5, 2.0, 11.0)
CreateEchelle (scn, 70.0, 42.0, 2.5, 70.0, 39.0, 4.8, 2.0, 11.0)
CreateDale    (scn, 68.0, 42.0, 2.5+0.2, 4.0, 1.0)





#=====================================================
# premier etage
#=====================================================
scn.setLayers ([3])


#parois externes de la Tour
CreateParois (scn, 66.0,  39.0,  0.0,  0.5, 4.0, 10.0)
CreateParois (scn, 66.0,  43.0,  0.0,  6.5, 0.5, 10.0)
CreateParois (scn, 72.0,  39.0,  0.0,  0.5, 4.0, 10.0)
CreateDale   (scn, 66.0,  39.0, 10.0,  6.5, 4.0)
#CreateSphere (scn, 69.0,  41.0, 10.0,  5.0)
da = CreateHemisphere (69, 41, 11, 5.0)
Colorize (da, 238.0/255.0, 92.0/255.0, 66.0/255.0)

cx = 69
cy = 41
ray= 1.8

for idx in range(1,7):
	CreateParois (scn, cx+ray*math.cos(2*idx*math.pi/6),\
                       cy+ray*math.sin(2*idx*math.pi/6),
                       10.0, 0.2, 0.2, 1.3)
	
CreateParois (scn, 72.0,  39.0,  0.0,  0.5, 4.0, 10.0)




da=CreateDale (scn, 10.5,-10, 5, 66.0, 10)

CreateDale   (scn,    0,  0, 5, 10.5,  39)
CreateDale   (scn, 66.5,  0, 5, 10.5,  29)

#parois externes du mini-theatre
CreateParois (scn, 10.5,  39.0, 5.0,  0.2, 6.5, 4.0)
CreateParois (scn,  0.0,  39.0, 5.0,  0.2, 6.5, 4.0)


#plafond couloir devant chapelle
CreateDale   (scn,   10.5+4, 29, 5, 60.0,  10)
CreateDale   (scn,   10.5  , 35, 5, 4.0,  4.0)
#CreateDale   (scn,   64.5  , 29, 5, 5.5,  7)


# plafond du micro-theatre
CreateDale   (scn,    0, 39, 5, 10.5,   6)


CreateDale   (scn, 10.5,-10, 5, 66.5,  10)



# ESTE

CreateParois (scn, 10.5,  0, 5,  0.5,  29, 4.0)
CreateParois (scn,  6.5,  0, 5,  0.3,  29, 4.0)
CreateParois (scn, 66.5,  0, 5,  0.5,  29, 4.0)
CreateParois (scn, 76.5,  0, 5,  0.5,  29, 4.0)
CreateParois (scn,   70,  0, 5,  0.3,  29, 4.0)
CreateParois (scn,    0, 45, 5, 10.5, 0.5, 4.0)
CreateParois (scn, 10.5, 29, 5, 66.5, 0.5, 4.0)

da = CreateParois (scn,    0,  0, 5,  10.5, 0.5, 4.0)
Colorize (da,.2, 0, .8)


# OUEST

#CreateParois (scn, 0,  0, 0,  0.5,  45, 9)
#parois fenetres labos au-dessus de D104 D105
CreateParois (scn,   0.0,  0, 5.0,  0.5,  45, 4)

#Colorize (da,.8, 0, .2)




#-----------------------------------------------
#fa\E7ade et fen\EAtres  (1er etage)
#-----------------------------------------------

da = CreateParois (scn, 10.5, 39, 5.0,   56, 0.5, 4.0)
Colorize(da,238./255., 130./255., 98./255.)

centre = 10.5 + (56.0 / 2.0)

da2 = None
for n in xrange (9):
	da2 = openHole (scn, da, centre + 3.0 + (2.0 * n), 39, 6.5,   1.5, 1.0, 1.6)
	da  = da2
	da2 = None
	da2 = openHole (scn, da, centre - 3.0 - (2.0 * n), 39, 6.5,   1.5, 1.0, 1.6)
	da  = da2
	da2 = None


#=====================================================
# toiture
#=====================================================
scn.setLayers ([4])

#toit lab informatique
CreateDale (scn,    0,  0, 9.0, 10.5, 29) 

#toit, oppose labo informatique
CreateDale (scn, 66.5,  0, 9.0, 10.5, 29) 

#toit chapelle
CreateDale (scn,   33,  5, 6.5,   12, 24)

CreateDale (scn,    0, 39, 9.0, 10.5,  6)

#facade
CreateDale (scn,    0, 29, 9.0, 66.5, 10)


#toiture micro-theatre
da = CreateDale   (scn, 0,  39, 6.0, 6.0, 4.0)   # teto
da.RotX = -math.pi/6.0
Colorize (da, 238.0/255.0, 92.0/255.0, 66.0/255.0)


#toiture chemin xerox
da = CreateDale   (scn, 62,  39, 3.3, 1.8, 25)
da.RotY = -math.pi/6.0
Colorize (da, 238.0/255.0, 92.0/255.0, 66.0/255.0)

da = CreateDale   (scn, 64,  39, 3.3, 1.8, 25)
da.RotY = math.pi/6.0
Colorize (da, 238.0/255.0, 92.0/255.0, 66.0/255.0)


#CreateEchelle (scn, 10, 50, 0, 30, 50, 30, 3, 10)

scn.setLayers ([1,2,3,4])

#print k_counter

Window.RedrawAll (-1)
