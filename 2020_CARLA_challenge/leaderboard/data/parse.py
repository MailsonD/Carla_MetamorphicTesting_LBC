import sys
import xml.etree.ElementTree as ET
import pathlib

TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<routes>
%s
</routes>"""

input_routes = pathlib.Path(sys.argv[1])
output_dir = pathlib.Path(sys.argv[2]) / input_routes.stem
output_dir.mkdir(exist_ok=True, parents=False)

for i, route in enumerate(ET.parse(input_routes).getroot()):
    (output_dir / ('route_%02d.xml' % i)).write_text(TEMPLATE % ET.tostring(route))
