"""
Purpose: Store the algorithms used in the project.
"""

import os
import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener
import ffmpeg

# Function to apply the PNG algorithm to a image
def apply_png_algorithm(image_file, optimize=True):
    output_file = "./image_results/" + image_file.split("/")[2][:-4] + ".png"

    # Converts image to format PIL
    pil_image = Image.open(image_file)

    # Saves image in the PNG format (the algorithm is applied automatically)
    pil_image.save(output_file, format="PNG", optimize=optimize)

# Function to apply the JPEG algorithm to a image
def apply_jpeg_algorithm(image_file, quality=85):
    output_file = "./image_results/" + image_file.split("/")[2][:-4] + ".jpeg"

    # Converts image to format PIL
    pil_image = Image.open(image_file)

    # Saves image in the JPEG format (the algorithm is applied automatically)
    pil_image.save(output_file, format="JPEG", quality=quality)

# Function to apply the HEIC algorithm to a image
def apply_heic_algorithm(image_file, quality=85):
    output_file = "./image_results/" + image_file.split("/")[2][:-4] + ".heic"

    register_heif_opener()

    # Converts image to format PIL
    pil_image = Image.open(image_file)

    # Saves image in the HEIC format (the algorithm is applied automatically)
    pil_image.save(output_file, quality=quality)

def convert_video_to_vp9(input_file, output_file):
    ffmpeg.input(input_file).output(output_file, codec='libvpx-vp9').run()

def convert_video_to_av1(input_file, output_file):
    ffmpeg.input(input_file).output(output_file, codec='libaom-av1').run()

def convert_video_to_mp4(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()

def calculate_rmse(image1, image2):
    # Converts image to format PIL
    pil_image1 = Image.open(image1)
    pil_image2 = Image.open(image2)

    # Converts from PIL to Numpy Array
    array1 = np.array(pil_image1)
    array2 = np.array(pil_image2)

    mse = np.mean((array1 - array2) ** 2)
    rmse = np.sqrt(mse)
    return rmse

def calculate_psnr(image1, image2):
    # Converts image to format PIL
    pil_image1 = Image.open(image1)
    pil_image2 = Image.open(image2)

    # Converts from PIL to Numpy Array
    array1 = np.array(pil_image1)
    array2 = np.array(pil_image2)

    max_value = 2**16 - 1  # Valor máximo para uma amostra de áudio de 16 bits
    mse = np.mean((array1 - array2) ** 2)
    psnr = 10 * np.log10((max_value ** 2) / mse)
    return psnr

def calculate_compression_rate(file1, file2):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    rate = size1 / size2
    return rate