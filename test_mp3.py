# Faster Whisper laden
model = 'tiny'
device = 'cuda'

from faster_whisper import WhisperModel

faster_whisper_model = WhisperModel( model_size_or_path = model, device = device, compute_type = "int8", download_root="./data/faster-whisper/" )

transcribe_segments_generator, transcribe_info = faster_whisper_model.transcribe('audio.mp3', task = "transcribe")
transcribe_segments = list(map(lambda segment: { "start": segment.start, "end": segment.end, "text": segment.text }, transcribe_segments_generator))
transcribe_full_text  =" ".join(map(lambda segment: segment["text"], transcribe_segments))
print(transcribe_info.language, transcribe_segments)