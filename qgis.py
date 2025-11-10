import os
from qgis.core import QgsRasterLayer, QgsPointXY, QgsCoordinateReferenceSystem
from qgis.analysis import QgsGeoreferencer

# === CONFIGURATION SECTION ===

# Folder containing the input JPG raster maps
input_folder = '/path/to/your/input_jpgs'

# Folder where the georeferenced GeoTIFF files will be saved
output_folder = '/path/to/your/output_tiffs'

# Raster dimensions in pixels (adjust to match your input maps)
width_px = 1000
height_px = 800

# Geographic coordinates of the raster corners (longitude/latitude)
Xmin = -180.0   # Minimum longitude
Xmax = 180.0    # Maximum longitude
Ymin = -90.0    # Minimum latitude
Ymax = 90.0     # Maximum latitude

# Target Coordinate Reference System (WGS 84)
target_crs = QgsCoordinateReferenceSystem('EPSG:4326')

# Ground Control Points for georeferencing: (pixel_x, pixel_y, longitude, latitude)
control_points = [
    (0, 0, Xmin, Ymax),  # Upper left corner
    (width_px, 0, Xmax, Ymax),  # Upper right corner
    (width_px, height_px, Xmax, Ymin),  # Lower right corner
    (0, height_px, Xmin, Ymin),  # Lower left corner
]

# === FUNCTION DEFINITIONS ===

def georeference_raster(input_raster_path, output_raster_path):
    """
    Georeferences a raster image using predefined control points and saves as GeoTIFF.

    Parameters:
        input_raster_path (str): Path to the input raster image (JPG)
        output_raster_path (str): Destination path for the georeferenced file (TIFF)
    """
    raster_layer = QgsRasterLayer(input_raster_path, os.path.basename(input_raster_path))
    if not raster_layer.isValid():
        print(f'Error loading: {input_raster_path}')
        return

    georef = QgsGeoreferencer()
    georef.setSourceRaster(raster_layer)
    for px, py, lon, lat in control_points:
        georef.addPoint(QgsPointXY(px, py), QgsPointXY(lon, lat))
    georef.setTransformationType(QgsGeoreferencer.TransformationType.Linear)
    georef.setTargetCrs(target_crs)
    georef.setResampling(QgsGeoreferencer.ResamplingMethod.Linear)
    georef.setOutputFile(output_raster_path)
    georef.setOutputRasterSize(width_px, height_px)

    success = georef.georeference()
    if success:
        print(f'Successfully georeferenced: {input_raster_path}')
    else:
        print(f'Failed to georeference: {input_raster_path}')

# === MAIN SCRIPT EXECUTION ===

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.jpg'):
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f'{base_name}.tif')
        georeference_raster(input_path, output_path)
