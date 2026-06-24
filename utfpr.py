import os
import bpy
import math

# --- Python 2 to Python 3 Compatibility Updates ---
xrange = range

# --- Monkeypatching Modern Objects with Legacy Rotation Properties ---
def get_rotx(self): return self.rotation_euler[0]
def set_rotx(self, val): self.rotation_euler[0] = val
bpy.types.Object.RotX = property(get_rotx, set_rotx)

def get_roty(self): return self.rotation_euler[1]
def set_roty(self, val): self.rotation_euler[1] = val
bpy.types.Object.RotY = property(get_roty, set_roty)

def get_rotz(self): return self.rotation_euler[2]
def set_rotz(self, val): self.rotation_euler[2] = val
bpy.types.Object.RotZ = property(get_rotz, set_rotz)

# --- Global Configurations ---
k_counter = 0

# Set to False to cut doors and windows; set to True to ignore cuts (Original default)
flag_no_doors = True 
current_collection = bpy.context.scene.collection


def move_to_current_collection(obj):
    """Ensures the object belongs exclusively to the active layer collection."""
    global current_collection
    if obj.name not in current_collection.objects:
        current_collection.objects.link(obj)
    for col in obj.users_collection:
        if col != current_collection:
            col.objects.unlink(obj)


def Colorize(ob, r, g, b):
    global k_counter
    k_counter += 1
    mat_name = f"cl_{k_counter}"

    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    
    if principled:
        principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
        principled.inputs['Alpha'].default_value = 0.2  # Matches old transparency
    
    # Viewport shading properties
    mat.diffuse_color = (r, g, b, 0.2)
    mat.blend_method = 'BLEND'

    if not ob.data.materials:
        ob.data.materials.append(mat)
    else:
        ob.data.materials[0] = mat


def CreateDale(scn, x, y, z, sx, sy):
    global k_counter
    k_counter += 1
    name = f"p{k_counter}"

    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.active_object
    ob.name = name

    # Transform and apply transformations for clean boolean operations
    ob.scale = (sx, sy, 0.2)
    bpy.ops.object.transform_apply(scale=True, location=False, rotation=False)
    ob.location = (x + (sx / 2.0), y + (sy / 2.0), z - 0.2)
    
    move_to_current_collection(ob)
    Colorize(ob, 238./255., 233./255., 233./255.)
    return ob


def CreateSphere(scn, x, y, z, radius):
    global k_counter
    k_counter += 1
    name = f"p{k_counter}"

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=radius, location=(x, y, z))
    ob = bpy.context.active_object
    ob.name = name
    
    move_to_current_collection(ob)
    return ob


def CreateHemisphere(ox, oy, oz, ray): 
    global k_counter
    k_counter += 1
    
    mesh_data = bpy.data.meshes.new(name=f"mesh_p{k_counter}")
    ob = bpy.data.objects.new(f"p{k_counter}", mesh_data)
    
    n = 16
    r_factor = (ray / 5.0) * 2.0
    
    verts = []
    grid = {}
    v_idx = 0

    # Generate explicit hemispherical vertices (z >= 0)
    for i in range(n):
        lat = -math.pi/2.0 + i * math.pi / (n - 1)
        z_val = math.sin(lat)
        if z_val >= -1e-5:
            for j in range(n):
                lon = j * math.pi * 2.0 / (n - 1)
                x_val = math.sin(lon) * math.cos(lat)
                y_val = math.cos(lon) * math.cos(lat)
                verts.append((x_val * r_factor, y_val * r_factor, z_val * r_factor))
                grid[(i, j)] = v_idx
                v_idx += 1
                
    faces = []
    for i in range(n - 1):
        for j in range(n - 1):
            if (i, j) in grid and (i, j+1) in grid and (i+1, j+1) in grid and (i+1, j) in grid:
                faces.append([grid[(i, j)], grid[(i, j+1)], grid[(i+1, j+1)], grid[(i+1, j)]])

    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()
    
    ob.location = (ox, oy, oz)
    move_to_current_collection(ob)
    return ob


def CreateMarche(scn, x, y, z, sx, sy, sz):
    global k_counter
    k_counter += 1
    name = f"p{k_counter}"

    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.active_object
    ob.name = name

    ob.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True, location=False, rotation=False)
    ob.location = (x + (sx / 2.0), y + (sy / 2.0), z + (sz / 2.0))
    
    move_to_current_collection(ob)
    Colorize(ob, 238./255., 233./255., 233./255.)
    return ob


