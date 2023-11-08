from pydub import AudioSegment
import os
from moviepy.editor import VideoFileClip

dir_dataset = "/Users/myungeunlee/Desktop/FOS_data"
dir_data = os.path.join(dir_dataset, 'Data')
dir_audio_processed = os.path.join(dir_dataset, 'Audio_processed')

paths_video = []
for root, dirs, files in os.walk(dir_data):
    for file in files:
        if file.endswith(('mp4', 'avi', 'mov', 'MP4', 'AVI', 'MOV')):  
            paths_video.append(os.path.join(root, file))

total_videos = len(paths_video)
print(f"Found {total_videos} video files.")

for index, path_video in enumerate(paths_video):
    video_number = index + 1
    video_name = os.path.basename(path_video)
    relative_path = os.path.relpath(path_video, start=dir_data)
    sub_dir = os.path.dirname(relative_path)
    
    # Make a similar directory structure in 'Audio_processed'
    audio_sub_dir = os.path.join(dir_audio_processed, sub_dir)
    audio_name = os.path.splitext(video_name)[0] + '.wav'
    audio_output_path = os.path.join(audio_sub_dir, audio_name)

    # pass existing folder
    if os.path.exists(audio_output_path):
        print(f"Audio for video {video_number}/{total_videos}: {video_name} already processed. Skipping.")
        continue
    # if there's no directory, create it
    os.makedirs(audio_sub_dir, exist_ok=True)
    print(f"Processing video {video_number}/{total_videos}: {video_name}")

    try:
        video_clip = VideoFileClip(path_video)
        video_clip.audio.write_audiofile(audio_output_path)
        video_clip.close()

        audio_clip = AudioSegment.from_file(audio_output_path)

        segment_length = 10 * 1000  # pydub works in milliseconds
        for i in range(0, len(audio_clip), segment_length):
            start_ms = i
            end_ms = min(i + segment_length, len(audio_clip))
            segment = audio_clip[start_ms:end_ms]
            segment_name = f"{os.path.splitext(audio_name)[0]}_{start_ms//1000}-{end_ms//1000}.mp3"
            segment_path = os.path.join(audio_sub_dir, segment_name)
            if not os.path.exists(segment_path):
                segment.export(segment_path, format="mp3")

        print(f"Processed audio for video: {video_name}, duration: {len(audio_clip)}ms")
    except Exception as e:
        print(f"An error occurred while processing {video_name}: {e}")
