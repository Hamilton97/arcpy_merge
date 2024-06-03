import sys

from pathlib import Path

try:
    import arcpy
except ImportError:
    print("Error: Arcpy is not on current python path...")
    sys.exit(1)


def main() -> None:
    args = sys.argv[1:]
    # get the rasters
    if len(args) != 2:
        print("<USAGE>: arcpy_merge <input_dir> <output_name>")
        sys.exit(1)

    input_dir = Path(args[0]).absolute()
    output_name = Path(args[1])
    
    if output_name.exists():
        print("Mosaic Already Exsits.. Exiting")
        sys.exit(1)
     
    output_location = output_name.parent.absolute()
    name_with_ext = output_name.name

    files = list(input_dir.glob("*.tif"))
    files = list(map(str, files))
    
    input_rasters = ';'.join(files)

    raster_obj = arcpy.Raster(files[0])
    nbands = raster_obj.bandCount
    
    pixel_type = {
        'U1': '1_BIT',
        'U2': '2_BIT',
        'U4': '4_BIT',
        'U8': '8_BIT_UNSIGNED',
        'S8': '8_BIT_SIGNED',
        'U16': '16_BIT_UNSIGNED',
        'S16': '16_BIT_SIGNED',
        'U32': '32_BIT_UNSIGNED',
        'S32': '32_BIT_SIGNED',
        'F32': '32_BIT_FLOAT',
        'F64': '64_BIT'
    }
    pixel_type = pixel_type.get(raster_obj.pixelType)

    arcpy.MosaicToNewRaster_management(
        input_rasters=input_rasters, 
        output_location=str(output_location),
        raster_dataset_name_with_extension=str(name_with_ext),
        pixel_type=pixel_type,
        number_of_bands=nbands,
    )
    sys.exit(0)
