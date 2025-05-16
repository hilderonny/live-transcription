# live-transcription

Transkription von Audioaufnahmen über das Mikrofon in (nahezu) Echtzeit mit Sprechererkennung.
Basiert auf https://github.com/hilderonny/faster-whisper.

## Installation

1. Dieses Repository klonen
2. [python-3.11.9.zip](python-3.11.9.zip) entpacken und den enthaltenen Unterordner in `./python` umbenennen
3. Python Bibliotheken installieren mit `python\python -m pip install faster-whisper==0.8.0`
4. [cuBLAS.and.cuDNN_CUDA11_win_v4.7z](https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_CUDA11_win_v4.7z) herunterladen und die enthaltenen DLLs nach `python/Lib/site-packages/ctranslate` entpacken
5. [vc_redist.x64.exe](./vc_redist.x64.exe]) bei Bedarf installieren


## Tests

Die Tests sollten vom Stammverzeichnis aus mit `python\python tests\xxxxx.py`aufgerufen werden, damit die relativen Pfadangaben funktionieren.

### [01-mp3-tiny.py](tests/01-mp3-tiny.py)

Transkription einer MP3 Datei mit faster-whisper Modell `tiny`

### [02-von-neumann-sonde.py](tests/02-von-neumann-sonde.py)

Transkription einer durch einen [TTS-Dienst](https://luvvoice.com/de) generierte MP3 Datei mit bekanntem textuellen Inhalt zur Qualitätsbeurteilung.
Die Audioaufzeichnung hat eine Länge von **95 Sekunden**.

Generell scheinen die Modelle keine Schwierigkeiten mit Segmentgrenzen zu haben.

|Modell|Zeit GPU|Zeit CPU|Bemerkungen|
|---|---|---|---|---|
|tiny|2,2s (43,2x)|5,6s (17,0x)|Fachbegriffe undeutlich|
|base|2,8s (33,9x)|9,3s (10,2x)|Segmente stellen Sätze dar, aber sehr ungenau|
|small|4,0s (23,8x)|23,1s (4,1x)|Brauchbar, auch für CPU geeignet|
|medium|7,4s (12,8x)|57,6s (1,6x)|Brauchbar|
|large-v2|10,7s (8,9x)|97,9s (0,97x)|Sehr genau, aber mit CPU zu langsam|
