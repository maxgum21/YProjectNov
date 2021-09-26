import pyaudio  # Для скачивания требуется устанавливать через pipwin
import wave


def musPlayer(number):
    musfile = wave.open(f"SoundUse//Sound{number}.wav", 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(musfile.getsampwidth()),
                    channels=musfile.getnchannels(),
                    rate=musfile.getframerate(), output=True)
    data = musfile.readframes(1024)
    while data:
        stream.write(data)
        data = musfile.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()


def musChanger(number, filename):
    chosen_file = wave.open(filename, mode="rb")
    new_custom = wave.open(f"SoundUse//Sound{number}.wav", mode="wb")
    new_custom.setparams(chosen_file.getparams())
    new_custom.writeframes(chosen_file.readframes(chosen_file.getnframes()))
    chosen_file.close()
    new_custom.close()


def musReset():
    for i in range(16):
        chosen_file = wave.open(f"SoundsBase/Sound{i + 1}.wav", mode="rb")
        new_custom = wave.open(f"SoundUse/Sound{i + 1}.wav", mode="wb")

        new_custom.setparams(chosen_file.getparams())
        new_custom.writeframes(chosen_file.readframes(chosen_file.getnframes()))
        chosen_file.close()
        new_custom.close()


def musPlayer_r(number):
    source = wave.open(f"SoundUse//Sound{number}.wav", 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(source.getsampwidth()),
                    channels=source.getnchannels(),
                    rate=source.getframerate(), output=True)
    data = source.readframes(1024)
    newdata = []
    while data:
        newdata.append(data)
        data = source.readframes(1024)

    for part in newdata[::-1]:
        if newdata[::-1].index(part) == 0:
            data = part
        else:
            data += part
    for i in range(0, len(data), 1024):
        stream.write(data[i:i + 1024])
    stream.stop_stream()
    stream.close()
    p.terminate()


def musPlayer_2x(number):
    source = wave.open(f"SoundUse//Sound{number}.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(source.getsampwidth()),
                    channels=source.getnchannels(),
                    rate=source.getframerate(), output=True)
    data = source.readframes(1024)
    newdata = []
    while data:
        newdata.append(data)
        data = source.readframes(1024)

    for part in newdata[::2]:
        if newdata[::-1].index(part) == 0:
            data = part
        else:
            data += part
    for i in range(0, len(data), 1024):
        stream.write(data[i:i + 1024])
    stream.stop_stream()
    stream.close()
    p.terminate()