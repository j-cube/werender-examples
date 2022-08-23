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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'shoes_usdz.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # get a USDZ files from:
    #   https://developer.apple.com/augmented-reality/quick-look/
    #   https://j-cube.jp/solutions/multiverse/assets/
    shoe_asset = session.upload(resolve_file('AirForce.usdz'), remote_folder)
    plane_asset = session.upload(resolve_file('plane.usd'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models
    shoeR = scene.new_model(shoe_asset)
    shoeL = scene.new_model(shoe_asset)
    plane = scene.new_model(plane_asset)

    # create & apply transforms to left shoe model (right one is at the origin)
    shoeL_xform = wr.Transform(translate=(0.0, 0.0, 32.489),
        rotate=(0.0, 144.537, 0.0),
        scale=(-1.0, 1.0, 1.0))
    shoeL.set_xform(shoeL_xform)

    plane_xform = wr.Transform(scale=(0.5, 0.5, 0.5))
    plane.set_xform(plane_xform)

    # create camera, transform and apply it
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(49.886, 31.109, -67.459),
        rotate=(-15.938, 148.200, 0.0))
    camera.set_xform(camera_xform)
    # apply transform and set focal length
    camera.set_focal_length(55.0)

    # create a couple of area lights, set values, transform and apply them
    area_light1 = scene.new_light(wr.lights.Area)
    area_light2 = scene.new_light(wr.lights.Area)

    area_light1.set_color(wr.Color(1.0, 0.845, 0.902))
    area_light2.set_color(wr.Color(0.845, 0.974, 1.0))
    area_light1.set_intensity(12000)
    area_light2.set_intensity(20000)

    area_light1_xform = wr.Transform(
        translate=(36.97, 26.122, 49.610),
        rotate=(-27.702, 47.997, 360.0),
        scale=(6.957, 6.957, 6.957))
    area_light2_xform = wr.Transform(
        translate=(-42.190, 19.854, -26.241),
        rotate=(-197.964, -43.549, -180.000),
        scale=(6.957, 6.957, 6.957))

    area_light1.set_xform(area_light1_xform)
    area_light2.set_xform(area_light2_xform)


    # create a material, procedural textures, set values, assign to plane
    plane_mat = scene.new_material(wr.materials.Generic)

    plane_col_tex = scene.new_texture(wr.textures.Grid)
    plane_hgt_tex = scene.new_texture(wr.textures.Cellnoise)

    plane_col_tex.set_line_color(wr.Color(0.5, 0.5, 0.5))
    plane_col_tex.set_filler_color(wr.Color(0.6, 0.6, 0.6))
    plane_col_tex.set_line_width(0.015)
    plane_col_tex.set_repeat_u(64.0)
    plane_col_tex.set_repeat_v(64.0)

    plane_hgt_tex.set_density(0.007)
    plane_hgt_tex.set_noise_type(2)

    plane_mat.set_color(plane_col_tex)
    plane_mat.set_specular_level(2.0)
    plane_mat.set_metallic(0.4)
    plane_mat.set_height(plane_hgt_tex)
    plane_mat.set_height_amount(0.004)
    plane_mat.set_height_type(3)

    plane.assign_material(plane_mat)

    # note that the usdz model contains materials and textures definitions!

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(960, 540)
    settings.set_image_name('shoes_usdz.png')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    result = session.start_render_and_wait(settings, scene)
    result.download_image(tempfile.gettempdir(), 'shoes_usdz.png')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
