import xml.etree.ElementTree as ET

def merge_svgs(glyph_paths, output_path):
    """
    Merges SVGs horizontally with 0 padding so internal lines connect.
    Adds a gap for spaces.
    """
    GLYPH_SIZE = 32      # Width of SVG images
    SPACE_WIDTH = 16     # Width of space character
    
    current_x = 0
    
    root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
    root.set("version", "1.1")
    
    main_group = ET.SubElement(root, 'g')

    for path in glyph_paths:
        if path == 'SPACE':
            current_x += SPACE_WIDTH
            continue
        tree = ET.parse(path)
        glyph_root = tree.getroot()
        
        glyph_group = ET.SubElement(main_group, 'g')
        glyph_group.set('transform', f'translate({current_x}, 0)')        
        for child in glyph_root:
            glyph_group.append(child)

        current_x += GLYPH_SIZE

    root.set("width", str(current_x))
    root.set("height", str(GLYPH_SIZE))
    root.set("viewBox", f"0 0 {current_x} {GLYPH_SIZE}")

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Generated: {output_path}")