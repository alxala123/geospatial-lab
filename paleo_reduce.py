import os
import rasterio

# === CONFIGURATION SECTION ===

# Input folder containing the original raster files (GeoTIFFs)
input_folder = "input_rasters"

# Output folder where compressed raster files will be saved
output_folder = "compressed_rasters"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

# === MAIN SCRIPT EXECUTION ===

for filename in os.listdir(input_folder):
    # Process only GeoTIFF files
    if filename.lower().endswith(".tif"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        print(f"Compressing {filename}...")

        # Open the input raster for reading
        with rasterio.open(input_path) as src:
            profile = src.profile.copy()

            # Update profile with compression and tiling options
            profile.update({
                'compress': 'LZW',
                'predictor': 2,
                'tiled': True,
                'blockxsize': 256,
                'blockysize': 256
            })

            # Write out the compressed raster
            with rasterio.open(output_path, 'w', **profile) as dst:
                for i in range(1, src.count + 1):
                    dst.write(src.read(i), i)
        print("Compression completed.")
