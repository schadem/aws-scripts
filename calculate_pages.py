import os
import pypdf
import csv
from PIL import Image


def get_pdf_page_count(file_path):
    with open(file_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        return len(reader.pages)


def get_image_page_count(file_path):
    with Image.open(file_path) as img:
        return img.n_frames

def calculate_pages(directory):
    if not os.path.exists(directory):
        print("The provided directory doesn't exist")
        return

    with open("folder_count.csv", 'w') as output_csv:
        csv_writer = csv.writer(output_csv)
        root_pages = dict()
        for root, dirs, files in os.walk(directory):
            page_count = 0
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if file_path.lower().endswith('.pdf'):
                        page_count += get_pdf_page_count(file_path)
                    elif file_path.lower().endswith(
                        ('.jpeg', '.jpg', '.png', '.tiff', '.tif')):
                        page_count += get_image_page_count(file_path)
                    else:
                        pass
                except pypdf.errors.EmptyFileError as efe:
                    pass
            root_pages[root] = page_count
            print([root,len(files),page_count])
            csv_writer.writerow([root,len(files),page_count])


directory = "/home/ec2-user/downloads/arxiv-pdfs/"
calculate_pages(directory)
