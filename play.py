import svgpathtools
from dxf2svg.pycore import save_svg_from_dxf
from tempfile import TemporaryDirectory

def svglength(filename):
    paths, _attributes = svgpathtools.svg2paths(filename)

    total = 0
    for path in paths:
        total += path.length()
    
    return total

def dxflength(filename):
    with TemporaryDirectory() as tempdir:
        #svgfilename = f"{tempdir}/temp.svg"
        svgfilename = "dxfs/test.svg"
        save_svg_from_dxf(filename, svgfilename)
        return svglength(svgfilename)

if __name__ == "__main__":
    print(dxflength("dxfs/eo2zxlo8.dxf"), svglength("dxfs/eo2zxlo8.svg"))