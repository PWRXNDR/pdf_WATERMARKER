import os
import PyPDF2


def get_directory_input(prompt):
    while True:
        directory = input(prompt)
        if os.path.isdir(directory):
            return directory
        else:
            print("Invalid directory. Please enter a valid path.")


def get_watermark_file(directory):
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            return os.path.join(directory, file)
    return None


def watermark_pdf(watermark_path, input_dir, output_dir):
    watermark_reader = PyPDF2.PdfReader(watermark_path)
    output_pdf = PyPDF2.PdfWriter()

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(input_dir, filename)
            with open(input_pdf_path, 'rb') as pdf:
                source_reader = PyPDF2.PdfReader(pdf)

                for page_num in range(len(source_reader.pages)):
                    page = source_reader.pages[page_num]
                    watermark_page = watermark_reader.pages[min(page_num, len(watermark_reader.pages)-1)]
                    page.merge_page(watermark_page)
                    output_pdf.add_page(page)

            output_pdf_file_path = os.path.join(output_dir, f"watermarked_{filename}")
            with open(output_pdf_file_path, 'wb') as output_pdf_file:
                output_pdf.write(output_pdf_file)
                print(f"Watermarked {filename} successfully.")


def main():
    print("Welcome to the PDF Watermarker!")
    watermark_dir = get_directory_input("Enter the directory path for your watermark PDF (leave blank for default): ")
    watermark_file = get_watermark_file(watermark_dir) if watermark_dir else 'default_watermark.pdf'
    if not watermark_file:
        print("No valid watermark PDF found. Exiting...")
        return

    input_dir = get_directory_input("Enter the directory path of PDFs to be watermarked: ")
    output_dir = get_directory_input("Enter the directory path for saving watermarked PDFs: ")
    os.makedirs(output_dir, exist_ok=True)

    watermark_pdf(watermark_file, input_dir, output_dir)
    print("All PDFs have been watermarked successfully.")


if __name__ == "__main__":
    main()
