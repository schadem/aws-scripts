import pypdf
import glob
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--glob", default="/home/ec2-user/downloads/1001")
args = parser.parse_args()


def get_pdf_page_count(file_path):
    with open(file_path, 'rb') as f:
        reader = pypdf.PdfFileReader(f)
        return reader.numPages


def get_image_page_count(file_path):
    with Image.open(file_path) as img:
        return img.n_frames


# Change this to the glob pattern you want to use

for file_path in glob.glob(args.glob):
    if file_path.lower().endswith('.pdf'):
        page_count = get_pdf_page_count(file_path)
        print(f'PDF file "{file_path}" has {page_count} pages.')
    elif file_path.lower().endswith(
        ('.jpeg', '.jpg', '.png', '.tiff', '.tif')):
        page_count = get_image_page_count(file_path)
        print(f'Image file "{file_path}" has {page_count} pages or frames.')
    else:
        print(f'File "{file_path}" is not a supported format.')
