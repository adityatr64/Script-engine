import random
import xml.etree.ElementTree as ET

def generate_handwritten_line_path(x1, y1, x2, y2, num_segments=4, jitter=0.5):
    """
    Generates a natural, hand-drawn squiggly line path (d attribute) between (x1, y1) and (x2, y2).
    """
    dx = (x2 - x1) / num_segments
    dy = (y2 - y1) / num_segments
    
    pts = [(x1, y1)]
    for i in range(1, num_segments):
        px = x1 + dx * i + random.uniform(-0.15, 0.15)
        py = y1 + dy * i + random.uniform(-jitter, jitter)
        pts.append((px, py))
    pts.append((x2, y2))
    
    path_d = f"M {pts[0][0]:.2f},{pts[0][1]:.2f}"
    for i in range(len(pts) - 1):
        p0 = pts[i]
        p1 = pts[i+1]
        c1x = p0[0] + (p1[0] - p0[0]) * 0.33 + random.uniform(-0.15, 0.15)
        c1y = p0[1] + (p1[1] - p0[1]) * 0.33 + random.uniform(-jitter * 0.6, jitter * 0.6)
        c2x = p0[0] + (p1[0] - p0[0]) * 0.67 + random.uniform(-0.15, 0.15)
        c2y = p0[1] + (p1[1] - p0[1]) * 0.67 + random.uniform(-jitter * 0.6, jitter * 0.6)
        path_d += f" C {c1x:.2f},{c1y:.2f} {c2x:.2f},{c2y:.2f} {p1[0]:.2f},{p1[1]:.2f}"
    
    return path_d

def merge_svgs(glyph_items, output_path, stack_y_offset=15.02167, vowel_line_inset=4):
    """
    Merges SVGs horizontally and supports Indic-style vowel stacking above consonants.
    glyph_items can contain strings ('SPACE'), dicts ({'path': str, 'is_attached': bool}), or raw file paths.
    """
    GLYPH_SIZE = 32      # Width of SVG images
    SPACE_WIDTH = 16     # Width of space character
    STACK_Y_OFFSET = stack_y_offset  # Vertical offset so attached vowels touch/connect to top of consonants
    
    current_x = 0
    min_y = 0
    max_y = GLYPH_SIZE
    
    root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
    root.set("version", "1.1")
    
    main_group = ET.SubElement(root, 'g')

    for item in glyph_items:
        if item == 'SPACE':
            current_x += SPACE_WIDTH
            continue
            
        if isinstance(item, str):
            path = item
            is_attached = False
        else:
            path = item.get('path')
            is_attached = item.get('is_attached', False)
            
        tree = ET.parse(path)
        glyph_root = tree.getroot()
        
        glyph_group = ET.SubElement(main_group, 'g')
        
        if is_attached:
            # Attached vowel: place above the preceding consonant
            target_x = max(0, current_x - GLYPH_SIZE)
            target_y = -STACK_Y_OFFSET
            glyph_group.set('transform', f'translate({target_x}, {target_y})')
            min_y = min(min_y, target_y)
        else:
            # Baseline glyph: place on baseline and advance X
            target_x = current_x
            target_y = 0
            glyph_group.set('transform', f'translate({target_x}, {target_y})')
            current_x += GLYPH_SIZE
            
        has_line = False
        for child in glyph_root:
            if child.tag.endswith('line') and child.get('id') == 'svg_6':
                has_line = True
            glyph_group.append(child)
            
        if not has_line:
            if is_attached:
                # Top lines for attached vowels: inset so adjacent top lines do not touch
                x1_val = float(vowel_line_inset)
                x2_val = float(GLYPH_SIZE - vowel_line_inset)
                y1_val = 21.02167 + random.uniform(-0.2, 0.2)
                y2_val = 20.91297 + random.uniform(-0.2, 0.2)
                d_str = generate_handwritten_line_path(x1_val, y1_val, x2_val, y2_val, num_segments=4, jitter=0.6)
            else:
                # Baseline normal line for consonants: full width to connect baseline
                x1_val = -0.22823
                x2_val = 32.27171
                y1_val = 21.02167
                y2_val = 20.91297
                d_str = generate_handwritten_line_path(x1_val, y1_val, x2_val, y2_val, num_segments=4, jitter=0.5)

            line_elem = ET.Element('path', {
                'id': 'svg_6',
                'd': d_str,
                'stroke': '#000',
                'fill': 'none'
            })
            glyph_group.append(line_elem)

    total_width = max(current_x, GLYPH_SIZE)
    total_height = max_y - min_y

    root.set("width", str(total_width))
    root.set("height", str(total_height))
    root.set("viewBox", f"0 {min_y} {total_width} {total_height}")

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Generated: {output_path}")