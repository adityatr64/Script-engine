import re
import xml.etree.ElementTree as ET

def tokenize_path(d_str):
    """Tokenizes an SVG path d string into commands and float values."""
    tokens = re.findall(r'([a-zA-Z])|([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)', d_str)
    result = []
    for cmd, num in tokens:
        if cmd:
            result.append(cmd)
        elif num:
            result.append(float(num))
    return result

def parse_path_to_subpaths(d_str, tx=0.0, ty=0.0):
    """
    Parses SVG path data string into a list of coordinate tuples (subpaths).
    Supports M/m, L/l, C/c, Z/z commands.
    """
    tokens = tokenize_path(d_str)
    subpaths = []
    current_subpath = []
    curr_x, curr_y = 0.0, 0.0
    start_x, start_y = 0.0, 0.0
    
    i = 0
    cmd = None
    while i < len(tokens):
        tok = tokens[i]
        if isinstance(tok, str):
            cmd = tok
            i += 1
            
        if cmd in ('M', 'm'):
            if i + 1 >= len(tokens) or isinstance(tokens[i], str):
                i += 1
                continue
            x = tokens[i]
            y = tokens[i+1]
            i += 2
            if cmd == 'm':
                curr_x += x
                curr_y += y
            else:
                curr_x = x
                curr_y = y
            start_x, start_y = curr_x, curr_y
            if current_subpath:
                subpaths.append(current_subpath)
            current_subpath = [(curr_x + tx, curr_y + ty)]
            cmd = 'l' if cmd == 'm' else 'L'
            
        elif cmd in ('L', 'l'):
            if i + 1 >= len(tokens) or isinstance(tokens[i], str):
                i += 1
                continue
            x = tokens[i]
            y = tokens[i+1]
            i += 2
            if cmd == 'l':
                curr_x += x
                curr_y += y
            else:
                curr_x = x
                curr_y = y
            current_subpath.append((curr_x + tx, curr_y + ty))
            
        elif cmd in ('C', 'c'):
            if i + 5 >= len(tokens) or isinstance(tokens[i], str):
                i += 1
                continue
            x1, y1 = tokens[i], tokens[i+1]
            x2, y2 = tokens[i+2], tokens[i+3]
            x3, y3 = tokens[i+4], tokens[i+5]
            i += 6
            if cmd == 'c':
                p1 = (curr_x + x1, curr_y + y1)
                p2 = (curr_x + x2, curr_y + y2)
                p3 = (curr_x + x3, curr_y + y3)
            else:
                p1 = (x1, y1)
                p2 = (x2, y2)
                p3 = (x3, y3)
            p0 = (curr_x, curr_y)
            num_steps = 10
            for step in range(1, num_steps + 1):
                t = step / num_steps
                u = 1.0 - t
                bx = u*u*u * p0[0] + 3*u*u*t * p1[0] + 3*u*t*t * p2[0] + t*t*t * p3[0]
                by = u*u*u * p0[1] + 3*u*u*t * p1[1] + 3*u*t*t * p2[1] + t*t*t * p3[1]
                current_subpath.append((bx + tx, by + ty))
            curr_x, curr_y = p3
            
        elif cmd in ('Z', 'z'):
            if current_subpath:
                current_subpath.append((start_x + tx, start_y + ty))
                subpaths.append(current_subpath)
                current_subpath = []
            curr_x, curr_y = start_x, start_y
        else:
            i += 1
            
    if current_subpath:
        subpaths.append(current_subpath)
        
    return subpaths

def render_svg_on_canvas(canvas, svg_xml_str, scale=3.0, offset_x=40, offset_y=80, stroke_color="#000000", bg_color="#ffffff"):
    """
    Renders SVG XML string onto a Tkinter Canvas with scale and offset.
    Returns (svg_width, svg_height, viewBox_min_y).
    """
    canvas.delete("all")
    
    if not svg_xml_str:
        return (0, 0, 0)
        
    try:
        root = ET.fromstring(svg_xml_str)
    except Exception as e:
        print(f"Error parsing SVG XML: {e}")
        return (0, 0, 0)
        
    viewbox_str = root.get("viewBox", "0 0 100 100")
    vb_parts = [float(p) for p in viewbox_str.split()]
    vb_min_x, vb_min_y, vb_w, vb_h = vb_parts if len(vb_parts) == 4 else (0, 0, 100, 100)
    
    # Draw background on canvas
    canvas_w = int(canvas.winfo_width() or 800)
    canvas_h = int(canvas.winfo_height() or 500)
    canvas.create_rectangle(0, 0, canvas_w, canvas_h, fill=bg_color, outline="")
    
    # Recursive element drawing with transform stack
    def process_element(elem, current_tx, current_ty):
        tx = current_tx
        ty = current_ty
        
        transform = elem.get('transform', '')
        if transform.startswith('translate('):
            try:
                coords = transform[10:-1].split(',')
                tx += float(coords[0])
                ty += float(coords[1])
            except Exception:
                pass
                
        # Parse <path>
        if elem.tag.endswith('path'):
            d_str = elem.get('d', '')
            if d_str:
                path_stroke = elem.get('stroke', stroke_color)
                if path_stroke == 'none':
                    path_stroke = stroke_color
                subpaths = parse_path_to_subpaths(d_str, tx=tx, ty=ty - vb_min_y)
                for pts in subpaths:
                    if len(pts) >= 2:
                        # Map points to canvas coordinates
                        canvas_pts = []
                        for px, py in pts:
                            cx = offset_x + px * scale
                            cy = offset_y + py * scale
                            canvas_pts.extend([cx, cy])
                        width_val = max(1.5, 1.8 * (scale / 3.0))
                        canvas.create_line(
                            canvas_pts,
                            fill=path_stroke,
                            width=width_val,
                            capstyle="round",
                            joinstyle="round",
                            smooth=True
                        )
                        
        for child in elem:
            process_element(child, tx, ty)

    # Process all root elements
    process_element(root, 0.0, 0.0)
    
    return (vb_w, vb_h, vb_min_y)
