"""
Purpose: Execute the objetive of the project.
"""

import pandas as pd

from read_media import get_media_addrs
from video_algorithms import convert_video_to_vp9, convert_video_to_av1, convert_video_to_mp4
from video_algorithms import calculate_ssim, calculate_rmse
from video_algorithms import calculate_psnr, calculate_compression_rate

id_vals = []
ssim_vals = []
rmse_vals = []
psnr_vals = []
cr_vals = []

def add_data(id_val, ssim_val, rmse_val, psnr_val, cr_val):
    id_vals.append(id_val)
    ssim_vals.append(ssim_val)
    rmse_vals.append(rmse_val)
    psnr_vals.append(psnr_val)
    cr_vals.append(cr_val)

# Prepare path to each x265 file
dataset_path = "./video_data/"
results_path = "./video_results/"
x265_files = get_media_addrs(dataset_path, '.265')

# Apply each compression algorithm to each video file
# for x265_file in x265_files:
#     convert_video_to_vp9(x265_file)
#     convert_video_to_av1(x265_file)
#     convert_video_to_mp4(x265_file)

# Prepare path to each png, jpeg, heic file
av1_files = get_media_addrs(results_path, '.mkv')
mp4_files = get_media_addrs(results_path, '.mp4')
vp9_files = get_media_addrs(results_path, '.webm')

# Compute measure SSIM, RMSE, PSNR and CR
for i in range(len(x265_files)):
    # Load audio file
    video1 = x265_files[i]
    video2 = av1_files[i]
    video3 = mp4_files[i]
    video4 = vp9_files[i]

    # Calculate error measure for av1 file
    ssim = calculate_ssim(video1, video2)
    rmse = calculate_rmse(video1, video2)
    psnr = calculate_psnr(video1, video2)
    compression_rate = calculate_compression_rate(x265_files[i], av1_files[i])

    # Print result for av1 file
    print('Structural Similarity Index Measure:', ssim)
    print('Root Mean Square Error:', rmse)
    print('Peak Signal Noise Ratio:', psnr)
    print('Compression Rate:', compression_rate)
    add_data(i, ssim, rmse, psnr, compression_rate)

    # Calculate error measure for mp4 file
    ssim = calculate_ssim(video1, video3)
    rmse = calculate_rmse(video1, video3)
    psnr = calculate_psnr(video1, video3)
    compression_rate = calculate_compression_rate(x265_files[i], mp4_files[i])

    # Print result for mp4 file
    print('Structural Similarity Index Measure:', ssim)
    print('Root Mean Square Error:', rmse)
    print('Peak Signal Noise Ratio:', psnr)
    print('Compression Rate:', compression_rate)
    add_data(i, ssim, rmse, psnr, compression_rate)

    # Calculate error measure for vp9 file
    ssim = calculate_ssim(video1, video4)
    rmse = calculate_rmse(video1, video4)
    psnr = calculate_psnr(video1, video4)
    compression_rate = calculate_compression_rate(x265_files[i], vp9_files[i])

    # Print result for vp9 file
    print('Structural Similarity Index Measure:', ssim)
    print('Root Mean Square Error:', rmse)
    print('Peak Signal Noise Ratio:', psnr)
    print('Compression Rate:', compression_rate)
    add_data(i, ssim, rmse, psnr, compression_rate)

df = pd.DataFrame({'id': id_vals, 'ssim': ssim_vals, 'rmse': rmse_vals, 'psnr': psnr_vals, 'compression_rate': cr_vals})
df.to_csv("./csv_results/video_dataframe.csv", index=False)