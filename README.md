# Blender Lithtech DAT Importer

⚠ Status Experimental ⚠

This is a blender addon to import Lithtech \*.dat (DAT) map files. The plugin is developed with Blender v(4.2.2) and "works" for Lithtech DAT files with version 85.
Keep in mind that these are compiled engine-specific game files.
Some things may not translate well in Blender, so details may be lost.
However, I try to do my best to make sense of the available data and display it meaningfully in Blender.
The Plugin is developed and tested for Combat Arms maps, but should work with every Lithtech game, provided that the version matches.

## Installation

1. Download the latest zip `blender-lithtech-dat-import.zip` archive from the [release page](https://github.com/leoschur/blender-lithtech-dat-import/releases)
2. In Blender navigate to: `Edit -> Preferences -> Add-ons -> Install`
3. Select the downloaded `blender-lithtech-dat-import.zip` file
4. Enable the Plugin with the checkbox

or

1. Clone this repository into the Blender Add-on folder. When cloning, don't forget to clone recursive to include the required submodules.
    ```bat
    cd "~\AppData\Roaming\Blender Foundation\Blender\3.4\scripts\addons"
    git clone --recurse-submodules https://github.com/leoschur/blender-lithtech-dat-import
    ```
2. Start Blender navigate to: `Edit -> Preferences -> Add-ons`
3. Search for `Lithtech DAT Map Format (.dat)` and enable the Plugin with the checkbox

## Usage

After installing you can import the file in Blender with `File -> Import -> Import Lithtech DAT map (.dat)`.

Alternatively with python:

```py
bpy.ops.import_scene.lithtech_dat(filepath)
```

Or over the Blender quick search with F3 `Import Lithtech Dat map (.dat)`

If you want to reinstall the Add-on or get a newer version

1.  **Disable** the Add-on first in `Edit -> Preferences -> Add-ons -> Import-Export: Lithtech DAT Map Format (.dat)` by clicking on the checkbox
2.  Click on the arrow on the left of the Add-on entry
3.  Click on Remove
4.  Restart Blender
5.  Only than you can reinstall the Add-on again

### Note:

Currently a texture directory must be specified upon the Import dialog.
This needs to contain the "Textures" directory with the original folder-/file-structure from the game.
The images need to be converted from `*.DTX`/ `*.dtx` into [`*.tga` file format](https://en.wikipedia.org/wiki/Truevision_TGA) beforehand.

## Current Limitation

-   WorldObjects are not yet supported
-   Only some shaders are considered
-   WorldModels are created only partially
-   The RenderNodes are created in a rather basic way