def CreateParois(scn, x, y, z, sx, sy, sz):
    return CreateMarche(scn, x, y, z, sx, sy, sz)


def CreateEchelle(scn, x, y, z, x2, y2, z2, largeur, nmarches):
    dx = x2 - x
    dy = y2 - y
    dz = z2 - z
    
    sx = dx / nmarches
    sy = dy / nmarches
    sz = dz / nmarches
    
    nmarches = int(nmarches)

    print(dx, dy, dz, sx, sy, sz)
    
    if (0 == dx):
        for i in xrange(nmarches):
            CreateMarche(scn, x, y + (i * sy), z + (i * sz), largeur, sy, sz)
    else:
        for i in xrange(nmarches):
            CreateMarche(scn, x + (i * sx), y, z + (i * sz), sx, largeur, sz)
	

def CreerChaise(scn, x, y, z, direction):
    dx = 0.35
    dy = 0.40

    if (1 == direction):
        dx = -dx
	
    CreateMarche(scn, x, y, z, 0.05, 0.05, 0.50)
    CreateMarche(scn, x + dx, y, z, 0.05, 0.05, 0.50)
    CreateMarche(scn, x, y + dy, z, 0.05, 0.05, 1.10)
    CreateMarche(scn, x + dx, y + dy, z, 0.05, 0.05, 1.10)
    CreateMarche(scn, x, y, z + .50, abs(dx), dy, 0.05)
    CreateMarche(scn, x, y + dy, z + .50, dx, 0.05, 0.60)


