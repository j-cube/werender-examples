# Copyright 2022 J Cube Inc. Yokohama, Japan. All Rights Reserved.
#
# https://werender.io/explore
#   by industry: automotive


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
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'porsche911.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    porsche_asset = session.upload(resolve_file('porsche.usd'), remote_folder)
    ground_asset = session.upload(resolve_file('ground_car.usd'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models
    porsche = scene.new_model(porsche_asset)
    ground = scene.new_model(ground_asset)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(0.0, 165.009, -444.921),
        rotate=(162.8, 0.0, -180.0))
    camera.set_xform(camera_xform)
    camera.set_focal_length(35.0)

    # create sky env light, and its properties
    envlight = scene.new_light(wr.lights.Envsky)
    envlight.set_intensity(1.5)
    envlight.set_elevation(40.0)
    envlight.set_azimuth(-45)
    envlight.set_sun_size(1.0)

    # create materials
    mat_generic = scene.new_material(wr.materials.Generic)
    mat_rims = scene.new_material(wr.materials.Carpaint)
    mat_carpaint = scene.new_material(wr.materials.Carpaint)
    mat_glass = scene.new_material(wr.materials.Glass)
    mat_ground = scene.new_material(wr.materials.Generic)
    mat_breakes = scene.new_material(wr.materials.Generic)
    mat_carbon = scene.new_material(wr.materials.Metal)
    mat_silver = scene.new_material(wr.materials.Metal)
    mat_rubber = scene.new_material(wr.materials.Generic)
    mat_redlight = scene.new_material(wr.materials.Generic)
    mat_orangelight = scene.new_material(wr.materials.Generic)
    mat_leather= scene.new_material(wr.materials.Generic)
    mat_interior= scene.new_material(wr.materials.Generic)

    # set material attributes

    mat_glass.set_ior(5.0)
    mat_glass.set_reflection_color(wr.Color(0.6, 0.6, 0.6))
    mat_glass.set_reflection_ior(5.0)
    mat_glass.set_thin_film_thickness(0.25)
    mat_glass.set_thin_film_ior(2.0)

    mat_carpaint.set_color(wr.Color(0.1, 0.294, 0.9))
    mat_carpaint.set_coating_color(wr.Color(0.2, 0.372, 0.8))
    mat_carpaint.set_flakes_color(wr.Color(0.2, 0.426, 1.0))
    mat_carpaint.set_flakes_scale(10.0)

    mat_breakes.set_color(wr.Color(1.0, 0.0, 0.0))
    mat_breakes.set_roughness(0.2)
    mat_breakes.set_specular_level(2.0)

    mat_carbon.set_color(wr.Color(0.154, 0.140, 0.131))
    mat_carbon.set_edge_color(wr.Color(1.0, 0.85, 0.796))
    mat_carbon.set_roughness(0.4)

    mat_rubber.set_color(wr.Color(0.01, 0.01, 0.01))
    mat_rubber.set_roughness(0.7)
    mat_rubber.set_specular_level(0.3)

    mat_silver.set_color(wr.Color(0.9, 0.9, 0.9))
    mat_silver.set_edge_color(wr.Color(1.0, 1.0, 1.0))
    mat_silver.set_roughness(0.131)

    mat_redlight.set_color(wr.Color(1.0, 0.0, 0.0))
    mat_redlight.set_opacity(0.25)

    mat_orangelight.set_color(wr.Color(1.0, 0.5, 0.0))
    mat_orangelight.set_opacity(0.25)

    mat_leather.set_color(wr.Color(1.0, 0.6, 0.4))
    mat_leather.set_roughness(0.4)

    mat_interior.set_color(wr.Color(0.3, 0.3, 0.3))
    mat_interior.set_roughness(0.4)

    tex_noise = scene.new_texture(wr.textures.Noise)
    tex_noise.set_scale(500.0)
    tex_noise.set_time(1.863)
    tex_noise.set_layers_contrast(2.0)

    mat_ground.set_color(wr.Color(0.0, 0.0, 0.0))
    mat_ground.set_roughness(tex_noise)
    mat_ground.set_specular_level(1.0)
    mat_ground.set_height(tex_noise)
    mat_ground.set_height_type(4) # displacement, zero centered
    mat_ground.set_height_amount(-0.0001)

    # assign materials
    porsche.assign_material(mat_generic)
    porsche.assign_material(mat_carpaint, '.*/body.*')
    porsche.assign_material(mat_rims, '.*/rims.*')
    porsche.assign_material(mat_glass, '.*/glass.*')
    porsche.assign_material(mat_breakes, '.*/breakes.*')
    porsche.assign_material(mat_carbon, '.*/connecting.*')
    porsche.assign_material(mat_carbon, '.*/bottom.*')
    porsche.assign_material(mat_silver, '.*/discs.*')
    porsche.assign_material(mat_rubber, '.*/tyres.*')
    porsche.assign_material(mat_leather, '.*/seats.*')
    porsche.assign_material(mat_orangelight, '.*/arrow_lights.*')
    porsche.assign_material(mat_orangelight, '.*/front_arrows.*')
    porsche.assign_material(mat_redlight, '.*/break_lights.*')
    porsche.assign_material(mat_interior, '.*/interior.*')

    ground.assign_material(mat_ground)

    # choose the camera
    scene.set_active_camera(camera)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(1920, 1080)
    settings.set_image_name('automotive_porsche911.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'automotive_porsche911.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
