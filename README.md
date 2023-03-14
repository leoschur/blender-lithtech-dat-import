# Blender Lithtech DAT Importer

This is a blender addon to import Lithtech \*.dat (DAT) map files. The plugin is developed with Blender v(3.4.1) and works for Lithtech DAT files with version 85.
The Plugin is developed and tested for Combat Arms maps, but should work with every Lithtech game, provided that the version matches.

## Installation

1. Download the latest zip archive from the release page or clone this repository and zip the entire folder. When cloning, don't forget to clone recursive to include the required submodules.
    ```
    git clone --recursive
    ```
2. In Blender navigate to: `Edit -> Preferences -> Add-ons -> Install`
3. Select the created \*.zip file
4. Enable the Plugin with the check-box

## Usage

After installing you can import the file in Blender with `File -> Import -> Import Lithtech DAT map`.

Alternatively with python:

```py
bpy.ops.import_scene.lithtech_dat(filepath)
```

Or over the Blender quick search with F3 `Import Lithtech Dat map`

## Limitation

-   Textures are currently not supported
-   WorldObjects are also not supported
-   The RenderNodes are created in a rather basic way
