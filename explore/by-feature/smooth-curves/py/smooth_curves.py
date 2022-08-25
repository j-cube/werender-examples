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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'smooth_curves.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    lollipop_asset = session.upload(resolve_file('lollipop.usd'), remote_folder)
    ground_asset = session.upload(resolve_file('ground.usd'), remote_folder)
    curves_asset = session.upload(resolve_file('curves_pwuv.usd'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models and transforms
    lollipop = scene.new_model(lollipop_asset)
    ground = scene.new_model(ground_asset)
    curves = scene.new_model(curves_asset)

    # transform the curves
    curves_xform = wr.Transform(
        translate=(-1.31, 17.104, 17.982),
        scale=(3.576, 3.576, 3.576))
    curves.set_xform(curves_xform)

    # infinitely smooth curves
    cuvres_all = curves.get_items('.*')
    curves.set_curve_smooth(True)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(-42.55, 63.604, 1.597),
        rotate=(-51.0, -89.2, 0.0))
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
    mat_fiber = scene.new_material(wr.materials.Fiber)
    mat_pink = scene.new_material(wr.materials.Generic)
    mat_white = scene.new_material(wr.materials.Generic)

    # set material attributes
    mat_white.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_white.set_roughness(0.1)
    mat_white.set_specular_level(1.0)

    mat_fiber.set_color(wr.Color(0.195, 0.048, 0.161))
    mat_fiber.set_consistency(0.25)

    mat_pink.set_color(wr.Color(0.8, 0.377, 0.661))
    mat_pink.set_roughness(0.3)
    mat_pink.set_specular_level(1.0)
    mat_pink.set_subsurface(1.0)

    # assign materials
    lollipop.assign_material(mat_pink, '.*/disc.*')
    lollipop.assign_material(mat_white, '.*/stick.*')
    ground.assign_material(mat_white)
    curves.assign_material(mat_fiber)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(1280, 720)
    settings.set_image_name('smooth_curves.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'smooth_curves.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
