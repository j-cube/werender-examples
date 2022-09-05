# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
#
# https://werender.io/explore
#   by feature: toon & outlines

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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'toon_outlines.log'))

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
    group_left_tetra = group.get_items('.*/tetra_l.*')
    group_left_tetra.set_mesh_smooth(True)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(-80.0, 50.0, 0.0),
        rotate=(-27.0, -90.0, 0.0))
    camera.set_xform(camera_xform)
    camera.set_focal_length(55.0)

    # create physical sky env light and its properties
    # note that for the toon material to correctly produce the quantized "color
    # regions", at least one directional, or spot, or environment light (better
    # if envsky) is required in the scene.

    envlight = scene.new_light(wr.lights.Envsky)
    envlight.set_intensity(2.0)
    envlight.set_visible_to_camera(1)
    envlight.set_azimuth(90.0)
    envlight.set_ground_enable(1)
    envlight.set_ground_color(wr.Color(0.216, 0.161, 0.139))

    # create materials
    mat_toon_green = scene.new_material(wr.materials.Toon)
    mat_toon_pink = scene.new_material(wr.materials.Toon)
    mat_white = scene.new_material(wr.materials.Generic)

    # set material attributes
    mat_white.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_white.set_roughness(0.1)
    mat_white.set_specular_level(1.0)

    # the toon effect is the sum of two "quantized" color regions and outlines:
    #  - color regions default: `lit_color` (66% gray), `dark_color` (33% gray)
    #  - outline color default: `outline_color` (50% gray)
    #  - outline colors are by default tinted by the region's colors, but NOT by
    #    the region's tint (this allows any color possibility):
    #    `set_outlines_tinting_enabled` (default: true)

    # rely on default color regions, tint them with a color.
    # specify outline color, which wil be tinted by the original color regions:
    #  mat_toon_green.set_lit_color(wr.Color(0.66, 0.66, 0.66)) # default
    #  mat_toon_green.set_dark_color(wr.Color(0.33, 0.33, 0.33)) # default
    #  mat_toon_green.set_outlines_tinting_enabled(True) # default
    mat_toon_green.set_tint(wr.Color(0.377, 0.8, 0.513))
    mat_toon_green.set_outlines_color(wr.Color(0.077, 0.5, 0.213))

    # specify region's colors, don't tint them, rely on the default outline
    # color, which will be tinted bt the region's colors:
    #  mat_toon_pink.set_tint(wr.Color(1.0, 1.0, 1.0)) # default
    #  mat_toon_pink.set_outlines_tinting_enabled(True) # default
    #  mat_toon_pink.set_outlines_color(wr.Color(0.5, 0.5, 0.5)) # default
    mat_toon_pink.set_lit_color(wr.Color(0.8, 0.377, 0.661))
    mat_toon_pink.set_dark_color(wr.Color(0.5, 0.077, 0.361))

    # assign materials
    group.assign_material(mat_toon_green, '.*/tetra_l.*')
    group.assign_material(mat_toon_pink, '.*/tetra_r.*')
    ground.assign_material(mat_white)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(1280, 720)
    settings.set_image_name('toon_outlines.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'toon_outlines.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
