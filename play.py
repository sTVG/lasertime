import ezdxf

doc = ezdxf.readfile("dxfs/eo2zxlo8.dxf")
msp = doc.modelspace()

for entity in msp:
    print(entity, entity.dxfattribs())