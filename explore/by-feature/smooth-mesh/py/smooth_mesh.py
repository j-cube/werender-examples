# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
#
# https://werender.io/explore
#   by feature: smooth mesh (infinitely smooth subdivision surface)

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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'smooth_mesh.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    group_asset = session.upload(resolve_file('tetra_group.usd'), remote_folder)
    ground_asset = session.upload(resolve_file('ground.usd'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models and transforms
    group = scene.new_model(group_asset)
    ground = scene.new_model(ground_asset)

    # set left tetra to render as infinite smooth mesh (subdivision surface)
    group_all = group.get_items('.*/tetra_l.*')
    group_all.set_mesh_smooth(True)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(-80.0, 50.0, 0.0),
        rotate=(-27.0, -90.0, 0.0))
    camera.set_xform(camera_xform)
    camera.set_focal_length(55.0)

    # create physical sky env light and its properties
    envlight = scene.new_light(wr.lights.Envsky)
    envlight.set_intensity(2.0)
    envlight.set_visible_to_camera(1)
    envlight.set_azimuth(90.0)
    envlight.set_ground_enable(1)
    envlight.set_ground_color(wr.Color(0.216, 0.161, 0.139))

    # create materials
    mat_green = scene.new_material(wr.materials.Generic)
    mat_pink = scene.new_material(wr.materials.Generic)
    mat_white = scene.new_material(wr.materials.Generic)

    # set material attributes
    mat_white.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_white.set_roughness(0.1)
    mat_white.set_specular_level(1.0)

    mat_green.set_color(wr.Color(0.377, 0.8, 0.513))
    mat_green.set_roughness(0.3)
    mat_green.set_specular_level(1.0)

    mat_pink.set_color(wr.Color(0.8, 0.377, 0.661))
    mat_pink.set_roughness(0.3)
    mat_pink.set_specular_level(1.0)

    # assign materials
    group.assign_material(mat_green, '.*/tetra_l.*')
    group.assign_material(mat_pink, '.*/tetra_r.*')
    ground.assign_material(mat_white)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(1280, 720)
    settings.set_image_name('smooth_mesh.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'smooth_mesh.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
