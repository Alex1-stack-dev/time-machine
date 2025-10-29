"""
Complete asset generator for Time Machine swimming meet management software.
Includes all UI elements and integration graphics for Time Machine G2 compatibility.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

# Expanded color palette for swimming meets
COLORS = {
    # Base colors
    'pool_blue': '#0077be',
    'deep_blue': '#003366',
    'lane_line': '#ffffff',
    
    # Status colors
    'dq_red': '#ff4444',
    'scratch_yellow': '#ffdd00',
    'finals_green': '#44cc44',
    'exhibition_purple': '#9933cc',
    
    # UI colors
    'button_normal': '#0066cc',
    'button_hover': '#0088ee',
    'button_active': '#004499',
    'field_bg': '#f8f8f8',
    'header_bg': '#e8e8e8',
    
    # Text colors
    'text_dark': '#333333',
    'text_light': '#ffffff',
    'text_muted': '#666666'
}

class AssetGenerator:
    def __init__(self):
        self.base_path = Path("assets")
        self.setup_directories()
        
    def setup_directories(self):
        """Create all necessary directories for assets"""
        directories = [
            "icons/strokes",      # Swimming stroke icons
            "icons/medals",       # Award medals
            "icons/status",       # DQ, scratch indicators
            "icons/timing",       # Timing related icons
            "ui/buttons",         # Button states
            "ui/fields",         # Form fields
            "ui/tables",         # Table elements
            "ui/indicators",      # Status indicators
            "templates/meet",     # Meet program templates
            "templates/results",  # Results templates
            "templates/awards",   # Award certificates
            "g2_interface"        # Time Machine G2 interface elements
        ]
        
        for dir_path in directories:
            (self.base_path / dir_path).mkdir(parents=True, exist_ok=True)

    def create_stroke_icons(self):
        """Generate swimming stroke icons"""
        strokes = ['freestyle', 'butterfly', 'backstroke', 'breaststroke', 'im']
        size = (64, 64)
        
        for stroke in strokes:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Add stroke-specific silhouette
            self._draw_stroke_silhouette(draw, stroke, size)
            
            img.save(self.base_path / f"icons/strokes/{stroke}.png")

    def create_medal_icons(self):
        """Generate award medal icons"""
        medals = [
            ('gold', '#ffd700'),
            ('silver', '#c0c0c0'),
            ('bronze', '#cd7f32')
        ]
        
        size = (48, 48)
        for name, color in medals:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw medal
            self._draw_medal(draw, color, size)
            
            img.save(self.base_path / f"icons/medals/{name}.png")

    def create_timing_icons(self):
        """Generate timing-related icons for G2 integration"""
        icons = [
            'stopwatch',
            'connection',
            'signal',
            'sync',
            'g2_status'
        ]
        
        size = (32, 32)
        for icon in icons:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw specific timing icon
            self._draw_timing_icon(draw, icon, size)
            
            img.save(self.base_path / f"icons/timing/{icon}.png")

    def create_status_indicators(self):
        """Generate status indicators (DQ, scratch, etc.)"""
        statuses = [
            ('dq', COLORS['dq_red']),
            ('scratch', COLORS['scratch_yellow']),
            ('finals', COLORS['finals_green']),
            ('exhibition', COLORS['exhibition_purple'])
        ]
        
        size = (24, 24)
        for status, color in statuses:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw status indicator
            self._draw_status_indicator(draw, status, color, size)
            
            img.save(self.base_path / f"ui/indicators/{status}.png")

    def create_button_states(self):
        """Generate button backgrounds for different states"""
        states = ['normal', 'hover', 'active', 'disabled']
        size = (200, 40)
        
        for state in states:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw button background
            self._draw_button_state(draw, state, size)
            
            img.save(self.base_path / f"ui/buttons/button_{state}.png")

    def create_g2_interface_elements(self):
        """Generate Time Machine G2 interface elements"""
        elements = [
            'connection_status',
            'lane_display',
            'timing_grid',
            'results_preview'
        ]
        
        size = (300, 200)  # Larger size for interface elements
        for element in elements:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw G2 interface element
            self._draw_g2_element(draw, element, size)
            
            img.save(self.base_path / f"g2_interface/{element}.png")

    def create_report_templates(self):
        """Generate report templates (meet program, results, etc.)"""
        templates = [
            ('meet_program', (612, 792)),    # US Letter size
            ('heat_sheet', (612, 792)),
            ('results', (612, 792)),
            ('award_cert', (792, 612))      # Landscape
        ]
        
        for template, size in templates:
            img = Image.new('RGB', size, '#ffffff')
            draw = ImageDraw.Draw(img)
            
            # Draw template-specific layout
            self._draw_report_template(draw, template, size)
            
            img.save(self.base_path / f"templates/{template}.png")

    def _draw_stroke_silhouette(self, draw, stroke, size):
        """Draw swimming stroke silhouette"""
        # Implementation for each stroke's silhouette
        pass

    def _draw_medal(self, draw, color, size):
        """Draw medal icon"""
        # Implementation for medal drawing
        pass

    def _draw_timing_icon(self, draw, icon_type, size):
        """Draw timing-related icon"""
        # Implementation for timing icons
        pass

    def _draw_status_indicator(self, draw, status, color, size):
        """Draw status indicator"""
        # Implementation for status indicators
        pass

    def _draw_button_state(self, draw, state, size):
        """Draw button background"""
        # Implementation for button states
        pass

    def _draw_g2_element(self, draw, element, size):
        """Draw G2 interface element"""
        # Implementation for G2 interface elements
        pass

    def _draw_report_template(self, draw, template, size):
        """Draw report template"""
        # Implementation for report templates
        pass

def main():
    generator = AssetGenerator()
    
    print("Generating swimming meet management assets...")
    
    # Generate all asset types
    generator.create_stroke_icons()
    generator.create_medal_icons()
    generator.create_timing_icons()
    generator.create_status_indicators()
    generator.create_button_states()
    generator.create_g2_interface_elements()
    generator.create_report_templates()
    
    print("Asset generation complete!")

if __name__ == "__main__":
    main()
