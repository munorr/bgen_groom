bl_info = {
    "name": "BGEN Groom",
    "author": "Munorr",
    "version": (1, 1, 2),
    "blender": (3, 5, 0),
    "location": "View3D > N",
    "description": "Control parameters from B-GEN v2 geometry node hair system",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy
import os
import time

from . import addon_updater_ops
from bpy.utils import previews
icons = previews.new()
icons.load(
    name='BGEN_GROOM',
    path=os.path.join(os.path.dirname(__file__), "bgen_groom_1080.png"),
    path_type='IMAGE'
)

# [FUNCTIONS]       
#=================================================================================

nodeID_1 = "ID:BV2_0001"
nodeID_2 = "ID:B-GEN_0002"
nodeID_3 = "ID:BV2_VtoS_0001"
nodeID_4 = "ID:BV2_GEN_HC"

def vts_nodes():
    vts = []
    for ng in bpy.data.node_groups:
        for node in ng.nodes:
            if node.name == nodeID_3:
                vts.append(ng.name)
    return vts

#=================================================================================================
#---------------------------------------- 01 [GETTERS]
#=================================================================================================
#== Gets the info of bgen nodes for curves attached to a mesh
def get_gNode(obj):
    #obj = bpy.context.active_object
    modName = ""
    nodeTreeName = "<NOT Applicable>"
    node_ID = ""
    try:
        if obj.modifiers:
            for modifier in obj.modifiers:
                if modifier.type == "NODES" and modifier.node_group:
                    a = obj.modifiers.get(modifier.name)
                    b = obj.modifiers.get(modifier.name).node_group.name
                    c = obj.modifiers.get(modifier.name).node_group
                    
                    if c:
                        for node in c.nodes:
                            if node.name == "ID:BV2_0001":
                                #print("Node present" , c.name)
                                modName = a
                                nodeTreeName = c.name
                                node_ID = "ID:BV2_0001"
                                break
                            elif node.name == "ID:B-GEN_0002":
                                #print("Node present" , c.name)
                                modName = a
                                nodeTreeName = c.name
                                node_ID = "ID:B-GEN_0002"
                                break
                            elif node.name == "ID:B-GEN_VtoS_0001":
                                #print("Node present" , c.name)
                                modName = a
                                nodeTreeName = c.name
                                node_ID = "ID:B-GEN_VtoS_0001"
                                break
                            elif node.name == "ID:BV2_GEN_HC":
                                #print("Node present" , c.name)
                                modName = a
                                nodeTreeName = c.name
                                node_ID = "ID:BV2_GEN_HC"
                                break
    except:
        pass              
    return modName, nodeTreeName, node_ID
#== Gets geometry node info for the vertex to strips
def get_gNode_2(obj):
    #obj = bpy.context.active_object
    vtsMod = ""
    nodeTreeName = "<NA>"
    node_ID = ""
    if obj.modifiers:
        for modifier in obj.modifiers:
            if modifier.type == "NODES" and modifier.node_group:
                a = obj.modifiers.get(modifier.name)
                b = obj.modifiers.get(modifier.name).node_group
                if b:
                    for node in b.nodes:
                        if node.name == "ID:BV2_VtoS_0001":
                            vtsMod = a
                            nodeTreeName = b.name
                            node_ID = "ID:BV2_VtoS_0001"
                            break

    return vtsMod, nodeTreeName, node_ID
#== Gets the list of curves attached to a mesh
def get_curveList():
    curveList = []
    obj = bpy.context.active_object
    if obj.type == "CURVES" and obj.parent:
        parent_obj = obj.parent
        #print(parent_obj)
        for child in parent_obj.children:
            if child.type == "CURVES":
                #print(child.name)
                curveList.append(child.name)
    if obj.type == "MESH" and obj.children:
        for child in obj.children:
            if child.type == "CURVES":
                #print(child.name)
                curveList.append(child.name)
                
    print(curveList)            
    return(curveList)

def get_sim_collection():
    simCol = []
    for coll in bpy.data.collections:
        if coll.name[:4] == "SIM=":
            simCol.append(coll)
    return simCol
        
def get_curveList_object():
    curveList = []
    obj = bpy.context.active_object
    if obj.type == "CURVES" and obj.parent:
        parent_obj = obj.parent
        #print(parent_obj)
        for child in parent_obj.children:
            if child.type == "CURVES":
                #print(child.name)
                curveList.append(child)
    if obj.type == "MESH" and obj.children:
        for child in obj.children:
            if child.type == "CURVES":
                #print(child.name)
                curveList.append(child)
                
    print(curveList)            
    return(curveList)

def get_bv2_curveList():
    curveList = []
    #obj = bpy.context.active_object
    #obj_ = bpy.data.objects[bpy.context.scene.bv2_tools.curveList]
    
    if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].children:
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index].children[0]
    else:
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        
    nodeID = get_gNode(obj_)[2]
    if obj_.type == "CURVES" and obj_.parent:
        parent_obj = obj_.parent
        #print(parent_obj)
        for child in parent_obj.children:
            if get_gNode(child)[2] != "":
                #print("node id is: " + nodeID)
                #print(child.name)
                curveList.append(child.name)
    if obj_.type == "MESH" and obj_.children:
        for child in obj_.children:
            if child.type == "CURVES" and get_gNode(child)[2] != "":
                #print(child.name)
                curveList.append(child.name)
                
    #print(curveList)            
    return(curveList)

def get_emitter(context)-> bpy.types.Object:
    scene_props = context.scene.bv2_tools
    if scene_props.pinned_obj:
        return scene_props.pinned_obj
    elif context.object and context.object.type != "CURVES":
        return context.object
    elif context.object and context.object.type == "CURVES" and context.object.parent and context.object.parent.type == "MESH":
        return context.object.parent

def has_curve_child(obj):
    if isinstance(obj, bpy.types.Object):
        for child in obj.children:
            if child.type == 'CURVES':
                return True
            elif child.type in ['EMPTY', 'ARMATURE']:
                if has_curve_child(child):
                    return True
    return False

def get_curveChild(obj):

    if obj.type == "MESH" and obj.children:
        child_obj = bpy.context.active_object.children
        childCurve = obj
        for child in child_obj:
                if child.type == "CURVES":
                    #dispCurve = bpy.context.scene.bv2_tools.curveList
                    dispCurve = bpy.context.active_object.hair_curves_active_index
                    childCurve = bpy.data.objects[dispCurve]
        return childCurve

    else:
        return obj
        
def get_materials():
    mattList = []
    for matt in bpy.data.materials:
        if matt.node_tree:
            #print(matt.node_tree.nodes)
            for node in matt.node_tree.nodes:
                #print(node)
                if node.name == 'ID:bv2_material':
                    #print(matt)
                    mattList.append(matt)
    return mattList

def get_hairCurve_list(obj):
    hcList = []
    if obj.type == "MESH":
        for hc in obj.children:
            hcList.append(hc)
        
    return hcList
#=========================================================================================================    
# 01 ---------------------------   [OPERATORS]
#=========================================================================================================
class BV2_OT_single_user(bpy.types.Operator):
    """ Make BGEN v2 modifier a single user """
    bl_idname = "object.bv2_single_user"
    bl_label = "Make single user"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):

        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False 
        
        obj_ =  bpy.data.objects[bpy.context.active_object.hair_curves_active_index]        
        modN = get_gNode(obj_)[0]
        ntN = get_gNode(obj_)[1]
        ntID = get_gNode(obj_)[2]
        if ntID == "":
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    def execute(self, context):
        obj_ =  bpy.data.objects[bpy.context.active_object.hair_curves_active_index]    
        node_group_name = get_gNode(obj_)[0].name
        org_mod = obj_.modifiers[node_group_name].node_group
        obj_.modifiers[node_group_name].node_group = obj_.modifiers[node_group_name].node_group.copy()
        
        return{'FINISHED'}

class BV2_OT_single_user_vts(bpy.types.Operator):
    """ Make sim modifier a single user """
    bl_idname = "object.bv2_single_user_vts"
    bl_label = "Make single user"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        vts_ = bpy.data.node_groups[bpy.context.scene.bv2_tools.vts_mod].copy()
        bpy.context.scene.bv2_tools.vts_mod = vts_.name
        return{'FINISHED'}
    
class BV2_OT_single_user_matt(bpy.types.Operator):
    """ Duplicate bgen Material """
    bl_idname = "object.bv2_single_user_matt"
    bl_label = "Duplicate bgen Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        mts_ = bpy.data.materials[bpy.context.scene.bv2_tools.mattList].copy()
        bpy.context.scene.bv2_tools.mattList = mts_.name
        return{'FINISHED'}
    
class BV2_OT_rename_nodeTree(bpy.types.Operator):
    """ Rename the current nodeTree"""
    bl_idname = "object.bv2_rename_nodetree"
    bl_label = "Rename bgen NodeTree"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        modN = get_gNode(obj_)[0]
        ntN = get_gNode(obj_)[1]
        ntID = get_gNode(obj_)[2]
        if ntID == "":
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"  

    ntName:bpy.props.StringProperty(name="Rename NodeTree", description="Rename bgen nodetree", default="bv2_")
    
    def execute(self, context):
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        node_group_name = get_gNode(obj_)[0].name
        obj_.modifiers[node_group_name].node_group.name = self.ntName
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class BV2_OT_generate_guides(bpy.types.Operator):
    """Adds Generate Guides modifier"""
    bl_idname = "object.bv2_generate_guides"
    bl_label = "Generate Guides"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if bpy.context.active_object.hair_curves_active_index < 0:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    def execute(self, context):
        objs = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        
        mod_01 = objs.modifiers.new(name="geometry_nodes_mod", type='NODES')
        mod_01.node_group = bpy.data.node_groups['00_bv2_Generate_guides']
        #mod1_index = objs.modifiers.find(mod_01.name)
        #objs.modifiers.move(mod1_index, 0)
        
        modName = objs.modifiers[-1].name
        objs.modifiers[modName]["Input_2"] = objs.parent
        objs.modifiers[modName]["Input_18_attribute_name"] = bpy.data.hair_curves[objs.data.name].surface_uv_map
        return{'FINISHED'}

class BV2_OT_apply_guides(bpy.types.Operator):
    """Applies the Guides modifier"""
    bl_idname = "object.bv2_apply_guides"
    bl_label = "Apply Guides"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        return context.mode == "OBJECT" or "SCULPT_CURVES" or "EDIT"
    
    def execute(self, context):
        objs = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        
        if len(objs.modifiers) > 0:
            first_modifier = objs.modifiers[-1]
            
            if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport == True:
                bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport = False
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                bpy.context.view_layer.objects.active = objs
                bpy.ops.object.modifier_apply(modifier=first_modifier.name)
                bpy.ops.object.editmode_toggle()
                bpy.ops.object.editmode_toggle()
                bpy.ops.curves.sculptmode_toggle()
                bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport = True
                
            else:
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                bpy.context.view_layer.objects.active = objs
                bpy.ops.object.modifier_apply(modifier=first_modifier.name)
                bpy.ops.object.editmode_toggle()
                bpy.ops.object.editmode_toggle()
                bpy.ops.curves.sculptmode_toggle()
        return{'FINISHED'}

class BV2_OT_delete_guides(bpy.types.Operator):
    """Deletes the Guides modifier"""
    bl_idname = "object.bv2_delete_guides"
    bl_label = "Delete Guides"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    def execute(self, context):
        objs = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        #while objs.modifiers:
        objs.modifiers.remove(objs.modifiers[-1])
            
        return{'FINISHED'}    

class BV2_OT_remove_sim_collection(bpy.types.Operator):
    """ Remove Sim Collection """
    bl_idname = "object.bv2_remove_sim_collection"
    bl_label = "Remove Sim Collection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        aObj = bpy.context.active_object
        
        if bpy.context.scene.bv2_tools.sim_collection:
            colls = bpy.data.collections[bpy.context.scene.bv2_tools.sim_collection]
            for obj in colls.objects:
                colls.objects.unlink(obj)
                bpy.data.objects.remove(obj)

            bpy.data.collections.remove(colls) 
            bgenMod = get_gNode(bpy.data.objects[bpy.context.active_object.hair_curves_active_index])[0]
            bgenMod["Input_2"] = False
        else:    
            self.report({"ERROR"},message="NO SIM COLLECTIONS")
            return {"CANCELLED"}

        return{'FINISHED'}
      
