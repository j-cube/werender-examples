# Copyright 2022 J Cube Inc. Yokohama, Japan. All Rights Reserved.
#
# https://werender.io/explore
#   by industry: nft


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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'thecube.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    thecube_asset = session.upload(resolve_file('thecube.usd'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models
    thecube = scene.new_model(thecube_asset)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(-29.04, -1.37, 47.951),
        rotate=(1.400, -31.2, 0.0))
    camera.set_xform(camera_xform)
    camera.set_focal_length(300.0)
    camera.set_dof_enabled(1)
    camera.set_dof_focal_distance(56.0)
    camera.set_dof_focal_length(30.0)
    camera.set_dof_fstop(32.0)

    # create white env light, and its properties
    envlight = scene.new_light(wr.lights.Env)
    envlight.set_intensity(0.01)
    envlight.set_color(wr.Color(1.0, 1.0, 1.0))

    # create main light, transform and its properties
    arealight_key = scene.new_light(wr.lights.Area)
    arealight_key.set_intensity(5000.0)
    arealight_key.set_color(wr.Color(1.0, 1.0, 1.0))

    arealight_key_xform = wr.Transform(
        translate=(-3.819, 23.394, -16.01),
        rotate=(845.197, -13.725, -180.0),
        scale=(3.282, 3.282, 3.282))
    arealight_key.set_xform(arealight_key_xform)

    # create fill light, transform and its properties
    arealight_fill = scene.new_light(wr.lights.Area)
    arealight_fill.set_intensity(25.0)
    arealight_fill.set_color(wr.Color(1.0, 1.0, 1.0))

    arealight_fill_xform = wr.Transform(
        translate=(-3.819, -17.269, -2.697),
        rotate=(794.574, -124.754, 0.0),
        scale=(2.473, 2.473, 2.473))
    arealight_fill.set_xform(arealight_fill_xform)

    # create materials
    mat_cube = scene.new_material(wr.materials.Generic)
    mat_cage = scene.new_material(wr.materials.Generic)

    # set material attributes
    mat_cube.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_cube.set_roughness(0.3)
    mat_cube.set_specular_level(0.5)

    mat_cage.set_color(wr.Color(0.5, 0.5, 0.5))
    mat_cage.set_roughness(1.0)
    mat_cage.set_specular_level(0.0)


    # assign materials
    thecube.assign_material(mat_cube, '.*/inner_cube.*')
    thecube.assign_material(mat_cage, '.*/outer_cage.*')

    # choose the camera
    scene.set_active_camera(camera)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(2000, 2000)
    # when using depth of field (or motion blur) on the camera, you should
    # increment pixel samples to a higher value than the default (16)
    settings.set_pixel_samples(64)
    settings.set_image_name('maneki_and_torii.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'thecube.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
