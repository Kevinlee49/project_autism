from pydub import AudioSegment
import os, re, time, glob
import pandas as pd
import cv2
from moviepy.editor import VideoFileClip

dir_dataset = "/Users/myungeunlee/Desktop/FOS_data/audio_test"
dir_audio_output = os.path.join(dir_dataset, 'Processed_Audio')
if not os.path.exists(dir_audio_output):
    os.makedirs(dir_audio_output)

paths_video = []

for file in os.listdir(dir_dataset):
    if file.endswith(('mp4', 'avi', 'mov', 'MP4', 'AVI', 'MOV')):  
            paths_video.append(os.path.join(dir_dataset, file))

print(f"Found {len(paths_video)} video files.")

for path_video in paths_video:
    try:
        print(f"Processing video {path_video}...") 
        video_name = os.path.basename(path_video)
        print(f"Extracting audio from {video_name}...")

        audio_name = os.path.splitext(video_name)[0] + '.mp3'
        audio_output_path = os.path.join(dir_audio_output, audio_name)

        video_clip = VideoFileClip(path_video)
        video_clip.audio.write_audiofile(audio_output_path)
        video_clip.close()

        audio_clip = AudioSegment.from_file(audio_output_path)
        print(f"Audio loaded for {video_name}, duration: {len(audio_clip)}ms")

        # Cut the audio into 10-second segments and save them
        segment_length = 10 * 1000  # pydub works in milliseconds
        for i in range(0, len(audio_clip), segment_length):
            start_ms = i
            end_ms = min(i + segment_length, len(audio_clip))
            segment = audio_clip[start_ms:end_ms]
            segment_name = f"{os.path.splitext(audio_name)[0]}_{start_ms//1000}-{end_ms//1000}.mp3"
            segment_path = os.path.join(dir_audio_output, segment_name)
            segment.export(segment_path, format="mp3")

        print(f"Processed audio for video: {video_name}")
    except Exception as e:
        print(f"An error occurred while processing {video_name}: {e}")