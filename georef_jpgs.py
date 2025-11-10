import os
from osgeo import gdal

# === CONFIGURATION SECTION ===

# Directory containing input JPG raster maps
input_folder = '/path/to/your/input_jpgs'

# Directory where georeferenced GeoTIFFs will be saved
output_folder = '/path/to/your/output_tiffs'

# Geographic coordinates for raster corners (longitude, latitude)
Xmin = -180.0  # Minimum longitude
Xmax = 180.0   # Maximum longitude
Ymin = -90.0   # Minimum latitude
Ymax = 90.0    # Maximum latitude

def georeference_with_gcps(input_path, output_path):
    """
    Georeferences a JPG raster image using hardcoded GCPs and exports as a GeoTIFF.

    Parameters:
        input_path (str): Path to the input JPG image
        output_path (str): Output path for the georeferenced TIFF file
    """
    ds = gdal.Open(input_path, gdal.GA_ReadOnly)
    if ds is None:
        print(f'Could not open: {input_path}')
        return

    width = ds.RasterXSize
    height = ds.RasterYSize

    # Define Ground Control Points: (geox, geoy, 0, pixel, line)
    gcps = [
        gdal.GCP(Xmin, Ymax, 0, 0, 0),            # Upper-left corner
        gdal.GCP(Xmax, Ymax, 0, width, 0),        # Upper-right corner
        gdal.GCP(Xmax, Ymin, 0, width, height),   # Lower-right corner
        gdal.GCP(Xmin, Ymin, 0, 0, height),       # Lower-left corner
    ]

    # Create a virtual dataset with GCPs
    ds = gdal.Translate('', ds, format='VRT', GCPs=gcps)

    # Warp virtual dataset to output GeoTIFF in WGS84
    gdal.Warp(
        output_path,
        ds,
        format='GTiff',
        dstSRS='EPSG:4326',
        outputType=gdal.GDT_Byte,
        resampleAlg='bilinear'
    )
    print(f'Georeferenced and saved: {output_path}')

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Process all JPG files in input directory
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.jpg'):
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f'{base_name}.tif')
        georeference_with_gcps(input_path, output_path)
