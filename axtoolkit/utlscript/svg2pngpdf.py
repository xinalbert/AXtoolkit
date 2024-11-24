import sys
from ..base_tools.file_tools import FileTools
import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# 使用 Pillow 来加载并保存 SVG 图片，Matplotlib 支持显示图像
from PIL import Image


def svg2pdf(svg_path, pdf_path):
    img_ = Image.open(svg_path)
    plt.imshow(img_)
    plt.axis('off')
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def draw2png(svg_path, png_file):
    img_ = Image.open(svg_path)
    plt.imshow(img_)
    plt.axis('off')
    plt.savefig(png_file, bbox_inches='tight', pad_inches=0)
    plt.close()
    



def main():
    if len(sys.argv) < 3:
        print("Usage: python image_tools.py svg_file pdf_file|png_file")
        sys.exit()
    svg_file = sys.argv[1]
    for extension_i in ['pdf', 'png']:
        out_file = FileTools.replace_extension(svg_file, extension_i)
        if extension_i == 'pdf':
            svg2pdf(svg_file, out_file)
        else:
            svg2png(svg_file, out_file)

if __name__ == '__main__':
    main()