class BV2_OT_choose_nodeTree(bpy.types.Operator):
    """ Choose which bgen Node to use"""
    bl_idname = "object.bv2_choose_nodetree"
    bl_label = "Choose bgen Node"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False

        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        modN = get_gNode(obj_)[0]
        ntN = get_gNode(obj_)[1]
        ntID = get_gNode(obj_)[2]
        if ntID == "":
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    bv2_nodes:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.node_groups for bn in b.nodes if bn.name == "ID:BV2_0001"],
        name="Change Modifier to:",
        description="Select bgen modifier",)
    
    def execute(self, context):
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        node_group_name = get_gNode(obj_)[0].name
        org_mod = obj_.modifiers[node_group_name].node_group
        obj_.modifiers[node_group_name].node_group = bpy.data.node_groups[self.bv2_nodes]
        return{'FINISHED'}
    
class BV2_OT_add_empty_hair(bpy.types.Operator):
    """ Add Empty hair curve """
    bl_idname = "object.bv2_add_ehc"
    bl_label = "Add Curve Empty Hair"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):

        active = context.active_object
        if active is None:
            return False
        if active.type != "MESH":
            return False
        if active.type == "MESH":
            if len(active.data.polygons) ==0:
                return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        return context.mode == "OBJECT" 
    
    name: bpy.props.StringProperty(name="Curve Name", description="Enter a name for the new hair curve", default="hair_")
    
    hairType: bpy.props.EnumProperty(
        items=(('EXISTING', "Use Existing", "Use existing bgen modifier"),
               ('NEW', "Create New", "Create with new hair modifier")),
        default='EXISTING',)
    
    bv2_nodes:bpy.props.EnumProperty(
        items=lambda self, context: [(b.name, b.name, "") for b in bpy.data.node_groups for bn in b.nodes if bn.name == "ID:BV2_0001"],
        name="BV2 Hair Modifiers",
        description="Select bgen modifier",)
      
    ng_name: bpy.props.StringProperty(name="Hair Mod name", description="Enter a name for the hair modifier", default="bgen_v2_")
    
    '''   
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self) '''
    
    def invoke(self, context, event):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        resource_folder = os.path.join(dirpath,"resources")
        nodelib_path = os.path.join(resource_folder, "bgen_v2_nodes.blend")

        def load_node(nt_name, link=True):
            if not os.path.isfile(nodelib_path):
                return False

            with bpy.data.libraries.load(nodelib_path, link=link) as (data_from, data_to):
                if nt_name in data_from.node_groups:
                    data_to.node_groups = [nt_name]
                    return True
            return False

        def load_material(nt_name, link=True):
            if not os.path.isfile(nodelib_path):
                return False

            with bpy.data.libraries.load(nodelib_path, link=link) as (data_from, data_to):
                if nt_name in data_from.materials:
                    data_to.materials = [nt_name]
                    return True
            return False
        
        if "bgen_v2_nodes" not in bpy.data.node_groups:
            load_node("bgen_v2_nodes", link=False)
            
        if "bgen_v2_hair" not in bpy.data.node_groups:
            load_node("bgen_v2_hair", link=False)

        if "BV2_Hair_Shader" not in bpy.data.materials:
            load_material("BV2_Hair_Shader", link=False)

        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        
        layout = self.layout
        col = layout.column()
        col_ = col.column()
        col_.scale_y = 1.2
        col_.prop(self,"name")
        col_.separator()
        
        box = col.box()
        col_ = box.column()
        col_.scale_y = 1.6
        row_ = col_.row()
        
        row_.prop(self,"hairType", expand = True)
        if self.hairType == "EXISTING":
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Hair Modifiers")
            grid_r.prop(self,"bv2_nodes", text = "")
        else:
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Name Modifier")
            grid_r.prop(self,"ng_name", text = "")
            
    def execute(self, context):
        aObj = bpy.context.active_object
        x = aObj.location[0]
        y = aObj.location[1]
        z = aObj.location[2]

        if aObj.type == "MESH":
            #Create new empty curve
            #------------------------------------------------------------------------------------------------
            uv_name = aObj.data.uv_layers.active.name
            bpy.ops.object.curves_empty_hair_add(align='WORLD', location=(x, y, z), scale=(1, 1, 1))
            hc_obj = bpy.context.active_object  #hair curve object
            #------------------------------------------------------------------------------------------------
            #Remove empty curve modifiers and make active
            #------------------------------------------------------------------------------------------------
            while hc_obj.modifiers:
               hc_obj.modifiers.remove(hc_obj.modifiers[0])
            hc_obj.name = self.name
            #bpy.ops.object.location_clear(clear_delta=False)
            bpy.context.view_layer.objects.active = hc_obj.parent
            #------------------------------------------------------------------------------------------------
            if self.hairType == "NEW": #If new hair modifier
                ''' Gets the geoNode hair modifier''' 
                get_mod_01 = bpy.data.node_groups.get("bgen_v2_hair")
                mod_01 = hc_obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
                mod_01.node_group = get_mod_01
                mod_01.node_group = mod_01.node_group.copy()
                mod_01.node_group.name = self.ng_name
            else:
                '''Uses existing one''' 
                mod_01 = hc_obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
                mod_01.node_group = bpy.data.node_groups[self.bv2_nodes]
            
            modName = get_gNode(hc_obj)[0].name
            hc_obj.modifiers[modName]["Input_41"] = uv_name
            hc_obj.modifiers[modName]["Input_14"] = hc_obj.parent
            #hc_obj.modifiers[modName]["Input_47"] = True
            #hc_obj.modifiers[modName]["Input_46"] = hg_obj
            hc_obj.modifiers[modName]["Input_2"] = False
            
            hc_obj.hide_select = True
            
            bpy.ops.object.select_all(action='DESELECT')
            #bpy.context.collection.objects.link(hc_obj)
            bpy.context.view_layer.objects.active = hc_obj
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.editmode_toggle()
            bpy.ops.curves.sculptmode_toggle()
            
            bpy.context.object.hair_curves_active_index = get_hair_curves_active_index(hc_obj)
            
            
        else:
            self.report({"ERROR"},message="Not a mesh object")
            return {"CANCELLED"}
        return{'FINISHED'}
    
class BV2_OT_remove_empty_hair(bpy.types.Operator):
    """ Deletes Higlighted hair curve """
    bl_idname = "object.bv2_remove_ehc"
    bl_label = "Delete Hair Curve"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if bpy.context.active_object.hair_curves_active_index < 0:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    def execute(self, context):
        
        objs = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        obj_mode = bpy.ops.object.mode_set(mode='OBJECT')
        
        if objs.type == "CURVES":
            parent_obj = objs.parent
            if bpy.context.object.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
                
            bpy.ops.object.select_all(action='DESELECT')
            
            if objs.children:
                for child in objs.children:
                    child.hide_select = False
                    child.hide_viewport = False
                    child.select_set(True)
                    bpy.ops.object.delete(use_global=True)
                    
            objs.hide_select = False
            objs.hide_viewport = False
            objs.select_set(True)
            bpy.ops.object.delete(use_global=True)

            
            bpy.context.view_layer.objects.active = parent_obj
            parent_obj.select_set(True)
                
        else:
            self.report({"ERROR"},message="Not a Curve object")
            return {"CANCELLED"}
        return{'FINISHED'}
        
class BV2_OT_hide_hair_curve(bpy.types.Operator):
    """ Remove Empty hair curve """
    bl_idname = "object.bv2_hide_hc"
    bl_label = "Hide Hair Curve"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):

        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        return context.mode == "OBJECT"
    
    def execute(self, context):
        sobj = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        parent_obj = sobj.parent
        if sobj.type == "CURVES":
            if sobj.hide_viewport == True:
                sobj.hide_viewport = False
            else:
                sobj.hide_viewport = True
        bpy.context.view_layer.objects.active = parent_obj
        return {'FINISHED'}

class BV2_OT_create_sculpt_guide(bpy.types.Operator):
    """Create optimised sculpt guides"""
    bl_idname = "object.bv2_create_sculpt_guide"
    bl_label = "Create Sculpt Guide"   
    
    @classmethod
    def poll(cls, context):

        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        modN = get_gNode(obj_)[0]
        ntN = get_gNode(obj_)[1]
        ntID = get_gNode(obj_)[2]
        if ntID == "":
            return False
        return context.mode == "OBJECT" 
      
    
    #sg_name: bpy.props.StringProperty(name="Sculpt Guide name", description = "Name the sculpt guide", default = "")
    
    def execute(self, context):
        obj = bpy.context.active_object
        #obj_ = bpy.data.objects[bpy.context.scene.bv2_tools.curveList]
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        
        # Duplicate the object
        new_obj = obj_.copy()
        new_obj.data = obj_.data.copy()

        # Remove all the modifiers from the duplicated object
        while new_obj.modifiers:
            new_obj.modifiers.remove(new_obj.modifiers[0])

        # Link the duplicated object to the scene and select it
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.collection.objects.link(new_obj)
        bpy.context.view_layer.objects.active = new_obj
        #new_obj.name = self.sg_name
        new_obj.name = obj_.name + "_[SG]" 
        
        
        mod_name = get_gNode(obj_)[0]
        nodeTree_name = get_gNode(obj_)[1]
        obj_.modifiers[mod_name.name]["Input_47"] = True
        obj_.modifiers[mod_name.name]["Input_46"] = new_obj
        obj_.modifiers[mod_name.name]["Input_2"] = False
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.curves.sculptmode_toggle()
        
        #parent_obj = obj_.parent
        #bpy.context.view_layer.objects.active = parent_obj

        return {'FINISHED'}   
    '''
    def invoke(self, context, event):
        # Display a popup asking for the collection name
        return context.window_manager.invoke_props_dialog(self)
'''

def convert_to_mesh(obj,int):
    # Duplicate the object
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()

    # Remove all the modifiers from the duplicated object
    while new_obj.modifiers:
        new_obj.modifiers.remove(new_obj.modifiers[0])

    # Link the duplicated object to the scene and select it
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.collection.objects.link(new_obj)
    bpy.context.view_layer.objects.active = new_obj

    group = bpy.data.node_groups.get("00_bv2: [Resample Curve]")
    mod = new_obj.modifiers.new(name="resample_mod", type='NODES')
    mod.node_group = group
    bpy.data.node_groups["00_bv2: [Resample Curve]"].nodes["ID:resample_curve"].inputs[2].default_value = int
    bpy.ops.object.convert(target='MESH')
    
    return new_obj

