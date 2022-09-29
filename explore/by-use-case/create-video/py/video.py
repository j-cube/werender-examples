# Copyright 2022 J Cube Inc. Yokohama, Japan. All Rights Reserved.
# https://werender.io
#   by use-case: create video

import os
import tempfile
import time

import werender as wr


def resolve_file(filename):
    return os.path.join(
        os.environ.get('WERENDER_ASSETS_PATH', './'), filename)


def render_frames(session):
    """Renders frames of a rotating maneki and then createts a video."""
    maneki_asset = session.upload(resolve_file('maneki.usdz'), '/assets')
    plane_asset = session.upload(resolve_file('plane.usd'), '/assets')

    scene = wr.Scene()

    maneki = scene.new_model(maneki_asset)
    plane = scene.new_model(plane_asset)

    camera = scene.new_camera(wr.cameras.Persp)
    camera.set_focal_length(45.0)
    camera_xform = wr.Transform(
        translate=(0.0, 23.0, 32.0),
        rotate=(-25.0, 0.0, 0.0))
    camera.set_xform(camera_xform)

    settings = wr.RenderSettings()
    settings.set_resolution(512, 512)
    settings.set_remote_folder('/MyRenders/rotating_maneki')

    area_light = scene.new_light(wr.lights.Area)
    area_light.set_intensity(500.0)
    area_light.set_xform(wr.Transform(
        translate=(11.0, 12.0, 8.0),
        rotate=(-24.0, 50.0, 0.0),
        scale=(4.0, 4.0, 4.0)))

    env_light = scene.new_light(wr.lights.Envsky)
    env_light.set_intensity(0.3)

    num_frames = 12
    turntable_xform = wr.Transform()

    requests = []
    for frame in range(num_frames):
        turntable_xform.set_rotation(0.0, 360.0 / num_frames * frame, 0.0)
        maneki.set_xform(turntable_xform)

        settings.set_image_name('rotating_maneki_{:02d}.png'.format(frame))
        requests.append(session.start_render(settings, scene))

    status_list = [session.query_render(request) for request in requests]
    while not all([status.done for status in status_list]):
        print('waiting for renders...')
        time.sleep(1)
        status_list = [session.query_render(request) for request in requests]

    if any([status.failed for status in status_list]):
        print('one or more renders have failed!')
        return

    # Retrieve asset information from the render results.
    render_assets = [status.get_result().get_asset() for status in status_list]

    video_settings = wr.VideoSettings()
    video_settings.set_filename('rotating_maneki.mp4')
    output_asset = session.create_video_clip(render_assets, video_settings)
    session.download_asset(output_asset, tempfile.gettempdir())


def create_video_from_rendered_images(session):
    """Creates a video using existing (remote) rendered frames."""
    input_assets = [
        session.reference_asset(
            f'/MyRenders/rotating_maneki_{i:02}.png')
        for i in range(12)
    ]

    video_settings = wr.VideoSettings()
    video_settings.set_filename('rotating_maneki.mp4')
    output_asset = session.create_video_clip(input_assets, video_settings)
    session.download_asset(output_asset, tempfile.gettempdir())


if __name__ == "__main__":
    session = wr.authenticate()

    # Use this function to render the animation frames and create a video for
    # it straight after the renders are done.
    render_frames(session)

    # Un-comment the following call once the animation frames exist in the
    # remote storage to create a video clip.
    #
    #create_video_from_rendered_images(session)
