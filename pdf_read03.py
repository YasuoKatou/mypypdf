from pathlib import Path
import argparse

from pdf_objects.mypdf import MyPDF

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='my PDF Reader')
    parser.add_argument('--file-path', type=str, help='file path', required=True)
    args = parser.parse_args()

    pdf = MyPDF(args.file_path)
    print(pdf.toString())
#[EOF]