######################## Only for test audio file #########################

# from pydub import AudioSegment
# import os
# from pathlib import Path

# dir_audio_output = Path("/Users/myungeunlee/Desktop/FOS_data/audio_test/Processed_Audio")

# dir_wav_output = dir_audio_output / 'Converted_to_WAV'
# os.makedirs(dir_wav_output, exist_ok=True)

# for mp3_file in dir_audio_output.glob("*.mp3"):
#     audio_clip = AudioSegment.from_file(mp3_file)
    
#     wav_file_name = mp3_file.stem + ".wav"
#     wav_file_path = dir_wav_output / wav_file_name
    
#     audio_clip.export(wav_file_path, format="wav")

#     print(f"Converted {mp3_file.name} to WAV and saved as {wav_file_name}")

######################## For all mp3 audio file #########################

from pydub import AudioSegment
import os
from pathlib import Path
from tqdm import tqdm

dir_all_audio_input = Path("/Users/myungeunlee/Desktop/FOS_data/Audio_processed")
dir_wav_output = dir_all_audio_input / 'Audio_processed_wav'
os.makedirs(dir_wav_output, exist_ok=True)

total_files = sum(1 for _ in dir_all_audio_input.rglob("*.mp3"))

with tqdm(total=total_files, unit="file", desc="Converting mp3 to wav") as pbar:
    for mp3_file in dir_all_audio_input.rglob("*.mp3"):
        relative_path = mp3_file.relative_to(dir_all_audio_input)
        wav_file_path = dir_wav_output / relative_path.with_suffix('.wav')
        
        if not wav_file_path.exists():
            wav_file_path.parent.mkdir(parents=True, exist_ok=True)  # 해당 폴더 생성
            audio_clip = AudioSegment.from_file(mp3_file)
            audio_clip.export(wav_file_path, format="wav")
            # print(f"Converted {mp3_file.name} to WAV and saved as {wav_file_path}")
        else:
            print(f"WAV file for {mp3_file.name} already exists. Skipping.")
        
        pbar.update(1)


