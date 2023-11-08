import torch
import torchaudio
from denoiser.denoiser.pretrained import dns64
from pathlib import Path
from torchaudio import save as save_audio
from tqdm import tqdm

model = dns64(pretrained=True)
audio_dir = Path("/Users/myungeunlee/Desktop/FOS_data/Audio_processed_wav")
denoised_audio_dir = Path("/Users/myungeunlee/Desktop/FOS_data/Denoised_Audio_processed")
denoised_audio_dir.mkdir(exist_ok=True)

model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

downsample_resampler = torchaudio.transforms.Resample(orig_freq=44100, new_freq=16000)
upsample_resampler = torchaudio.transforms.Resample(orig_freq=16000, new_freq=44100)

total_files = sum(1 for _ in audio_dir.rglob("*.wav"))
pbar = tqdm(total=total_files, desc="Overall progress", unit="file")

for audio_path in audio_dir.rglob("*.wav"):
    relative_path = audio_path.relative_to(audio_dir)
    person_out_folder = denoised_audio_dir / relative_path.parent
    person_out_folder.mkdir(parents=True, exist_ok=True)

    audio_tensor, _ = torchaudio.load(audio_path)
    audio_tensor = downsample_resampler(audio_tensor)

    if audio_tensor.shape[0] == 2:  # 2채널 오디오를 모노로 변환
        audio_tensor = audio_tensor.mean(dim=0, keepdim=True)

    audio_tensor = audio_tensor.unsqueeze(0).to(device)

    with torch.no_grad():
        denoised_tensor = model(audio_tensor)

    denoised_tensor = upsample_resampler(denoised_tensor.squeeze(0)).cpu()

    save_path = person_out_folder / f"denoised_{audio_path.name}"
    save_audio(save_path, denoised_tensor, 44100)

    pbar.update(1)

pbar.close()
