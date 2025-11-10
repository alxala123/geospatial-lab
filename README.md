# georaster-toolkit

A collection of open-source Python and Blender scripts for georeferencing, compressing, and converting raster map data into 3D visualizations. This toolkit automates workflows for GeoTIFF and JPG raster files, supporting both geospatial analysis and 3D modeling.

## Contents

- `qgis.py`: Georeference JPG raster maps to GeoTIFF using QGIS Python API.
- `paleo_reduce.py`: Compress GeoTIFF files with LZW and tiling using rasterio.
- `mapas_batch_3d.py`: Generate 3D UV spheres textured with raster maps and export as GLB files in Blender.
- `georef_jpgs.py`: Georeference JPGs to GeoTIFF using GDAL with Ground Control Points.

---

## Features

- Batch georeferencing of raster maps (JPG, TIFF)
- Efficient compression of geospatial TIFF files
- Automated generation of 3D models from rasters
- Open tools for geospatial analysis and visualization

---

## Installation

Install Python dependencies:

pip install rasterio
pip install GDAL

> Note: QGIS and Blender scripts require their respective environments for execution.

---

## Usage

1. Georeference your JPG maps with `georef_jpgs.py` or `qgis.py`.
2. Compress generated TIFFs with `paleo_reduce.py`.
3. Create 3D model visualizations in Blender using `mapas_batch_3d.py`.

Edit input/output directories and other configuration variables as needed at the top of each script.

---

## Attribution

This project is open-use under the MIT license.  
**Attribution to the author (alxala123) is required in any redistribution, fork, or derivative.**  
Include this credit in documentation, README files, or other appropriate locations:

Code by alxala123 – https://github.com/alxala123/georaster-toolkit


See [LICENSE.md](LICENSE.md) for full license terms.

---

## Contributing

Contributions, suggestions, and pull requests are welcome!

---

## Author

[alxala123](https://github.com/alxala123)

---
