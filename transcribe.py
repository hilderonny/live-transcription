# Live Transkription mit Sprechertrennung und Sprachekennung
# ------------------------------------------------------------
# Dieses Projekt erfasst Sprache direkt vom Mikrofon, verarbeitet sie in einem Sliding-Window-Verfahren,
# trennt verschiedene Sprecher (mittels resemblyzer), erkennt automatisch die Sprache und transkribiert
# satzweise mit faster-whisper.

import sounddevice as sd
import queue
import numpy as np
import threading
# from resemblyzer import VoiceEncoder, preprocess_wav
from faster_whisper import WhisperModel
import time
from datetime import datetime
import os

# -------------------- KONFIGURATION --------------------
SAMPLE_RATE = 16000            # Whisper-Modell erwartet 16kHz
WINDOW_SIZE = 8                # Analysefenster in Sekunden
STEP_SIZE = 2                  # Schrittweite des Sliding-Windows (Overlap = WINDOW_SIZE - STEP_SIZE)
DEVICE = "cuda"                # Oder "cpu", falls keine GPU vorhanden
MODEL_SIZE = "large-v2"         # faster-whisper Modell (tiny, base, small, medium, large-v3)
BEAM_SIZE = 5                  # für bessere Qualität bei der Transkription

# -------------------- INITIALISIERUNG --------------------
audio_q = queue.Queue()
# voice_encoder = VoiceEncoder()
whisper_model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type = "int8", download_root="./data/faster-whisper/")
speaker_profiles = []  # Liste gespeicherter Sprecher-Embeddings
speaker_ids = []       # Zugeordnete Sprecher-IDs zu Profilen
speaker_counter = 1

# -------------------- AUDIO CALLBACK --------------------
def audio_callback(indata, frames, time, status):
    if status:
        print("Audio Callback Status:", status)
    audio_q.put(indata.copy())

# -------------------- AUDIO VERARBEITUNG --------------------
def audio_collector():
    buffer = np.zeros((0, 1), dtype=np.float32)
    while True:
        data = audio_q.get()
        buffer = np.concatenate((buffer, data), axis=0)

        if len(buffer) >= SAMPLE_RATE * WINDOW_SIZE:
            segment = buffer[-SAMPLE_RATE * WINDOW_SIZE:].copy()
            threading.Thread(target=process_segment, args=(segment,)).start()
            buffer = buffer[SAMPLE_RATE * STEP_SIZE:]  # Sliding-Window Schritt

# -------------------- SPRECHER-ZUORDNUNG --------------------
def identify_speaker(audio_segment):
    global speaker_counter
    wav = audio_segment.flatten()
    try:
        embedding = voice_encoder.embed_utterance(wav)
    except Exception as e:
        print("Embedding Error:", e)
        return "unknown"

    if not speaker_profiles:
        speaker_profiles.append(embedding)
        speaker_ids.append(f"Speaker {speaker_counter}")
        speaker_counter += 1
        return speaker_ids[-1]

    similarities = [np.inner(embedding, ref) for ref in speaker_profiles]
    best_idx = int(np.argmax(similarities))
    if similarities[best_idx] > 0.75:
        return speaker_ids[best_idx]
    else:
        speaker_profiles.append(embedding)
        speaker_ids.append(f"Speaker {speaker_counter}")
        speaker_counter += 1
        return speaker_ids[-1]

# -------------------- TRANSKRIPTION --------------------
def process_segment(audio_segment):
    # audio_fp32 = audio_segment.T.astype(np.float32)
    audio_fp32 = audio_segment.flatten().astype(np.float32)
    # speaker = identify_speaker(audio_segment)

    try:
        segments, info = whisper_model.transcribe(audio_fp32, beam_size=BEAM_SIZE, language=None)
    except Exception as e:
        print("Whisper Error:", e)
        return

    language = info.language
    timestamp = datetime.now().strftime("%H:%M:%S")
    for segment in segments:
        text = segment.text.strip()
        if text and text[-1] in ".!?":
            start = segment.start
            end = segment.end
            # print(f"[{timestamp}] [{speaker}] [{language}] {start:.2f}-{end:.2f}s: {text}")
            print(f"[{timestamp}] [] [{language}] {start:.2f}-{end:.2f}s: {text}")

# -------------------- MAIN --------------------
def main():
    print("Starte Live-Transkription mit Sprechererkennung...")
    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', callback=audio_callback)
    with stream:
        collector_thread = threading.Thread(target=audio_collector)
        collector_thread.daemon = True
        collector_thread.start()
        input("\nDrücke Enter zum Beenden...\n")

if __name__ == "__main__":
    main()
