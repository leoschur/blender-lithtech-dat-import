import bpy
import bmesh
import numpy
from os.path import splitext, basename
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from .kaitai_lithtech_dat_struct import LithtechDat
from mathutils import Vector


def createRenderNode(parent, rn_name, rn):
    """Create a collection for the render node and all objects within
    Positional arguments:
        parent: parent collection the node gets appended to
        rn_name: name for the render node collection
        rn: the data for the render node from type LithtechDat.RenderNode
    """
    # renderNode
    renderNode_collection = bpy.data.collections.new(rn_name)
    #
    # render nodes can no vertices
    if 0 < rn.num_vertices:
        #
        vertices = [[*map(lambda x: x*0.01, [v.v_pos.x, v.v_pos.z, v.v_pos.y])]
                    for v in rn.vertices]
        triangles = [tri.t for tri in rn.triangles]
        tri_counts = [s.triangle_count for s in rn.sections]
        #
        for i, s in enumerate(rn.sections):
            t_from = sum(tri_counts[:i])
            t_till = t_from + tri_counts[i]
            #
            # this steps undercuts the polyIndex
            section_tris = [t.t for t in rn.triangles[t_from:t_till]]
            # dont forget about polyIndices
            section_tris_poly_indices = [
                t.poly_index for t in rn.triangles[t_from:t_till]]
            # preparation for next step
            section_tris = numpy.asarray(section_tris).reshape(-1)
            section_vert_indices = numpy.unique(section_tris)
            # find for each triangle the new correct indices to the separated vertices
            section_tris = numpy.asarray(
                [(numpy.where(section_vert_indices == t))[0][0] for t in section_tris])
            # reshape back to triangle
            section_tris = section_tris.reshape(
                len(section_tris) // 3, 3).tolist()
            #
            # now we separate the verticies from the render node to the section
            # one bmesh for each section
            bm = bmesh.new()
            for i in section_vert_indices:
                bm.verts.new([
                    rn.vertices[i].v_pos.x * 0.01,
                    rn.vertices[i].v_pos.z * 0.01,
                    rn.vertices[i].v_pos.y * 0.01
                ])
                continue
            bm.verts.ensure_lookup_table()
            # for debugging (does the same thing)
            # section_vertices = [[rn.vertices[i].v_pos.x * 0.01,rn.vertices[i].v_pos.z * 0.01,rn.vertices[i].v_pos.y * 0.01] for j in section_vert_indices]
            # create the faces from triangles
            for t, poly_index in zip(section_tris, section_tris_poly_indices):
                verts = [bm.verts[i] for i in t]
                # face can already exist
                try:
                    face = bm.faces.new(verts)
                    bm.faces.ensure_lookup_table()
                    face.material_index = poly_index
                except:
                    pass
                continue
            #
            # still missing the texture from the section data can be empty if StrWithLen2 has length 0
            # texture_name0 = s.texture_name[0].data
            # texture_name1 = s.texture_name[1].data
            #
            m = bpy.data.meshes.new(f"{rn_name}_Section_{i:04}")
            bm.to_mesh(m)
            o = bpy.data.objects.new(f"{rn_name}_Object_{i:04}", m)
            renderNode_collection.objects.link(o)
            continue
        pass
    # no vertices available only create empty object
    else:
        o = bpy.data.objects.new(f"{rn_name}_Object", None)
        o.empty_display_type = 'CUBE'
        o.location = Vector((rn.v_center.x, rn.v_center.z, rn.v_center.y))
        o.empty_display_size = max(
            [rn.v_half_dims.x, rn.v_half_dims.z, rn.v_half_dims.y])
        renderNode_collection.objects.link(o)
        pass
    parent.children.link(renderNode_collection)
    return

# requires createRenderNode


def createWMRenderNode(parent, wmrn):
    """create a World Model Render Node
    Positional Arguments:
        parent: collection the render node is going to be append to
        wmrn: dat_importer.lithtech_dat.LithtechDat.RenderNode node to be created
    """
    node_collection = bpy.data.collections.new(f"WMRN_{wmrn.name.data}")
    for i, render_node in enumerate(wmrn.render_nodes):
        createRenderNode(
            node_collection, f"{wmrn.name.data}_RN_{i}", render_node)
        continue
    parent.children.link(node_collection)
    return

# requires createRenderNode


def createRenderNodes(parent, world):
    """create Render Nodes
    Positional Arguments:
        parent: collection the render node group is append to
        world: dat_importer.lithtech_dat.LithtechDat imported map file
    """
    render_nodes = bpy.data.collections.new("RenderNodes")
    for i, render_node in enumerate(world.render_data.render_nodes):
        createRenderNode(render_nodes, f"RenderNode_{i:03}", render_node)
        continue
    parent.children.link(render_nodes)
    return

# requires createRenderNode
# requires createWMRenderNode


def createWMRenderNodes(parent, world):
    """Create the World Model Render Nodes
    Positional Arguments:
        parent: the parent collection the world model render node group is append to
        world: dat_importer.lithtech_dat.LithtechDat imported map file
    """
    wm_render_nodes = bpy.data.collections.new("WMRenderNodes")
    for node in world.render_data.world_model_render_nodes:
        createWMRenderNode(wm_render_nodes, node)
        continue
    parent.children.link(wm_render_nodes)
    return


def createPhysicsData(parent, world):
    """Create the physics/ collision data
    Positional Arguments:
        parent: collection the data physics collection is append to
        world: dat_importer.lithtech_dat.LithtechDat imported map file
    """
    physics = vertigo.collision_data.polygons
    poly_vertices = []
    poly_triangles = []
    index = 0
    scale = 0.01
    for poly in physics:
        poly_triangles.append([])
        for vec in poly.vertices_pos:
            poly_vertices.append([vec.x * scale, vec.z * scale, vec.y * scale])
            poly_triangles[-1].append(index)
            index += 1
            continue
        continue
    m = bpy.data.meshes.new("CollisionData")
    m.from_pydata(poly_vertices, [], poly_triangles)
    o = bpy.data.objects.new("CollisionData", m)
    parent.objects.link(o)
    return


def read_some_data(C, filepath, use_some_setting):
    print("running read_some_data...")
    dat = LithtechDat.from_file(filepath)
    name = basename(splitext(filepath)[0])
    map = bpy.data.collections.new(name)
    createRenderNodes(map, dat)
    createWMRenderNodes(map, dat)
    C.collection.children.link(map)

    return {'FINISHED'}


class ImportLithtechDat(Operator, ImportHelper):
    """Import a Lithtech DAT map file
    This importer is developed and tested for Combat Arms maps.
    It should work for all Lithtech engine map files, but no guarantees!
    If you encounter any issue feel free to open a issue on GitHub.
    """
    # # important since its how bpy.ops.import_scene.lithtech_dat is constructed
    bl_idname = "import_scene.lithtech_dat"
    bl_label = "Import Lithtech DAT map (.dat)"

    # ImportHelper mixin class uses this
    filename_ext = ".dat"

    filter_glob: StringProperty(
        default="*.dat",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return read_some_data(context, self.filepath, self.use_setting)
