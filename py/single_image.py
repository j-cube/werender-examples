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

    # assets
    maneki_asset = session.upload(resolve_file('maneki.usd'), remote_folder)
    torii_asset = session.upload(resolve_file('torii.usd'), remote_folder)
    base_asset = session.upload(resolve_file('base.usd'), remote_folder)
    grass_asset = session.upload(resolve_file('grass2.usd'), remote_folder)
    maneki_tex_col_asset = session.upload(resolve_file('manekiAR_BaseColor.png'), remote_folder)
    wood_tex_rou_asset = session.upload(resolve_file('wood_rough.tif'), remote_folder)
    copper_tile_tex_col_asset = session.upload(resolve_file('rooftiles_col.jpg'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create models
    maneki = scene.new_model(maneki_asset)
    torii = scene.new_model(torii_asset)
    base = scene.new_model(base_asset)
    grass = scene.new_model(grass_asset)

    # create persp camera, create and apply transform, set attributes
    camera = scene.new_camera(wr.cameras.Persp)
    camera_xform = wr.Transform(
        translate=(0.0, 24.236, 100.896),
        rotate=(-8.000, 0.0, 0.0))
    camera.set_xform(camera_xform)
    camera.set_focal_length(90.0)

    # create physical sky env light and its properties
    envlight = scene.new_light(wr.lights.Envsky)
    envlight.set_intensity(2.0)
    envlight.set_visible_to_camera(1)
    envlight.set_azimuth(145.8)
    envlight.set_ground_enable(1)
    envlight.set_ground_color(wr.Color(0.216, 0.161, 0.139))

    # create materials
    mat_ceramic = scene.new_material(wr.materials.Generic)
    mat_belt = scene.new_material(wr.materials.Generic)
    mat_gold = scene.new_material(wr.materials.Metal)
    mat_eyebulb = scene.new_material(wr.materials.Generic)
    mat_cornea = scene.new_material(wr.materials.Glass)
    mat_whiskers = scene.new_material(wr.materials.Generic)
    mat_red_wood = scene.new_material(wr.materials.Generic)
    mat_black_wood = scene.new_material(wr.materials.Generic)
    mat_copper_tile = scene.new_material(wr.materials.Generic)
    mat_granite = scene.new_material(wr.materials.Generic)
    mat_base = scene.new_material(wr.materials.Generic)
    mat_grass = scene.new_material(wr.materials.Fiber)


    # set material attributes
    mat_ceramic.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_ceramic.set_roughness(0.1)
    mat_ceramic.set_specular_level(1.0)

    mat_belt.set_color(wr.Color(0.55, 0.05, 0.05))

    tex_eyebulb_col = scene.new_texture(wr.textures.File)
    tex_eyebulb_col.set_texture_file(maneki_tex_col_asset)
    mat_eyebulb.set_color(tex_eyebulb_col)

    mat_cornea.set_reflection_ior(2.0)
    mat_cornea.set_ior(2.0)
    mat_cornea.set_thin_film_thickness(2.0)

    mat_whiskers.set_color(wr.Color(0.04, 0.04, 0.04))
    mat_whiskers.set_roughness(0.0)
    mat_whiskers.set_specular_level(2.0)

    tex_wood_rou = scene.new_texture(wr.textures.File)
    tex_wood_rou.set_texture_file(wood_tex_rou_asset)
    tex_wood_rou.set_colorspace("linear")
    tex_wood_rou.set_alpha_is_luminance(1)
    tex_wood_rou.set_tonal_adjust(1)

    mat_red_wood.set_color(wr.Color(0.549, 0.053, 0.053))
    mat_red_wood.set_specular_level(1.0)
    mat_red_wood.set_roughness(tex_wood_rou)
    mat_red_wood.set_height(tex_wood_rou)
    mat_red_wood.set_height_amount(0.1)
    mat_red_wood.set_height_type(0)

    mat_black_wood.set_color(wr.Color(0.05, 0.05, 0.05))
    mat_black_wood.set_specular_level(1.0)
    mat_black_wood.set_roughness(tex_wood_rou)
    mat_black_wood.set_height(tex_wood_rou)
    mat_black_wood.set_height_amount(0.1)
    mat_black_wood.set_height_type(0)

    tex_roof_col = scene.new_texture(wr.textures.File)
    tex_roof_col.set_texture_file(copper_tile_tex_col_asset)
    tex_roof_col.set_repeat_u(2.0)
    tex_roof_col.set_repeat_v(2.0)
    mat_copper_tile.set_color(tex_roof_col)
    mat_copper_tile.set_specular_level(2.0)

    tex_granite_col = scene.new_texture(wr.textures.Noise)
    tex_granite_col.set_scale(0.2)
    tex_granite_col.set_offset(0.6)
    mat_granite.set_color(tex_granite_col)
    mat_granite.set_subsurface(1.0)

    mat_base.set_color(wr.Color(0.5, 0.5, 0.5))
    mat_base.set_specular_level(2.0)

    mat_grass.set_color(wr.Color(0.11, 0.207, 0.081))
    mat_grass.set_consistency(0.5)
    mat_grass.set_synthetic(0.5)
    mat_grass.set_color_variation(0.2)


    # assign materials
    maneki.assign_material(mat_ceramic, '.*/body.*')
    maneki.assign_material(mat_gold, '.*/bell.*')
    maneki.assign_material(mat_gold, '.*/coin.*')
    maneki.assign_material(mat_belt, '.*/belt.*')
    maneki.assign_material(mat_eyebulb, '.*/bulb.*')
    maneki.assign_material(mat_cornea, '.*/cornea.*')
    maneki.assign_material(mat_whiskers, '.*/whiskers.*')

    torii.assign_material(mat_red_wood, '.*/column.*')
    torii.assign_material(mat_red_wood, '.*/hbar.*')
    torii.assign_material(mat_red_wood, '.*/joints.*')
    torii.assign_material(mat_black_wood, '.*/step.*')
    torii.assign_material(mat_black_wood, '.*/mbar.*')
    torii.assign_material(mat_black_wood, '.*/tbar.*')
    torii.assign_material(mat_granite, '.*/baseR.*')
    torii.assign_material(mat_granite, '.*/baseL.*')
    torii.assign_material(mat_granite, '.*/platform.*')
    torii.assign_material(mat_copper_tile, '.*/roof.*')

    base.assign_material(mat_base)

    grass.assign_material(mat_grass)

    # choose the camera
    scene.set_active_camera(camera)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(720, 720)
    settings.set_image_name('maneki_torii_single.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/tests')

    # now we render!
    result = session.start_render_and_wait(settings, scene)

    # optionally download the image
    result.download_image(tempfile.gettempdir(), 'maneki_torii_single.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
