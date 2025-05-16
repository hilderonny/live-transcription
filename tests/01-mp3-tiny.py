import os
import datetime

print('Importing faster_whisper ...')

from faster_whisper import WhisperModel

print('Loading faster_whisper ...')

device = 'cuda' # 'cpu'
file_path = 'tests/russisch.mp3'
model = 'tiny'

faster_whisper_model = WhisperModel( model_size_or_path = model, device = device, compute_type = 'int8', download_root='./data/faster-whisper/' )
faster_whisper_model_version = os.listdir('./data/faster-whisper/models--guillaumekln--faster-whisper-' + model + '/snapshots')[0]

print('Transcribing with device %s ...' % (device))

start_time = datetime.datetime.utcnow()

segments, info = faster_whisper_model.transcribe(file_path, task = 'transcribe')

stop_time = datetime.datetime.utcnow()
duration = stop_time - start_time

print('Detected language "%s" with probability %f' % (info.language, info.language_probability))

for segment in segments:
    print('[%.2fs -> %.2fs] %s' % (segment.start, segment.end, segment.text))

print('Duration: %s' % (duration))