# faster-whisper

Dieses Repository dient als funktionsfähige Grundlage für Anwendungen, die auf [faster-whisper](https://github.com/SYSTRAN/faster-whisper) basieren.

## Installation

1. Dieses Repository klonen
2. [python-3.11.9.zip](python-3.11.9.zip) entpacken und den enthaltenen Unterordner in `./python` umbenennen
3. Python Bibliotheken installieren mit `python\python -m pip install faster-whisper==0.8.0`
4. [cuBLAS.and.cuDNN_CUDA11_win_v4.7z](https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_CUDA11_win_v4.7z) herunterladen und die enthaltenen DLLs nach `python/Lib/site-packages/ctranslate` entpacken
5. [vc_redist.x64.exe](./vc_redist.x64.exe]) bei Bedarf installieren

Ausprobieren geht so, dabei wird beim ersten Aufruf das `tiny` Modell heruntergeladen (ca. 75 MB):

```cmd
python\python test.py
```

Bei Erfolg sollte die Datei `test.mp3` transkribiert und der Text angezeigt werden.

```
Importing faster_whisper ...
Loading faster_whisper ...
Transcribing with device cuda ...
Estimating duration from bitrate, this may be inaccurate
Detected language "ru" with probability 0.988281
[0.00s -> 6.32s]  Шторы решают массу вопросов. Закрыться от посторонних глаз, от света и даже от
[6.32s -> 11.68s]  сквозняка. Но главная задача это создать в доме уют и комфорт. Только четыре дня
[11.68s -> 17.68s]  с 30 марта до 2 апреля в ДК Рыбакоп. Большая выставка-ярмарка из города Иваново в
[17.68s -> 20.60s]  магазине Марго.
Duration: 0:00:03.670486
```

## Bemerkungen

1. Python-Pakete sollten mit `.\python\python -m pip install ...` installiert werden, da die `pip.exe` aufgrund falscher Bezüge zur Python-Installation nicht vorhanden ist.
2. Es wird Python 3.11 verwendet, weil faster-whisper 0.8.0 mit dieser Version am Besten funktioniert. Hier müssen keine abhängigen Pakete neu kompiliert werden.
3. Es wird faster-whisper in der Version 0.8.0 verwendet, weil die darin enthaltene `ctranslate2` Bibliothek in der Version 3.24.0 enthalten ist, welches problemlos mit CUDA 11 und CDNN 8 funktioniert. CUDA 12 oder CDNN 9 habe ich mit faster-whisper nicht zum Laufen bekommen.
3. In dieser Kombination (Python 3.11 und faster-whisper 0.8.0) funktioniert auch PyTorch mit CUDA-Erweiterung, wenn neben faster-whisper auch andere KNNs verwendet werden sollen, die auf torch oder transformers basieren.