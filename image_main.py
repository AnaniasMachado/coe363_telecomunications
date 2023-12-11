"""
Purpose: Execute the objetive of the project.
"""

import pandas as pd
from pillow_heif import register_heif_opener

from read_media import get_media_addrs
from image_algorithms import apply_png_algorithm, apply_jpeg_algorithm, apply_heic_algorithm
from image_algorithms import calculate_rmse, calculate_psnr, calculate_compression_rate

id_vals = []
rmse_vals = []
psnr_vals = []
cr_vals = []

def add_data(id_val, rmse_val, psnr_val, cr_val):
    id_vals.append(id_val)
    rmse_vals.append(rmse_val)
    psnr_vals.append(psnr_val)
    cr_vals.append(cr_val)

# Prepare path to each cr2 file
dataset_path = "./image_data/"
results_path = "./image_results/"
cr2_files = get_media_addrs(dataset_path, '.cr2')

# Apply each compression algorithm to each image file
for cr2_file in cr2_files:
    apply_png_algorithm(cr2_file)
    apply_jpeg_algorithm(cr2_file)
    apply_heic_algorithm(cr2_file)

# Prepare path to each png, jpeg, heic file
png_files = get_media_addrs(results_path, '.png')
jpeg_files = get_media_addrs(results_path, '.jpeg')
heic_files = get_media_addrs(results_path, '.heic')

# Compute measure RMSE, PSNR and CR
for i in range(len(cr2_files)):
    # Load audio file
    image1 = cr2_files[i]
    image2 = png_files[i]
    image3 = jpeg_files[i]
    image4 = heic_files[i]

    # Calculate error measure for png file
    rmse = calculate_rmse(image1, image2)
    psnr = calculate_psnr(image1, image2)
    compression_rate = calculate_compression_rate(cr2_files[i], png_files[i])

    # Print result for png file
    print('Root Mean Square Error:', rmse)
    print('Peak Signal Noise Ratio:', psnr)
    print('Compression Rate:', compression_rate)
    add_data(i, rmse, psnr, compression_rate)

    # Calculate error measure for jpeg file
    rmse = calculate_rmse(image1, image3)
    psnr = calculate_psnr(image1, image3)
    compression_rate = calculate_compression_rate(cr2_files[i], jpeg_files[i])

    # Print result for jpeg file
    print('Root Mean Square Error:', rmse)
    print('Peak Signal Noise Ratio:', psnr)
    print('Compression Rate:', compression_rate)
    add_data(i, rmse, psnr, compression_rate)

    # Calculate error measure for heic file
    register_heif_opener()
    rmse = calculate_rmse(image1, image4)
    psnr = calculate_psnr(image1, image4)
    compression_rate = calculate_compression_rate(cr2_files[i], heic_files[i])

    # Print result for heic file
    print('Root Mean Square Error:', rmse)
    print('Peak Signal Noise Ratio:', psnr)
    print('Compression Rate:', compression_rate)
    add_data(i, rmse, psnr, compression_rate)

df = pd.DataFrame({'id': id_vals, 'rmse': rmse_vals, 'psnr': psnr_vals, 'compression_rate': cr_vals})
df.to_csv("./csv_results/image_dataframe.csv", index=False)