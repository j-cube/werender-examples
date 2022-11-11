# Copyright 2022 J-CUBE Inc. Yokohama, Japan. All Rights Reserved.
# https://werender.io

import os
import tempfile

import werender as wr

# a convenience function to find all assets via env var
def resolve_file(filename):
    return os.path.join(
        os.environ.get('WERENDER_ASSETS_PATH', './'), filename)


#
def main(session):
    # optional: save a log file
    wr.set_log_file(os.path.join(tempfile.gettempdir(), 'maneki_automatic.log'))

    # where to store assets in the cloud storage
    remote_folder = '/assets/examples'

    # assets
    maneki_asset = session.upload(resolve_file('maneki.usdz'), remote_folder)

    # create a scene
    scene = wr.Scene()

    # create model(s), if .usdz materials are embedded
    maneki = scene.new_model(maneki_asset)

    # create render settings
    settings = wr.RenderSettings()
    settings.set_resolution(720, 720)
    settings.set_image_name('maneki_automatic.jpg')
    settings.set_enable_ground(True)
    
    # optional: specify where renders will be stored in the cloud storage
    settings.set_remote_folder('/MyRenders/examples')

    # now we render (pun intended)
    result = session.start_render_and_wait(settings, scene)

    # optional: download the image
    result.download_image(tempfile.gettempdir(), 'maneki_automatic.jpg')

if __name__ == '__main__':
    session = wr.authenticate()
    main(session)
