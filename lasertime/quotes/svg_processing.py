from dxf2svg.pycore import save_svg_from_dxf
from tempfile import TemporaryDirectory
import svgpathtools
from svgpathtools import wsvg


###################### LENGTH COLOUR ##########################


# Helper function to extract colour from style string
def get_colour_from_style(style, prop):
    for item in style.split(';'):
        key, _, value = item.partition(':')
        if key.strip() == prop:
            return value.strip()
    return None

def extract_svg_colors(svg_file_path):
    paths, attributes = svgpathtools.svg2paths(svg_file_path)
    colors = set()
    for attr in attributes:
        color = attr.get('stroke', None) or attr.get('fill', None)
        if not color and 'style' in attr:
            color = get_colour_from_style(attr['style'], 'stroke') or get_colour_from_style(attr['style'], 'fill')
        if color:
            colors.add(color)
    return list(colors)

def process_svg_file(svg_file_path):
    paths, attributes = svgpathtools.svg2paths(svg_file_path)

    # Iterate through the paths and calculate their lengths
    for path, attr in zip(paths, attributes):
        colour = attr.get('stroke', None) or attr.get('fill', None)
    
    # Check for the colour in the 'style' attribute if not found in 'stroke' or 'fill'
    if not colour and 'style' in attr:
        colour = get_colour_from_style(attr['style'], 'stroke') or get_colour_from_style(attr['style'], 'fill')
    
    length = path.length()
    print(f"colour: {colour}, Path Length: {length}mm")



def svglength(svg_file_path):
    # Load the SVG file
    paths, _ = svgpathtools.svg2paths(svg_file_path)
    
    # Compute the total length by summing up the lengths of individual paths
    total = sum(path.length() for path in paths)
    
    return total


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
    - cutcost (float, optional): Cost of the cut. Defaults to 0.2. because cut time is in seconds, and cost of cutting is R12 / minute = R0.2 / sec

    Returns:
    - float: The calculated cut price.
    """
    cuttime = calculate_cuttime(svglength, cutspeed)
    return cuttime * cutcost
