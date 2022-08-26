# werender-examples
Public examples scripts for [WeRender](https://werender.io).

These scripts are used to generate the images or videos in the [explore section](https://werender.io/explore) of the WeRender website.

Folder structure:

```
.
├── assets
|   └── (various models and textures -- coming soon)
└── explore
    ├── by-feature
    |   ├── 3d-noise
    |   ├── bump
    |   ├── displacement
    |   ...
    ├── by-industry
    └── by-use-case
        ├── create-video
        ├── render-360-panorama
        ├── render-animation
        ├── render-asset
        ├── render-turntable
        ├── render-usdz-asset
        ├── render-variations
        ...

```


## Common instructions

To submit a request to WeRender follow these steps:

1. Register a free account on on [werender.io](https://werender.io)
   > Note: while in beta you can apply for early access.

2. Download the werender package and unzip it to a desired location, for this
   document we will use a mock path `/path/to/werender`

3. Read the werender documentation, especially the [get started section](https://werender.io/docs/guide/get-started.html)


### For Python users

4. Set `PYTHONPATH` to find the werender libraries:
   ```
   export PYTHONPATH=/path/to/werender/py
   ```

5. Set `WERENDER_ASSETS_PATH` so to find the assets to upload used in these
   examples:
   ```
   export WERENDER_ASSETS_PATH=/path/to/werender/assets
   ```
   > Note: the name of this environment variable is arbitrarily decided in your
   > scripts.

6. Open a terminal and authenticate with your user/pwd pair:
   ```
   `/path/to/werender-app authenticate`
   ```
   > Note: in the near future we will provide api key access in a similar
   > fashion as AWS.


7. Submit a render request for an example, e.g:
  ```
  python render_usdz_asset.py
  ```

Last but not least, explore the examples, read the docs and leverage on the
programming language to automate scene description generation, render request
submission, sharing to other internet services or users, etc. The possibilities
are unlimited.

Feel free to contact us at [info@j-cube.jp](mailto:info@j-cube.jp) for more
information about WeRender.


> Have fun,
>   -- the WeRender team
