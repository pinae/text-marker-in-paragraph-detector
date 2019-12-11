#!/usr/bin/python3
# -*- coding: utf-8 -*-
from skimage.draw import rectangle
from PIL import Image
import numpy as np
import random
import cairo
from wand.image import Image as WImage


def area_mask(arr, mask_rect):
    rr, cc = rectangle(start=mask_rect[0:2], end=mask_rect[2:4], shape=arr.shape)
    msk = np.zeros(arr.shape[:2], dtype=np.uint8)
    msk[rr, cc] = 255
    msk = np.stack([msk, msk, msk, np.ones(arr.shape[:2], dtype=np.uint8) * 255], axis=2)
    return np.minimum(arr, msk)


def apply_marker(c, mask_rect):
    c.set_source_rgba(0, random.gauss(0.95, 0.05), random.gauss(0.75, 0.05), random.gauss(0.35, 0.1))
    c.set_line_width(min(41, random.gauss(41, 20)))
    mask_width = mask_rect[3] - mask_rect[1]
    mask_height = mask_rect[2] - mask_rect[0]
    x_variance_proportion = 0.2
    y_variance = 45
    bezier_dist_proportion = 0.1
    start_x = round(random.gauss(mask_rect[1] + 0.5 * mask_width, x_variance_proportion * mask_width))
    while mask_rect[1] + 10 > start_x > mask_rect[3] - 10:
        start_x = round(random.gauss(mask_rect[1] + 0.5 * mask_width, x_variance_proportion * mask_width))
    start_y = round(random.gauss(mask_rect[0] + min(0.1 * mask_height, 15), y_variance))
    bezier_start_y_dist = round(random.gauss(mask_height * bezier_dist_proportion,
                                             mask_height * bezier_dist_proportion * 0.5))
    bezier_start_x = round(random.gauss(start_x, bezier_start_y_dist * 0.5))
    bezier_start_y = start_y + bezier_start_y_dist
    end_x = round(random.gauss(start_x, bezier_dist_proportion * mask_width))
    end_y = round(random.gauss(mask_rect[2] - min(0.1 * mask_height, 15), y_variance))
    bezier_end_y_dist = round(random.gauss(mask_height * bezier_dist_proportion,
                                           mask_height * bezier_dist_proportion * 0.5))
    bezier_end_x = round(random.gauss(end_x, bezier_end_y_dist * 0.5))
    bezier_end_y = end_y - bezier_end_y_dist
    c.move_to(start_x, start_y)
    c.curve_to(bezier_start_x, bezier_start_y,
               bezier_end_x, bezier_end_y,
               end_x, end_y)
    c.stroke()
    if random.random() < 0.5:
        if random.random() < 0.2:
            c.set_line_width(min(41, random.gauss(41, 20)))
        c.move_to(start_x, start_y)
        c.line_to((start_x + bezier_start_x) // 2, (start_y + bezier_start_y) // 2)
        c.stroke()
    if random.random() < 0.5:
        if random.random() < 0.2:
            c.set_line_width(min(41, random.gauss(41, 20)))
        c.move_to(start_x, start_y)
        c.curve_to((start_x + bezier_start_x) // 2, (start_y + bezier_start_y) // 2,
                   bezier_start_x, bezier_start_y,
                   (start_x + bezier_start_x) // 2, (start_y + bezier_start_y) // 2)
        c.stroke()
    if random.random() < 0.5:
        c.set_source_rgba(1, 1, 1, 1)
        c.set_line_width(41)
        c.move_to(start_x-max(1, round(random.gauss(41/2, 10))), start_y)
        c.curve_to(bezier_start_x-max(1, round(random.gauss(41/2, 10))), bezier_start_y,
                   bezier_end_x-max(1, round(random.gauss(41/2, 10))), bezier_end_y,
                   end_x-max(1, round(random.gauss(41/2, 10))), end_y)
        c.stroke()
    return c


def convert_to_numpy(surf):
    converted_array = np.array(surf.get_data())
    converted_array = converted_array.reshape((surf.get_height(), surf.get_width(), 4))
    converted_array = np.stack([
        converted_array[:, :, 2],
        converted_array[:, :, 1],
        converted_array[:, :, 0],
        converted_array[:, :, 3]
    ], axis=2)
    return converted_array


def extract_pdf_page(filename, page_no=0):
    wimg = WImage(filename=filename + '[' + str(page_no) + ']', resolution=100)
    nparr = np.array(wimg)
    return nparr.reshape([nparr.shape[1], nparr.shape[0], *nparr.shape[2:]])


def compress_and_write_image(arr, fp):
    rgba_img = Image.fromarray(arr, 'RGBA')
    background = Image.new("RGB", rgba_img.size, (255, 255, 255))
    background.paste(rgba_img, mask=rgba_img.split()[3])
    background.save(fp, format='JPEG', quality=83)


if __name__ == '__main__':
    img = Image.open("dataset/without_marker/20191205142548420_0001.jpg")
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, img.width, img.height)
    c = cairo.Context(surface)
    c.set_source_rgb(1, 1, 1)
    c.paint()
    m_rect = 1725, 702, 1999, 1193
    apply_marker(c, m_rect)
    img_array = np.array(img, dtype=np.uint8)
    img_alpha = np.ones((*img_array.shape[:2], 1), dtype=np.uint8) * 255
    a = np.concatenate([img_array, img_alpha], axis=2)
    b = convert_to_numpy(surface)
    mix = np.minimum(a, b)
    mix = area_mask(mix, m_rect)
    final_image = Image.fromarray(mix, 'RGBA')
    final_image = final_image.crop((m_rect[1]-100, m_rect[0]-100, m_rect[3]+100, m_rect[2]+100))
    final_image.show("marked image")
