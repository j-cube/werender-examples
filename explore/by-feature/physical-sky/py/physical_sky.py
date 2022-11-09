# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
#
# https://werender.io/explore
#   by feature: Physical Sky Image Based Lighting
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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'envsky.log'))

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

    # everuthing is a subd
    group.set_mesh_smooth(True)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(-80.0, 50.0, 0.0),
        rotate=(-27.0, -90.0, 0.0))
    camera.set_xform(camera_xform)
    camera.set_focal_length(55.0)

    # create physical sky env light and its properties
    envsky_light = scene.new_light(wr.lights.Envsky)
    envsky_light.set_visible_to_camera(1)
    envsky_light.set_azimuth(90.0)
    envsky_light.set_intensity(1.0)
    
    # create materials
    mat_gold = scene.new_material(wr.materials.Metal)
    mat_chrome = scene.new_material(wr.materials.Metal)
    mat_white = scene.new_material(wr.materials.Generic)

    # set material attributes
    mat_white.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_white.set_roughness(0.1)
    mat_white.set_specular_level(1.0)

    mat_gold.set_roughness(0.15)

    mat_chrome.set_roughness(0.0)
    mat_chrome.set_edge_color(wr.Color(1.0, 1.0, 1.0))
    mat_chrome.set_color(wr.Color(0.9, 0.9, 0.9))

    # assign materials
    group.assign_material(mat_chrome, '.*/tetra_l.*')
    group.assign_material(mat_gold, '.*/tetra_r.*')
    ground.assign_material(mat_white)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(1280, 720)
    settings.set_image_name('physical_sky.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'physical_sky.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
