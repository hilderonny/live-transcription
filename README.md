# live-transcription

Transkription von Audioaufnahmen über das Mikrofon in (nahezu) Echtzeit mit Sprechererkennung.
Basiert auf https://github.com/hilderonny/faster-whisper.

## Installation

1. Dieses Repository klonen
2. [python-3.11.9.zip](python-3.11.9.zip) entpacken und den enthaltenen Unterordner in `./python` umbenennen
3. Python Bibliotheken installieren mit `python\python -m pip install faster-whisper==0.8.0`
4. [cuBLAS.and.cuDNN_CUDA11_win_v4.7z](https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_CUDA11_win_v4.7z) herunterladen und die enthaltenen DLLs nach `python/Lib/site-packages/ctranslate` entpacken
5. [vc_redist.x64.exe](./vc_redist.x64.exe]) bei Bedarf installieren

## Nächste Schritte

**diart** und **pyannote** erscheinen mir vielversprechend.
Die **pyannote** Modelle lassen sich Offline laden, ohne dass man die Online-Lizenzabfrage machen muss.
Ich sollte mal die Demo von [speaker aware transcription](https://medium.com/better-programming/color-your-captions-streamlining-live-transcriptions-with-diart-and-openais-whisper-6203350234ef) zum Laufen bringen und im Browser einfach mal ein Talkrundenvideo laufen lassen und dieses mit dem Mikrofon aufnehmen. Mal sehen, wie schnell und genau die Sprecheridentifizierung und Transkription funktioniert.

## Erkenntnisse

Mit faster-whisper 0.8.0 kann man die Segmentiertung nicht beeinflussen. Version 1.1.1 hat mehr Funktionen, zum Beispiel auch die segmentweise Spracherkennung.

Ebenso benötigt die Erkennung der Sprache relativ viel Zeit. Daher sollte beim Verarbeiten kleiner Audioschnipsel nicht jedesmal die Sprache erkannt werden, sondern nur zu Beginn der Aufnahme. Oder ich zeige eine Selektbox mit Sprachen an, deren Änderung sich sofort auf den nächsten Chunk auswirkt.

Ich bräuchte vor faster-whisper eine Segmentierung, etwa durch silero VAD. Das kann ruhig sehr empfindlich eingestellt sein, ich möchte halt nur nicht, dass die Audioschnipsel genau in einem Wort unterbrechen.

Kann ich die Sprecheridentifizierung mit pyannote.audio verwenden, um Segmente für faster-whisper vorzubereiten?

- [sounddevice callback streams](https://python-sounddevice.readthedocs.io/en/0.5.1/usage.html#callback-streams)
- [pyannote diarization mopdel](https://huggingface.co/pyannote/speaker-diarization-3.1)
- [silero VAD examples](https://github.com/snakers4/silero-vad/wiki/Examples-and-Dependencies#dependencies)
- [diart audio stream processing](https://github.com/juanmc2005/diart)
- [speaker aware transcription](https://medium.com/better-programming/color-your-captions-streamlining-live-transcriptions-with-diart-and-openais-whisper-6203350234ef)
- https://huggingface.co/pyannote/segmentation
- https://huggingface.co/pyannote/embedding

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