class BV2_OT_create_sim_guides(bpy.types.Operator):
    """Create Simulation Guide"""
    bl_idname = "object.bv2_create_sim_guides"
    bl_label = "Create Sim Guide"
    
    @classmethod
    def poll(cls, context):

        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport == True:
            return False
        return context.mode == "OBJECT" 
    
    '''
    def invoke(self, context, event):
        # Display a popup asking for the collection name
        return context.window_manager.invoke_props_dialog(self)
    '''
    def invoke(self, context, event):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        nodelib_path = os.path.join(dirpath, "bgen_v2_nodes.blend")

        def load_node(nt_name, link=True):
            if not os.path.isfile(nodelib_path):
                return False

            with bpy.data.libraries.load(nodelib_path, link=link) as (data_from, data_to):
                if nt_name in data_from.node_groups:
                    data_to.node_groups = [nt_name]
                    return True
            return False

        if "bgen_v2_nodes" not in bpy.data.node_groups:
            load_node("bgen_v2_nodes", link=False)

        if "00_bv2: [Vertex To Strip]" not in bpy.data.node_groups:
            load_node("00_bv2: [Vertex To Strip]", link=False)
        
        return context.window_manager.invoke_props_dialog(self)
    
    try:
        collision_collection: bpy.props.EnumProperty(
            items=lambda self, context: [(c.name, c.name, "") for c in context.scene.collection.children],
            name="Collision Collection")
        
        resolution : bpy.props.IntProperty(name= "Resolution", soft_min= 0, soft_max= 50, default= (16))
        
        def execute(self, context):
            obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
            obj_.hide_select = False
            main_obj = obj_.name

            bpy.ops.object.select_all(action='DESELECT')
            
            obj_.select_set(True)
            bpy.context.view_layer.objects.active = obj_
            obj = bpy.context.active_object
            
            convert_to_mesh(obj,self.resolution)  # Used method to convert to mesh
            obj = bpy.context.active_object
            
            obj_.hide_select = True
            #--------------------------------------------------------------------------
            # add modifiers
            get_mod_01 = bpy.data.node_groups.get("00_bv2: [Vertex To Strip]")
            mod_01 = obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
            mod_01.node_group = get_mod_01
            
            mod_02 = obj.modifiers.new(name="Cloth", type='CLOTH')
            # Remove all vertex groups from the object
            for group in obj.vertex_groups:
                obj.vertex_groups.remove(group)

            # Add a new vertex group to the object
            new_group = obj.vertex_groups.new(name="Group")
            
            #mod_02 = obj.modifiers.new(name="Cloth", type='CLOTH')
            cloth_modifier = obj.modifiers["Cloth"]    
            cloth_modifier.settings.vertex_group_mass = "Group"  # Sets Pin group
            cloth_modifier.collision_settings.vertex_group_object_collisions = "" # Sets Collision group
            cloth_modifier.collision_settings.distance_min = 0.001
            if self.collision_collection == "":
                pass
                #cloth_modifier.collision_settings.collection = bpy.data.collections[self.collision_collection]
            else:
                cloth_modifier.collision_settings.collection = bpy.data.collections[self.collision_collection]
            
            
            
            get_mod_03 = bpy.data.node_groups.get("00_bv2: [Strips To Curves]")
            mod_03 = obj.modifiers.new(name="geometry_nodes_mod", type='NODES')
            mod_03.node_group = get_mod_03
            

            
            # Separate each strand
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.editmode_toggle()

            new_collection = bpy.data.collections.new("")

            # Add the new collection to the active scene
            bpy.context.scene.collection.children.link(new_collection)
            
            # Add all selected objects to the new collection
            selected_objects = bpy.context.selected_objects
            for obj in selected_objects:
                scene_collection = bpy.context.scene.collection
                
                if obj.users_collection:
                    collection = obj.users_collection[0]
                    collection.objects.unlink(obj)
                
                new_collection.objects.link(obj)
            
            bpy.context.view_layer.objects.active = obj_
            new_collection.name = "SIM=[" + obj_.name + "]"
            
            if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].children:
                obj0 = bpy.data.objects[bpy.context.active_object.hair_curves_active_index].children[0]
            else:
                obj0 = bpy.data.objects[bpy.context.active_object.hair_curves_active_index] 
                
            #obj0 = bpy.data.objects[self.sim_target]
            
            mod_name = get_gNode(obj0)[0]
            nodeTree_name = get_gNode(obj0)[1]

            bpy.data.node_groups[nodeTree_name].nodes["ID:bv2_CC_001"].inputs[1].default_value = new_collection
            obj0.modifiers[mod_name.name]["Input_3"] = new_collection
            obj0.modifiers[mod_name.name]["Input_2"] = True  
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode='OBJECT')
            new_collection.hide_render = True
            new_collection.hide_viewport = True
            bpy.data.scenes[bpy.context.scene.name].view_layers[bpy.context.view_layer.name].layer_collection.children[new_collection.name].exclude = True
            
            bpy.context.view_layer.objects.active = obj_.parent
            obj_.parent.select_set(True)

                
            return {'FINISHED'}
    except:
        pass
        
class BV2_OT_duplicate_hair(bpy.types.Operator):
    """Dupicates higlighted hair curve"""
    bl_idname = "object.bv2_duplicate_hair"
    bl_label = "Duplicate hair"
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport == True:
            return False
        return context.mode == "OBJECT" 
    
    def execute(self, context):
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        parent_obj = obj_.parent
        obj_.hide_select = False
        bpy.ops.object.select_all(action='DESELECT')
        obj_.select_set(True)
        bpy.context.view_layer.objects.active = obj_
        bpy.ops.object.duplicate()
        obj = bpy.context.active_object
        obj.name = obj_.name + "_copy"

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = parent_obj
        parent_obj.select_set(True)
        return {'FINISHED'}

class BV2_OT_exit_sculpt_mode(bpy.types.Operator):

    """Exit Sculpt Mode"""
    bl_idname = "object.bv2_exit_sculpt_mode"
    bl_label = "Exit sculpt mode"
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if bpy.context.active_object.hair_curves_active_index < 0:
            return False
        return context.mode == "SCULPT_CURVES" or "EDIT" and context.mode != 'OBJECT'
    
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj.select_set(False) 

        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]

        if obj_.hide_viewport == True:
            obj_.hide_viewport = False
            
            #obj_.hide_select = False
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active =  obj_.parent
            obj_.parent.select_set(True)
            obj_.hide_viewport = True

        else:
            #obj_.hide_select = False
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active =  obj_.parent
            obj_.parent.select_set(True)


        return {'FINISHED'}   

class BV2_OT_groom_curve(bpy.types.Operator):
    """Switches to sculpt curve object"""
    bl_idname = "object.bv2_groom_curve"
    bl_label = "Sculpt curve"
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    
    
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj.select_set(False) 
        try: 
            if context.mode == "OBJECT" or context.mode == "SCULPT_CURVES":
                if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport == True:
                    bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport = False
                    bpy.context.view_layer.objects.active =  bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
                    bpy.data.objects[bpy.context.active_object.hair_curves_active_index].select_set(True)
                    bpy.ops.object.mode_set(mode='SCULPT_CURVES', toggle=False)
                    bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport = True
                    
                if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport == False:
                    bpy.context.view_layer.objects.active =  bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
                    bpy.data.objects[bpy.context.active_object.hair_curves_active_index].select_set(True)
                    bpy.ops.object.mode_set(mode='SCULPT_CURVES', toggle=False)

                
             
        except:
            pass
        return {'FINISHED'} 

class BV2_OT_rescale_hair(bpy.types.Operator):
    """Rescales hair and emiter object for more accurate generation (Needed only if object is too small)"""
    bl_idname = "object.bv2_rescale_hair"
    bl_label = "Rescale hair"
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport == True:
            return False
        return context.mode == "OBJECT" 
    
    scale_option: bpy.props.EnumProperty(
        items=(('RESCALE', "Rescale hair", "Rescale by Factor"),
               ('RESET', "Reset hair scale", "Revert to original scale")),
        default='RESCALE',)
    
    scale : bpy.props.FloatProperty(name= "Re-Scale Factor", soft_min= 1, soft_max= 5, default= (2))

    def invoke(self, context, event):
        # Display a popup asking for the collection name
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        
        layout = self.layout
        col = layout.column()
        box = col.box()
        col_ = box.column()
        col_.scale_y = 1.6
        row_ = col_.row()
        row_.prop(self,"scale_option", expand = True)

        if self.scale_option == "RESCALE":
            row_ = col_.row()
            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            grid_l.alignment = "RIGHT"
            grid_l.scale_x = 1.1
            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
            
            grid_l.label(text = "Re-scale Factor")
            grid_r.prop(self,"scale", text = "")
        else:
            col_.label(text="[Click 'ok' to reset scale]")

    def execute(self, context):
        if self.scale_option == "RESCALE":
            mesh_obj = bpy.data.objects[bpy.context.active_object.hair_curves_active_index].parent
            bpy.ops.object.select_all(action='DESELECT')
            for obj_ in get_hairCurve_list(mesh_obj):
                #obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
                obj_.hide_select = False
                obj_.select_set(True)

            mesh_obj.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.transform.resize(value=(self.scale, self.scale, self.scale))
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.transform.resize(value=(1/self.scale, 1/self.scale, 1/self.scale))

            bpy.ops.object.select_all(action='DESELECT')
            obj_.parent.select_set(True)
            bpy.context.view_layer.objects.active = obj_.parent
        else:
            mesh_obj = bpy.data.objects[bpy.context.active_object.hair_curves_active_index].parent
            bpy.ops.object.select_all(action='DESELECT')
            for obj_ in get_hairCurve_list(mesh_obj):
                #obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
                obj_.hide_select = False
                obj_.select_set(True)

            obj_.parent.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.object.select_all(action='DESELECT')
            obj_.parent.select_set(True)
            bpy.context.view_layer.objects.active = obj_.parent
        return {'FINISHED'}

class BV2_OT_resample_guides(bpy.types.Operator):
    """Resamples the nuber of control points on a guide"""
    bl_idname = "object.bv2_resample_guides"
    bl_label = "Resample guide"
    
    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active is None:
            return False
        if get_curveChild(active).type != "CURVES":
            return False
        selected_objects = context.selected_objects
        if selected_objects is None:
            return False
        if bpy.data.objects[bpy.context.active_object.hair_curves_active_index].hide_viewport == True:
            return False
        return context.mode == "OBJECT", context.mode == "SCULPT_CURVES"
    
    
    resample : bpy.props.IntProperty(name= "Point count", soft_min= 4, soft_max= 50, default= (12))

    def invoke(self, context, event):
        # Display a popup asking for the collection name
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_ = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        group = bpy.data.node_groups.get("00_bv2: [Resample Curve]")
        mod = obj_.modifiers.new(name="Resample_Guides", type='NODES')
        mod.node_group = group
        bpy.data.node_groups["00_bv2: [Resample Curve]"].nodes["ID:resample_curve"].inputs[2].default_value = self.resample
        bpy.ops.object.select_all(action='DESELECT')
        obj_.select_set(True)
        bpy.context.view_layer.objects.active = obj_
        bpy.ops.object.modifier_apply(modifier=mod.name,report = True)

        obj_.hide_select = False
        bpy.context.view_layer.objects.active =  obj_
        obj_.select_set(True)
        bpy.ops.object.mode_set(mode="SCULPT_CURVES")

        return {'FINISHED'}

class BV2_OT_execute_cloth_settings(bpy.types.Operator):
    ''' Executes the settings from the parameters above'''
    bl_label = "EXECUTE SIM VALUES"
    bl_idname = "object.bv2_execute_cloth_settings"
    bl_context = "scene"
    
    def execute(self, context):
        gName = bpy.context.scene.bv2_tools.sim_collection
        root_collection = bpy.data.collections[gName]
        collection_stack = [root_collection]
        collectionKeys = bpy.data.collections.keys()

        # Context Values
        quality_Val = bpy.context.scene.bv2_tools.my_int1
        mass_Val = bpy.context.scene.bv2_tools.my_float1
        gravity_Val = bpy.context.scene.bv2_tools.my_float2
        stifTension_Val = bpy.context.scene.bv2_tools.my_float3
        clsnColl = bpy.context.scene.bv2_tools.col_collection
        #pinStiff = bpy.context.scene.bv2_tools.my_float5
        airVis = bpy.context.scene.bv2_tools.my_float6
        disk_cache = bpy.context.scene.bv2_tools.disk_cache

        frame_start = bpy.context.scene.bv2_tools.sim_start
        frame_end = bpy.context.scene.bv2_tools.sim_end

        while collection_stack:
            current_collection = collection_stack.pop()
            for obj in current_collection.objects:
                
                if get_gNode_2(obj)[2] == nodeID_3:
                    vtsMod = get_gNode_2(obj)[0]
                    vtsMod.node_group = bpy.data.node_groups[bpy.context.scene.bv2_tools.vts_mod]
                    if obj.modifiers['Cloth']:
                        cloth_modifier = obj.modifiers["Cloth"]
                        if bpy.context.scene.bv2_tools.simToggle_ == "ON":
                            cloth_modifier.show_viewport = True
                            cloth_modifier.show_render = True
                        if bpy.context.scene.bv2_tools.simToggle_ == "OFF":
                            cloth_modifier.show_viewport = False
                            cloth_modifier.show_render = False
                            
                        cs = cloth_modifier.settings
                        cs.quality = quality_Val
                        cs.mass = mass_Val
                        
                        cs.tension_stiffness = stifTension_Val
                        cs.compression_stiffness = stifTension_Val
                        
                        cs.pin_stiffness = 25
                        cs.effector_weights.all = 1 
                        cs.effector_weights.gravity = gravity_Val
                        cs.air_damping = airVis
                        
                        for clsn in collectionKeys:
                            if clsnColl != clsn:
                                pass
                            else:
                                cloth_modifier.collision_settings.collection = bpy.data.collections[clsnColl]
                        
                        for vg in obj.vertex_groups:
                            obj.vertex_groups.remove(vg)

                        new_vg = obj.vertex_groups.new(name="Group")
                        
                        cloth_modifier.settings.vertex_group_mass = "Group"  # Sets Pin group
                        cloth_modifier.collision_settings.vertex_group_object_collisions = "" # Sets Collision group
                        cloth_modifier.collision_settings.collision_quality = 5
                        cloth_modifier.collision_settings.distance_min = 0.001
                        cloth_modifier.collision_settings.impulse_clamp = 20

                        cloth_modifier.point_cache.frame_start = frame_start
                        cloth_modifier.point_cache.frame_end = frame_end
                        if disk_cache == False:
                            cloth_modifier.point_cache.use_disk_cache = False
                        else:
                            cloth_modifier.point_cache.use_disk_cache = True
                    
                for child_collection in current_collection.children:
                    collection_stack.append(child_collection)

        #change_cloth_Settings()
        self.report({"INFO"},message="Sim Values EXECUTED")
        return {'FINISHED'} 

