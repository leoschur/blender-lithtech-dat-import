# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from .kaitai_struct_python_runtime import kaitaistruct
from .kaitai_struct_python_runtime.kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class LithtechDat(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = LithtechDat.Header(self._io, self, self._root)
        self.world = LithtechDat.World(self._io, self, self._root)
        self.world_tree = LithtechDat.WorldTree(self._io, self, self._root)

    class WorldObjectProperty(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = LithtechDat.StrWithLen2(self._io, self, self._root)
            self.magic = self._io.read_u1()
            self.property_flags = self._io.read_u4le()
            self.len_data = self._io.read_u2le()
            _on = self.magic
            if _on == 0:
                self.data = LithtechDat.StrWithLen2(self._io, self, self._root)
            elif _on == 6:
                self.data = self._io.read_s4le()
            elif _on == 7:
                self.data = LithtechDat.Quaternion(self._io, self, self._root)
            elif _on == 1:
                self.data = LithtechDat.Vec3(self._io, self, self._root)
            elif _on == 3:
                self.data = self._io.read_f4le()
            elif _on == 5:
                self.data = self._io.read_u1()
            elif _on == 2:
                self.data = LithtechDat.Color(self._io, self, self._root)


    class WorldObject(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_object = self._io.read_u2le()
            self.object_type = LithtechDat.StrWithLen2(self._io, self, self._root)
            self.num_object_properties = self._io.read_u4le()
            if self.num_object_properties != 0:
                self.object_properties = []
                for i in range(self.num_object_properties):
                    self.object_properties.append(LithtechDat.WorldObjectProperty(self._io, self, self._root))




    class Vertex(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.v_pos = LithtechDat.Vec3(self._io, self, self._root)
            self.uv0 = LithtechDat.Vec2(self._io, self, self._root)
            self.uv1 = LithtechDat.Vec2(self._io, self, self._root)
            self.color = self._io.read_s4le()
            self.v_normal = LithtechDat.Vec3(self._io, self, self._root)
            self.v_tangent = LithtechDat.Vec3(self._io, self, self._root)
            self.v_binormal = LithtechDat.Vec3(self._io, self, self._root)


    class Plane(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.normal = LithtechDat.Vec3(self._io, self, self._root)
            self.dist = self._io.read_f4le()


    class Polygon(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.plane = LithtechDat.Plane(self._io, self, self._root)
            self.num_vertices_pos = self._io.read_u4le()
            self.vertices_pos = []
            for i in range(self.num_vertices_pos):
                self.vertices_pos.append(LithtechDat.Vec3(self._io, self, self._root))



    class Surface(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.flags = self._io.read_u4le()
            self.texture_index = self._io.read_u2le()
            self.texture_flags = self._io.read_u2le()


    class RenderNode(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.v_center = LithtechDat.Vec3(self._io, self, self._root)
            self.v_half_dims = LithtechDat.Vec3(self._io, self, self._root)
            self.num_sections = self._io.read_u4le()
            if self.num_sections != 0:
                self.sections = []
                for i in range(self.num_sections):
                    self.sections.append(LithtechDat.RenderSection(self._io, self, self._root))


            self.num_vertices = self._io.read_u4le()
            if self.num_vertices != 0:
                self.vertices = []
                for i in range(self.num_vertices):
                    self.vertices.append(LithtechDat.Vertex(self._io, self, self._root))


            self.num_triangles = self._io.read_u4le()
            if self.num_triangles != 0:
                self.triangles = []
                for i in range(self.num_triangles):
                    self.triangles.append(LithtechDat.Triangle(self._io, self, self._root))


            self.num_sky_portals = self._io.read_u4le()
            if self.num_sky_portals != 0:
                self.sky_portals = []
                for i in range(self.num_sky_portals):
                    self.sky_portals.append(LithtechDat.SkyPortal(self._io, self, self._root))


            self.num_occluder_polygons = self._io.read_u4le()
            if self.num_occluder_polygons != 0:
                self.occluder_polygons = []
                for i in range(self.num_occluder_polygons):
                    self.occluder_polygons.append(LithtechDat.OccluderPoly(self._io, self, self._root))


            self.num_light_groups = self._io.read_u4le()
            if self.num_light_groups != 0:
                self.light_groups = []
                for i in range(self.num_light_groups):
                    self.light_groups.append(LithtechDat.LightGroup(self._io, self, self._root))


            self.child_flags = self._io.read_u1()
            self.child_node_indices = []
            for i in range(2):
                self.child_node_indices.append(self._io.read_u4le())



    class WorldObjectsData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_world_objects = self._io.read_u4le()
            if self.num_world_objects != 0:
                self.world_objects = []
                for i in range(self.num_world_objects):
                    self.world_objects.append(LithtechDat.WorldObject(self._io, self, self._root))




    class ParticleBlockerData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_polygons = self._io.read_u4le()
            if self.num_polygons != 0:
                self.polygons = []
                for i in range(self.num_polygons):
                    self.polygons.append(LithtechDat.Polygon(self._io, self, self._root))




    class RenderSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.texture_name = []
            for i in range(2):
                self.texture_name.append(LithtechDat.StrWithLen2(self._io, self, self._root))

            self.shader_code = self._io.read_u1()
            self.triangle_count = self._io.read_u4le()
            self.texture_effect = LithtechDat.StrWithLen2(self._io, self, self._root)
            self.lm_width = self._io.read_u4le()
            self.lm_height = self._io.read_u4le()
            self.len_lm_data = self._io.read_u4le()
            self.lm_data = self._io.read_bytes(self.len_lm_data)


    class World(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.world_info_string = LithtechDat.StrWithLen4(self._io, self, self._root)
            self.world_extends_min = LithtechDat.Vec3(self._io, self, self._root)
            self.world_extends_max = LithtechDat.Vec3(self._io, self, self._root)
            self.world_offset = LithtechDat.Vec3(self._io, self, self._root)


    class WorldModel(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved = self._io.read_u4le()
            self.world_info_flag = self._io.read_u4le()
            self.world_name = LithtechDat.StrWithLen2(self._io, self, self._root)
            self.num_points = self._io.read_u4le()
            self.num_planes = self._io.read_u4le()
            self.num_surfaces = self._io.read_u4le()
            self.reserved1 = self._io.read_u4le()
            self.num_polygons = self._io.read_u4le()
            self.reserved2 = self._io.read_u4le()
            self.num_polygons_vertices = self._io.read_u4le()
            self.reserved3 = self._io.read_u4le()
            self.reserved4 = self._io.read_u4le()
            self.num_nodes = self._io.read_u4le()
            self.world_b_box_min = LithtechDat.Vec3(self._io, self, self._root)
            self.world_b_box_max = LithtechDat.Vec3(self._io, self, self._root)
            self.world_translation = LithtechDat.Vec3(self._io, self, self._root)
            self.texture_names_size = self._io.read_u4le()
            self.num_texture_names = self._io.read_u4le()
            self.texture_names = []
            for i in range(self.num_texture_names):
                self.texture_names.append((self._io.read_bytes_term(0, False, True, True)).decode(u"ASCII"))

            self.vertices_lengths = []
            for i in range(self.num_polygons):
                self.vertices_lengths.append(self._io.read_u1())

            self.planes = []
            for i in range(self.num_planes):
                self.planes.append(LithtechDat.Plane(self._io, self, self._root))

            self.surfaces = []
            for i in range(self.num_surfaces):
                self.surfaces.append(LithtechDat.Surface(self._io, self, self._root))

            self.polygons = []
            for i in range(self.num_polygons):
                self.polygons.append(LithtechDat.WorldModelPolygon(self.vertices_lengths[i], self._io, self, self._root))

            self.nodes = []
            for i in range(self.num_nodes):
                self.nodes.append(LithtechDat.WorldModelNode(self._io, self, self._root))

            self.points = []
            for i in range(self.num_points):
                self.points.append(LithtechDat.Vec3(self._io, self, self._root))

            self.root_node_index = self._io.read_s4le()
            self.sections = self._io.read_u4le()


    class SkyPortal(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_vertices_pos = self._io.read_u1()
            if self.len_vertices_pos != 0:
                self.vertices_pos = []
                for i in range(self.len_vertices_pos):
                    self.vertices_pos.append(LithtechDat.Vec3(self._io, self, self._root))


            self.plane = LithtechDat.Plane(self._io, self, self._root)


    class Color(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r = self._io.read_f4le()
            self.g = self._io.read_f4le()
            self.b = self._io.read_f4le()


    class Triangle(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.t = []
            for i in range(3):
                self.t.append(self._io.read_u4le())

            self.poly_index = self._io.read_u4le()


    class StrWithLen2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_data = self._io.read_u2le()
            if self.num_data != 0:
                self.data = (self._io.read_bytes(self.num_data)).decode(u"ASCII")



    class LightGrid(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.lookup_start = LithtechDat.Vec3(self._io, self, self._root)
            self.block_size = LithtechDat.Vec3(self._io, self, self._root)
            self.lookup_size = []
            for i in range(3):
                self.lookup_size.append(self._io.read_u4le())

            self.num_light_grid_data = self._io.read_u4le()
            if self.num_light_grid_data != 0:
                self.light_grid_data = []
                for i in range(self.num_light_grid_data):
                    self.light_grid_data.append(self._io.read_u1())




    class Vec2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()


    class OccluderPoly(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_vertices_pos = self._io.read_u1()
            if self.len_vertices_pos != 0:
                self.vertices_pos = []
                for i in range(self.len_vertices_pos):
                    self.vertices_pos.append(LithtechDat.Vec3(self._io, self, self._root))


            self.plane = LithtechDat.Plane(self._io, self, self._root)
            self.name = self._io.read_u4le()


    class WorldModelRenderNode(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = LithtechDat.StrWithLen2(self._io, self, self._root)
            self.num_render_nodes = self._io.read_u4le()
            if self.num_render_nodes != 0:
                self.render_nodes = []
                for i in range(self.num_render_nodes):
                    self.render_nodes.append(LithtechDat.RenderNode(self._io, self, self._root))


            self.no_child_flag = self._io.read_u4le()


    class WorldTree(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.root_b_box_min = LithtechDat.Vec3(self._io, self, self._root)
            self.root_b_box_max = LithtechDat.Vec3(self._io, self, self._root)
            self.num_sub_nodes = self._io.read_u4le()
            self.terrain_depth = self._io.read_u4le()
            self.world_layout = self._io.read_bytes(int(((self.num_sub_nodes * 0.125) + 1)))
            self.num_world_models = self._io.read_u4le()
            self.world_models = []
            for i in range(self.num_world_models):
                self.world_models.append(LithtechDat.WorldModel(self._io, self, self._root))



    class Quaternion(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()
            self.w = self._io.read_f4le()


    class LightGroup(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = LithtechDat.StrWithLen2(self._io, self, self._root)
            self.v_color = LithtechDat.Vec3(self._io, self, self._root)
            self.len_n_intensity_data = self._io.read_u4le()
            self.n_intensity_data = self._io.read_bytes(self.len_n_intensity_data)
            self.num_lm_sections_matrix = self._io.read_u4le()
            if self.num_lm_sections_matrix != 0:
                self.lm_sections_matrix = []
                for i in range(self.num_lm_sections_matrix):
                    self.lm_sections_matrix.append(LithtechDat.LmSectionArray(self._io, self, self._root))




    class WorldModelPolygon(KaitaiStruct):
        def __init__(self, num_vertices_indices, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.num_vertices_indices = num_vertices_indices
            self._read()

        def _read(self):
            self.surface_index = self._io.read_u4le()
            self.plane_index = self._io.read_u4le()
            self.vertices_indices = []
            for i in range(self.num_vertices_indices):
                self.vertices_indices.append(self._io.read_u4le())



    class StrWithLen4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_data = self._io.read_u4le()
            if self.num_data != 0:
                self.data = (self._io.read_bytes(self.num_data)).decode(u"ASCII")



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dat_version = self._io.read_bytes(4)
            if not self.dat_version == b"\x55\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x55\x00\x00\x00", self.dat_version, self._io, u"/types/header/seq/0")
            self.object_list_pos = self._io.read_u4le()
            self.blind_data_pos = self._io.read_u4le()
            self.light_grid_pos = self._io.read_u4le()
            self.physics_data_pos = self._io.read_u4le()
            self.particle_data_pos = self._io.read_u4le()
            self.render_data_pos = self._io.read_u4le()
            self.future = []
            for i in range(8):
                self.future.append(self._io.read_u4le())



    class Vec3(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()


    class RenderData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_render_nodes = self._io.read_u4le()
            if self.num_render_nodes != 0:
                self.render_nodes = []
                for i in range(self.num_render_nodes):
                    self.render_nodes.append(LithtechDat.RenderNode(self._io, self, self._root))


            self.num_world_model_render_nodes = self._io.read_u4le()
            if self.num_world_model_render_nodes != 0:
                self.world_model_render_nodes = []
                for i in range(self.num_world_model_render_nodes):
                    self.world_model_render_nodes.append(LithtechDat.WorldModelRenderNode(self._io, self, self._root))




    class LmSectionArray(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_lm_sections = self._io.read_u4le()
            if self.num_lm_sections != 0:
                self.lm_sections = []
                for i in range(self.num_lm_sections):
                    self.lm_sections.append(LithtechDat.LmSection(self._io, self, self._root))




    class LmSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.left = self._io.read_u4le()
            self.top = self._io.read_u4le()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.num_data = self._io.read_u4le()
            self.data = self._io.read_bytes(self.num_data)


    class CollisionData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_polygons = self._io.read_u4le()
            if self.num_polygons != 0:
                self.polygons = []
                for i in range(self.num_polygons):
                    self.polygons.append(LithtechDat.Polygon(self._io, self, self._root))




    class WorldModelNode(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.poly_index = self._io.read_u4le()
            self.reserved = self._io.read_u2le()
            self.node_sides_indices = []
            for i in range(2):
                self.node_sides_indices.append(self._io.read_u4le())



    @property
    def render_data(self):
        if hasattr(self, '_m_render_data'):
            return self._m_render_data

        _pos = self._io.pos()
        self._io.seek(self.header.render_data_pos)
        self._m_render_data = LithtechDat.RenderData(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_render_data', None)

    @property
    def particle_blocker(self):
        if hasattr(self, '_m_particle_blocker'):
            return self._m_particle_blocker

        _pos = self._io.pos()
        self._io.seek(self.header.particle_data_pos)
        self._m_particle_blocker = LithtechDat.ParticleBlockerData(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_particle_blocker', None)

    @property
    def world_objects(self):
        if hasattr(self, '_m_world_objects'):
            return self._m_world_objects

        _pos = self._io.pos()
        self._io.seek(self.header.object_list_pos)
        self._m_world_objects = LithtechDat.WorldObjectsData(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_world_objects', None)

    @property
    def light_grid(self):
        if hasattr(self, '_m_light_grid'):
            return self._m_light_grid

        _pos = self._io.pos()
        self._io.seek(self.header.light_grid_pos)
        self._m_light_grid = LithtechDat.LightGrid(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_light_grid', None)

    @property
    def collision_data(self):
        if hasattr(self, '_m_collision_data'):
            return self._m_collision_data

        _pos = self._io.pos()
        self._io.seek(self.header.physics_data_pos)
        self._m_collision_data = LithtechDat.CollisionData(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_collision_data', None)

    @property
    def blind_object_len(self):
        """not yet supported."""
        if hasattr(self, '_m_blind_object_len'):
            return self._m_blind_object_len

        _pos = self._io.pos()
        self._io.seek(self.header.blind_data_pos)
        self._m_blind_object_len = self._io.read_u4le()
        self._io.seek(_pos)
        return getattr(self, '_m_blind_object_len', None)


