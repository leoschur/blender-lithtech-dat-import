import bpy
import bmesh
import numpy as np
from os.path import splitext, basename, isfile
from itertools import accumulate
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator, Collection
from bpy.app.handlers import persistent
from .kaitai_lithtech_dat_struct import LithtechDat
from mathutils import Vector
from .utils import vec3_to_xzy, int32_to_rgba, decompress_lm_data


class ImportLithtechDat(Operator, ImportHelper):
    """Import a Lithtech DAT map file
    This importer is developed and tested for Combat Arms maps.
    It should work for all Lithtech engine map files, but no guarantees!
    If you encounter any issue feel free to open a issue on GitHub.
    """

    # # important since its how bpy.ops.import_scene.lithtech_dat is constructed
    bl_idname = "import_scene.lithtech_dat"
    bl_label = "Import Lithtech DAT map (.dat)"
    bl_context = "material"

    # ImportHelper mixin class uses this
    filename_ext = ".dat"

    filter_glob: StringProperty(
        default="*.dat",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )  # type: ignore

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    # use_setting: BoolProperty(
    #     name="Example Boolean",
    #     description="Example Tooltip",
    #     default=True,
    # )

    # type: EnumProperty(
    #     name="Example Enum",
    #     description="Choose between two items",
    #     items=(
    #         ('OPT_A', "First Option", "Description one"),
    #         ('OPT_B', "Second Option", "Description two"),
    #     ),
    #     default='OPT_A',
    # )

    def createTexture(self, rel_path):
        """Create a image_texture if it doesn't exist already
        Positional arguments:
            rel_path: [str] relative path to texture starting with textures or TEXTURES (root of texture folder)
        Returns:
            material: [bpy.types.Material] either newly created material or existing material
        """
        tex_path = rel_path.replace(".dtx", "")
        tex_name = tex_path.replace("textures\\", "").replace("TEXTURES\\", "")
        img_path = self.texture_dir_path + "\\" + tex_path + ".tga"
        mat = None
        if tex_name in bpy.data.materials:
            mat = bpy.data.materials[tex_name]
            pass
        elif isfile(img_path):
            mat = bpy.data.materials.new(tex_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            sn_om = nodes.get("Material Output")
            sn_bsdfp = nodes.get("Principled BSDF")
            links.new(sn_bsdfp.outputs["BSDF"], sn_om.inputs["Surface"])
            sn_tex = nodes.new(type="ShaderNodeTexImage")
            # TODO file exists at this point, but this might still fail for some reason
            img = bpy.data.images.load(img_path)
            sn_tex.image = img
            links.new(sn_tex.outputs["Color"], sn_bsdfp.inputs["Base Color"])
            links.new(sn_tex.outputs["Alpha"], sn_bsdfp.inputs["Alpha"])
            mat.blend_method = "CLIP"
            sn_uv = nodes.new(type="ShaderNodeUVMap")
            # TODO outsource uv_map
            sn_uv.uv_map = "uv0"
            links.new(sn_uv.outputs["UV"], sn_tex.inputs["Vector"])
            pass
        else:
            # TODO raise file not found
            pass
        return mat

    def createWorldModelNew(self, parent, wm):
        # TODO leftof here
        # mesh
        # - points (missung uvs?)
        # - polygons
        # - - plane
        # - - surface
        wm_name = f"WM_{wm.world_name.data}" if wm.world_name.num_data else "WM"
        node_collection = bpy.data.collections.new(wm_name)
        for i, node in enumerate(wm.nodes):
            bm = bmesh.new()
            node_name = f"Node_{i:05}"
            #
            poly = wm.polygons[node.poly_index]
            plane = wm.planes[poly.plane_index]
            surf = wm.surfaces[poly.surface_index]
            points = [bm.verts.new((wm.points[j].x * 0.01, wm.points[j].z * 0.01, wm.points[j].y * 0.01))
                      for j in poly.vertices_indices]
            #
            m = bpy.data.meshes.new(f"{node_name}_Mesh")
            bm.to_mesh(m)
            o = bpy.data.objects.new(f"{node_name}", m)
            node_collection.objects.link(o)
        parent.children.link(node_collection)
        pass

    def createWorldModel(self, parent: Collection, wm: LithtechDat.WorldModel):
        """Create a collection for the worldmodel
        Postional arguments:
            parent: [bpy.types.Collection] parent collection
            wm: [kaitai_lithtech_dat_struct.lithtech_dat.LithtechDat.WorldModel] worldmodel to create
        """
        bm = bmesh.new()
        if wm.num_points and wm.num_polygons:
            verts = [bm.verts.new((p.x * 0.01, p.z * 0.01, p.y * 0.01))
                     for p in wm.points]
            bm.verts.index_update()
            bm.verts.ensure_lookup_table()
            for p in wm.polygons:
                try:
                    bm.faces.new([verts[vi] for vi in p.vertices_indices])
                    pass
                except ValueError:
                    pass
                continue
            bm.faces.index_update()
            bm.faces.ensure_lookup_table()
            #
            name = wm.world_name.data if wm.world_name.num_data else "WM"
            m = bpy.data.meshes.new(f"{name}_Mesh")
            bm.to_mesh(m)
            o = bpy.data.objects.new(name, m)
            parent.objects.link(o)
            pass
        return

    def createRenderNode(self, parent, rn_name, rn):
        """Create a collection for the render node and all objects within
        Positional arguments:
            parent: parent collection the node gets appended to
            rn_name: name for the render node collection
            rn: the data for the render node from type LithtechDat.RenderNode
        """
        o = None
        #
        # render nodes has no vertices
        # TODO for now only render triangles that have a texture
        if 0 < rn.num_vertices and 0 < rn.num_triangles:
            # section beginnings
            t_till = list(accumulate([s.triangle_count for s in rn.sections]))
            # section endings
            t_from = [0] + t_till[:-1]
            for si, (s, tf, tt) in enumerate(zip(rn.sections, t_from, t_till)):
                match s.shader_code:  # EPCShaderType
                    case 0:  # No shading
                        pass
                    case 1:  # Textured and vertex-lit
                        # Might have a texture, might not have one
                        pass
                    case 2:  # Base light map
                        # This can be skipped, as lightmaps are not used
                        lm_name = f"LightMap_{rn_name}_S{si:04}"
                        img = bpy.data.images.new(
                            lm_name, width=s.lm_width, height=s.lm_height
                        )
                        img.pixels = decompress_lm_data(s.lm_data)
                        mat = bpy.data.materials.new(lm_name)
                        mat.use_nodes = True
                        nodes = mat.node_tree.nodes
                        links = mat.node_tree.links
                        sn_om = nodes.get("Material Output")
                        sn_bsdfp = nodes.get("Principled BSDF")
                        links.new(sn_bsdfp.outputs["BSDF"],
                                  sn_om.inputs["Surface"])
                        sn_tex = nodes.new(type="ShaderNodeTexImage")
                        sn_tex.image = img
                        links.new(sn_tex.outputs["Color"],
                                  sn_bsdfp.inputs["Base Color"])
                        sn_uv = nodes.new(type="ShaderNodeUVMap")
                        sn_uv.uv_map = "uv1"
                        links.new(sn_uv.outputs["UV"], sn_tex.inputs["Vector"])
                        pass
                    case 1 | 4 | 8 | 9:  # Texturing pass of lightmapping
                        # TODO this actually handles only case 4, other ones are slightly incorrect
                        # yet creating these this way is better than not handling them at all
                        bm = bmesh.new()
                        tris = np.sort([t.t for t in rn.triangles[tf:tt]])
                        # create the vertices for the current section
                        verts = np.unique(tris).tolist()
                        # actual vert index = np.searchsorted(verts, vert)
                        lay_col = bm.verts.layers.color.new("color")
                        lay_nor = bm.verts.layers.float_vector.new("normal")
                        lay_bin = bm.verts.layers.float_vector.new("binormal")
                        lay_tan = bm.verts.layers.float_vector.new("tangent")
                        for vi in verts:
                            v = rn.vertices[vi]
                            bm_vert = bm.verts.new(
                                [v.v_pos.x * 0.01, v.v_pos.z *
                                    0.01, v.v_pos.y * 0.01]
                            )
                            bm_vert.normal = Vector(
                                (v.v_normal.x, v.v_normal.y, v.v_normal.z)
                            )
                            bm_vert[lay_col] = int32_to_rgba(v.color)
                            bm_vert[lay_nor] = Vector(
                                (v.v_normal.x, v.v_normal.y, v.v_normal.z)
                            )
                            bm_vert[lay_bin] = Vector(
                                (v.v_binormal.x, v.v_binormal.y, v.v_binormal.z)
                            )
                            bm_vert[lay_tan] = Vector(
                                (v.v_tangent.x, v.v_tangent.y, v.v_tangent.z)
                            )
                            continue
                        bm.verts.ensure_lookup_table()
                        bm.verts.index_update()

                        # ignore poly_index for now
                        # lay_poly_index = bm.faces.layers.int.new("poly_index")
                        # create the triangles
                        for tri in tris:
                            # TODO this might raise value error for duplicate faces
                            try:
                                bm.faces.new([bm.verts[verts.index(i)]
                                              for i in tri])
                                pass
                            except ValueError:
                                pass
                            continue
                        bm.faces.ensure_lookup_table()
                        bm.faces.index_update()

                        lay_uv0 = bm.loops.layers.uv.new("uv0")
                        lay_uv1 = bm.loops.layers.uv.new("uv1")
                        for face in bm.faces:
                            for loop in face.loops:
                                # resolve index to grep lithtech vertex for uv data
                                v = rn.vertices[verts[loop.vert.index]]
                                loop[lay_uv0].uv = Vector((v.uv0.x, -v.uv0.y))
                                loop[lay_uv1].uv = Vector((v.uv1.x, -v.uv1.y))
                                continue
                            face.normal_update()
                            continue

                        # create object
                        m = bpy.data.meshes.new(
                            f"{rn_name}_Section{si:04}_Mesh")
                        bm.to_mesh(m)
                        o = bpy.data.objects.new(
                            f"{rn_name}_Section{si:04}", m)
                        o.data['Shader Code'] = s.shader_code
                        parent.objects.link(o)

                        # create and apply textures
                        if s.texture_name[0].num_data:
                            # TODO check if the ending can be '.DTX' as well
                            # tex_name = s.texture_name[0].data.replace('.dtx', '')
                            tex_path = s.texture_name[0].data.replace(
                                ".dtx", "")
                            tex_name = tex_path.replace("textures\\", "").replace(
                                "TEXTURES\\", ""
                            )
                            mat = None
                            img_path = self.texture_dir_path + "\\" + tex_path + ".tga"
                            # check if material already exists
                            if tex_name in bpy.data.materials:
                                mat = bpy.data.materials[tex_name]
                                pass
                            elif isfile(img_path):  # TODO handle if img_path doesn't exists
                                # if not create material with texture
                                mat = bpy.data.materials.new(tex_name)
                                mat.use_nodes = True
                                nodes = mat.node_tree.nodes
                                links = mat.node_tree.links
                                sn_om = nodes.get("Material Output")
                                sn_bsdfp = nodes.get("Principled BSDF")
                                links.new(
                                    sn_bsdfp.outputs["BSDF"], sn_om.inputs["Surface"])
                                sn_tex = nodes.new(type="ShaderNodeTexImage")
                                # TODO file exists at this point, but this might still fail for some reason
                                img = bpy.data.images.load(img_path)
                                sn_tex.image = img
                                links.new(
                                    sn_tex.outputs["Color"], sn_bsdfp.inputs["Base Color"]
                                )
                                links.new(
                                    sn_tex.outputs["Alpha"], sn_bsdfp.inputs["Alpha"])
                                mat.blend_method = "CLIP"
                                sn_uv = nodes.new(type="ShaderNodeUVMap")
                                # This is hardcoded and corresponds to the previously created UV layer
                                sn_uv.uv_map = "uv0"
                                links.new(sn_uv.outputs["UV"],
                                          sn_tex.inputs["Vector"])
                                pass
                            # append texture to object if not already done
                            if tex_name not in o.data.materials:
                                o.data.materials.append(mat)
                                pass
                            # find triangles and set material_index to corresponding texture
                            mat_idx = o.data.materials.find(tex_name)
                            # TODO handle when material was not found // could be because of case sensitivity
                            if 0 < mat_idx:
                                for face in bm.faces:
                                    face.material_index = mat_idx
                                    continue
                                pass
                            # update the mesh after modifying it!!!
                            bm.to_mesh(m)
                            pass
                        pass
                    case 5:  # Skypan
                        # TODO should refer to the Skybox in Blender
                        pass
                    case 6:  # Skyportal
                        # TODO should refer to the Area Lights/ Portal Lights in Blender
                        # https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html#area-lights
                        # skyportal data contained within the "outer" rendernode?
                        pass
                    case 7:  # Occluder
                        # occluder data contained within the "outer" rendernode?
                        pass
                    case 8:  # Gouraud shaded dual texture
                        pass
                    case 9:  # Texture stage of lightmap shaded dual texture
                        # (can) contains two textures/ textureNames
                        pass
                    case _:
                        pass
                continue
            pass
        # no vertices available only create empty object
        else:
            o = bpy.data.objects.new(f"{rn_name}_Object", None)
            o.empty_display_type = "CUBE"
            o.location = Vector((rn.v_center.x, rn.v_center.z, rn.v_center.y))
            o.empty_display_size = max(
                [rn.v_half_dims.x, rn.v_half_dims.z, rn.v_half_dims.y]
            )
            parent.objects.link(o)
            pass
        return

    # requires createRenderNode

    def createWMRenderNode(self, parent, wmrn):
        """create a World Model Render Node
        Positional Arguments:
            parent: collection the render node is going to be append to
            wmrn: dat_importer.lithtech_dat.LithtechDat.RenderNode node to be created
        """
        node_collection = bpy.data.collections.new(f"WMRN_{wmrn.name.data}")
        for i, render_node in enumerate(wmrn.render_nodes):
            self.createRenderNode(
                node_collection, f"{wmrn.name.data}_RN_{i}", render_node
            )
            continue
        parent.children.link(node_collection)
        return

    # requires createRenderNode

    def createRenderNodes(self, parent, world):
        """create Render Nodes
        Positional Arguments:
            parent: collection the render node group is append to
            world: dat_importer.lithtech_dat.LithtechDat imported map file
        """
        render_nodes = bpy.data.collections.new("RenderNodes")
        for i, render_node in enumerate(world.render_data.render_nodes):
            self.createRenderNode(
                render_nodes, f"RenderNode_{i:03}", render_node
            )
            continue
        parent.children.link(render_nodes)
        return

    # requires createRenderNode
    # requires createWMRenderNode

    def createWMRenderNodes(self, parent, world):
        """Create the World Model Render Nodes
        Positional Arguments:
            parent: the parent collection the world model render node group is append to
            world: dat_importer.lithtech_dat.LithtechDat imported map file
        """
        wm_render_nodes = bpy.data.collections.new("WMRenderNodes")
        for node in world.render_data.world_model_render_nodes:
            self.createWMRenderNode(wm_render_nodes, node)
            continue
        parent.children.link(wm_render_nodes)
        return

    def createPhysicsData(self, parent, world):
        """Create the physics/ collision data
        Positional Arguments:
            parent: collection the data physics collection is append to
            world: dat_importer.lithtech_dat.LithtechDat imported map file
        """
        physics = world.collision_data.polygons
        poly_vertices = []
        poly_triangles = []
        index = 0
        scale = 0.01
        for poly in physics:
            poly_triangles.append([])
            for vec in poly.vertices_pos:
                poly_vertices.append(
                    [vec.x * scale, vec.z * scale, vec.y * scale])
                poly_triangles[-1].append(index)
                index += 1
                continue
            continue
        m = bpy.data.meshes.new("CollisionData")
        m.from_pydata(poly_vertices, [], poly_triangles)
        o = bpy.data.objects.new("CollisionData", m)
        parent.objects.link(o)
        return

    texture_dir_path: StringProperty(
        name="Texture Directory",
        subtype="DIR_PATH",
        description="Select the folder containing the TEXTURES directory that contains the texture files in '*.tga' file format with the original folder structure!",
    )  # type: ignore

    # https://blender.stackexchange.com/a/8732
    @persistent
    def read_some_data(self, C):
        print("running read_some_data...")
        dat = LithtechDat.from_file(self.filepath)
        name = basename(splitext(self.filepath)[0])
        map = bpy.data.collections.new(name)
        self.createRenderNodes(map, dat)
        self.createWMRenderNodes(map, dat)
        self.createPhysicsData(map, dat)
        C.collection.children.link(map)

        return {"FINISHED"}

    def execute(self, context):
        # TODO check self.filepath
        # TODO check self.texture_dir_path
        return self.read_some_data(context)
