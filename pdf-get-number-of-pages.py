import pypdf
import glob
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--glob", default="/home/ec2-user/downloads/1001/**")
args = parser.parse_args()


def get_pdf_page_count(file_path):
    with open(file_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        return len(reader.pages)


def get_image_page_count(file_path):
    with Image.open(file_path) as img:
        return img.n_frames


# Change this to the glob pattern you want to use
total_page_count = 0
for file_path in glob.glob(args.glob, recursive=True):
    try:
        if file_path.lower().endswith('.pdf'):
            page_count = get_pdf_page_count(file_path)
            print(f'{file_path},{page_count}')
        elif file_path.lower().endswith(
            ('.jpeg', '.jpg', '.png', '.tiff', '.tif')):
            page_count = get_image_page_count(file_path)
            print(f'{file_path},{page_count}')
        else:
            print(f'File "{file_path}" is not a supported format.')
            page_count = 0
    except pypdf.errors.EmptyFileError as efe:
        print("emtpy file")
        page_count = 0
    total_page_count += page_count
print(total_page_count)

