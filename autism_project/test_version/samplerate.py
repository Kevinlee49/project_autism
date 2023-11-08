import torchaudio
from torchaudio.transforms import Resample
import os

# 오디오 파일의 경로를 지정합니다.
audio_folder_path = '/Users/myungeunlee/Desktop/FOS_data/audio_test/Processed_Audio/Converted_to_WAV'

# Iterate over all files in the folder
for audio_file in os.listdir(audio_folder_path):
    file_path = os.path.join(audio_folder_path, audio_file)
    # Check if the file is an audio file
    if file_path.lower().endswith(('.wav', '.mp3')):
        try:
            # Load the audio file
            waveform, sample_rate = torchaudio.load(file_path)
            print(f"File: {audio_file}, Sample Rate: {sample_rate}")
        except Exception as e:
            # If loading the audio file failed, print the error
            print(f"Failed to load {audio_file}: {e}")

