# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
# https://werender.io

import os
import sys
import tempfile

import werender as wr

# a convenience function to find all assets via env var
def resolve_file(filename):
    return os.path.join(
        os.environ.get('WERENDER_ASSETS_PATH', './'), filename)


#
def main(session):
    # log file
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'werender.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # upload assets
    flat_asset = session.upload(resolve_file('flat_vr.fbx'), remote_folder)
    hdri_asset = session.upload(resolve_file('beach.exr'), remote_folder)
    art1_asset = session.upload(resolve_file('art1.jpg'), remote_folder)
    art2_asset = session.upload(resolve_file('art2.jpg'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models
    flat = scene.new_model(flat_asset)

    # create camera, transform and apply it
    vr_cam = scene.new_camera(wr.cameras.Spherical)
    vr_cam_xform = wr.Transform(
        translate=(0.0, 163.357, 0.0))
    vr_cam.set_xform(vr_cam_xform)

    # create HDRI texture, env light and its properties
    tex_hdri = scene.new_texture(wr.textures.File)
    tex_hdri.set_texture_file(hdri_asset)
    tex_hdri.set_colorspace("linear")

    envlight = scene.new_light(wr.lights.Envhdri)
    envlight.set_hdri_image(tex_hdri)
    envlight_xform = wr.Transform(rotate=(0.0, 110.0, 0.0))
    envlight.set_xform(envlight_xform)

    # create a materials
    mat_white = scene.new_material(wr.materials.Generic)
    mat_glass = scene.new_material(wr.materials.Glass)
    mat_gold = scene.new_material(wr.materials.Metal)
    mat_mirror = scene.new_material(wr.materials.Metal)
    mat_emissive = scene.new_material(wr.materials.Constant)
    mat_art1 = scene.new_material(wr.materials.Generic)
    mat_art2 = scene.new_material(wr.materials.Generic)
    mat_floor = scene.new_material(wr.materials.Generic)
    mat_sweeper = scene.new_material(wr.materials.Generic)
    mat_frame = scene.new_material(wr.materials.Generic)

    mat_frame.set_color(wr.Color(0.22, 0.25, 0.20))

    mat_sweeper.set_color(wr.Color(0.4, 0.4, 0.4))

    mat_glass.set_ior(2.0)
    mat_glass.set_reflection_ior(2.0)

    mat_emissive.set_intensity(1.0)
    mat_emissive.set_color(wr.Color(1.0, 1.0, 1.0))

    mat_mirror.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_mirror.set_edge_color(wr.Color(1.0, 1.0, 1.0))
    mat_mirror.set_roughness(0.0)

    floor_col_tex = scene.new_texture(wr.textures.Grid)
    floor_col_tex.set_line_color(wr.Color(0.1, 0.1, 0.1))
    floor_col_tex.set_filler_color(wr.Color(0.8, 0.8, 0.8))
    floor_col_tex.set_line_width(0.01)
    floor_col_tex.set_repeat_u(16.0)
    floor_col_tex.set_repeat_v(16.0)
    floor_col_tex.set_rotate_uv(45.0)
    mat_floor.set_color(floor_col_tex)

    art1_col_tex = scene.new_texture(wr.textures.File)
    art1_col_tex.set_texture_file(art1_asset)
    mat_art1.set_color(art1_col_tex)
    mat_art1.set_specular_level(2.0)

    art2_col_tex = scene.new_texture(wr.textures.File)
    art2_col_tex.set_texture_file(art2_asset)
    mat_art2.set_color(art2_col_tex)
    mat_art2.set_specular_level(2.0)



    # material assignment and overrides
    flat.assign_material(mat_white)
    flat.assign_material(mat_glass, '.*/glass.*')
    flat.assign_material(mat_glass, '.*/pyramidA_small.*')
    flat.assign_material(mat_gold, '.*/torus.*')
    flat.assign_material(mat_mirror, '.*/mirror.*')
    flat.assign_material(mat_emissive, '.*_emit.*')
    flat.assign_material(mat_art1, '.*/art1.*')
    flat.assign_material(mat_art2, '.*/art2.*')
    flat.assign_material(mat_floor, '.*/floor.*')
    flat.assign_material(mat_sweeper, '.*/sweepers.*')
    flat.assign_material(mat_frame, '.*/frame1.*')
    flat.assign_material(mat_frame, '.*/frame2.*')

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(960, 480)
    settings.set_image_name('flat_vr360.png')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/tests')

    result = session.start_render_and_wait(settings, scene)
    result.download_image(tempfile.gettempdir(), 'flat_vr360.png')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
