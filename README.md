# live-transcription

Transkription von Audioaufnahmen über das Mikrofon in (nahezu) Echtzeit mit Sprechererkennung.
Basiert auf https://github.com/hilderonny/faster-whisper.

## Installation

1. Dieses Repository klonen
2. [python-3.10.11.zip](python-3.10.11.zip) entpacken und den enthaltenen Unterordner in `./python` umbenennen
3. Python Bibliotheken installieren mit `python\python -m pip install diart`
4. Auf HuggingFace einen [Token erstellen](https://huggingface.co/settings/tokens)
5. `python\Scripts\huggingface-cli login` ausführen und den Token eintragen
6. `python-3.10.11\python tests\03-diart.py` ausführen

Ergebnis: Geht nicht, es wird eine Rekursionsfehlermeldung ausgegeben. Das passiert, wenn das LazyModule `speechbrain.inference` geladen werden soll.

```
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 172, in ensure_module
    module = super().ensure_module(stacklevel + 1)
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 80, in ensure_module
    importer_frame = inspect.getframeinfo(sys._getframe(stacklevel + 1))
  File "inspect.py", line 1620, in getframeinfo
  File "inspect.py", line 829, in getsourcefile
  File "inspect.py", line 869, in getmodule
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 112, in __getattr__
    return getattr(self.ensure_module(1), attr)
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 172, in ensure_module
    module = super().ensure_module(stacklevel + 1)
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 80, in ensure_module
    importer_frame = inspect.getframeinfo(sys._getframe(stacklevel + 1))
  File "inspect.py", line 1620, in getframeinfo
  File "inspect.py", line 829, in getsourcefile
  File "inspect.py", line 869, in getmodule
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 112, in __getattr__
    return getattr(self.ensure_module(1), attr)
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 172, in ensure_module
    module = super().ensure_module(stacklevel + 1)
  File "C:\github\hilderonny\live-transcription\python-3.10.11\lib\site-packages\speechbrain\utils\importutils.py", line 80, in ensure_module
    importer_frame = inspect.getframeinfo(sys._getframe(stacklevel + 1))
  File "inspect.py", line 1620, in getframeinfo
  File "inspect.py", line 829, in getsourcefile
  File "inspect.py", line 861, in getmodule
  File "inspect.py", line 845, in getabsfile
  File "ntpath.py", line 566, in abspath
  File "ntpath.py", line 512, in normpath
  File "ntpath.py", line 169, in splitdrive
RecursionError: maximum recursion depth exceeded while calling a Python object
```

Versuch mit Conda:

1. Installation von [Miniconda3-latest-Windows-x86_64](Miniconda3-latest-Windows-x86_64) mit Adminsitratorrechten und allen Checkboxen aktiviert
2. `conda env create -f environment.yml`(dauert eine Weile ohne Rückmeldung)
3. `conda activate diart`
4. `diart.stream .\tests\von-neumann-sonde.mp3`- Funktioniert, es wird etwas angezeigt
5. `diart.stream microphone` funktioniert nicht, `sounddevice`bringt eine Fehlermeldung:

```
Traceback (most recent call last):
  File "C:\Users\Ronny\.conda\envs\diart\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\Ronny\.conda\envs\diart\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "C:\Users\Ronny\.conda\envs\diart\Scripts\diart.stream.exe\__main__.py", line 7, in <module>
  File "C:\Users\Ronny\.conda\envs\diart\lib\site-packages\diart\console\stream.py", line 130, in run
    audio_source = src.MicrophoneAudioSource(config.step, device)
  File "C:\Users\Ronny\.conda\envs\diart\lib\site-packages\diart\sources.py", line 172, in __init__
    self._mic_stream = sd.InputStream(
  File "C:\Users\Ronny\.conda\envs\diart\lib\site-packages\sounddevice.py", line 1440, in __init__
    _StreamBase.__init__(self, kind='input', wrap_callback='array',
  File "C:\Users\Ronny\.conda\envs\diart\lib\site-packages\sounddevice.py", line 909, in __init__
    _check(_lib.Pa_OpenStream(self._ptr, iparameters, oparameters,
  File "C:\Users\Ronny\.conda\envs\diart\lib\site-packages\sounddevice.py", line 2794, in _check
    raise PortAudioError(errormsg, err, hosterror_info)
sounddevice.PortAudioError: Error opening InputStream: Unanticipated host error [PaErrorCode -9999]: 'Undefined external error.' [MME error 1]
```

Die Lösung von https://github.com/spatialaudio/python-sounddevice/issues/173#issuecomment-2331978534 hat auch nichts gebracht.

## Nächste Schritte

Als nächste versuche ich mal https://github.com/ggml-org/whisper.cpp, das hat bei Andreas zumindest auf dem Raspberry funktioniert.

## Erkenntnisse

Python 3.10 wird verwendet, weil sich `diart` in der Installationsanleitung darauf bezieht.




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
