# Kaitai Struct Lithtech DAT

A Kaitai Struct template for the \*.dat map file format from the Lithtech game engine.
The template is developed for DAT file version 85 only.

Do not edit [`./lithtech_dat.py`](./lithtech_dat.py), it is automatically generated with [Kaitai Struct compiler](https://kaitai.io/).
Changes have to be made in [`./lithtech_dat.ksy`](./lithtech_dat.ksy).

To compile the template simply run:

```bash
kaitai-struct-compiler ./lithtech_dat.ksy -t python
```

After compiling the imports from the Kaitai Struct python runtime inside of [`./lithtech_dat.py`](./lithtech_dat.py) needs to be updated manually to:

```py
from .kaitai_struct_python_runtime import kaitaistruct
from .kaitai_struct_python_runtime.kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
```

That is, only if you use the Kaitai Struct runtime as submodule. If you have a better way, create a issue or PR and let me know.

You don't need to do this if you install the Kaitai Struct runtime with pip.

```bash
pip install kaitaistruct
```
