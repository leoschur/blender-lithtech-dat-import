from .kaitai_lithtech_dat_struct import LithtechDat
from mathutils import Vector


def vec3_to_xzy(p: LithtechDat.Vec3):
    """Convert a LithtechDat Vec3 into a Unity Coordinate
    Positional arguments:
        p: [LithtechDat.Vec3] Point
    Returns:
        Coordinate: [typing.Tuple<float>]
    """
    return (p.x * 0.01, p.z * 0.01, p.y * 0.01)


def int32_to_rgba(color_int32):
    """Convert an int32 color value to an RGBA vector.
    Args:
        color_int32 (int): The color value stored as an int32.
    Returns:
        mathutils.Vector: A Vector of the form (red, green, blue, alpha=1) containing the RGB values.
    """
    r = (color_int32 >> 16) & 0xFF
    g = (color_int32 >> 8) & 0xFF
    b = color_int32 & 0xFF
    return Vector((r, g, b, 1))


def decompress_lm_data(compressed):
    """RLE decompression
    Arts:
        compressed (byte array): Compressed data
    Returns:
        decompressed (list): Decompressed data
    """
    decompressed = []
    i = 0
    while i < len(compressed):
        tag = compressed[i]
        i += 1
        # see if it is a run or a span
        is_run = True if tag & 0x80 else False  # (tag & 0x80) != 0
        # blit the color span
        run_len = (tag & 0x7F) + 1
        j = 0
        while j < run_len:
            j += 1
            decompressed.append(compressed[i])  # r
            decompressed.append(compressed[i + 1])  # g
            decompressed.append(compressed[i + 2])  # b
            decompressed.append(1)  # a this is for the transparancy
            if not is_run:
                i += 3
                pass
            continue
        if is_run:
            i += 3
            pass
        continue
    return decompressed
