import requests
import json
from pathlib import Path
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# JWT token
auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk0MDU1NDMsImlhdCI6MTY5OTM4Mzk0MywianRpIjoiMHJZUjY3TTNLUlZ0QWczUEVrVmsiLCJwbGFuIjoiYmFzaWMiLCJzY29wZSI6InNwZWVjaCIsInN1YiI6ImpxT3lmcUVzQjJueEtISGNPcTZHIiwidWMiOmZhbHNlfQ.m3H3fJv-ZXgJx_ofZ_P1n53bar1CQ7SWR_770r1RMCA' 
headers = {'Authorization': f'Bearer {auth_token}'}
audio_dir = Path("/Users/myungeunlee/Desktop/FOS_data/Audio_processed_wav")
transcribe_results = {}

# 이미 전사가 완료된 파일들의 리스트를 관리하는 파일
completed_transcriptions_path = audio_dir / 'completed_transcriptions.json'
if completed_transcriptions_path.exists():
    with open(completed_transcriptions_path, 'r', encoding='utf-8') as f:
        completed_transcriptions = json.load(f)
else:
    completed_transcriptions = {}

transcribe_results = {}

# Configuration for the transcription request
config = {
    "use_diarization": True,
    "diarization": {
        "spk_count": 2
    },
    "use_paragraph_splitter": True,
    "paragraph_splitter": {
        "max": 50
    }
}

# Function to request transcription and return result
def request_transcription(audio_file):
    with open(audio_file, 'rb') as f:
        files = {'file': f}
        data = {'config': json.dumps(config)}
        response = requests.post(
            'https://openapi.vito.ai/v1/transcribe',
            headers=headers,
            data=data,
            files=files
        )
        return response, audio_file

# Function to poll for a single transcription result
def poll_transcription(transcribe_id, file_name):
    while True:
        response = requests.get(f'https://openapi.vito.ai/v1/transcribe/{transcribe_id}', headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'completed':
                return result, file_name, 'completed'
            elif result['status'] == 'failed':
                return None, file_name, 'failed'
        time.sleep(5)  # Pause for 5 seconds before the next poll

# Set up a ThreadPoolExecutor for concurrent requests
executor = ThreadPoolExecutor(max_workers=10)

# Request transcription for each audio file with progress tracking
with tqdm(total=len(list(audio_dir.rglob('*.wav'))), desc="Requesting transcription", unit="file") as pbar_request:
    transcription_tasks = {executor.submit(request_transcription, audio_file): audio_file for audio_file in audio_dir.rglob('*.wav')}
    for future in as_completed(transcription_tasks):
        response, audio_file = future.result()
        pbar_request.update(1)
        if response.status_code == 200:
            transcribe_id = response.json()['id']
            transcribe_results[transcribe_id] = audio_file.name

# Poll for results with progress tracking
with tqdm(total=len(transcribe_results), desc="Polling results", unit="file") as pbar_poll:
    polling_tasks = {executor.submit(poll_transcription, transcribe_id, file_name): transcribe_id for transcribe_id, file_name in transcribe_results.items()}
    for future in as_completed(polling_tasks):
        result, file_name, status = future.result()
        pbar_poll.update(1)
        if status == 'completed':
            utterances = result['results'].get('utterances', [])
            transcribed_text = " ".join(u['msg'] for u in utterances)
            completed_transcriptions[file_name] = transcribed_text
        elif status == 'failed':
            completed_transcriptions[file_name] = "Failed to transcribe"

# Save the transcription texts to a JSON file
with open(completed_transcriptions_path, 'w', encoding='utf-8') as f:
    json.dump(completed_transcriptions, f, ensure_ascii=False, indent=4)

print(f"Transcription texts saved to {completed_transcriptions_path}")