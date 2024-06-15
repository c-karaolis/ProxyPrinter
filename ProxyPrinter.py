import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

def get_images_from_folder(folder_path):
    # Get list of all image files in the folder
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(supported_formats)]

def create_card_layout_with_images(filename, card_width, card_height, space_between, folder_path):
    # A4 page size in mm
    page_width, page_height = A4
    page_width /= mm
    page_height /= mm

    # Convert page size to points
    page_width_pt, page_height_pt = page_width * mm, page_height * mm

    # Create a new canvas
    c = canvas.Canvas(filename, pagesize=(page_width_pt, page_height_pt))

    c.setStrokeColor(HexColor(guideline_color))
    c.setLineWidth(0)
    # Number of cards per row and column
    cards_per_row = 3
    cards_per_col = 3
    
    no_top_margin_start = page_height - card_height
    normal_top_start = page_height - (page_height - (cards_per_col * card_height + (cards_per_col - 1) * space_between)) / 2 - card_height
    preferred_top_start = normal_top_start
    
    # Initial position
    start_x = (page_width - (cards_per_row * card_width + (cards_per_row - 1) * space_between)) / 2
    # added at the top to save me a side cut
    start_y = preferred_top_start

    # Get images from folder
    image_paths = get_images_from_folder(folder_path)
    image_index = 0

    # Loop through all images and create pages as necessary
    while image_index < len(image_paths):
        # Draw the cards and add images
        for row in range(cards_per_col):
            for col in range(cards_per_row):
                if image_index >= len(image_paths):
                    break
                
                x = start_x + col * (card_width + space_between)
                y = start_y - row * (card_height + space_between)
                
                # Draw card border
                c.rect(x * mm, y * mm, card_width * mm, card_height * mm)
                
                # Add image to card
                image_path = image_paths[image_index]
                img = ImageReader(image_path)
                c.drawImage(img, x * mm, y * mm, width=card_width * mm, height=card_height * mm, preserveAspectRatio=False, anchor='c')
                image_index += 1
            
            # Draw guidelines
            # c.line(x * mm, 0, x * mm, page_height_pt)
            # c.line((x + card_width) * mm, 0, (x + card_width) * mm, page_height_pt)
            # c.line(0, y * mm, page_width_pt, y * mm)
            # removed the top guideline and set the cards to be at the top so I can save me a side cut
            # c.line(0, (y + card_height) * mm, page_width_pt, (y + card_height) * mm)

                if col == 0 or col == cards_per_row - 1:  # Left edge of the first column
                    c.line(x * mm, 0, x * mm, page_height_pt)
                if col == 0 or col == cards_per_row - 1:  # Right edge of the last column
                    c.line((x + card_width) * mm, 0, (x + card_width) * mm, page_height_pt)
                if row == 0:  # Top edge of the first row
                    c.line(0, (y + card_height) * mm, page_width_pt, (y + card_height) * mm)
                if row == cards_per_col - 1:  # Bottom edge of the last row
                    c.line(0, y * mm, page_width_pt, y * mm)
                    
        # Draw outer border guidelines
        c.line(0, start_y * mm, page_width_pt, start_y * mm)
        c.line(0, (start_y - (cards_per_col * card_height + (cards_per_col - 1) * space_between)) * mm, page_width_pt, (start_y - (cards_per_col * card_height + (cards_per_col - 1) * space_between)) * mm)
        c.line(start_x * mm, 0, start_x * mm, page_height_pt)
        c.line((start_x + (cards_per_row * card_width + (cards_per_row - 1) * space_between)) * mm, 0, (start_x + (cards_per_row * card_width + (cards_per_row - 1) * space_between)) * mm, page_height_pt)
        
        # Create a new page if there are more images left
        if image_index < len(image_paths):
            c.showPage()
            c.setStrokeColor(HexColor(guideline_color))
            c.setLineWidth(0)
            start_y = preferred_top_start  # Reset the start_y for new pages

    # Save the PDF
    c.save()

card_width_mm = 63
card_height_mm = 88
space_between_mm = 0.1
guideline_color = '#FF0000'  # Red color

# Folder containing images
folder_path = './proxies/test'

create_card_layout_with_images(f"{folder_path}/proxies.pdf", card_width_mm, card_height_mm, space_between_mm, folder_path)
