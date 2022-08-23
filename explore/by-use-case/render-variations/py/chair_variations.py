# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
# https://werender.io

import os
import sys
import tempfile
import time

import werender as wr

# a convenience function to find all assets via env var
def resolve_file(filename):
    return os.path.join(
        os.environ.get('WERENDER_ASSETS_PATH', './'), filename)


#
def render(session, asset_name, cam_name, cam_xform, mat_name, mat_value):
    # log file
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'chair_variations.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    chair_asset = session.upload(resolve_file(asset_name + '.usd'), remote_folder)
    backdrop_asset = session.upload(resolve_file('backdrop_4.usd'), remote_folder)
    hdri_asset = session.upload(resolve_file('studio_03.exr'), remote_folder)
    wood_tex_asset = session.upload(resolve_file('wood_col.jpg'), remote_folder)

    # create scenes
    scene = wr.Scene()

    # create models
    chair = scene.new_model(chair_asset)
    backdrop = scene.new_model(backdrop_asset)

    # create & apply transforms to chair
    chair_xform = wr.Transform(rotate=(0.0, 103.751, 0.0))
    chair.set_xform(chair_xform)

    # create camera, create and apply transform, set attribute
    camera = scene.new_camera(wr.cameras.Persp)
    camera.set_xform(cam_xform)
    camera.set_focal_length(90.0)

    # create hdri texture, env light and its properties
    tex_hdri = scene.new_texture(wr.textures.File)
    tex_hdri.set_texture_file(hdri_asset)
    envlight = scene.new_light(wr.lights.Envhdri)
    envlight.set_hdri_image(tex_hdri)
    envlight.set_intensity(1.0)
    envlight_xform = wr.Transform(rotate=(0.0, 66.947, 0.0))
    envlight.set_xform(envlight_xform)

    # create materials
    mat_seat = scene.new_material(wr.materials.Generic)
    mat_legs_steel = scene.new_material(wr.materials.Metal)
    mat_legs_wood = scene.new_material(wr.materials.Generic)
    mat_screws = scene.new_material(wr.materials.Metal)
    mat_stoppers = scene.new_material(wr.materials.Generic)
    mat_frame = scene.new_material(wr.materials.Metal)
    mat_backdrop = scene.new_material(wr.materials.Generic)

    # set material attributes
    mat_legs_steel.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_legs_steel.set_edge_color(wr.Color(1.0, 1.0, 1.0))
    mat_legs_steel.set_roughness(0.2)

    mat_frame.set_color(wr.Color(0.1, 0.1, 0.1))
    mat_frame.set_edge_color(wr.Color(1.0, 1.0, 1.0))
    mat_frame.set_roughness(0.7)

    mat_screws.set_color(wr.Color(0.154, 0.139, 0.131))
    mat_screws.set_edge_color(wr.Color(0.78, 0.78, 0.78))
    mat_screws.set_roughness(0.2)

    mat_stoppers.set_color(wr.Color(0.2, 0.2, 0.2))
    mat_stoppers.set_specular_level(1.0)
    mat_stoppers.set_roughness(0.623)

    mat_backdrop.set_color(wr.Color(1.0, 1.0, 1.0))
    mat_backdrop.set_specular_level(1.0)
    mat_backdrop.set_roughness(0.2)

    # create seat texture and set its attributes
    seat_hgt_tex = scene.new_texture(wr.textures.Cellnoise)
    seat_hgt_tex.set_scale(1.0)
    seat_hgt_tex.set_noise_type(3)
    seat_hgt_tex.set_invert(1)

    # create material for seat and set attributes: it uses the above texture
    mat_seat.set_color(mat_value)
    mat_seat.set_height(seat_hgt_tex)
    mat_seat.set_height_amount(0.9)
    mat_seat.set_height_type(3)
    mat_seat.set_roughness(0.247)

    # create legs texture and its attributes
    wood_tex_col = scene.new_texture(wr.textures.File)
    wood_tex_col.set_texture_file(wood_tex_asset)

    # create material for seat and set attributes: it uses the above texture
    mat_legs_wood.set_color(wood_tex_col)
    mat_legs_wood.set_height(wood_tex_col)
    mat_legs_wood.set_height_amount(0.1)
    mat_legs_wood.set_height_type(0)

    # assign materials
    chair.assign_material(mat_seat, '.*/seat.*')
    chair.assign_material(mat_legs_steel, '.*/legs_steel.*')
    chair.assign_material(mat_legs_wood, '.*/legs_wood.*')
    chair.assign_material(mat_screws, '.*/screws.*')
    chair.assign_material(mat_stoppers, '.*/stoppers.*')
    chair.assign_material(mat_frame, '.*/frame.*')
    backdrop.assign_material(mat_backdrop)


    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(720, 720)
    settings.set_image_name(asset_name + '_' + cam_name + '_' + mat_name + '.jpg')
    # specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # render synchronously
    # result = session.start_render_and_wait(settings, scene)
    # download the image
    # result.download_image(tempfile.gettempdir(), asset_name + '_' + cam_name +
    #    '_' + mat_name + '_' + '.jpg')

    # render asynchronously
    requests = []
    requests.append(session.start_render(settings, scene))
    wait_for_all_renders(session, requests, asset_name, cam_name, mat_name)


def wait_for_all_renders(session, requests, asset_name, cam_name, mat_name):
    # 1. Wait until all the renders have finished.
    statuses = [session.query_render(request) for request in requests]
    while not all([status.done for status in statuses]):
        print('waiting for renders...')
        time.sleep(1)
        statuses = [session.query_render(request) for request in requests]

    # 2. Download all the images.
    for i, status in enumerate(statuses):
        if status.failed:
            print('render {} failed!'.format(i))
        else:
            status.get_result().download_image(tempfile.gettempdir(), asset_name
                + '_' + cam_name + '_' + mat_name + '_' + '.jpg')


def main(session):

    # array of strings for the asset filenames
    chair_assets = ['chair_dsr', 'chair_dsw', 'chair_dsx']

    # dictionary of camera transforms
    cam_dict = {
        "wide": wr.Transform(translate=(1560.608, 828.903, 2184.463),
            rotate=(-9.938, 35.800, 0.0)),
        "near": wr.Transform(translate=(823.326, 59.707, 319.407),
            rotate=(23.062, 67, 0.0))}

    # dictionary of camera transforms
    mat_dict = {
        "yellow": wr.Color(0.710, 0.607, 0.0),
        "green": wr.Color(0.0, 0.710, 0.607)}

    for asset in chair_assets:
        for (cam_name, cam_xform) in cam_dict.items():
            for (mat_name, mat_value) in mat_dict.items():
                    render(session, asset, cam_name, cam_xform, mat_name,
                        mat_value)


if __name__ == '__main__':
    session = wr.authenticate()
    main(session)


