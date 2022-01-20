import requests
import websocket
import json

import time, os, sys, contextlib

from pydub import AudioSegment
from pydub.playback import play

import pyaudio
import wave

@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


def tts(text, output_file):
    headers = {'accept': 'application/json'}

    params = (('text', text),)

    r = requests.get('http://127.0.0.1:8002/tts', headers=headers, params=params)

    r.raise_for_status()

    with open(output_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192): 
            if chunk: 
                f.write(chunk)


def kaldi(audio_file):
    headers = {'accept': 'application/json'}

    files = {'my_file': open(audio_file, mode='rb')}

    r = requests.post('http://127.0.0.1:8001/stt', files=files)

    r.raise_for_status()
    
    return r.text


def stt(audio_file):
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8080/api/v1/stt")

    with open(audio_file, mode='rb') as f:  
        audio = f.read()
        ws.send_binary(audio)
        result =  ws.recv()

    return json.loads(result)['text']


def play_audio(filename):
    with ignoreStderr():
        sound = AudioSegment.from_wav(filename)
        play(sound)


def record_audio(filename, seconds=None):
    with ignoreStderr():
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')
        sys.stdout.write("\033[F")

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames


        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')
        
        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        sys.stdout.write("\033[F")
