meta:
  id: lithtech_dat
  title: Lithtech dat map file format
  file-extension: dat
  ks-version: 0.0.1
  endian: le

types:
  # basic types
  str_with_len2:
    seq:
      - id: num_data
        type: u2
      - id: data
        type: str
        encoding: ASCII
        size: num_data
        if: num_data != 0
  str_with_len4:
    seq:
      - id: num_data
        type: u4
      - id: data
        type: str
        encoding: ASCII
        size: num_data
        if: num_data != 0
  surface:
    seq:
      - id: flags
        type: u4
      - id: texture_index
        type: u2
      - id: texture_flags
        type: u2
  vec2:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
  vec3:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
      - id: z
        type: f4
  color:
    seq:
      - id: r
        type: f4
      - id: g
        type: f4
      - id: b
        type: f4
  quaternion:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
      - id: z
        type: f4
      - id: w
        type: f4
  plane:
    seq:
      - id: normal
        type: vec3
      - id: dist
        type: f4
  vertex:
    seq:
      - id: v_pos
        type: vec3
      - id: uv0
        type: vec2
      - id: uv1
        type: vec2
      - id: color
        type: s4
      - id: v_normal
        type: vec3
      - id: v_tangent
        type: vec3
      - id: v_binormal
        type: vec3
  polygon:
    seq:
      - id: plane
        type: plane
      - id: num_vertices_pos
        type: u4
      - id: vertices_pos
        type: vec3
        repeat: expr
        repeat-expr: num_vertices_pos
  triangle:
    seq:
      - id: t
        type: u4
        repeat: expr
        repeat-expr: 3
      - id: poly_index
        type: u4
  # world object types
  wop_string:
    seq:
      - id: value
        type: str_with_len2
  wop_vec3:
    seq:
      - id: value
        type: vec3
  wop_color:
    seq:
      - id:  value
        type: color
  wop_f4:
    seq:
      - id: value
        type: f4
  wop_flag:
    seq:
      - id: value
        type: u4
  wop_bool:
    seq:
      - id: value
        type: u1
  wop_int:
    seq:
      - id: value
        type: s4
  wop_quaternion:
    seq:
      - id: value
        type: quaternion
  world_object_property:
    seq:
      - id: name
        type: str_with_len2
      - id: magic
        type: u1
      - id: property_flags
        type: u4
      - id: len_data
        type: u2
      - id: data
        type:
          switch-on: magic
          cases:
            0x00: wop_string
            0x01: wop_vec3
            0x02: wop_color
            0x03: wop_f4
            0x04: wop_flag
            0x05: wop_bool
            0x06: wop_int
            0x07: wop_quaternion
  world_object:
    seq:
      - id: len_object
        type: u2
      - id: object_type
        type: str_with_len2
      - id: num_object_properties
        type: u4
      - id: object_properties
        type: world_object_property
        if: num_object_properties != 0
        repeat: expr
        repeat-expr: num_object_properties
  # world model types
  world_model_polygon:
    params:
      - id: num_vertices_indices
        type: u4
    seq:
      - id: surface_index
        type: u4
      - id: plane_index
        type: u4
      - id: vertices_indices
        type: u4
        repeat: expr
        repeat-expr: num_vertices_indices
  world_model_node:
    seq:
      - id: poly_index
        type: u4
      - id: reserved
        type: u2
      - id: node_sides_indices
        type: u4
        repeat: expr
        repeat-expr: 2
  world_model:
    seq:
      - id: reserved
        type: u4
        doc: always zero
      - id: world_info_flag
        type: u4
      - id: world_name
        type: str_with_len2
        doc: mainly used for world models
      - id: num_points
        type: u4
      - id: num_planes
        type: u4
      - id: num_surfaces
        type: u4
      - id: reserved1
        type: u4
      - id: num_polygons
        type: u4
      - id: reserved2
        type: u4
      - id: num_polygons_vertices
        type: u4
      - id: reserved3
        type: u4
      - id: reserved4
        type: u4
      - id: num_nodes
        type: u4
      - id: world_b_box_min
        type: vec3
      - id: world_b_box_max
        type: vec3
      - id: world_translation
        type: vec3
      - id: texture_names_size
        type: u4
      - id: num_texture_names
        type: u4
      - id: texture_names
        type: str
        terminator: 0
        encoding: ASCII
        repeat: expr
        repeat-expr: num_texture_names
      - id: vertices_lengths
        type: u1
        repeat: expr
        repeat-expr: num_polygons
      - id: planes
        type: plane
        repeat: expr
        repeat-expr: num_planes
      - id: surfaces
        type: surface
        repeat: expr
        repeat-expr: num_surfaces
      - id: polygons
        type: world_model_polygon(vertices_lengths[_index])
        repeat: expr
        repeat-expr: num_polygons
      - id: nodes
        type: world_model_node
        repeat: expr
        repeat-expr: num_nodes
      - id: points
        type: vec3
        repeat: expr
        repeat-expr: num_points
      - id: root_node_index
        type: s4
      - id: sections
        type: u4
        doc: reserved
  world_tree:
    seq:
      - id: root_b_box_min
        type: vec3
      - id: root_b_box_max
        type: vec3
      - id: num_sub_nodes
        type: u4
      - id: terrain_depth
        type: u4
      - id: world_layout
        size: (num_sub_nodes * 0.125 + 1).to_i
        doc: Oct-tree stored bitwise
      - id: num_world_models
        type: u4
      - id: world_models
        type: world_model
        repeat: expr
        repeat-expr: num_world_models
  # render world types
  sky_portal:
    seq:
      - id: len_vertices_pos
        type: u1
      - id: vertices_pos
        type: vec3
        if: len_vertices_pos != 0
        repeat: expr
        repeat-expr: len_vertices_pos
      - id: plane
        type: plane
  occluder_poly:
    seq:
      - id: len_vertices_pos
        type: u1
      - id: vertices_pos
        type: vec3
        if: len_vertices_pos != 0
        repeat: expr
        repeat-expr: len_vertices_pos
      - id: plane
        type: plane
      - id: name
        type: u4
  render_section:
    seq:
      - id: texture_name
        type: str_with_len2
        repeat: expr
        repeat-expr: 2
      - id: shader_code
        type: u1
      - id: triangle_count
        type: u4
      - id: texture_effect
        type: str_with_len2
      - id: lm_width
        type: u4
      - id: lm_height
        type: u4
      - id: len_lm_data
        type: u4
      - id: lm_data
        size: len_lm_data
  lm_section:
    seq:
      - id: left
        type: u4
      - id: top
        type: u4
      - id: width
        type: u4
      - id: height
        type: u4
      - id: num_data
        type: u4
      - id: data
        size: num_data
  lm_section_array:
    seq:
      - id: num_lm_sections
        type: u4
      - id: lm_sections
        type: lm_section
        if: num_lm_sections != 0
        repeat: expr
        repeat-expr: num_lm_sections
  light_group:
    seq:
      - id: name
        type: str_with_len2
      - id: v_color
        type: vec3
      - id: len_n_intensity_data
        type: u4
      - id: n_intensity_data
        size: len_n_intensity_data
        doc: Data is zero compressed
      - id: num_lm_sections_matrix
        type: u4
      - id: lm_sections_matrix
        type: lm_section_array
        if: num_lm_sections_matrix != 0
        repeat: expr
        repeat-expr: num_lm_sections_matrix
  render_node:
    seq:
      - id: v_center
        type: vec3
      - id: v_half_dims
        type: vec3
        # section array
      - id: num_sections
        type: u4
      - id: sections
        type: render_section
        if: num_sections != 0
        repeat: expr
        repeat-expr: num_sections
        # vertex array
      - id: num_vertices
        type: u4
      - id: vertices
        type: vertex
        if: num_vertices != 0
        repeat: expr
        repeat-expr: num_vertices
        # triangle array
      - id: num_triangles
        type: u4
      - id: triangles
        type: triangle
        if: num_triangles != 0
        repeat: expr
        repeat-expr: num_triangles
        # sky_portal array
      - id: num_sky_portals
        type: u4
      - id: sky_portals
        type: sky_portal
        if: num_sky_portals != 0
        repeat: expr
        repeat-expr: num_sky_portals
        # occluder array
      - id: num_occluder_polygons
        type: u4
      - id: occluder_polygons
        type: occluder_poly
        if: num_occluder_polygons != 0
        repeat: expr
        repeat-expr: num_occluder_polygons
        # light_group array
      - id: num_light_groups
        type: u4
      - id: light_groups
        type: light_group
        if: num_light_groups != 0
        repeat: expr
        repeat-expr: num_light_groups
        # children
      - id: child_flags
        type: u1
      - id: child_node_indices
        type: u4
        repeat: expr
        repeat-expr: 2
  world_model_render_node:
    seq:
      - id: name
        type: str_with_len2
      - id: num_render_nodes
        type: u4
      - id: render_nodes
        type: render_node
        if: num_render_nodes != 0
        repeat: expr
        repeat-expr: num_render_nodes
      - id: no_child_flag
        type: u4
        doc: allways zero
  # light_grid types
  light_grid:
    seq:
      - id: lookup_start
        type: vec3
      - id: block_size
        type: vec3
      - id: lookup_size
        type: u4
        repeat: expr
        repeat-expr: 3
      - id: num_light_grid_data
        type: u4
      - id: light_grid_data
        type: u1
        if: num_light_grid_data != 0
        repeat: expr
        repeat-expr: num_light_grid_data
        doc: RLE compressed data
  # header
  header:
    seq:
      - id: dat_version
        contents: [0x55, 0x00, 0x00, 0x00]
      - id: object_list_pos
        type: u4
      - id: blind_data_pos
        type: u4
      - id: light_grid_pos
        type: u4
      - id: physics_data_pos
        type: u4
      - id: particle_data_pos
        type: u4
      - id: render_data_pos
        type: u4
      - id: future
        type: u4
        repeat: expr
        repeat-expr: 8
  world:
    seq:
      - id: world_info_string
        type: str_with_len4
      - id: world_extends_min
        type: vec3
      - id: world_extends_max
        type: vec3
      - id: world_offset
        type: vec3
  # instances
  world_objects_data:
    seq:
      - id: num_world_objects
        type: u4
      - id: world_objects
        type: world_object
        if: num_world_objects != 0
        repeat: expr
        repeat-expr: num_world_objects
  collision_data:
    seq:
      - id: num_polygons
        type: u4
      - id: polygons
        type: polygon
        if: num_polygons != 0
        repeat: expr
        repeat-expr: num_polygons
  particle_blocker_data:
    seq:
      - id: num_polygons
        type: u4
      - id: polygons
        type: polygon
        if: num_polygons != 0
        repeat: expr
        repeat-expr: num_polygons
  render_data:
    seq:
      - id: num_render_nodes
        type: u4
      - id: render_nodes
        type: render_node
        if: num_render_nodes != 0
        repeat: expr
        repeat-expr: num_render_nodes
      - id: num_world_model_render_nodes
        type: u4
      - id: world_model_render_nodes
        type: world_model_render_node
        if: num_world_model_render_nodes != 0
        repeat: expr
        repeat-expr: num_world_model_render_nodes

seq:
  - id: header
    type: header
  - id: world
    type: world
  - id: world_tree
    type: world_tree

instances:
  world_objects:
    pos: header.object_list_pos
    type: world_objects_data
  blind_object_len:
    pos: header.blind_data_pos
    type: u4
    doc: not yet supported
  light_grid:
    pos: header.light_grid_pos
    type: light_grid
  collision_data:
    pos: header.physics_data_pos
    type: collision_data
  particle_blocker:
    pos: header.particle_data_pos
    type: particle_blocker_data
  render_data:
    pos: header.render_data_pos
    type: render_data
