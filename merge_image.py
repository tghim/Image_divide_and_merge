import argparse
import pickle
from PIL import Image


def main(opt):
    col = opt.column_num
    row = opt.row_num
    img_num = col*row

    with open('inf.pkl', 'rb') as f:
        pkl_list = pickle.load(f)

    for i in range(img_num):
        freg_name = opt.input_filename_prefix + '_' + str(pkl_list[i]['idx']) + '.jpg'
        freg_img = Image.open(freg_name)

        if pkl_list[i]['rot'] == True:
            freg_img = rotation(freg_img)
        if pkl_list[i]['flip'] == True:
            freg_img = flipping(freg_img)
        if pkl_list[i]['mir'] == True:
            freg_img = mirroring(freg_img)

        img_h, img_w = freg_img.size

        if i == 0:
            merged_img = Image.new('RGB', (row*img_h, col*img_w))

        col_itr = i // row
        row_itr = i % row

        merged_img.paste(freg_img, (row_itr*img_h, col_itr*img_w))

    merged_img.save(opt.output_filename)


def mirroring(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def flipping(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def rotation(img):
    return img.rotate(270, expand=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Implement image merging')

    parser.add_argument('--input_filename_prefix', type=str, default='test', help='prefix of input image file')
    parser.add_argument('--column_num', type=int, help='number of column')
    parser.add_argument('--row_num', type=int, help='number of row')
    parser.add_argument('--output_filename', type=str, default='output.jpg', help='name of output image file')

    opt = parser.parse_args()

    main(opt)