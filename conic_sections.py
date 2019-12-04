import bpy
import bmesh
import numpy as np

rr = 50

def apply_boolean(obj_A, obj_B, bool_type = 'INTERSECT'):
    
    print('+++',obj_A, obj_B)
    bpy.ops.object.select_all(action='DESELECT')
    obj_A.select= True
    
    bpy.context.scene.objects.active = obj_A
    bpy.ops.object.modifier_add(type='BOOLEAN')

    mod = obj_A.modifiers
    mod[0].name = obj_A.name + bool_type
    mod[0].object = obj_B
    mod[0].operation = bool_type

    bpy.ops.object.modifier_apply(apply_as='DATA', 
								  modifier=mod[0].name)

def cut(obj_A, obj_B):
    
    print(obj_A, obj_B)
    bpy.ops.object.select_all(action='DESELECT')
    obj_A.select= True
    bpy.context.scene.objects.active = obj_A
    bpy.ops.object.duplicate()
    cpy = bpy.context.scene.objects.active
    
    apply_boolean(cpy, obj_B, bool_type = 'INTERSECT')
  
    apply_boolean(obj_A, obj_B, bool_type = 'DIFFERENCE')
    
    return cpy
    


def mk_cubes(scale_factor=40):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cube_add(location = [0,0,0]) 
    bb = bpy.context.scene.objects.active

    me = bpy.context.object.data
    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me) 
    bm.verts.ensure_lookup_table()

    for v in  bm.verts:
        v.co.z += 1
        #v.co.x -= 1

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    bm.free()  # free and prevent further access
      

    bb.scale = [scale_factor,scale_factor,scale_factor]
   

    cubes = [bb]
    for rot in [-np.pi/6,-np.pi/3 -.2, -np.pi/2] :
        bpy.ops.object.duplicate()
        bb = bpy.context.scene.objects.active
        bb.rotation_euler = [0,rot,0]
        cubes.append(bb)
    
    cubes[0].location = [0,0,12]
    cubes[1].location = [0,0,8]
    cubes[2].location = [0,0,-5]
    cubes[3].location = [10,0,0]
    
    return cubes


bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cone_add(location = [0,0,0] ) 
cone = bpy.context.scene.objects.active
print('>>',cone)
rr = 20
cone.scale = [rr,rr,rr]

bpy.ops.mesh.primitive_cylinder_add(location = [0,0,0] ) 
peg = bpy.context.scene.objects.active
peg_width = 1.5



boxes = mk_cubes()

cones = []
for bb in boxes:
    cones.append(cut(cone,bb))

#clean up before placing the peg
bpy.ops.object.select_all(action='DESELECT')
for box in  boxes:
	box.select = True
#get rid of the
bpy.ops.object.delete() 

peg.scale = [peg_width,peg_width,6]
peg.location = [0,0,8]
#cut holes using the peg
for obj in cones[:2]:
    apply_boolean(obj,peg, bool_type = 'DIFFERENCE')
    

#shrink the peg before gluing it to the base
peg.scale = [peg_width - .2,peg_width - .2 ,6]
apply_boolean(cones[2],peg, bool_type = 'UNION')
    

peg.rotation_euler = [0,np.pi/2,0]
peg.location = [3,0,-16]

peg.scale = [peg_width,peg_width,11]
apply_boolean(cone,peg, bool_type = 'DIFFERENCE')
apply_boolean(cones[2],peg, bool_type = 'DIFFERENCE')

peg.scale = [peg_width - .2,peg_width - .2 ,11]
apply_boolean(cones[3],peg, bool_type = 'UNION')


bpy.ops.object.select_all(action='DESELECT')
peg.select = True
bpy.ops.object.delete() 

 
    