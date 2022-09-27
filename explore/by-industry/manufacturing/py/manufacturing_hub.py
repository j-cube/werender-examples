# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
#
# https://werender.io/explore
#   by industry: manufacturing


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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'manufacturing_hub.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    hub_asset = session.upload(resolve_file('4X_Wrap_FSAE_Hub_v3.usdz'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models
    hub = scene.new_model(hub_asset)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(-20.260, 7.463, 3.954),
        rotate=(342.200, 294.4, 0.0))
    camera.set_xform(camera_xform)
    camera.set_focal_length(55.0)

    # create an env light, apply to it a gradient, and set some attributes
    envlight = scene.new_light(wr.lights.Env)
    gradient_tex = scene.new_texture(wr.textures.Gradient)
    gradient_tex.set_repeat(2.0)
    gradient_tex.set_shape(1)
    envlight.set_color(gradient_tex)
    envlight.set_intensity(1.0)
    envlight.set_visible_to_camera(True)

    # create also a distant light
    distantlight = scene.new_light(wr.lights.Distant)
    distantlight_xform = wr.Transform(rotate=(328.952, -55.108, -387.648))
    distantlight.set_xform(distantlight_xform)

    # note: this is a USDZ model with materials, by default, if you do not
    #       assign any materials, the materials defines in the USDZ will be
    #       used.
    #       In this example we are creating and overriding a material by
    #       assigning it on a specific item:

    # create materials
    metal_mat = scene.new_material(wr.materials.Metal)

    # set material attributes
    metal_mat.set_thin_film_thickness(0.12)
    metal_mat.set_thin_film_ior(1.5)

    # assign materials
    hub.assign_material(metal_mat, '.*/MeshInstance_30/Body1.*')

    # choose the camera
    scene.set_active_camera(camera)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(1280, 720)
    settings.set_image_name('manufacturing_hub.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'manufacturing_hub.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
