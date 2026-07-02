# Cities Skylines OBJ Importer

A Blender add-on for importing **Cities: Skylines** OBJ models with automatic texture detection and material creation.

![Blender](https://img.shields.io/badge/Blender-3.6%2B-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-GPL--2.0--or--later-green)

---

## Features

* Import one or multiple OBJ files at once
* Automatically detect and assign game textures
* Automatic Principled BSDF material creation
* Optional texture import for each texture type
* X-axis mirror correction without negative scale
* Blender 3.6+ compatible
* Multi-language interface (12 languages)

---

## Supported Texture Types

The importer automatically searches for textures located in the same folder as the OBJ file.

| Suffix | Description             |
| ------ | ----------------------- |
| `_d`   | Diffuse                 |
| `_a`   | Alpha / Transparency    |
| `_c`   | Color Variation         |
| `_i`   | Illumination / Emission |
| `_n`   | Normal Map              |
| `_s`   | Specular                |

Example:

```text
Building.obj
Building_d.png
Building_a.png
Building_c.png
Building_i.png
Building_n.png
Building_s.png
```

The importer also supports fuzzy filename matching if the exact filename cannot be found.

---

## Installation

1. Download this repository as ZIP.
2. Open Blender.
3. Go to:

```
Edit → Preferences → Add-ons
```

4. Click **Install...**
5. Select the downloaded ZIP file.
6. Enable **Cities Skylines OBJ Importer**.

---

## Usage

Open:

```
File → Import → Import Cities Skylines OBJ
```

Select one or more OBJ files.

Available options:

* Import Diffuse (_d)
* Import Alpha (_a)
* Import Color Variation (_c)
* Import Illumination (_i)
* Import Normal Map (_n)
* Import Specular (_s)
* Flip X Axis (Mirror Fix)

The importer will automatically:

* Import OBJ models
* Search textures
* Create Blender materials
* Connect shader nodes
* Apply transparency settings
* Optionally fix mirrored meshes

---

## Multi-language Support

Supported UI languages:

* English
* 简体中文
* 繁體中文
* 日本語
* 한국어
* Français
* Deutsch
* Español
* Português
* Polski
* Русский
* Türkçe

The add-on automatically follows Blender's interface language.

---

## Requirements

* Blender 3.6 or newer
* OBJ model exported from Cities: Skylines
* PNG textures stored in the same directory

---

## License

This project is licensed under the **GNU General Public License v2.0 or later (GPL-2.0-or-later)**.

See the LICENSE file for details.

SPDX Identifier:

```text
GPL-2.0-or-later
```

---

## Author

**liuhua520-svg**

GitHub:

https://github.com/liuhua520-svg/CSL_OBJ_Importer

---

## Changelog

### v1.0.0

* Initial release
* Automatic texture detection
* Automatic material generation
* Batch OBJ import
* X-axis mirror correction
* Multi-language support (12 languages)
* Alpha transparency fix
* Normal map support
* Emission support
* Specular support

---

## Acknowledgements

Thanks to:

* Blender Foundation
* Cities: Skylines modding community
* All users who provide feedback and suggestions