class BV2_OT_bake_hair_sim(bpy.types.Operator):
    bl_idname = "object.bake_hair_sim"
    bl_label = "Bake Dynamics"
    bl_description = "Bake all dynamics in the specified collection"

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        if bpy.context.scene.bv2_tools.sim_collection == "":
            pass
        else:
            bpy.data.scenes[bpy.context.scene.name].view_layers[bpy.context.view_layer.name].layer_collection.children[bpy.context.scene.bv2_tools.sim_collection].exclude = False
            bpy.ops.ptcache.bake_all(bake=True)
            bpy.data.scenes[bpy.context.scene.name].view_layers[bpy.context.view_layer.name].layer_collection.children[bpy.context.scene.bv2_tools.sim_collection].exclude = True
        self.report({"INFO"},message="SIM BAKE FINISHED")
        return {'FINISHED'}
    

    
#=========================================================================================================    
# 01 ---------------------------   [TEMPLATE LIST IMPLIMENTATION]
#=========================================================================================================  
HAIR_CURVE_TYPE = "CURVES"

def is_hair_curve_object(curve_object, parent):
    """Checks if the given curve_object is a hair curves object of the parent"""
    if curve_object.type != HAIR_CURVE_TYPE:
        # Skip non curve hair objects
        return False

    if curve_object.data is None:
        # Skip if data is None
        return False

    if curve_object.data.surface is None:
        # Skip if parent object is None
        return False

    if curve_object.data.surface != parent:
        # Skip if parent object does not equal active object
        return False
    
    ################

    if curve_object.parent and curve_object.parent.type != "MESH":
        return False
    

    return True

class BV2_UL_hair_curves(bpy.types.UIList):
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname
    ):
        # bpy_data = data
        curve_object = item
        obj = active_data
        #
        # NEW CODE
        #
        if obj.type == HAIR_CURVE_TYPE:
            if obj.data.surface is None:
                return
            else:
                obj = obj.data.surface

        if not is_hair_curve_object(curve_object, obj):
            return

        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {"DEFAULT", "COMPACT"}:

            row = layout.row()
            row.prop(
                curve_object, "name", text="", emboss=False, icon="OUTLINER_OB_CURVES"
            )
            sub_row = row.row(align=True)
            sub_row.prop(curve_object, "hide_select", icon_only=True, emboss=False)
            #sub_row.prop(curve_object, "hide_viewport", icon_only=True, emboss=False)
            sub_row.prop(curve_object, "hide_viewport", icon_only=True, emboss=False)
            sub_row.prop(curve_object, "hide_render", icon_only=True, emboss=False)

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == "GRID":
            #layout.alignment = "CENTER"
            #layout.label(text="", icon="OUTLINER_OB_CURVES")
            
            row = layout.row()
            row.prop(
                curve_object, "name", text="", emboss=False,icon = "CURVES"
            )
            sub_row = row.row(align=True)
            #sub_row.prop(curve_object, "hide_select", icon_only=True, emboss=False)
            sub_row.prop(curve_object, "hide_viewport", icon_only=True, emboss=False)
            #sub_row.prop(curve_object, "hide_render", icon_only=True, emboss=False)

    def filter_items(self, context, data, propname):
        objects = getattr(data, propname)

        obj = context.object

        #
        # NEW CODE (context.obj below was changed to obj too)
        #
        if obj.type == HAIR_CURVE_TYPE:
            if obj.data.surface is None:
                return
            else:
                obj = obj.data.surface

        flt_flags = [
            self.bitflag_filter_item
            if is_hair_curve_object(hcobj, obj)
            else ~self.bitflag_filter_item
            for hcobj in objects
        ]

        return flt_flags, list(range(len(objects)))

def count_hair_curves(obj):
    num_hair_curves = 0
    for child_obj in obj.children:
        if child_obj.type == HAIR_CURVE_TYPE:
            num_hair_curves += 1
    return num_hair_curves

def get_hair_curves_active_index(obj):
    if obj.type == HAIR_CURVE_TYPE:
        if obj.data.surface is None:
            return -1
        else:
            obj = obj.data.surface

    index = obj.get("_hair_curves_active_index", -1)
    if index == -1:
        return -1

    index_found = False
    for i, other_obj in enumerate(bpy.data.objects):
        if other_obj.type != HAIR_CURVE_TYPE:
            # Skip non curve hair objects
            continue
        if other_obj.data is None:
            # Skip if data is None
            continue

        if other_obj.data.surface is None:
            # Skip if parent object is None
            continue

        if other_obj.data.surface != obj:
            # Skip if parent object does not equal active object
            continue

        if i == index:
            index_found = True

    if index_found:
        return index
    obj["_hair_curves_active_index"] = -1
    return -1

def set_hair_curves_active_index(obj, value):
    if obj.type == HAIR_CURVE_TYPE:
        if obj.data.surface is None:
            return
        else:
            obj = obj.data.surface

    if value < 0:
        obj["_hair_curves_active_index"] = -1
    else:
        obj["_hair_curves_active_index"] = value
             

#=========================================================================================================    
# 00 ---------------------------            [CUSTOM PROPERTIES]
#=========================================================================================================      
class BV2_PT_bv2Properties(bpy.types.PropertyGroup):
    
    #my_exp1 : bpy.props.BoolProperty(default=True)
    
    clumpBool1 : bpy.props.BoolProperty(name="Guide Clump", description="Big Clump Profile", default=True)
    clumpBool2 : bpy.props.BoolProperty(name="Interpulated Clump", description="Interpulated Clump Profile", default=False)

    pinned_obj: bpy.props.PointerProperty(name="Pinned Object", type=bpy.types.Object,)

    def set_pin_obj(self, value):
        if value:
            self.pinned_obj = bpy.context.object
        else:
            self.pinned_obj = None
    
    def get_pin_obj(self):
        return self.pinned_obj is not None

    pin_obj : bpy.props.BoolProperty(name="Pin Object", description="Pins active object", default=False, set=set_pin_obj, get=get_pin_obj)

    #pin_obj : bpy.props.BoolProperty(name="Pin Object", description="Pins active object", default=False)
    
    
        
    clumpChoice: bpy.props.EnumProperty(
        items=(('BIGCLUMP', "Guide Clump", "Guide Clump Profile"),
               ('SMALLCLUMP', "Interpulated Clump", "Interpulated Clump Profile")),
        default='BIGCLUMP')
        
    guideChoice: bpy.props.EnumProperty(
        items=(('GUIDES', "Guides", "Hair Guide Control"),
               ('STRANDS', "Hair Stands", "Hair Strands control")),
        default='GUIDES')
        
    curlType: bpy.props.EnumProperty(
        items=(('TYPE1', "Type 1", "Curl type 1"),
               ('TYPE2', "Type 2", "Curl type 2")),
        default='TYPE1')
    
    mattren: bpy.props.EnumProperty(
        items=(('EEVEE', "Eevee", "Rendered with Eevee"),
               ('CYCLES', "Cycles", "Rendered with Cycles")),
        default='EEVEE')
    
    material_color: bpy.props.EnumProperty(
        items=(('STRAND', "Strand", "Takes Color of Strand"),
               ('SURFACE', "Surface", "Inherits the color of the surface")),
        default='STRAND')
        
    utilDrawer: bpy.props.EnumProperty(
        items=(('INITIALIZE', "Initialize", "Set up hair Curve"),
               ('DEFORMERS', "Deformers", "Add deformers to hair curve"),
               ('SIMULATION', "Simulation", "Simulate hair curves")),
        default='INITIALIZE')
    
    my_string1 : bpy.props.StringProperty(name= "")
    my_string2 : bpy.props.StringProperty(name= "")
    
    ntName : bpy.props.StringProperty(name= "")
    
    my_int1 : bpy.props.IntProperty(name= "", soft_min= 0, soft_max= 20, default= (5))

    sim_start : bpy.props.IntProperty(name= "", soft_min= 0, soft_max= 4000, default= (1),description="Bake to cache starts from frame ...")
    sim_end : bpy.props.IntProperty(name= "", soft_min= 0, soft_max= 4000, default= (250),description="Bake to cache end in frame ...")
    
    my_float1 : bpy.props.FloatProperty(name= "", soft_min= 0, soft_max= 20, default= (0.5),)
    my_float2 : bpy.props.FloatProperty(name= "", soft_min= 0, soft_max= 1, default= (1))
    my_float3 : bpy.props.FloatProperty(name= "", soft_min= 0, soft_max= 50, default= (15))
    my_float4 : bpy.props.FloatProperty(name= "", soft_min= 0.01, soft_max= 1, default= (.02))
    my_float5 : bpy.props.FloatProperty(name= "", soft_min= 1, soft_max= 50, default= (1)) #Pin Stiffness Value
    my_float6 : bpy.props.FloatProperty(name= "", soft_min= 0, soft_max= 10, default= (1)) # Air Viscusity
    
    
    my_float_vector : bpy.props.FloatVectorProperty(name= "", soft_min= 0, soft_max= 20, default= (1,1,1))

    my_enum : bpy.props.EnumProperty(
        name= "",
        description= "sample text",
        items= [])
        
    texture: bpy.props.EnumProperty(
        items=lambda self, context: [(t.name, t.name, "") for t in bpy.data.images if t.type == 'IMAGE'],
        name="Texture",
        description="Select the texture",)
     
          
    hair_collection:bpy.props.EnumProperty(
        items=lambda self, context: [(c.name, c.name, "") for c in bpy.data.collections],
        name="Hair Collection",
        description="Select the hair collection",)
        
    col_collection:bpy.props.EnumProperty(
        items=lambda self, context: [(c.name, c.name, "") for c in bpy.data.collections],
        name="Collision Collection",
        description="Select the collision collection",)
        
    vts_mod:bpy.props.EnumProperty(
        items=lambda self, context: [(s, s, "") for s in vts_nodes()],
        name="Sim Mod",
        description="Select sim mod",)
     
    mattList:bpy.props.EnumProperty(
        items=lambda self, context: [(m.name, m.name, "") for m in get_materials()],
        name="Bgen Materials",
        description="Select Material",)
    
    sim_collection:bpy.props.EnumProperty(
        items=lambda self, context: [(sc.name, sc.name, "") for sc in get_sim_collection()],
        name="Sim Collections",
        description="List of Sim Collections",)
    
    simToggle : bpy.props.BoolProperty(name="Sim Toggle",default=True)

    disk_cache : bpy.props.BoolProperty(name="Disk Cache",default=False , description="Toggle disk Cache")
    
    simToggle_: bpy.props.EnumProperty(
        items=(('ON', "Sim On", "Turn simulation on"),
               ('OFF', "Sim Off", "Turn simulation off")),
        default='ON')
    
class BV2_PT_bv2ExpandProp(bpy.types.PropertyGroup):
    
    my_exp1 : bpy.props.BoolProperty(default=False) # INITIALIZE
    my_exp2 : bpy.props.BoolProperty(default=False)
    my_exp3 : bpy.props.BoolProperty(default=False)
    my_exp4 : bpy.props.BoolProperty(default=False)
    my_exp5 : bpy.props.BoolProperty(default=False)
    my_exp6 : bpy.props.BoolProperty(default=False)
    my_exp7 : bpy.props.BoolProperty(default=False)
    my_exp8 : bpy.props.BoolProperty(default=False) # EXTRA SETTINGS
    my_exp9 : bpy.props.BoolProperty(default=False) # Parting Map
    my_exp10 : bpy.props.BoolProperty(default=False) # Bake to Cache Settings
    
    my_expF1 : bpy.props.BoolProperty(default=False)
    my_expF2 : bpy.props.BoolProperty(default=False) 
    my_expF3 : bpy.props.BoolProperty(default=False) # CURL
    my_expF4 : bpy.props.BoolProperty(default=False) # BRAID
    my_expF5 : bpy.props.BoolProperty(default=False)
    my_expF5 : bpy.props.BoolProperty(default=False) # NOISE
    
    my_expS1 : bpy.props.BoolProperty(default=False) # Weight Paint
    my_expS2 : bpy.props.BoolProperty(default=False) # Sim Values
    
    my_expT1 : bpy.props.BoolProperty(default=False) # Material
    
    #-------------------------------------------------------------------------------------
    def curve_index_update(self, context: bpy.types.Context):
        mode = context.mode
        if len(self.curve_items) == 0:
            return
        if mode == "SCULPT_CURVES":
            bpy.ops.object.mode_set(mode="OBJECT")
            context.active_object.select_set(False)
            new_obj = self.curve_items[self.curve_index].obj
            context.view_layer.objects.active = new_obj
            if new_obj and new_obj.name in context.view_layer.objects:
                new_obj.select_set(True)
                bpy.ops.object.mode_set(mode="SCULPT_CURVES")

