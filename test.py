"""
Purpose: Test code.
"""

import ffmpeg

def video_to_vp9(input_file, output_file):
    ffmpeg.input(input_file).output(output_file, codec='libvpx-vp9').run()

# Exemplo de uso
input_file = "video_data/AncientThought_s000.265"
output_file = "video_vp9.webm"
video_to_vp9(input_file, output_file)