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

def merge_svgs(glyph_items, output_path=None, stack_y_offset=14.73, vowel_line_inset=4, jitter=0.5, max_line_width=500, line_spacing=56.0):
    """
    Merges SVGs horizontally into multi-line script illustrations with Indic-style vowel stacking.
    Supports max_line_width word wrapping and explicit NEWLINE items.
    Always renders strokes in pure black (#000000).
    """
    GLYPH_SIZE = 32      # Width of SVG images
    SPACE_WIDTH = 16     # Width of space character
    STACK_Y_OFFSET = stack_y_offset  # Vertical offset so attached vowels touch/connect to top of consonants
    
    # 1. Group glyph_items into words, spaces, and newlines for clean line wrapping
    tokens = []
    current_word_items = []
    current_word_width = 0.0
    
    for item in glyph_items:
        if item == 'SPACE' or item == 'NEWLINE':
            if current_word_items:
                tokens.append({'type': 'WORD', 'items': current_word_items, 'width': current_word_width})
                current_word_items = []
                current_word_width = 0.0
            tokens.append({'type': item})
        else:
            current_word_items.append(item)
            is_attached = item.get('is_attached', False) if isinstance(item, dict) else False
            if not is_attached:
                current_word_width += GLYPH_SIZE
                
    if current_word_items:
        tokens.append({'type': 'WORD', 'items': current_word_items, 'width': current_word_width})

    # 2. Render tokens onto SVG element tree
    root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
    root.set("version", "1.1")
    main_group = ET.SubElement(root, 'g')

    current_x = 0.0
    current_y = 0.0
    max_reached_x = float(GLYPH_SIZE)
    min_y = 0.0
    max_y = float(GLYPH_SIZE)

    for token in tokens:
        tok_type = token['type']
        
        if tok_type == 'NEWLINE':
            current_x = 0.0
            current_y += line_spacing
            max_y = max(max_y, current_y + GLYPH_SIZE)
            continue
            
        if tok_type == 'SPACE':
            if current_x > 0:
                current_x += SPACE_WIDTH
                max_reached_x = max(max_reached_x, current_x)
            continue
            
        if tok_type == 'WORD':
            w_items = token['items']
            w_width = token['width']
            
            # Word wrapping check
            if max_line_width and max_line_width > 0 and current_x > 0 and (current_x + w_width > max_line_width):
                current_x = 0.0
                current_y += line_spacing
                max_y = max(max_y, current_y + GLYPH_SIZE)
                
            for item in w_items:
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
                    target_x = max(0.0, current_x - GLYPH_SIZE)
                    target_y = current_y - STACK_Y_OFFSET
                    glyph_group.set('transform', f'translate({target_x}, {target_y})')
                    min_y = min(min_y, target_y)
                else:
                    target_x = current_x
                    target_y = current_y
                    glyph_group.set('transform', f'translate({target_x}, {target_y})')
                    current_x += GLYPH_SIZE
                    max_reached_x = max(max_reached_x, current_x)
                    max_y = max(max_y, current_y + GLYPH_SIZE)
                    
                has_line = False
                for child in glyph_root:
                    if child.tag.endswith('line') and child.get('id') == 'svg_6':
                        has_line = True
                    glyph_group.append(child)
                    
                if not has_line:
                    if is_attached:
                        x1_val = float(vowel_line_inset)
                        x2_val = float(GLYPH_SIZE - vowel_line_inset)
                        y1_val = 21.02167 + random.uniform(-0.2, 0.2)
                        y2_val = 20.91297 + random.uniform(-0.2, 0.2)
                        d_str = generate_handwritten_line_path(x1_val, y1_val, x2_val, y2_val, num_segments=4, jitter=jitter)
                    else:
                        x1_val = -0.22823
                        x2_val = 32.27171
                        y1_val = 21.02167
                        y2_val = 20.91297
                        d_str = generate_handwritten_line_path(x1_val, y1_val, x2_val, y2_val, num_segments=4, jitter=jitter)

                    line_elem = ET.Element('path', {
                        'id': 'svg_6',
                        'd': d_str,
                        'stroke': '#000000',
                        'fill': 'none'
                    })
                    glyph_group.append(line_elem)

    total_width = max(max_reached_x, float(GLYPH_SIZE))
    total_height = max_y - min_y

    root.set("width", str(total_width))
    root.set("height", str(total_height))
    root.set("viewBox", f"0 {min_y} {total_width} {total_height}")

    tree = ET.ElementTree(root)
    if output_path:
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"Generated: {output_path}")

    svg_str = ET.tostring(root, encoding='utf-8').decode('utf-8')
    return svg_str
