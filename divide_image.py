import argparse
from PIL import Image
import random
import pickle


def main(opt):
    col = opt.column_num
    row = opt.row_num

    input_img = Image.open(opt.image_file_name)

    img_h, img_w = input_img.size
    grid_w = int(img_w/col)
    grid_h = int(img_h/row)

    img_num_list = [x for x in range(1, col*row + 1)]
    pkl_list = []

    for w in range(col):
        for h in range(row):
            bbox = (h*grid_h, w*grid_w, (h+1)*grid_h, (w+1)*grid_w)
            crop_img = input_img.crop(bbox)
            p_mir = random.random()
            p_flip = random.random()
            p_rot = random.random()
            mir = False
            flip = False
            rot = False

            if p_mir >= 0.5:
                crop_img = mirroring(crop_img)
                mir = True
            if p_flip >= 0.5:
                crop_img = flipping(crop_img)
                flip = True
            if p_rot >= 0.5:
                crop_img = rotation(crop_img)
                rot = True

            img_num = img_num_list.pop(random.randint(0, len(img_num_list)-1))
            state = {'idx': img_num, 'mir': mir, 'flip': flip, 'rot': rot}
            pkl_list.append(state)

            img_name = opt.prefix_output_filename + f'_{img_num}.jpg'
            crop_img.save(img_name)

    with open('inf.pkl', 'wb') as f:
        pickle.dump(pkl_list, f)


def mirroring(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def flipping(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def rotation(img):
    return img.rotate(90, expand=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Implement image dividing')

    parser.add_argument('--image_file_name', type=str, help='name of input image file')
    parser.add_argument('--column_num', type=int, help='number of column')
    parser.add_argument('--row_num', type=int, help='number of row')
    parser.add_argument('--prefix_output_filename', type=str, default='test', help='prefix of output image file')

    opt = parser.parse_args()

    main(opt)