#=========================================================================================================    
# 00 ---------------------------         [PANEL LAYOUT]
#=========================================================================================================

class BV2_PT_ui_panel(bpy.types.Panel):
    bl_label = " BGEN Groom"
    bl_idname = "OBJECT_PT_bgen_v2_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BGEN HAIR'
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon_value=icons["BGEN_GROOM"].icon_id)

    def draw(self, context):
        addon_updater_ops.update_notice_box_ui(self,context)
        #try:
        if context.active_object is not None:
            bv2_tools = context.scene.bv2_tools
            obj_exp = context.object.bv2_expand
            if bv2_tools.pin_obj == True:
                if bv2_tools.pinned_obj.hair_curves_active_index == -1:
                    obj = bpy.context.scene.bv2_tools.pinned_obj
                else:
                    obj = bpy.data.objects[bpy.context.scene.bv2_tools.pinned_obj.hair_curves_active_index]
            else:
                if bpy.context.active_object.hair_curves_active_index == -1:
                    obj = context.active_object
                else:
                    obj = bpy.data.objects[bpy.context.active_object.hair_curves_active_index]
        else:
            obj = context.active_object

        if context.active_object is None:
            layout = self.layout                
            col = layout.column()
            box = col.box()
            box1 = box.box()
            
            col_nt = box1.column()
            col_nt.scale_y = 1.4
            row_nt = col_nt.row(align = True)
            row_nt.scale_x = 1.2

            row_nt.alignment = "CENTER"
            row_nt.label(text="[Not Applicable]")

            box = col.box()
            col1 = box.column()
            col1.scale_y = 1
            col1.alignment = "CENTER"
            col1.label(text = "No selected Object", icon = "ERROR")

        elif not get_gNode(obj)[2] == "ID:BV2_0001" and not get_gNode(obj)[2] == "ID:BV2_GEN_HC":

            mainCurve = get_curveChild(obj)
            bgenMod = get_gNode(obj)[0]
            bgenModName = get_gNode(obj)[1]
            bgenNodeID = get_gNode(obj)[2]

            layout = self.layout
            col = layout.column()
            box1 = col.box()
            
            box2 = box1.box()
            box2.scale_y = 1.4
            col_nt = box2.column()
            row_nt = col_nt.row(align = True)
            row_nt.scale_x = 1.2

            row_nt.alignment = "CENTER"
            row_nt.label(text="[Not Applicable]")
   
            col = layout.column()
            col.scale_y = 1.2
            
            box_main = col.box()
            
            row_label = box_main.row(align=False)
            row_label.alignment = "LEFT"
            
            # OBJECT LABELING
            if bv2_tools.pin_obj == True:
                obj_ac = bv2_tools.pinned_obj
            else:
                obj_ac = bpy.context.active_object

            #try: 
            row_label.label(text = obj_ac.name, icon = "OBJECT_DATAMODE")
                
            col = box_main.column()
            col.scale_y = 1.1

            row0 = col.row(align = False)
            row0.scale_x = 1.1
            
            col0 = row0.column(align = False)
            col0.scale_y = 1
            col00 = row0.column(align = True)
            col00.scale_x = 1.1
            
            row_0 = col.row(align =False)
            row_0.scale_y = 1.2

            col00.operator("object.bv2_add_ehc", text="", icon = "ADD")  
            col00.operator("object.bv2_remove_ehc", text="", icon = "REMOVE")
            col00.separator()
            col00.operator("object.bv2_duplicate_hair", text="", icon = "DUPLICATE")
            col00.separator()
            col00.operator("object.bv2_rescale_hair", text="", icon = "TOOL_SETTINGS")
            

            row_0.operator("object.bv2_groom_curve", text="GROOM", icon = "SCULPTMODE_HLT")
            row_0.operator("object.bv2_exit_sculpt_mode", text="EXIT GROOM", icon = "OBJECT_DATAMODE")

            obj_l = context.object


            if obj.type == HAIR_CURVE_TYPE:
                if obj.data.surface is None:
                    return
                else:
                    obj_l = obj.data.surface

            col0.template_list("BV2_UL_hair_curves","",bpy.data,"objects",obj_l,"hair_curves_active_index", rows = 4, type = "DEFAULT",columns = 2)

        #elif get_gNode(obj)[2] == "ID:BV2_0001" or get_gNode(obj)[2] == "ID:BV2_GEN_HC": 
        else:

            mainCurve = get_curveChild(obj)
            bgenMod = get_gNode(obj)[0]
            bgenModName = get_gNode(obj)[1]
            bgenNodeID = get_gNode(obj)[2]

            layout = self.layout
            col = layout.column()
            box1 = col.box()
            
            box2 = box1.box()
            box2.scale_y = 1.4
            col_nt = box2.column()
            row_nt = col_nt.row(align = True)
            row_nt.scale_x = 1.2

            row_nt.operator_menu_enum("object.bv2_choose_nodetree",'bv2_nodes', text="" , icon = "NODETREE")
            try:
                mn = bpy.data.node_groups[bgenModName]
                row_nt.prop(mn,"name", text = "",toggle=True, emboss = True)
                row_nt.prop(mn,"use_fake_user", text = "",toggle=True, emboss = True)
                
            except:
                row_nt.alignment = "CENTER"
                row_nt.label(text="[Not Applicable]")

            row_nt.operator("object.bv2_single_user", text="", icon = "DUPLICATE" ) 
            
            
            #==========================================================================    
            col = layout.column()
            col.scale_y = 1.2
            
            box_main = col.box()
            row_main = box_main.row()

            row_label = row_main.row(align=False)
            row_label.alignment = "LEFT"
            
            # OBJECT LABELING
            if bv2_tools.pin_obj == True:
                obj_ac = bv2_tools.pinned_obj
            else:
                obj_ac = bpy.context.active_object

            #try: 
            if obj_ac.type == "MESH":
                if has_curve_child(obj_ac):
                    row_label.label(text = obj_ac.name, icon = "OBJECT_DATAMODE")
                    row_label.label(text = "", icon = 'RIGHTARROW')
                    row_label.label(text = obj.name, icon = "OUTLINER_DATA_CURVES")
                    #if get_gNode(obj)[2] == nodeID_1:
                    row_label.label(text = "", icon = 'RIGHTARROW')
                else:
                    row_label.label(text = obj_ac.name, icon = "OBJECT_DATAMODE")

            if obj_ac.type == "CURVES":
                if get_gNode(obj)[2] == nodeID_1:
                    row_label.label(text = obj.parent.name, icon = "OBJECT_DATAMODE")
                    row_label.label(text = "", icon = 'RIGHTARROW')
                    row_label.label(text = obj.name, icon = "OUTLINER_DATA_CURVES")
                    row_label.label(text = "", icon = 'RIGHTARROW')
                else:
                    row_label.label(text = obj.parent.name, icon = "OBJECT_DATAMODE")
                    row_label.label(text = "", icon = 'RIGHTARROW')
                    row_label.label(text = obj.name, icon = "OUTLINER_DATA_CURVES")
                    row_label.label(text = "", icon = 'RIGHTARROW')

            row_pin = row_main.row()
            row_pin.alignment = "RIGHT"
            row_pin.prop(bv2_tools, "pin_obj", text="", icon = "PINNED" if bv2_tools.pin_obj else "UNPINNED", icon_only = True, emboss=False)

            #except:
            #    pass
                
            col = box_main.column()
            col.scale_y = 1.1
            gcol = col.column()
            
            obj_t = obj.evaluated_get(context.evaluated_depsgraph_get())
            if get_gNode(obj_t)[0]:
                bgenMod_ = get_gNode(obj_t)[0]
                execTime = str(int(bgenMod_.execution_time *1000))
                row_exec = row_label.row()
                row_exec.alignment = "RIGHT"
                row_exec.label(text = execTime + "ms", icon = "PREVIEW_RANGE")
            
            

            row0 = col.row(align = False)
            row0.scale_x = 1.1
            
            col0 = row0.column(align = False)
            col0.scale_y = 1
            col00 = row0.column(align = True)
            col00.scale_x = 1.1
            
            row_0 = col.row(align =False)
            row_0.scale_y = 1.2

            col00.operator("object.bv2_add_ehc", text="", icon = "ADD")  
            col00.operator("object.bv2_remove_ehc", text="", icon = "REMOVE")
            col00.separator()
            col00.operator("object.bv2_duplicate_hair", text="", icon = "DUPLICATE")
            col00.separator()
            col00.operator("object.bv2_rescale_hair", text="", icon = "TOOL_SETTINGS")
            

            row_0.operator("object.bv2_groom_curve", text="GROOM", icon = "SCULPTMODE_HLT")
            row_0.operator("object.bv2_exit_sculpt_mode", text="EXIT GROOM", icon = "OBJECT_DATAMODE")

            obj_l = context.object


            if obj.type == HAIR_CURVE_TYPE:
                if obj.data.surface is None:
                    return
                else:
                    obj_l = obj.data.surface

            col0.template_list("BV2_UL_hair_curves","",bpy.data,"objects",obj_l,"hair_curves_active_index", rows = 4, type = "DEFAULT",columns = 2)
        
            #UTILITY TABS
            col = layout.column()
            ubox = col.box()
            col = ubox.column()
            urow = col.row()
            
            urow.prop(bv2_tools, "utilDrawer",expand = True)
            urow.scale_y = 1.4
            #utilD = bpy.context.scene.bv2_tools.utilDrawer
    

            # INITIALIZE TAB
            if bpy.context.scene.bv2_tools.utilDrawer == "INITIALIZE": 
                #--------------------------------------------------------------------------------------------------------
                
                #if obj.modifiers and obj.modifiers[-1].node_group.name == "00_bv2_Generate_guides":
                if obj.modifiers and obj.modifiers[-1].type == "NODES":
                    if obj.modifiers[-1].node_group.name == "00_bv2_Generate_guides":
                        gcMod = obj.modifiers[-1]
                        #gcModName = obj.modifiers[-1].node_group.name
                        
                        box = col.box()
                        col1 = box.column()
                        row1 = col1.row()
                        col_ = col1.column(align = False)
                        col_.scale_y = 1.4
                        
                        gcMsCntr = obj.modifiers[-1].node_group.nodes["ID:bv2_GC_TM_01"].inputs[0]
                        gcMsNode = obj.modifiers[-1].node_group.nodes["ID:bv2_GC_TM_01"]
                        
                        col_.label(text = "Generate Guide Curves:", icon = "CURVES")
                        row_ = col_.row(align = True)
                        row_.alignment = "RIGHT"
                        gcMsCntr.draw(context, col_, gcMsNode, text = '')
                        
                        box_ = col_.box()
                        row_ = box_.row(align = False)
                        row_.scale_y = 1.2
                        grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        grid_l.alignment = "RIGHT"
                        grid_l.scale_x = 1.5
                        grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        
                        grid_l.label(text = "        Density")
                        grid_l.label(text = "   Hair Length")
                        grid_l.label(text = "Control Points")
                        grid_l.label(text = "           Seed")
                        
                        grid_r.prop(gcMod, '["Input_15"]', text = '')
                        grid_r.prop(gcMod, '["Input_20"]', text = '')
                        grid_r.prop(gcMod, '["Input_27"]', text = '')
                        grid_r.prop(gcMod, '["Input_16"]', text = '')
                        
                        row_ = col_.row(align = True)
                        row_.scale_y = 1.2
                        row_.operator("object.bv2_apply_guides", text = "Apply Guides", icon = "CHECKMARK", depress = True)
                        row_.operator("object.bv2_delete_guides", text = "Delete Guides", icon = "CANCEL")
                        
                    else:
                        col_ = col.column(align = False)
                        col_.separator(factor=.4)
                        col_.scale_y = 1.6
                        row_ = col_.row(align = True)
                        row_.operator("object.bv2_generate_guides", text = "Generate Guides", icon = "OUTLINER_DATA_CURVES", depress = True)
                        row_.separator(factor=1)
                        row_.operator("object.bv2_resample_guides", text = "Resample Guides", icon = "OUTLINER_DATA_CURVES", depress = True)
                        col_.separator(factor=.4)
                        
                #--------------------------------------------------------------------------------------------------------

                
                if mainCurve and get_gNode(obj)[2] == "ID:BV2_0001":  
                    main_obj = obj.name
                    mytool = context.scene.bv2_tools

                    matCntr = bpy.data.node_groups[bgenModName].nodes["ID:bv2_MC_001"].inputs[0]
                    matNode = bpy.data.node_groups[bgenModName].nodes["ID:bv2_MC_001"]

                    collCntr = bpy.data.node_groups[bgenModName].nodes["ID:bv2_CC_001"].inputs[1]
                    collNode = bpy.data.node_groups[bgenModName].nodes["ID:bv2_CC_001"]
                    
                    dmCntr = bpy.data.node_groups[bgenModName].nodes["ID:bv2_DM_001"].inputs[1]
                    dmNode = bpy.data.node_groups[bgenModName].nodes["ID:bv2_DM_001"]

                    pmCntr = bpy.data.node_groups[bgenModName].nodes["ID:bv2_PM_001"].inputs[1]
                    pmNode = bpy.data.node_groups[bgenModName].nodes["ID:bv2_PM_001"]
                    
                #================================================================================================================
                                                                #[INITIALIZE]    
                #================================================================================================================  
                
                    box_ = col.box()
                    col_ = box_.column(align = True)
                    col_.scale_y = 1.2
                    row1 = col_.row()

                    #INITIALIZE DRAWER
                    if obj_exp.my_exp1:
                        row1.prop(obj_exp, "my_exp1",icon="TRIA_DOWN", text="INITIALIZE", emboss=False)
                        row1.prop(bgenMod, '["Input_42"]', text = 'Low Poly', icon = "RADIOBUT_ON")
                        #col_ = col.column(align = True)
                        

                        box_00 = col_.box()
                        col_c = box_00.column(align = False)
                        col_c.label(text="Hair Children Type:",icon="CURVES_DATA")

                        row_c = col_c.row(align = True)
                        row_c.scale_y = 1.2
                        
                        if obj.modifiers[bgenMod.name]["Input_66"] == True:
                            row_c.prop(bgenMod, '["Input_66"]', text = 'Interpulated', icon="BLANK1",invert_checkbox=True)
                            row_c.prop(bgenMod, '["Input_66"]', text = 'Children', icon="BLANK1")
                        if obj.modifiers[bgenMod.name]["Input_66"] == False:
                            row_c.prop(bgenMod, '["Input_66"]', text = 'Interpulated', icon="BLANK1",invert_checkbox=True)
                            row_c.prop(bgenMod, '["Input_66"]', text = 'Children', icon="BLANK1")
                        #-------------------------------------------------------------------------------------------------
                        box_00 = col_.box()
                        box_00.label(text = "Density Mask:",icon="BRUSH_CURVES_DENSITY")
                        dmCntr.draw(context, box_00, dmNode, text = '')
                        
                        box_00 = col_.box()
                        uvr = box_00.row()
                        uvr.alignment = "RIGHT"
                        uvr.scale_x = 1.4
                        uvr.label(text = "UV Map name")
                        uvr.prop(bgenMod, '["Input_41"]', text = '')

                        atr = box_00.row()
                        atr.alignment = "RIGHT"
                        atr.scale_x = 1.4
                        atr.label(text = "         Attach To")
                        atr.prop(bgenMod, '["Input_14"]', text = '')
                        #-------------------------------------------------------------------------------------------------
                        box_00 = col_.box()
                        pmrow = box_00.row()
                        pmrow.alignment = "LEFT"
                        if obj_exp.my_exp9:
                            pmrow.prop(obj_exp, "my_exp9",icon="TRIA_DOWN", text="Parting Mask", emboss=False)
                            pmCntr.draw(context, box_00, pmNode, text = '')
                        else:
                            pmrow.prop(obj_exp, "my_exp9",icon="TRIA_RIGHT", text="Parting Mask", emboss=False)

                    else:
                        row1.prop(obj_exp, "my_exp1",icon="TRIA_RIGHT", text="INITIALIZE", emboss=False)
                        row1.prop(bgenMod, '["Input_42"]', text = 'Low Poly', icon = "RADIOBUT_ON")

                    box_ = col.box()
                    col_ = box_.column(align = True)
                    col_.scale_y = 1.2
                    row1 = col_.row()

                    #MATERIAL CONTROL DATA
                    #-------------------------------------------------------------------------------------------------
                    if len(get_materials()) > 0:
                        mattName = bpy.data.materials[bpy.context.scene.bv2_tools.mattList].name
                        mattData = bpy.data.materials[mattName]
                        material_nt_data = bpy.data.materials[mattName].node_tree.nodes
                        node_data = bpy.data.node_groups[bgenModName].nodes

                        #Eevee Material
                        emix1Node = material_nt_data['Eevee Mix']
                        ecolvar = material_nt_data['Eevee Variation']
                        egrad = material_nt_data['Eevee Gradient']
                        ebsdf = material_nt_data['Eevee bsdf']

                        #Cycles Material
                        cgrad = material_nt_data['Cycles Gradient']
                        cbsdf = material_nt_data['Cycles bsdf']
                        ccolvar = material_nt_data['Cycles Variation']
                        
                        #MATERIAL DRWAWER
                        if obj_exp.my_expT1: #MATERIAL DRAWER OPEN
                            row1.prop(obj_exp, "my_expT1",icon="TRIA_DOWN", text="MATERIAL", emboss=False)
                            matCntr.draw(context, row1, matNode, text = '')
                            mbox1 = col_.box()
                            mcol1 = mbox1.column(align = True)
                            mrow1 = mcol1.row(align = True)
                            mrow1.scale_x = 1.1
                            mrow1.scale_y = 1.2
                            
                            mrow_ = col_.row()
                            mytool = context.scene.bv2_tools

                            mrow1.prop(mytool, "mattList", text = "", icon = "MATERIAL", icon_only = True)
                            mts_ = bpy.data.materials[bpy.context.scene.bv2_tools.mattList]
                            mrow1.prop(mts_,"name", text = "",toggle=True, emboss = True)
                            mrow1.operator("object.bv2_single_user_matt", text="", icon = "DUPLICATE")

                            mrow_.prop(mytool, "mattren",expand = True)
                            
                            if bpy.context.scene.bv2_tools.mattren == 'EEVEE':
                                mbox_ = col_.box()
                                mcol_ = mbox_.column()
                                mrow_ = mcol_.row(align = True)
                                mrow_.label(text = "Hair Color:")

                                #-------------------------------------------------------------------------------
                                if 'color_switch_eevee' in material_nt_data and "ID:bv2_SC_001" in node_data:
                                    scCntr = node_data["ID:bv2_SC_001"].inputs[0]
                                    mrow_.prop(mytool, "material_color",expand = True)
                                    color_switch_eevee = material_nt_data["color_switch_eevee"]
                                    if bpy.context.scene.bv2_tools.material_color == "STRAND":
                                        mcol_.template_color_ramp(egrad, "color_ramp",expand = False)
                                    else:
                                        scCntr.draw(context, mcol_, dmNode, text = '')
                                    color_switch_eevee.inputs[0].draw(context, mrow_, color_switch_eevee, text = '')
                                else:
                                    mcol_.template_color_ramp(egrad, "color_ramp",expand = False)

                                #-------------------------------------------------------------------------------

                                row_ = col_.row(align = False)
                                grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=False)
                                grid_l.alignment = "RIGHT"
                                grid_l.scale_x = 1.4
                                grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=False)
                                
                                grid_l.label(text = "Color Variation")
                                grid_l.label(text = "            Metalic")
                                grid_l.label(text = "         Specular")
                                grid_l.label(text = "      Roughness")
                                grid_l.label(text = "   Transmission")
                                
                                ecolvar.inputs[7].draw(context, grid_r, ecolvar, text = '')
                                ebsdf.inputs[6].draw(context, grid_r, emix1Node, text = '')
                                ebsdf.inputs[7].draw(context, grid_r, emix1Node, text = '')
                                ebsdf.inputs[9].draw(context, grid_r, emix1Node, text = '')
                                ebsdf.inputs[17].draw(context, grid_r, emix1Node, text = '')
                            
                            if bpy.context.scene.bv2_tools.mattren == 'CYCLES':
                                mbox_ = col_.box()
                                mcol_ = mbox_.column()
                                mrow_ = mcol_.row(align = True)
                                mrow_.label(text = "Hair Color:")
                                #-------------------------------------------------------------------------------
                                if 'color_switch_cycles' in material_nt_data and "ID:bv2_SC_001" in node_data:
                                    scCntr = node_data["ID:bv2_SC_001"].inputs[0]
                                    mrow_.prop(mytool, "material_color",expand = True)
                                    color_switch_cycles = material_nt_data["color_switch_cycles"]
                                    if bpy.context.scene.bv2_tools.material_color == "STRAND":
                                        mcol_.template_color_ramp(cgrad, "color_ramp",expand = False)
                                    else:
                                        scCntr.draw(context, mcol_, dmNode, text = '')
                                    color_switch_cycles.inputs[0].draw(context, mrow_, color_switch_cycles, text = '')
                                else:
                                    mcol_.template_color_ramp(cgrad, "color_ramp",expand = False)

                                #-------------------------------------------------------------------------------
                                
                                row_ = col_.row(align = False)
                                grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=False)
                                grid_l.alignment = "RIGHT"
                                grid_l.scale_x = 1.2
                                grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=False)
                                
                                grid_l.label(text = "      Color Variation")
                                grid_l.label(text = "            Roughness")
                                grid_l.label(text = "Radial Roughness")
                                grid_l.label(text = "                        Coat")
                                grid_l.label(text = "Random Roughness")
                                grid_l.label(text = "                           IOR")
                                
                                ccolvar.inputs[7].draw(context, grid_r, ecolvar, text = '')
                                cbsdf.inputs[5].draw(context, grid_r, emix1Node, text = '')
                                cbsdf.inputs[6].draw(context, grid_r, emix1Node, text = '')
                                cbsdf.inputs[7].draw(context, grid_r, emix1Node, text = '')
                                cbsdf.inputs[11].draw(context, grid_r, emix1Node, text = '')
                                cbsdf.inputs[8].draw(context, grid_r, emix1Node, text = '')
                        else: #MATERIAL DRAWER CLOSE
                            row1.prop(obj_exp, "my_expT1",icon="TRIA_RIGHT", text="MATERIAL", emboss=False)
                            matCntr.draw(context, row1, matNode, text = '')

                    else:
                        row1.label(text="BGEN Material not available")
                        
            # DEFORMERS TAB
            if bpy.context.scene.bv2_tools.utilDrawer == "DEFORMERS":
                if mainCurve and get_gNode(obj)[2] == "ID:BV2_0001":
                    #================================================================================================================
                                                                    #[HAIR STRANDS]    
                    #================================================================================================================
                    #box = box_main.box()
                    fc_clump_01 = bpy.data.node_groups[bgenModName].nodes['bv2_Float_CLUMP_01']
                    fc_clump_02 = bpy.data.node_groups[bgenModName].nodes['bv2_Float_CLUMP_02']
                    
                    box = col.box()
                    col1 = box.column(align = True)
                    col1.scale_y = 1.2
                    row1 = col1.row()
                    
                    # HAIR STRANDS DRAWER
                    if obj_exp.my_exp2:
                        row1.prop(obj_exp, "my_exp2",icon="TRIA_DOWN", text="HAIR STRANDS", emboss=False)
                        row1.label(text = "", icon = "OUTLINER_DATA_CURVES")
                        
                        box_00 = col1.box()
                        box_ = col1.box()
                        col_ = box_.column()
                        col_.scale_y = 1.2
                        
                        #-------------------------------------------------------------------------------------------------
                        colhs = box_00.column()
                        
                        hSize = colhs.row(align = True)
                        hSize.scale_y = 1.2
                        
                        hSize.prop(bgenMod, '["Input_39"]', text = 'Root Width')
                        hSize.prop(bgenMod, '["Input_40"]', text = 'Tip Width')
                        #-------------------------------------------------------------------------------------------------
                        if obj.modifiers[bgenMod.name]["Input_66"] == False:
                            row_ = col_.row(align = False)

                            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            grid_l.alignment = "RIGHT"
                            grid_l.scale_x = 1.3
                            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            
                            grid_l.label(text = "      Viewport Amount")
                            grid_l.label(text = "Interpulation Amount")
                            

                            grid_r.prop(bgenMod, '["Input_12"]', text = '')
                            grid_r.prop(bgenMod, '["Input_8"]', text = '')
                            

                            if obj_exp.my_exp8:
                                col_.prop(obj_exp, "my_exp8",icon="TRIA_DOWN", text="Less Settings", emboss=False)
                                row_ = col_.row(align = False)

                                grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                                grid_l.alignment = "RIGHT"
                                grid_l.scale_x = 1.3
                                grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                                #grid_l.separator(factor=.5)
                                #grid_l.label(text = "                       Density")
                                #grid_l.label(text = "          Density Radius")
                                #grid_l.separator(factor=.5)
                                grid_l.label(text = "             Mesh Subdiv")
                                grid_l.label(text = "Interpulation Guides")
                                #grid_l.label(text = "           [Clump Factor]")

                                #grid_r.separator(factor=.5)
                                #grid_r.prop(bgenMod, '["Input_11"]', text = '')
                                #grid_r.prop(bgenMod, '["Input_13"]', text = '')
                                #grid_r.separator(factor=.5)
                                grid_r.prop(bgenMod, '["Input_63"]', text = '')
                                grid_r.prop(bgenMod, '["Input_64"]', text = '')
                                #grid_r.prop(bgenMod, '["Input_38"]', text = '')
                            else:
                                col_.prop(obj_exp, "my_exp8",icon="TRIA_RIGHT", text="More Settings", emboss=False)
                        else:
                            row_ = col_.row(align = False)

                            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            grid_l.alignment = "RIGHT"
                            grid_l.scale_x = 1.3
                            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            
                            grid_l.label(text = "Viewport Amount")
                            grid_l.label(text = "Children Amount")
                            grid_l.label(text = "                   Radius")


                            grid_r.prop(bgenMod, '["Input_67"]', text = '')
                            grid_r.prop(bgenMod, '["Input_68"]', text = '')
                            grid_r.prop(bgenMod, '["Input_69"]', text = '')

                            if bgenMod["Input_70"] != None:
                                col_.prop(bgenMod, '["Input_70"]', text = 'Even Thickness')

                        
                        '''
                        row_.label(text = 'Viewport Amount: ')
                        row_.prop(bgenMod, '["Input_12"]', text = '')
                        
                        row_ = col_.row(align = True)
                        row_.label(text = 'Interpulation Amount: ')
                        row_.prop(bgenMod, '["Input_8"]', text = '')
                        '''
                        #------------------------------------------------------------------------
                        row_ = col_.row(align = False)
                        row_.prop(bgenMod, '["Input_51"]', text = 'Guide Clump',icon="BRUSH_CURVES_PINCH")
                        
                        if bgenMod["Input_50"] == 1:
                            row_.prop(bgenMod, '["Input_50"]', text = 'Interpulated Clump:',icon="BRUSH_CURVES_PINCH")
                            col_.prop(bgenMod, '["Input_52"]', text = 'Interpulated Clump Amount')
                        else:
                            row_.prop(bgenMod, '["Input_50"]', text = 'Interpulated Clump:',icon="BRUSH_CURVES_PINCH")
                            
                        # [Clump_02 Float Curve]
                        fcc = col1.box()
                        fcr = fcc.row()
                        if obj_exp.my_expF2:
                            fcr.prop(obj_exp, "my_expF2",icon="TRIA_DOWN", text="Clump Profile", emboss=False)
                            
                            mytool = context.scene.bv2_tools
                            fcr = fcc.row(align = True)
                            fcc.scale_x = 1.4
                            fcr.prop(mytool, "clumpChoice",expand = True)
                            if bpy.context.scene.bv2_tools.clumpChoice == 'BIGCLUMP':
                                fc_clump_02.draw_buttons_ext(context, fcc)
                            if bpy.context.scene.bv2_tools.clumpChoice == 'SMALLCLUMP':
                                fc_clump_01.draw_buttons_ext(context, fcc)
                        else:
                            fcr.prop(obj_exp, "my_expF2",icon="TRIA_RIGHT", text="Clump Profile", emboss=False)
                    else:
                        row1.prop(obj_exp, "my_exp2",icon="TRIA_RIGHT", text="HAIR STRANDS", emboss=False)
                        row1.label(text = "", icon = "OUTLINER_DATA_CURVES")
                            
                        
                    #================================================================================================================
                                                                    #[CURL]    
                    #================================================================================================================
                    fc_curl_01 = bpy.data.node_groups[bgenModName].nodes['bv2_Float_CURL_01']
                    
                    #box = box_main.box()
                    box = col.box()
                    col1 = box.column(align=True)
                    col1.scale_y = 1.2
                    row1 = col1.row()
                    
                    if obj_exp.my_exp3:
                        row1.prop(obj_exp, "my_exp3",icon="TRIA_DOWN", text="CURL", emboss=False)
                        row1.prop(bgenMod, '["Input_16"]', text = '')
                        box_ = col1.box()
                        col_ = box_.column()
                        col_.scale_y = 1.2
                        row_ = col_.row(align = True)
                        
                        mytool = context.scene.bv2_tools
                        #row_.prop(mytool, "curlType",expand = True)
                        #bgenMod(obj)["Input_57"]
                        row_.prop(bgenMod, '["Input_57"]', text = 'Curl Type 1', expand = True, icon = "CURVES", invert_checkbox = True)
                        row_.prop(bgenMod, '["Input_57"]', text = 'Curl Type 2', expand = True, icon = "CURVES")
                        
                        if obj.modifiers[bgenMod.name]["Input_57"] == False:

                            row_ = box_.row(align = False)
                            row_.scale_y = 1.2
                            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            grid_l.alignment = "RIGHT"
                            grid_l.scale_x = 1.5
                            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            
                            grid_l.label(text = "     Resolution")
                            grid_l.label(text = "     Frequency")
                            grid_l.label(text = "    Curl Radius")
                            grid_l.label(text = "Random Offset")

                            grid_r.prop(bgenMod, '["Input_17"]', text = '')
                            grid_r.prop(bgenMod, '["Input_18"]', text = '')
                            grid_r.prop(bgenMod, '["Input_19"]', text = '')
                            grid_r.prop(bgenMod, '["Input_59"]', text = '')
                        
                        if obj.modifiers[bgenMod.name]["Input_57"] == True:
                            
                            row_ = box_.row(align = False)
                            row_.scale_y = 1.2
                            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            grid_l.alignment = "RIGHT"
                            grid_l.scale_x = 1.5
                            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            
                            grid_l.label(text = "     Resolution")
                            grid_l.label(text = "     Frequency")
                            grid_l.label(text = "    Curl Radius")
                            grid_l.label(text = "Random Offset")
                            
                            grid_r.prop(bgenMod, '["Input_17"]', text = '')
                            grid_r.prop(bgenMod, '["Input_18"]', text = '')
                            grid_r.prop(bgenMod, '["Input_19"]', text = '')
                            grid_r.prop(bgenMod, '["Input_60"]', text = '')
                        
                        # [Curl Float Curve]
                        fcc = col1.box()
                        fcr = fcc.row()
                        fcc.scale_x = 1.2
                        
                        if obj_exp.my_expF3:
                            fcr.prop(obj_exp, "my_expF3",icon="TRIA_DOWN", text="Curl Profile", emboss=False)
                            fc_curl_01.draw_buttons_ext(context, fcc)
                        else:
                            fcr.prop(obj_exp, "my_expF3",icon="TRIA_RIGHT", text="Curl Profile", emboss=False)
                    else:
                        row1.prop(obj_exp, "my_exp3",icon="TRIA_RIGHT", text="CURL", emboss=False)
                        row1.prop(bgenMod, '["Input_16"]', text = '')
                        
                    #================================================================================================================
                                                                    #[BRAID]    
                    #================================================================================================================
                    fc_braid_01 = bpy.data.node_groups[bgenModName].nodes['bv2_Float_BRAID_01']
                    #box = box_main.box()
                    box = col.box()
                    col1 = box.column(align=True)
                    col1.scale_y = 1.2
                    row1 = col1.row()
                    
                    if obj_exp.my_exp4:
                        row1.prop(obj_exp, "my_exp4",icon="TRIA_DOWN", text="BRAID", emboss=False)
                        row1.prop(bgenMod, '["Input_21"]', text = '')
                        box_ = col1.box()
                        col_ = box_.column()
                        col_.scale_y = 1.2
                        row_ = box_.row(align = False)
                        row_.scale_y = 1.2
                        
                        grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        grid_l.alignment = "RIGHT"
                        grid_l.scale_x = 1.6
                        grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        
                        grid_l.label(text = "       Resolution")
                        grid_l.label(text = "       Frequency")
                        grid_l.label(text = "     Braid Width")
                        grid_l.label(text = "Braid Thickness")

                        grid_r.prop(bgenMod, '["Input_22"]', text = '')
                        grid_r.prop(bgenMod, '["Input_23"]', text = '')
                        grid_r.prop(bgenMod, '["Input_24"]', text = '')
                        grid_r.prop(bgenMod, '["Input_49"]', text = '')
                        #grid_r.prop(bgenMod, '["Input_25"]', text = '')
                        
                        # [Braid Float Curve]
                        fcc = col1.box()
                        fcr = fcc.row()
                        fcc.scale_x = 1.2
                        if obj_exp.my_expF4:
                            fcr.prop(obj_exp, "my_expF4",icon="TRIA_DOWN", text="Braid Profile", emboss=False)
                            fc_braid_01.draw_buttons_ext(context, fcc)
                        else:
                            fcr.prop(obj_exp, "my_expF4",icon="TRIA_RIGHT", text="Braid Profile", emboss=False)
                    else:
                        row1.prop(obj_exp, "my_exp4",icon="TRIA_RIGHT", text="BRAID", emboss=False)
                        row1.prop(bgenMod, '["Input_21"]', text = '')
                    
                    #================================================================================================================
                                                                    #[NOISE]    
                    #================================================================================================================
                    #box = box_main.box()
                    box = col.box()
                    col1 = box.column(align=True)
                    col1.scale_y = 1.2
                    row1 = col1.row()
                    
                    if obj_exp.my_exp5:
                        row1.prop(obj_exp, "my_exp5",icon="TRIA_DOWN", text="NOISE", emboss=False)
                        row1.prop(bgenMod, '["Input_31"]', text = '')
                        box_ = col1.box()
                        col_ = box_.column()
                        col_.scale_y = 1.2
                        row_ = box_.row(align = False)
                        row_.scale_y = 1.2
                        
                        grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        grid_l.alignment = "RIGHT"
                        grid_l.scale_x = 1.5
                        grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        
                        grid_l.label(text = "  Resolution")
                        grid_l.label(text = " Frequency")
                        grid_l.label(text = "Noise Width")
                        
                        grid_r.prop(bgenMod, '["Input_32"]', text = '')
                        grid_r.prop(bgenMod, '["Input_33"]', text = '')
                        grid_r.prop(bgenMod, '["Input_34"]', text = '')
                        
                        fcc = col1.box()
                        fcr = fcc.row()
                        fcc.scale_x = 1.2
                        if obj_exp.my_expF5:
                            fcr.prop(obj_exp, "my_expF5",icon="TRIA_DOWN", text="Fly Away Strands", emboss=False)
                            fcr.prop(bgenMod, '["Input_53"]', text = '')
                            row_ = fcc.row(align = False)
                            row_.scale_y = 1.2
                            
                            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            grid_l.alignment = "RIGHT"
                            grid_l.scale_x = 1.2
                            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            
                            grid_l.label(text = "        Amount")
                            grid_l.label(text = "Displacement")
                            grid_l.label(text = "          Length")
                            grid_l.label(text = "              Seed")
                        
                            grid_r.prop(bgenMod, '["Input_55"]', text = '')
                            grid_r.prop(bgenMod, '["Input_54"]', text = '')
                            grid_r.prop(bgenMod, '["Input_65"]', text = '')
                            grid_r.prop(bgenMod, '["Input_56"]', text = '')
                            
                        else:
                            fcr.prop(obj_exp, "my_expF5",icon="TRIA_RIGHT", text="Fly Away Strands", emboss=False)
                            fcr.prop(bgenMod, '["Input_53"]', text = '')
                    else:
                        row1.prop(obj_exp, "my_exp5",icon="TRIA_RIGHT", text="NOISE", emboss=False)
                        row1.prop(bgenMod, '["Input_31"]', text = '')
                        
                    #================================================================================================================
                                                                    #[TRIM]    
                    #================================================================================================================
                    tmCntr = bpy.data.node_groups[bgenModName].nodes["ID:bv2_TM_001"].inputs[1]
                    tmNode = bpy.data.node_groups[bgenModName].nodes["ID:bv2_TM_001"]
                    
                    #box = box_main.box()
                    box = col.box()
                    col1 = box.column(align = True)
                    col1.scale_y = 1.2
                    row1 = col1.row()
                    
                    if obj_exp.my_exp6:
                        row1.prop(obj_exp, "my_exp6",icon="TRIA_DOWN", text="TRIM", emboss=False)
                        row1.prop(bgenMod, '["Input_36"]', text = '')
                        
                        box_ = col1.box()
                        col_ = box_.column()
                        col_.scale_y = 1.2
                        col_.prop(bgenMod, '["Input_62"]', text = 'Length Variation')
                        
                        box_ = col1.box()
                        col_ = box_.column()
                        col_.scale_y = 1.2
                        col_.label(text = "Trim Mask:")
                        tmCntr.draw(context, col_, tmNode, text = '')
                        #bpy.context.scene.bv2_tools.texture 
                    else:
                        row1.prop(obj_exp, "my_exp6",icon="TRIA_RIGHT", text="TRIM", emboss=False)
                        row1.prop(bgenMod, '["Input_36"]', text = '')
                        
            # SIMULATION TAB   
            if bpy.context.scene.bv2_tools.utilDrawer == "SIMULATION":     
                #================================================================================================================
                                                                #[SIM-SETTINGS]    
                #================================================================================================================
                myTools = context.scene.bv2_tools
                mytool = context.scene.bv2_tools
                obj_exp = context.object.bv2_expand
                #main_obj = obj.name
                
                #----------------------------------------------------------------------------------------------------------------
                #col = layout.column()
                cols = col.column(align = True)
                cols.scale_y = 1.6
                cols.operator("object.bv2_create_sim_guides", text="Create Sim Guides", icon = "FORCE_WIND", depress = True)
                
                box_ = col.box()
                sgCol = box_.column(align = False)
                sgCol.scale_y = 1.4
                sgRow = sgCol.row()
                    
                scrow = sgCol.row(align = True, heading = "")
                scrow.scale_x = 1.2
                
                scrow.prop(bv2_tools, "sim_collection", text = "", icon = "COLLECTION_COLOR_05")
                scrow.operator("object.bv2_remove_sim_collection", text="", icon = "CANCEL")
                #simCol = bpy.data.materials[bpy.context.scene.bv2_tools.sim_collection]
                    
                if mainCurve and get_gNode(obj)[2] == "ID:BV2_0001":
                    collCntr = bpy.data.node_groups[bgenModName].nodes["ID:bv2_CC_001"].inputs[1]
                    collNode = bpy.data.node_groups[bgenModName].nodes["ID:bv2_CC_001"] 
                    
                    #sgRow = col.row(align = True)
                    sgRow.prop(bgenMod, '["Input_2"]', text = 'Use Sim Guides')
                    collCntr.draw(context, sgRow, collNode, text = '')
                #----------------------------------------------------------------------------------------------------------------
            
                
                
                box = col.box()
                col1 = box.column()
                col1.scale_y = 1.2
                row1 = col1.row()
                if obj_exp.my_exp7:
                    row1.prop(obj_exp, "my_exp7",icon="TRIA_DOWN", text="HAIR SIM", emboss=False)
                    row1.label(text = "", icon = "OUTLINER_OB_POINTCLOUD")
                    col_ = col1.column()
                    col_.scale_y = 1.4
                    vbox = col_.box()
                    vcol = vbox.column()
                    vcol.scale_x = 1.2
                    vrow = vcol.row(align = True)
                    
                    #bpy.context.scene.bv2_tools.vts_mod = 'ID:BV2_VtoS_0001'
                    #vtsNode = bpy.data.node_groups["00_bv2: [Vertex To Strip]"].name
                    try:
                        vtsNode = bpy.data.node_groups[bpy.context.scene.bv2_tools.vts_mod].name
                        swCntr = bpy.data.node_groups[vtsNode].nodes["ID:bv2_SW_001"].inputs[4]
                        swNode = bpy.data.node_groups[vtsNode].nodes["ID:bv2_SW_001"]
                    
                        #bpy.ops.node.new_geometry_node_group_assign()
                        
                        vrow.prop(myTools, "vts_mod", text = "", icon = "NODETREE", icon_only = True)
                        vts_ = bpy.data.node_groups[bpy.context.scene.bv2_tools.vts_mod]
                        vrow.prop(vts_,"name", text = "",toggle=True, emboss = True)
                        vrow.prop(vts_,"use_fake_user", text = "",toggle=True, emboss = True)
                        vrow.operator("object.bv2_single_user_vts", text="", icon = "DUPLICATE")
                    except:
                        vrow.label(text = "[VTS NODE NOT AVIALABLE]")
                    
                    row_ = col_.row()
                    grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                    grid_l.alignment = "RIGHT"
                    grid_l.scale_x = 1.1
                    grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        
                    
                    grid_l.label(text = "       Sim Collection:", icon = "COLLECTION_COLOR_05")
                    grid_l.label(text = "Collision Collection:", icon = "COLLECTION_COLOR_01")
                    
                    grid_r.prop(mytool, "sim_collection", text = "")
                    grid_r.prop(mytool, "col_collection", text = "")
                    
                    
                    
                    try:
                        fc_wp = bpy.data.node_groups[vtsNode].nodes['Vertex_Paint_FC'] 
                    except:
                        pass
                    
                    #[Weight Paint Float Curve]
                    col_ = col1.column()
                    fcc = col1.box()
                    fcr = fcc.row()
                    
                    if obj_exp.my_expS1:
                        fcr.prop(obj_exp, "my_expS1",icon="TRIA_DOWN", text="Weigth Paint", emboss=False)
                        try:
                            fc_wp.draw_buttons_ext(context, fcc)
                        except:
                            fcc.label(text = "[VTS NODE NOT AVIALABLE]")
                    
                    else:
                        fcr.prop(obj_exp, "my_expS1",icon="TRIA_RIGHT", text="Weigth Paint", emboss=False)
                        

                    boxSv = col1.box()
                    colSv = boxSv.column(align = False)
                    colSv.scale_y = 1.2
                    rowSv = colSv.row()
                    
                    if obj_exp.my_expS2:
                        rowSv.prop(obj_exp, "my_expS2",icon="TRIA_DOWN", text="Sim Values", emboss=False)
                        row_ = colSv.row()
                        grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                        grid_l.alignment = "RIGHT"
                        grid_l.scale_x = 1.8
                        grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            
                        grid_l.label(text = "      Quality")
                        grid_l.label(text = "Air Viscusity")
                        grid_l.label(text = "         Mass")
                        grid_l.label(text = "      Gravity")
                        grid_l.label(text = "      Tension")
                        grid_l.separator()

                        grid_r.prop(mytool, "my_int1", text = "")
                        grid_r.prop(mytool, "my_float6", text = "")
                        grid_r.prop(mytool, "my_float1", text = "")
                        grid_r.prop(mytool, "my_float2", text = "")
                        grid_r.prop(mytool, "my_float3", text = "")

                        if obj_exp.my_exp10:
                            colSv.prop(obj_exp, "my_exp10",icon="TRIA_DOWN", text="Bake to Cache Settings", emboss=False)
                            row_ = colSv.row(align = False)

                            grid_l = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)
                            grid_l.alignment = "RIGHT"
                            grid_l.scale_x = 1.3
                            grid_r = row_.grid_flow(row_major=False, columns=1, even_columns=False, even_rows=False, align=True)

                            grid_l.label(text = "Simulation Start")
                            grid_l.label(text = "               End")
                            grid_l.label(text = "")

                            grid_r.prop(mytool, "sim_start", text = "")
                            grid_r.prop(mytool, "sim_end", text = "")
                            grid_r.prop(mytool, "disk_cache", text = "Use Disk Cache")

                            col_cache = colSv.column()
                            col_cache.alignment = "RIGHT"
                            if bpy.context.scene.bv2_tools.sim_collection != "":
                                sim_obj_data = bpy.data.collections[bpy.context.scene.bv2_tools.sim_collection].objects[0]
                                for mod in sim_obj_data.modifiers:
                                    if mod.type == "CLOTH":
                                        cache_data = sim_obj_data.modifiers["Cloth"].point_cache
                                        col_cache.label(text = cache_data.info)
                            else:
                                pass

                        else:
                            colSv.prop(obj_exp, "my_exp10",icon="TRIA_RIGHT", text="Bake to Cache Settings", emboss=False)
                        
                        
  
                    else:
                        rowSv.prop(obj_exp, "my_expS2",icon="TRIA_RIGHT", text="Sim Values", emboss=False)
                    
                    colSv = boxSv.column()
                    rowSv = colSv.row(align = False)
                    
                    colsm = colSv.column(align=False)
                    rowsm = colsm.row()
                    colsm.scale_y = 1.8
                    rowsm.scale_y = .6
                    rowsm.prop(mytool, "simToggle_", expand = True)
                    colsm.operator('object.bv2_execute_cloth_settings')
                    
                    #col1.label(text = 'Simulation Cache')
                    boxSv = col1.box()
                    colSv = boxSv.column(align = False)
                    colSv.scale_y = 1.2

                    scene = bpy.context.scene
                    frame_count = scene.frame_end - scene.frame_start + 1

                    row_ = colSv.row()
                    
                    col_cache = colSv.column()
                    col_cache.alignment = "RIGHT"
                    if bpy.context.scene.bv2_tools.sim_collection != "":
                        sim_obj_data = bpy.data.collections[bpy.context.scene.bv2_tools.sim_collection].objects[0]
                        for mod in sim_obj_data.modifiers:
                            if mod.type == "CLOTH":
                                cache_data = sim_obj_data.modifiers["Cloth"].point_cache
                                col_cache.label(text = "Current baking cache starts at [" + 
                                                str(cache_data.frame_start) + "] and ends at frame [" + str(cache_data.frame_end)+"]")
                    else:
                        pass

                    rowSv = colSv.row()
                    rowSv.scale_y = 1.2
                    #rowSv.operator("ptcache.bake_all")
                    rowSv.operator("object.bake_hair_sim",text="Bake all Physics")
                    rowSv.operator("ptcache.free_bake_all")
                               
                else:
                    row1.prop(obj_exp, "my_exp7",icon="TRIA_RIGHT", text="HAIR SIM", emboss=False)
                    row1.label(text = "", icon = "OUTLINER_DATA_POINTCLOUD")
                
                
    
        #except:
        #    pass
        #    print("An error occurred:")
              
