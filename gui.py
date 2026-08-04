import sys
import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Ensure src directory is in sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.engine import generate_script, get_glyph_dictionary
from src.render.canvas_renderer import render_svg_on_canvas

# Unified GUI Dark Theme Palette
STYLE = {
    "app_bg": "#1E1E2E",         # Deep Slate background
    "card_bg": "#282A36",        # Card frame background
    "input_bg": "#343746",       # Text entry background
    "fg": "#F8F8F2",             # Primary text color
    "fg_muted": "#A0A8C0",       # Muted label color
    "accent": "#6272A4",         # Accent indigo
    "accent_btn": "#4F46E5",     # Primary action button
    "accent_btn_hover": "#4338CA",
    "btn_secondary": "#3B4252",  # Secondary button background
    "btn_secondary_hover": "#4C566A",
    "canvas_bg": "#FFFFFF",      # Crisp White Drawing Board
    "script_stroke": "#000000"   # Pure Black Script Stroke
}

class ScriptEngineGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Script Engine - English to Vector Script Generator")
        self.geometry("1100x740")
        self.minsize(920, 640)
        self.configure(bg=STYLE["app_bg"])
        
        # State variables
        self.current_svg = ""
        self.current_ipa = ""
        self.glyph_count = 0
        
        # Canvas transform state
        self.zoom_scale = 3.5
        self.pan_offset_x = 50.0
        self.pan_offset_y = 120.0
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        self._setup_ttk_style()
        self._create_widgets()
        
        # Set default text and render initial script
        self.input_entry.insert("1.0", "the quick brown fox jumps over the lazy dog")
        self.on_generate()

    def _setup_ttk_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Configure TScale (Sliders)
        style.configure(
            "TScale",
            background=STYLE["card_bg"],
            troughcolor=STYLE["input_bg"],
            sliderlength=18,
            sliderrelief=tk.FLAT
        )
        
        # Configure TTreeview (Dictionary)
        style.configure(
            "Treeview",
            background=STYLE["card_bg"],
            foreground=STYLE["fg"],
            fieldbackground=STYLE["card_bg"],
            rowheight=26,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=STYLE["input_bg"],
            foreground=STYLE["fg"],
            font=("Segoe UI", 10, "bold")
        )
        style.map("Treeview", background=[("selected", STYLE["accent_btn"])])

    def _create_widgets(self):
        # 1. Header Bar
        header = tk.Frame(self, bg=STYLE["card_bg"], padx=20, pady=12)
        header.pack(fill=tk.X, side=tk.TOP, padx=16, pady=(12, 6))
        
        title_label = tk.Label(
            header,
            text="Script Engine",
            font=("Segoe UI", 16, "bold"),
            fg=STYLE["fg"],
            bg=STYLE["card_bg"]
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header,
            text="— English to Indic-Style Vector Script Generator",
            font=("Segoe UI", 11),
            fg=STYLE["fg_muted"],
            bg=STYLE["card_bg"]
        )
        subtitle_label.pack(side=tk.LEFT, padx=10)

        # 2. Text Input Card
        input_card = tk.Frame(self, bg=STYLE["card_bg"], padx=16, pady=14)
        input_card.pack(fill=tk.X, side=tk.TOP, padx=16, pady=6)
        
        lbl_text = tk.Label(
            input_card,
            text="English Text Input:",
            font=("Segoe UI", 10, "bold"),
            fg=STYLE["fg"],
            bg=STYLE["card_bg"]
        )
        lbl_text.pack(anchor="w", pady=(0, 4))
        
        row_input = tk.Frame(input_card, bg=STYLE["card_bg"])
        row_input.pack(fill=tk.X, expand=True)
        
        self.input_entry = tk.Text(
            row_input,
            font=("Segoe UI", 11),
            bg=STYLE["input_bg"],
            fg=STYLE["fg"],
            insertbackground=STYLE["fg"],
            relief=tk.FLAT,
            bd=6,
            height=3,
            wrap=tk.WORD
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.gen_btn = tk.Button(
            row_input,
            text="Generate Script 🚀",
            font=("Segoe UI", 10, "bold"),
            bg=STYLE["accent_btn"],
            fg="#FFFFFF",
            activebackground=STYLE["accent_btn_hover"],
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=18,
            pady=6,
            cursor="hand2",
            command=self.on_generate
        )
        self.gen_btn.pack(side=tk.RIGHT)
        
        # IPA Transliteration display bar
        ipa_bar = tk.Frame(input_card, bg=STYLE["input_bg"], padx=10, pady=6)
        ipa_bar.pack(fill=tk.X, expand=True, pady=(10, 0))
        
        tk.Label(
            ipa_bar,
            text="IPA Transliteration:",
            font=("Segoe UI", 9, "bold"),
            fg=STYLE["fg_muted"],
            bg=STYLE["input_bg"]
        ).pack(side=tk.LEFT)
        
        self.ipa_label = tk.Label(
            ipa_bar,
            text="-",
            font=("Segoe UI Symbol", 11, "italic"),
            fg="#8BE9FD",
            bg=STYLE["input_bg"]
        )
        self.ipa_label.pack(side=tk.LEFT, padx=10)
        
        # 3. Main Workspace (Sidebar + Interactive Canvas)
        workspace = tk.Frame(self, bg=STYLE["app_bg"])
        workspace.pack(fill=tk.BOTH, expand=True, padx=16, pady=6)
        
        # Left Controls Sidebar
        sidebar = tk.Frame(workspace, bg=STYLE["card_bg"], width=270, padx=14, pady=14)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        sidebar.pack_propagate(False)
        
        tk.Label(
            sidebar,
            text="⚙️ Script Parameters",
            font=("Segoe UI", 11, "bold"),
            fg=STYLE["fg"],
            bg=STYLE["card_bg"]
        ).pack(anchor="w", pady=(0, 12))
        
        # Max Line Width Slider
        f_w = tk.Frame(sidebar, bg=STYLE["card_bg"])
        f_w.pack(fill=tk.X, pady=(4, 0))
        tk.Label(f_w, text="Max Line Width:", font=("Segoe UI", 9, "bold"), fg=STYLE["fg"], bg=STYLE["card_bg"]).pack(side=tk.LEFT)
        self.lbl_max_width_val = tk.Label(f_w, text="480 px", font=("Segoe UI", 9), fg=STYLE["fg_muted"], bg=STYLE["card_bg"])
        self.lbl_max_width_val.pack(side=tk.RIGHT)
        
        self.scale_max_width = ttk.Scale(sidebar, from_=150.0, to=1200.0, value=480.0, command=self._on_slider_change)
        self.scale_max_width.pack(fill=tk.X, pady=(2, 10))
        
        # Jitter Slider
        f_j = tk.Frame(sidebar, bg=STYLE["card_bg"])
        f_j.pack(fill=tk.X, pady=(4, 0))
        tk.Label(f_j, text="Handwriting Jitter:", font=("Segoe UI", 9, "bold"), fg=STYLE["fg"], bg=STYLE["card_bg"]).pack(side=tk.LEFT)
        self.lbl_jitter_val = tk.Label(f_j, text="0.50", font=("Segoe UI", 9), fg=STYLE["fg_muted"], bg=STYLE["card_bg"])
        self.lbl_jitter_val.pack(side=tk.RIGHT)
        
        self.scale_jitter = ttk.Scale(sidebar, from_=0.0, to=1.5, value=0.5, command=self._on_slider_change)
        self.scale_jitter.pack(fill=tk.X, pady=(2, 10))
        
        # Vowel Stack Y-Offset Slider
        f_y = tk.Frame(sidebar, bg=STYLE["card_bg"])
        f_y.pack(fill=tk.X, pady=(4, 0))
        tk.Label(f_y, text="Vowel Stack Height:", font=("Segoe UI", 9, "bold"), fg=STYLE["fg"], bg=STYLE["card_bg"]).pack(side=tk.LEFT)
        self.lbl_stack_y_val = tk.Label(f_y, text="14.73", font=("Segoe UI", 9), fg=STYLE["fg_muted"], bg=STYLE["card_bg"])
        self.lbl_stack_y_val.pack(side=tk.RIGHT)
        
        self.scale_stack_y = ttk.Scale(sidebar, from_=5.0, to=25.0, value=14.73, command=self._on_slider_change)
        self.scale_stack_y.pack(fill=tk.X, pady=(2, 10))
        
        # Top Line Inset Slider
        f_inset = tk.Frame(sidebar, bg=STYLE["card_bg"])
        f_inset.pack(fill=tk.X, pady=(4, 0))
        tk.Label(f_inset, text="Top Line Inset:", font=("Segoe UI", 9, "bold"), fg=STYLE["fg"], bg=STYLE["card_bg"]).pack(side=tk.LEFT)
        self.lbl_inset_val = tk.Label(f_inset, text="4.00", font=("Segoe UI", 9), fg=STYLE["fg_muted"], bg=STYLE["card_bg"])
        self.lbl_inset_val.pack(side=tk.RIGHT)
        
        self.scale_inset = ttk.Scale(sidebar, from_=0.0, to=10.0, value=4.0, command=self._on_slider_change)
        self.scale_inset.pack(fill=tk.X, pady=(2, 14))
        
        # Reset Parameters Button
        self.reset_btn = tk.Button(
            sidebar,
            text="🔄 Reset Defaults",
            font=("Segoe UI", 9),
            bg=STYLE["btn_secondary"],
            fg=STYLE["fg"],
            activebackground=STYLE["btn_secondary_hover"],
            activeforeground=STYLE["fg"],
            relief=tk.FLAT,
            pady=4,
            cursor="hand2",
            command=self.reset_parameters
        )
        self.reset_btn.pack(fill=tk.X, pady=8)

        # Right Preview Area (Drawing Paper Canvas)
        canvas_card = tk.Frame(workspace, bg=STYLE["card_bg"], padx=10, pady=10)
        canvas_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas Toolbar
        toolbar = tk.Frame(canvas_card, bg=STYLE["card_bg"])
        toolbar.pack(fill=tk.X, side=tk.TOP, pady=(0, 8))
        
        self.badge_info = tk.Label(
            toolbar,
            text="Script Canvas (Black Ink on White Paper)",
            font=("Segoe UI", 9, "bold"),
            fg=STYLE["fg_muted"],
            bg=STYLE["card_bg"]
        )
        self.badge_info.pack(side=tk.LEFT)
        
        # Zoom controls
        zoom_bar = tk.Frame(toolbar, bg=STYLE["card_bg"])
        zoom_bar.pack(side=tk.RIGHT)
        
        tk.Button(
            zoom_bar, text="🔍 Reset View", font=("Segoe UI", 8),
            bg=STYLE["btn_secondary"], fg=STYLE["fg"], relief=tk.FLAT,
            command=self.reset_view, cursor="hand2"
        ).pack(side=tk.RIGHT, padx=2)
        
        tk.Button(
            zoom_bar, text="➖ Zoom Out", font=("Segoe UI", 8),
            bg=STYLE["btn_secondary"], fg=STYLE["fg"], relief=tk.FLAT,
            command=lambda: self.zoom(0.85), cursor="hand2"
        ).pack(side=tk.RIGHT, padx=2)
        
        tk.Button(
            zoom_bar, text="➕ Zoom In", font=("Segoe UI", 8),
            bg=STYLE["btn_secondary"], fg=STYLE["fg"], relief=tk.FLAT,
            command=lambda: self.zoom(1.15), cursor="hand2"
        ).pack(side=tk.RIGHT, padx=2)

        # White Paper Vector Canvas
        self.canvas = tk.Canvas(
            canvas_card,
            bg=STYLE["canvas_bg"],
            highlightthickness=1,
            highlightbackground="#E2E8F0",
            cursor="fleur"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Canvas Drag & Zoom Bindings
        self.canvas.bind("<ButtonPress-1>", self.on_pan_start)
        self.canvas.bind("<B1-Motion>", self.on_pan_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        # 4. Footer Bar
        footer = tk.Frame(self, bg=STYLE["card_bg"], padx=16, pady=10)
        footer.pack(fill=tk.X, side=tk.BOTTOM, padx=16, pady=(4, 12))
        
        self.btn_export = tk.Button(
            footer,
            text="💾 Save SVG File",
            font=("Segoe UI", 9, "bold"),
            bg=STYLE["accent_btn"],
            fg="#FFFFFF",
            activebackground=STYLE["accent_btn_hover"],
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=14,
            pady=4,
            cursor="hand2",
            command=self.export_svg
        )
        self.btn_export.pack(side=tk.LEFT, padx=(0, 6))
        
        self.btn_copy = tk.Button(
            footer,
            text="📋 Copy SVG XML",
            font=("Segoe UI", 9),
            bg=STYLE["btn_secondary"],
            fg=STYLE["fg"],
            activebackground=STYLE["btn_secondary_hover"],
            activeforeground=STYLE["fg"],
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.copy_svg_xml
        )
        self.btn_copy.pack(side=tk.LEFT, padx=6)

        self.btn_dict = tk.Button(
            footer,
            text="📖 Phoneme Dictionary",
            font=("Segoe UI", 9),
            bg=STYLE["btn_secondary"],
            fg=STYLE["fg"],
            activebackground=STYLE["btn_secondary_hover"],
            activeforeground=STYLE["fg"],
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.show_dictionary
        )
        self.btn_dict.pack(side=tk.LEFT, padx=6)

        self.status_label = tk.Label(
            footer,
            text="Ready",
            font=("Segoe UI", 9),
            fg=STYLE["fg_muted"],
            bg=STYLE["card_bg"]
        )
        self.status_label.pack(side=tk.RIGHT, padx=8)

    # --- Event Handlers ---
    
    def on_generate(self):
        text = self.input_entry.get("1.0", tk.END)
        if not text.strip():
            self.status_label.config(text="Please enter text.")
            return
            
        t0 = time.time()
        options = {
            "jitter": float(self.scale_jitter.get()),
            "stack_y_offset": float(self.scale_stack_y.get()),
            "vowel_line_inset": float(self.scale_inset.get()),
            "max_line_width": float(self.scale_max_width.get())
        }
        
        result = generate_script(text, options)
        dt = (time.time() - t0) * 1000.0
        
        if result.get("error"):
            self.status_label.config(text=f"Error: {result['error']}")
            return
            
        self.current_svg = result["svg_content"]
        self.current_ipa = result["ipa_text"]
        self.glyph_count = result["glyph_count"]
        
        self.ipa_label.config(text=self.current_ipa)
        self.render_canvas()
        
        self.status_label.config(text=f"Rendered {self.glyph_count} glyphs in {dt:.1f}ms")

    def render_canvas(self):
        if not self.current_svg:
            return
            
        w, h, min_y = render_svg_on_canvas(
            self.canvas,
            self.current_svg,
            scale=self.zoom_scale,
            offset_x=self.pan_offset_x,
            offset_y=self.pan_offset_y,
            stroke_color=STYLE["script_stroke"],  # Pure Black (#000000)
            bg_color=STYLE["canvas_bg"]           # Crisp White (#FFFFFF)
        )
        self.badge_info.config(text=f"Canvas: Black Ink on White Paper | Dimensions: {int(w)}×{int(h)}px | Glyphs: {self.glyph_count}")

    def _on_slider_change(self, val):
        self.lbl_max_width_val.config(text=f"{int(self.scale_max_width.get())} px")
        self.lbl_jitter_val.config(text=f"{self.scale_jitter.get():.2f}")
        self.lbl_stack_y_val.config(text=f"{self.scale_stack_y.get():.2f}")
        self.lbl_inset_val.config(text=f"{self.scale_inset.get():.2f}")
        self.on_generate()

    def reset_parameters(self):
        self.scale_max_width.set(480.0)
        self.scale_jitter.set(0.5)
        self.scale_stack_y.set(14.73)
        self.scale_inset.set(4.0)
        self._on_slider_change(None)

    def on_pan_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_pan_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.pan_offset_x += dx
        self.pan_offset_y += dy
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.render_canvas()

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.zoom(1.15)
        else:
            self.zoom(0.85)

    def zoom(self, factor):
        self.zoom_scale = max(0.5, min(20.0, self.zoom_scale * factor))
        self.render_canvas()

    def reset_view(self):
        self.zoom_scale = 3.5
        self.pan_offset_x = 50.0
        self.pan_offset_y = 120.0
        self.render_canvas()

    def export_svg(self):
        if not self.current_svg:
            messagebox.showwarning("Export Warning", "No SVG content to export.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG Files", "*.svg"), ("All Files", "*.*")],
            title="Save Generated Script SVG"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_svg)
                self.status_label.config(text=f"Saved SVG to {os.path.basename(file_path)}")
                messagebox.showinfo("Export Successful", f"Saved SVG successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save SVG: {e}")

    def copy_svg_xml(self):
        if not self.current_svg:
            return
        self.clipboard_clear()
        self.clipboard_append(self.current_svg)
        self.status_label.config(text="SVG XML copied to clipboard!")

    def show_dictionary(self):
        dict_win = tk.Toplevel(self)
        dict_win.title("Phoneme Glyph Dictionary")
        dict_win.geometry("520x520")
        dict_win.configure(bg=STYLE["app_bg"])
        
        tk.Label(
            dict_win,
            text="Mapping of IPA Phonemes to Vector Glyphs",
            font=("Segoe UI", 12, "bold"),
            fg=STYLE["fg"],
            bg=STYLE["app_bg"],
            pady=12
        ).pack()
        
        tree_frame = tk.Frame(dict_win, bg=STYLE["app_bg"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)
        
        tree = ttk.Treeview(tree_frame, columns=("phoneme", "glyph"), show="headings")
        tree.heading("phoneme", text="IPA Phoneme")
        tree.heading("glyph", text="Glyph SVG File")
        tree.column("phoneme", width=220, anchor="center")

        tree.column("glyph", width=240, anchor="center")
        
        mapping = get_glyph_dictionary()
        for k, v in sorted(mapping.items()):
            tree.insert("", tk.END, values=(k, v))
            
        tree.pack(fill=tk.BOTH, expand=True)

def main():
    app = ScriptEngineGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
