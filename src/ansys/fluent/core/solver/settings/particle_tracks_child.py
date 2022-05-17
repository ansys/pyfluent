#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .name import name
from .uid import uid
from .options_6 import options
from .filter_settings import filter_settings
from .range import range
from .style_attribute_1 import style_attribute
from .vector_settings import vector_settings
from .plot import plot
from .track_single_particle_stream import track_single_particle_stream
from .skip import skip
from .coarsen import coarsen
from .field import field
from .injections_list import injections_list
from .free_stream_particles import free_stream_particles
from .wall_film_particles import wall_film_particles
from .track_pdf_particles import track_pdf_particles
from .color_map import color_map
from .draw_mesh import draw_mesh
from .mesh_object import mesh_object
from .display_state_name import display_state_name
from .display_1 import display
class particle_tracks_child(Group):
    """
    'child_object_type' of particle_tracks
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'filter_settings', 'range',
         'style_attribute', 'vector_settings', 'plot',
         'track_single_particle_stream', 'skip', 'coarsen', 'field',
         'injections_list', 'free_stream_particles', 'wall_film_particles',
         'track_pdf_particles', 'color_map', 'draw_mesh', 'mesh_object',
         'display_state_name']

    name: name = name
    """
    name child of particle_tracks_child
    """
    uid: uid = uid
    """
    uid child of particle_tracks_child
    """
    options: options = options
    """
    options child of particle_tracks_child
    """
    filter_settings: filter_settings = filter_settings
    """
    filter_settings child of particle_tracks_child
    """
    range: range = range
    """
    range child of particle_tracks_child
    """
    style_attribute: style_attribute = style_attribute
    """
    style_attribute child of particle_tracks_child
    """
    vector_settings: vector_settings = vector_settings
    """
    vector_settings child of particle_tracks_child
    """
    plot: plot = plot
    """
    plot child of particle_tracks_child
    """
    track_single_particle_stream: track_single_particle_stream = track_single_particle_stream
    """
    track_single_particle_stream child of particle_tracks_child
    """
    skip: skip = skip
    """
    skip child of particle_tracks_child
    """
    coarsen: coarsen = coarsen
    """
    coarsen child of particle_tracks_child
    """
    field: field = field
    """
    field child of particle_tracks_child
    """
    injections_list: injections_list = injections_list
    """
    injections_list child of particle_tracks_child
    """
    free_stream_particles: free_stream_particles = free_stream_particles
    """
    free_stream_particles child of particle_tracks_child
    """
    wall_film_particles: wall_film_particles = wall_film_particles
    """
    wall_film_particles child of particle_tracks_child
    """
    track_pdf_particles: track_pdf_particles = track_pdf_particles
    """
    track_pdf_particles child of particle_tracks_child
    """
    color_map: color_map = color_map
    """
    color_map child of particle_tracks_child
    """
    draw_mesh: draw_mesh = draw_mesh
    """
    draw_mesh child of particle_tracks_child
    """
    mesh_object: mesh_object = mesh_object
    """
    mesh_object child of particle_tracks_child
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of particle_tracks_child
    """
    command_names = \
        ['display']

    display: display = display
    """
    display command of particle_tracks_child
    """
