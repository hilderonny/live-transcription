# live-transcription

Transkription von Audioaufnahmen über das Mikrofon in (nahezu) Echtzeit mit Sprechererkennung.

## Installation

1. [Python 3.9 Embedded](python-3.9.13-embed-amd64.zip) in Unterordner `python` entpacken
2. Dateien [get-pip.py](get-pip.py) und [python39._pth](python39._pth) in Unterordner `python` kopieren
3. ????? MS Build Tools mit [vs_BuildTools.exe](vs_BuildTools.exe) installieren (Im Installer ist bereits alles notwendig vorausgewählt, 135 MB)

```sh
# PIP installieren
cd python
python ./get-pip.py
# Projektabhängigkeiten installieren
cd ..
# PyTorch mit CUDA 11 Unterstützung
python\python -m pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu118
python\python -m pip install faster-whisper==0.8.0 sounddevice==0.5.1
#python\python -m pip install webrtcvad-wheels==2.0.14
#python\python -m pip install
#python\python -m pip install --force-reinstall ctranslate2==3.24.0
```

4. CUDA-DLLs von https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_CUDA11_win_v4.7z herunterladen und in Verzeichnis `python/Lib/site-packages/ctranslate2` extrahieren

Testen mit

```
python\python test_mp3.py
```

pip install sounddevice numpy faster-whisper resemblyzer torch torchaudio


Mit Python 2.9 bricht die Installation von resemblyzer ab, auch wenn die Build Tools installiert wurden und die Installation aus dem Developer Command Prompt heraus gestartet wurde.