@addon_updater_ops.make_annotations
class BV2_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # Addon updater preferences.
    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True)

    updater_interval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)

    updater_interval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=0,
        max=31)

    updater_interval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_interval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        box = col.box()
        col1 = box.column()
        col1.label(text= "Prefereces go here")  
        
        addon_updater_ops.update_settings_ui(self,context)

# [REGISTER]       
#===================================================================================


bv2Classes = (BV2_UL_hair_curves, BV2_PT_bv2Properties, BV2_PT_bv2ExpandProp, BV2_PT_ui_panel, BV2_OT_groom_curve, BV2_OT_duplicate_hair,
                BV2_OT_exit_sculpt_mode, BV2_OT_create_sim_guides, BV2_OT_create_sculpt_guide, BV2_OT_single_user, 
                BV2_OT_single_user_vts, BV2_OT_single_user_matt, BV2_OT_choose_nodeTree, BV2_OT_rename_nodeTree, BV2_OT_resample_guides,
                BV2_OT_generate_guides, BV2_OT_add_empty_hair, BV2_OT_apply_guides, BV2_OT_delete_guides, BV2_OT_rescale_hair, 
                BV2_OT_remove_sim_collection, BV2_OT_remove_empty_hair, BV2_OT_hide_hair_curve, BV2_OT_execute_cloth_settings,BV2_preferences,BV2_OT_bake_hair_sim)
                

def register():  
    addon_updater_ops.register(bl_info)
    bpy.types.Object.hair_curves_active_index = bpy.props.IntProperty(
        name="Hair Curves Active Index",
        description="Index that points to one of the hair curves child objects of this object (if any, otherwise should be -1), intended to be used with UIList and template_list",
        get=get_hair_curves_active_index,
        set=set_hair_curves_active_index,
    )
    for cls in bv2Classes:
        addon_updater_ops.make_annotations(cls)
        bpy.utils.register_class(cls)
    bpy.types.Scene.bv2_tools = bpy.props.PointerProperty(type= BV2_PT_bv2Properties)
    bpy.types.Object.bv2_expand = bpy.props.PointerProperty(type= BV2_PT_bv2ExpandProp)

                         
def unregister(): 
    addon_updater_ops.unregister()
    for cls in bv2Classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bv2_tools
    del bpy.types.Object.bv2_expand
    del bpy.types.Object.hair_curves_active_index
    
'''                 
if __name__ == "__main__":
    register()
    unregister()
'''