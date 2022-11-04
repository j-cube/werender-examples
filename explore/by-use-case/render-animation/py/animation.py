# Copyright 2022 J Cube Inc. Yokohama, Japan. All Rights Reserved.
# https://werender.io
#   by use-case: animation

import os
import tempfile
import time

import werender as wr


def resolve_file(filename):
    return os.path.join(
        os.environ.get('WERENDER_ASSETS_PATH', './'), filename)


def turntable_serial(session):
    """Creates an animation  by translating the main model.

    The images are generated sequentially calling the `render()` function in
    a loop. Each `render.start_and_wait()` function will block until the
    submitted render is finished.
    """
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
    # Set shutter open/close to half time.
    camera.set_shutter_open(-0.5)
    camera.set_shutter_close(0.5)

    settings = wr.RenderSettings()
    settings.set_resolution(512, 512)
    settings.set_remote_folder('/MyRenders/animation')

    area_light = scene.new_light(wr.lights.Area)
    area_light.set_intensity(500.0)
    area_light.set_xform(wr.Transform(
        translate=(11.0, 12.0, 8.0),
        rotate=(-24.0, 50.0, 0.0),
        scale=(4.0, 4.0, 4.0)))

    env_light = scene.new_light(wr.lights.Envsky)
    env_light.set_intensity(0.3)

    num_frames = 12

    # Model transformation.
    xform1 = wr.Transform(translate=(-6.0, 0.0, 0.0))
    xform2 = wr.Transform(translate=(6.0, 0.0, 0.0))

    # Set different transformations at time 0 and 11.
    maneki.set_xform_at(xform1, 0.0)
    maneki.set_xform_at(xform1, 1.0) # no motion blur on first frame
    maneki.set_xform_at(xform2, 10.0)
    maneki.set_xform_at(xform2, 11.0) # no motion blur on last frame


    for frame in range(num_frames):
        settings.set_image_name('animation_serial_{:02d}.png'.format(frame))
        # Set the current frame.
        settings.set_frame(frame)
        # Render with 3D motion blur.
        settings.set_motion_blur(True)
        result = session.start_render_and_wait(settings, scene)
        result.download_image(tempfile.gettempdir())


def turntable_async(session):
    """Creates a turn-table sequence by rotating a light around the model.

    The images are generated _in parallel_ on the cloud by submitting each
    render using the `render.start()` function. `render.start()` starts a
    render job on the cloud and returns immediately an object of type
    `RenderRequest`. Such object can be used to query the status of the render
    and finally obtain and download the rendered image.
    """
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
    settings.set_remote_folder('/MyRenders/turntable')

    area_light = scene.new_light(wr.lights.Area)
    area_light.set_intensity(500.0)
    area_light.set_xform(wr.Transform(
        translate=(11.0, 12.0, 8.0),
        rotate=(-24.0, 50.0, 0.0),
        scale=(4.0, 4.0, 4.0)))

    env_light = scene.new_light(wr.lights.Envsky)
    env_light.set_intensity(0.3)

    requests = []
    num_frames = 12

    # Model transformation.
    xform1 = wr.Transform(translate=(-7.0, 0.0, 0.0))
    xform2 = wr.Transform(translate=(7.0, 0.0, 0.0))

    # Set different transformations at time 0 and 11.
    maneki.set_xform_at(xform1, 0.0)
    maneki.set_xform_at(xform1, 1.0) # no motion blur on first frame
    maneki.set_xform_at(xform2, 10.0)
    maneki.set_xform_at(xform2, 11.0) # no motion blur on last frame

    for frame in range(num_frames):
        # Set the current frame.
        settings.set_frame(frame)
        # Render with 3D motion blur.
        settings.set_motion_blur(True)

        settings.set_image_name('animation_async_{:02d}.png'.format(frame))
        requests.append(session.start_render(settings, scene))

    wait_for_all_renders(session, requests)


def wait_for_all_renders(session, requests):
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
            status.get_result().download_image(tempfile.gettempdir())


if __name__ == "__main__":
    session = wr.authenticate()

    # Un-comment / comment the following call to choose whether to render serial
    # or async

    #turntable_serial(session)
    turntable_async(session)
