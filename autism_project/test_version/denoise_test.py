import os
import torch
import torchaudio
from denoiser.denoiser.pretrained import dns64
from denoiser.denoiser.audio import Audioset
from pathlib import Path
from torchaudio import save as save_audio
from tqdm import tqdm

model = dns64()
audio_dir = Path("/Users/myungeunlee/Desktop/FOS_data/audio_test/Processed_Audio/Converted_to_WAV")
audio_files = list(audio_dir.glob("*.wav"))

dataset = Audioset(files=[(str(file), None) for file in audio_files],
                   length=None, 
                   stride=None,
                   pad=False,
                   with_path=True)  

model.eval()

denoised_audio_dir = audio_dir / 'denoised_with_orinialSR'
os.makedirs(denoised_audio_dir, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
# print(device)

downsample_resampler = torchaudio.transforms.Resample(orig_freq=44100, new_freq=16000)
upsample_resampler = torchaudio.transforms.Resample(orig_freq=16000, new_freq=44100)

for i in tqdm(range(len(dataset)), total=len(dataset), unit="file"):
    result = dataset[i]
    if result is None:
        print(f"Skipping file at index {i}: cannot load.")
        continue

    audio_tensor, file_path = result

    audio_tensor = downsample_resampler(audio_tensor)

    if audio_tensor.shape[0] == 2:  # convert 2 channel audio to mono
        audio_tensor = audio_tensor.mean(dim=0, keepdim=True)

    audio_tensor = audio_tensor.unsqueeze(0).to(device)

    with torch.no_grad():
        denoised_tensor = model(audio_tensor)

    denoised_tensor = upsample_resampler(denoised_tensor)
    denoised_tensor = denoised_tensor.squeeze(0).cpu()

    save_path = denoised_audio_dir / f"denoised_with_orinialSR_{Path(file_path).stem}.wav"
    save_audio(save_path, denoised_tensor, 44100)
