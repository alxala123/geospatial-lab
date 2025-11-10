import bpy
import os

# === CONFIGURATION SECTION ===

# Directory containing your TIFF raster maps
input_map_dir = "/path/to/your/tiff_maps"

# Directory where the exported 3D models will be saved
output_dir = "/path/to/your/output_3d_models"

# Radius for the 3D sphere
sphere_radius = 1.0

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

def create_material(image_path):
    """
    Create a Blender material using a raster map as texture.
    
    Args:
        image_path (str): Path to the TIFF image file.
    Returns:
        bpy.types.Material: Configured Blender material.
    """
    img = bpy.data.images.load(image_path)
    mat = bpy.data.materials.new(name=os.path.basename(image_path))
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    tex_image = nodes.new("ShaderNodeTexImage")
    tex_image.image = img

    bsdf = nodes.get("Principled BSDF")
    links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])

    return mat

def create_high_res_sphere(name, radius):
    """
    Create a smoothed and subdivided UV sphere in Blender.
    
    Args:
        name (str): Name for the new sphere object.
        radius (float): Radius of the sphere.
    Returns:
        bpy.types.Object: The created sphere object.
    """
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        segments=128,
        ring_count=64,
        location=(0, 0, 0)
    )
    obj = bpy.context.object
    obj.name = name

    # Apply smooth shading
    bpy.ops.object.shade_smooth()

    # Add subdivision modifier for higher resolution
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    bpy.ops.object.modifier_apply(modifier=subsurf.name)

    return obj

# Reset Blender's scene to a clean state
bpy.ops.wm.read_factory_settings(use_empty=True)

# Process all TIFF files in the input directory
for filename in os.listdir(input_map_dir):
    if not filename.lower().endswith(".tif"):
        continue
    image_path = os.path.join(input_map_dir, filename)
    model_name = os.path.splitext(filename)[0]
    print(f"🌍 Processing: {model_name}")

    # Create high-res sphere and apply texture map
    sphere = create_high_res_sphere(name=model_name, radius=sphere_radius)
    mat = create_material(image_path)
    sphere.data.materials.append(mat)

    # Select only the current sphere for export
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select_set(True)
    bpy.context.view_layer.objects.active = sphere

    # Export as GLB/GLTF
    export_path = os.path.join(output_dir, f"{model_name}.glb")
    bpy.ops.export_scene.gltf(filepath=export_path, use_selection=True)

    # Delete the sphere to clean up before next iteration
    bpy.ops.object.delete()

print("All 3D models were created successfully.")
