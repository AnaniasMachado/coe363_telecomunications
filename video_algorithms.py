"""
Purpose: Store the algorithms used in the project.
"""

import os
import numpy as np
import ffmpeg
import cv2
from skimage.metrics import structural_similarity

def convert_video_to_vp9(input_file):
    output_file = "./video_results/" + input_file.split("/")[2][:-4] + ".webm"
    ffmpeg.input(input_file).output(output_file, codec='libvpx-vp9').run()

def convert_video_to_av1(input_file):
    output_file = "./video_results/" + input_file.split("/")[2][:-4] + ".mkv"
    ffmpeg.input(input_file).output(output_file, acodec='libaom-av1').run()

def convert_video_to_mp4(input_file):
    output_file = "./video_results/" + input_file.split("/")[2][:-4] + ".mp4"
    ffmpeg.input(input_file).output(output_file).run()

def video_to_np_array(video):
    # Opens video using OpenCV
    cap = cv2.VideoCapture(video)

    # Verify if video was opened successfully
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        exit()

    # Initialize a list to store video frames as Numpy Arrays
    frames = []

    # Loop to read all video frames
    while True:
        # Read next video frame
        ret, frame = cap.read()

        # Verify if frame was read correctly
        if not ret:
            break

        # Converts frame to Numpy Array
        frame = np.array(frame)

        # Adds frame to list of frames
        frames.append(frame)

    # Realeases video capture object
    cap.release()

    # Converts list of frames to a 3 dimensional Numpy Array
    video_array = np.array(frames)
    return video_array

def calculate_ssim(video1, video2):
    # Opens videos using OpenCV
    video1_capture = cv2.VideoCapture(video1)
    video2_capture = cv2.VideoCapture(video2)

    # Initialize variables to calculate SSIM
    total_ssim = 0
    frames = 0

    # Loop to proccess each video frame
    while True:
        # Read a frame of each video
        ret1, frame1 = video1_capture.read()
        ret2, frame2 = video2_capture.read()
        
        # Verify if some video ended
        if not ret1 or not ret2:
            break
        
        # Converts the frames of to gray scale
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculates SSIM between frames
        ssim = structural_similarity(frame1_gray, frame2_gray, multichannel=True)
        
        # Adds SSIM to total SSIM and increments counter of frames
        total_ssim += ssim
        frames += 1

    # Calculates mean of SSIM
    mean_ssim = total_ssim / frames
    return mean_ssim

def calculate_rmse(video1, video2):
    # Converts video to Numpy Array
    array1 = video_to_np_array(video1)
    array2 = video_to_np_array(video2)

    mse = np.mean((array1 - array2) ** 2)
    rmse = np.sqrt(mse)
    return rmse

def calculate_psnr(video1, video2):
    # Converts video to Numpy Array
    array1 = video_to_np_array(video1)
    array2 = video_to_np_array(video2)

    max_value = 2**16 - 1  # Valor máximo para uma amostra de áudio de 16 bits
    mse = np.mean((array1 - array2) ** 2)
    psnr = 10 * np.log10((max_value ** 2) / mse)
    return psnr

def calculate_compression_rate(file1, file2):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    rate = size1 / size2
    return rate