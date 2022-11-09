# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
#
# https://werender.io/explore
#   by feature: displacement procedural

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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'displacement-procedural.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    group_asset = session.upload(resolve_file('group.usd'), remote_folder)
    ground_asset = session.upload(resolve_file('ground.usd'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models and transforms
    group = scene.new_model(group_asset)
    ground = scene.new_model(ground_asset)

    # note: when rendering displacement we should always use subdivision
    # surfacesif possile as it will ensure no cracks and infinite smoothness:
    group_all = group.get_items('/.*')
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
    mat_white = scene.new_material(wr.materials.Generic)

    # set material attributes
    mat_white.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_white.set_roughness(0.1)
    mat_white.set_specular_level(1.0)

    # create 3D procedural texture
    # note: this requires no UVs (and ignores abny existing UVs)
    tex_disp_proc = scene.new_texture(wr.textures.Noise)
    tex_disp_proc.set_self_distorsion(True) # distort displacement with itself
    tex_disp_proc.set_self_distorsion_accumulation(1.0) # and accumulate it
    tex_disp_proc.set_scale(40.0)

    mat_green.set_color(wr.Color(0.377, 0.8, 0.513))
    mat_green.set_roughness(0.3)
    mat_green.set_specular_level(1.0)
    mat_green.set_height(tex_disp_proc) # use 3D procedural for displacement height
    mat_green.set_height_type(4) # displacement, 0.5-centered
    mat_green.set_height_amount(0.2)

    # assign materials
    group.assign_material(mat_green)
    ground.assign_material(mat_white)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(1280, 720)
    settings.set_image_name('displacement_procedural.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'displacement_procedural.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
