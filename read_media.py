"""
Purpose: Read media. Where media can be image or video.
"""

import os

def get_media_addrs(dataset_path, media_format):
    media_addrs = []

    # List all files in the folder
    files = os.listdir(dataset_path)

    # Run for all files in the folder
    for file in files:
        # Checks if the file has a specified format
        media_formats = [media_format]
        if any(file.endswith(file_format) for file_format in media_formats):
            media_addrs.append(dataset_path+file)
    return media_addrs
