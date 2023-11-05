from dxf2svg.pycore import save_svg_from_dxf
from tempfile import TemporaryDirectory
import svgpathtools
from svgpathtools import wsvg





###################### LENGTH COLOUR ##########################

paths, attributes = svgpathtools.svg2paths('test-files/colours.svg')

# Helper function to extract colour from style string
def get_colour_from_style(style, prop):
    for item in style.split(';'):
        key, _, value = item.partition(':')
        if key.strip() == prop:
            return value.strip()
    return None

# Iterate through the paths and calculate their lengths
for path, attr in zip(paths, attributes):
    colour = attr.get('stroke', None) or attr.get('fill', None)
    
    # Check for the colour in the 'style' attribute if not found in 'stroke' or 'fill'
    if not colour and 'style' in attr:
        colour = get_colour_from_style(attr['style'], 'stroke') or get_colour_from_style(attr['style'], 'fill')
    
    length = path.length()
    print(f"colour: {colour}, Path Length: {length}mm")

def svglength(svg_file):
    # Load the SVG file
    paths, _ = svgpathtools.svg2paths(svg_file)
    
    # Compute the total length by summing up the lengths of individual paths
    total = sum(path.length() for path in paths)
    
    print(f"total length:                 {total}mm")



######################PRICE##########################
def calculate_cuttime(svglength, cutspeed=10):
    """
    Calculate the cut time based on svglength and cutspeed.

    Parameters:
    - svglength (float): The length of the SVG.
    - cutspeed (float, optional): Speed at which the cut is made. Defaults to 10.

    Returns:
    - float: The calculated cut time.
    """
    return svglength / cutspeed

def calculate_cutprice(svglength, cutspeed=20, cutcost=0.2):
    """
    Calculate the cut price based on svglength, setupcost, cutspeed, and cutcost.

    Parameters:
    - svglength (float): The length of the SVG.
    - setupcost (float, optional): The setup cost. Defaults to 10.
    - cutspeed (float, optional): Speed at which the cut is made. Defaults to 10.
    - cutcost (float, optional): Cost of the cut. Defaults to 12.

    Returns:
    - float: The calculated cut price.
    """
    cuttime = calculate_cuttime(svglength, cutspeed)
    return cuttime * cutcost

# Test
svg_length_sample = svglength("test-files\colours.svg")
#print(f"Cut price for SVG length {round(svg_length_sample, 3)}mm is: R{round(calculate_cutprice(svg_length_sample), 2)}")