def openHole(scn, obj1, x, y, z, sx, sy, sz): 
    if flag_no_doors:
        return obj1
	
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    hole_ob = bpy.context.active_object
    hole_ob.name = "furo"
    hole_ob.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True, location=False, rotation=False)
    hole_ob.location = (x + (sx / 2.0), y + (sy / 2.0), z + (sz / 2.0))

    # Apply boolean operator contextually
    bpy.ops.object.select_all(action='DESELECT')
    obj1.select_set(True)
    bpy.context.view_layer.objects.active = obj1

    mod = obj1.modifiers.new(name="HoleBool", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = hole_ob
	
    bpy.ops.object.modifier_apply(modifier=mod.name)
	
    bpy.ops.object.select_all(action='DESELECT')
    hole_ob.select_set(True)
    bpy.ops.object.delete()

    obj1.select_set(True)
    bpy.context.view_layer.objects.active = obj1
    return obj1


def Texturize(me, texpath):
    # Legacy texture logic stub to ensure no failure breaks if uncommented
    pass


# --- Legacy Scene Manager Wrapper ---
class SceneWrapper:
    def setLayers(self, layers):
        global current_collection
        if not layers: return
        col_name = f"Layer_{layers[0]}"
        if col_name not in bpy.data.collections:
            col = bpy.data.collections.new(col_name)
            bpy.context.scene.collection.children.link(col)
        current_collection = bpy.data.collections[col_name]


# --- Clear Environment and Initialize Script Environment ---
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

# Total cleanup of prior generations
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for mesh in bpy.data.meshes: bpy.data.meshes.remove(mesh)
for mat in bpy.data.materials: bpy.data.materials.remove(mat)
for col in list(bpy.data.collections): 
    if col.name.startswith("Layer_"): bpy.data.collections.remove(col)

scn = SceneWrapper()

# =====================================================
# EXECUTION GENERATION (Original Script Core Logic)
# =====================================================

# sous sol
scn.setLayers([1])
da = CreateDale(scn, 0,  39, -1.0, 62, 65)   # GRAMADO
Colorize(da, .3, .6, .3)

CreateDale(scn,     0,  0, -3, 10.5, 29)
CreateDale(scn,  66.5,  0, -3, 10.5, 29)
CreateDale(scn,     0, 29, -3, 66.5, 10)
CreateParois(scn,    70,  0, -3,  0.3,  29, 3)
CreateParois(scn,  66.5,  0, -3,  0.5,  29, 3)
CreateParois(scn,  76.5,  0, -3,  0.5,  29, 3)
CreateParois(scn,   6.5,  0, -3,  0.3,  29, 3)
CreateParois(scn,     0,  0, -3,  0.5,  39, 3)
CreateParois(scn,  10.5,  0, -3,  0.5,  29, 3)

da = CreateParois(scn,     0, 39, -3, 66.5, 0.5, 3)
Colorize(da, 105./255., 105./255., 105./255.)

CreateParois(scn,  10.5, 29, -3, 66.5, 0.5, 3)
CreateParois(scn,  10.5, 35, -3, 66.5, 0.5, 3)
CreateParois(scn,     0,  0, -3, 10.5, 0.5, 3)
CreateDale(scn,  10.5, 0, -2,  10, 29)

# chemin xerox
CreateDale(scn, 62,  39, 0.1, 3, 25)
CreateDale(scn, 62,  39, 3.1, 3, 25)
CreateParois(scn,  65, 39, 0, 0.2, 25, 3)
da = CreateParois(scn,  62, 39, -1.0, 0.2, 25, 2.0)

# rez de chausse
scn.setLayers([2])
CreateDale(scn,     0,  0, 0, 10.5, 29) 
CreateDale(scn,  66.5,  0, 0, 10.5, 29) 
CreateDale(scn,     0, 29, 0, 10.5, 10) 
CreateDale(scn,  10.5, 35, 0,  6.0, 4.5)  
CreateDale(scn,  15.5, 29, 0, 60.0, 10) 
CreateDale(scn,  33,  5, 0,   12, 24)
CreateDale(scn,     0, 39, 0, 10.5,  6.5)

CreateParois(scn,  0.0,  45.0, -1.0, 10.5, 0.5, 6.0)
CreateParois(scn, 10.5,  39.0, -1.0,  0.2, 6.5, 6.0)
CreateParois(scn,  0.0,  39.0, -1.0,  0.2, 6.5, 6.0)
CreateParois(scn, 0,  0,  0,   1, 0.5, 5)

CreateParois(scn, 0, 28,  0, 6.5,  .3, 5)
CreateParois(scn, 0, 17,  0, 6.5,  .3, 5)
CreateParois(scn, 0,  9,  0, 6.5,  .3, 5)
CreateParois(scn, 0,  4,  0, 6.5,  .3, 5)

da = CreateParois(scn,   6.5,  0, 0,  0.3,  39, 5)
da2 = openHole(scn, da , 6, 37, 0.0, 1.0, 1.5, 3.0)
da  = openHole(scn, da2, 6, 19, 0.0, 1.0, 1.5, 3.0)
da2 = openHole(scn, da , 6, 11, 0.0, 1.0, 1.5, 3.0)
da  = openHole(scn, da2, 6,  6, 0.0, 1.0, 1.5, 3.0)
da2 = openHole(scn, da , 6,  2, 0.0, 1.0, 1.5, 3.0)

da = CreateParois(scn,   0.0,  0, 0,  0.5,  45, 5)
for y in [2, 6, 10, 11, 12.5, 14, 15.5, 18, 19.5, 21, 22.5, 24, 25.5, 29, 30.5, 32, 33.5, 35, 36.5]:
	da2 = openHole(scn, da, -0.6, y, 1.2,   1.5, 1.0, 2.0)
	da  = da2
	da2 = None

CreateParois(scn,  67,  0, 0,  0.5,  35, 5)
CreateParois(scn,    70,  0, 0,  0.3,  34, 5)
CreateParois(scn,  76.5,  0, 5,  0.5,  35, 5) # Layer 3 fix safely grouped inside old sequence
CreateParois(scn,  10.5, 29, 0,   22, 0.5, 5)
CreateParois(scn,    45, 29, 0,   22, 0.5, 5)
CreateParois(scn,  15.0, 29.0, 0, 0.5, 6.0, 5.0)
CreateParois(scn,  10.5+4.5, 35, 0,   57-4.5, 0.5, 5)

CreateEchelle(scn, 10.5, 35.0, 0.0, 10.5, 30.0, 2.5, 2.0, 8.0)
CreateEchelle(scn, 12.5, 30.0, 2.0, 12.5, 35.0, 5.0, 2.0, 8.0)
CreateEchelle(scn, 12.5, 31.0,-3.0, 12.5, 35.0, 0.0, 2.0, 8.0)

da  = CreateParois(scn,  10.5,  0,  0, 0.5,  33, 5)
da2 = openHole(scn, da, 10.5, 18, 0.0, 1.0, 2.0, 3.0)
CreateEchelle(scn, 10.5, 18.0,  0, 13.0, 18.0, -2.0, 2, 12)

CreateParois(scn,    33,  5, 0,  12, 0.5, 6.5)
da = CreateParois(scn,  32.5,  5, 0, 0.5, 24, 6.5)
openHole(scn, da, 32.5, 7, 0.0,   1.0, 3.0, 6.5)
CreateParois(scn,  32.5,  28, 0, 0.5, 7, 4.9)

da = CreateParois(scn,    45,  5, 0, 0.5,  24, 6.5)
openHole(scn, da, 45, 7, 0.0,   1.0, 3.0, 6.5)
CreateParois(scn,  45,  28, 0, 0.5, 7, 4.9)

CreateDale(scn,   0.0, -10,  0,  15, 10)
CreateDale(scn,  15.0, -10.0,  1.0,  62.0, 7.0)
CreateDale(scn,  11.0,  -3.0,  1.0,  66.0-10.5-1.0,  3.0)
CreateDale(scn,  66.0,  -3.0,  0.0,  10.0,  3.0)

CreateEchelle(scn, 10.,  -2.3,  0, 11.2, -2.3, 0.90, 2.2, 5)
CreateEchelle(scn, 66.0-1.0,  -3.0,  1.0, 66.0, -3.0, 0.0, 3.0, 5)
CreateParois(scn,     0, -10,  0,    77, 0.5, 5)

CreateParois(scn,  10.5 - 3.5,  -10,  0,  0.3, 7, 5)
CreateParois(scn,  15.0,  -10,  0,  0.3, 7, 5)
CreateParois(scn,  30.0,  -10,  0,  0.3, 7, 5)
CreateParois(scn,  40.0,  -10,  0,  0.3, 7, 5)
CreateParois(scn,  50.0,  -10,  0,  0.3, 7, 5)

da = CreateParois(scn,  10.5 - 3.5,   -3,  0,  66.5+3.5, 0.5, 5)
da2 = openHole(scn, da, 8.0, -3.1, 0, 1.0, 1.0, 2.5)
da  = da2
da2 = None
for x in [16, 31, 41, 51]:
	da2 = openHole(scn, da, x, -3.1, 1.0,   1.0, 1.0, 2.0)
	da  = da2
	da2 = None

CreateParois(scn,     0,   0,  1,   6.5, 0.5, 5)
CreateParois(scn,  10.5,   0,  1,  66.5, 0.5, 5)
CreateParois(scn,  76.5, -10,  1,   0.5,  10, 5)
CreateDale(scn,   0.0, 0,  0,  10.5, 29)

da = CreateParois(scn, 0, 39, 0.0,   66.0, 0.5, 5.0)
Colorize(da, 238./255., 130./255., 98./255.)
centre = 56.0 / 2.0

da2 = openHole(scn, da, 10.5 + centre, 39, 0.0,   2.0, 1.0, 3.0)  
da = da2
da2 = None
CreateEchelle(scn, 10.5+centre, 41.4, -1.0, 10.5+centre, 39.0, 0.1, 2.0, 10.0)

da2 = openHole(scn, da, 8, 39, 0.0,   1.0, 1.0, 3.0)  
centre = 10.5 + (56.0 / 2.0)
da = da2
da2= None

for n in range(9):
	da2 = openHole(scn, da, centre + 3.0 + (2.0 * n), 39, 1.2,   1.5, 1.0, 2.0)
	da  = da2
	da2 = None
	da2 = openHole(scn, da, centre - 3.0 - (2.0 * n), 39, 1.2,   1.5, 1.0, 2.0)
	da  = da2
	da2 = None

CreateEchelle(scn, 68.0, 39.0, 0.0, 68.0, 42.0, 2.5, 2.0, 11.0)
CreateEchelle(scn, 70.0, 42.0, 2.5, 70.0, 39.0, 4.8, 2.0, 11.0)
CreateDale(scn, 68.0, 42.0, 2.5+0.2, 4.0, 1.0)

# premier etage
scn.setLayers([3])
CreateParois(scn, 66.0,  39.0,  0.0,  0.5, 4.0, 10.0)
CreateParois(scn, 66.0,  43.0,  0.0,  6.5, 0.5, 10.0)
CreateParois(scn, 72.0,  39.0,  0.0,  0.5, 4.0, 10.0)
CreateDale(scn, 66.0,  39.0, 10.0,  6.5, 4.0)

da = CreateHemisphere(69, 41, 11, 5.0)
Colorize(da, 238.0/255.0, 92.0/255.0, 66.0/255.0)
cx, cy, ray = 69, 41, 1.8

for idx in range(1, 7):
	CreateParois(scn, cx+ray*math.cos(2*idx*math.pi/6), cy+ray*math.sin(2*idx*math.pi/6), 10.0, 0.2, 0.2, 1.3)
	
CreateParois(scn, 72.0,  39.0,  0.0,  0.5, 4.0, 10.0)
da = CreateDale(scn, 10.5,-10, 5, 66.0, 10)
CreateDale(scn,    0,  0, 5, 10.5,  39)
CreateDale(scn, 66.5,  0, 5, 10.5,  29)

CreateParois(scn, 10.5,  39.0, 5.0,  0.2, 6.5, 4.0)
CreateParois(scn,  0.0,  39.0, 5.0,  0.2, 6.5, 4.0)
CreateDale(scn,   10.5+4, 29, 5, 60.0,  10)
CreateDale(scn,   10.5  , 35, 5, 4.0,  4.0)
CreateDale(scn,    0, 39, 5, 10.5,   6)
CreateDale(scn, 10.5,-10, 5, 66.5,  10)

CreateParois(scn, 10.5,  0, 5,  0.5,  29, 4.0)
CreateParois(scn,  6.5,  0, 5,  0.3,  29, 4.0)
CreateParois(scn, 66.5,  0, 5,  0.5,  29, 4.0)
CreateParois(scn, 76.5,  0, 5,  0.5,  29, 4.0)
CreateParois(scn,   70,  0, 5,  0.3,  29, 4.0)
CreateParois(scn,    0, 45, 5, 10.5, 0.5, 4.0)
CreateParois(scn, 10.5, 29, 5, 66.5, 0.5, 4.0)

da = CreateParois(scn,    0,  0, 5,  10.5, 0.5, 4.0)
Colorize(da, .2, 0, .8)
CreateParois(scn,   0.0,  0, 5.0,  0.5,  45, 4)

da = CreateParois(scn, 10.5, 39, 5.0,   56, 0.5, 4.0)
Colorize(da, 238./255., 130./255., 98./255.)
centre = 10.5 + (56.0 / 2.0)

da2 = None
for n in range(9):
	da2 = openHole(scn, da, centre + 3.0 + (2.0 * n), 39, 6.5,   1.5, 1.0, 1.6)
	da  = da2
	da2 = None
	da2 = openHole(scn, da, centre - 3.0 - (2.0 * n), 39, 6.5,   1.5, 1.0, 1.6)
	da  = da2
	da2 = None

# toiture
scn.setLayers([4])
CreateDale(scn,    0,  0, 9.0, 10.5, 29) 
CreateDale(scn, 66.5,  0, 9.0, 10.5, 29) 
CreateDale(scn,   33,  5, 6.5,   12, 24)
CreateDale(scn,    0, 39, 9.0, 10.5,  6)
CreateDale(scn,    0, 29, 9.0, 66.5, 10)

da = CreateDale(scn, 0,  39, 6.0, 6.0, 4.0)   
da.RotX = -math.pi/6.0
Colorize(da, 238.0/255.0, 92.0/255.0, 66.0/255.0)

da = CreateDale(scn, 62,  39, 3.3, 1.8, 25)
da.RotY = -math.pi/6.0
Colorize(da, 238.0/255.0, 92.0/255.0, 66.0/255.0)

da = CreateDale(scn, 64,  39, 3.3, 1.8, 25)
da.RotY = math.pi/6.0
Colorize(da, 238.0/255.0, 92.0/255.0, 66.0/255.0)

print("Building Generation Complete.")


# Define where you want to save the file (this saves to your Desktop)
#desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
#output_file = os.path.join(desktop_path, "generated_building.gltf")

output_file = "Modelo_UTFPR"

print(f"Exporting geometry to: {output_file}")

# Export to glTF 2.0 format 
# (Change to bpy.ops.export_scene.fbx for FBX format if preferred)
bpy.ops.export_scene.gltf(
    filepath="UTFPR.glb", 
    export_format='GLB', # Packages textures/geometry into one file
    use_selection=False            # Exports everything in the scene
)

# FBX
bpy.ops.export_scene.fbx(filepath="UTFPR.fbx")

# OBJ
bpy.ops.wm.obj_export(filepath="UTFPR.obj")

# STL
bpy.ops.wm.stl_export(filepath="UTFPR.stl")


print("Export Complete! Exiting Blender.")
