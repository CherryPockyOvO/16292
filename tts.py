import asyncio
import os
import time
import edge_tts
import librosa
import requests as rq
import soundfile as sf
import numpy as np
from threading import Thread
from kokoro_onnx import Kokoro
from misaki import zh
from config import *
from openai import OpenAI

playing_flag = False
voice_path = 'data/cache/cache_voice'
wav_path = 'data/cache/cache_voice.wav'
kokoro = None
g2p = zh.ZHG2P() 

def play_live2d():  # 播放Live2D对口型
    try:
        path = voice_path
        x, sr = librosa.load(path, sr = 8000)
        x = x - min(x)
        x = x / max(x)
        eps = 1e-6 
        x = np.log(x + eps) + 1  
        x = x / max(x) * 1.2
        s_time = time.time()
        for _ in range(int(len(x) / 800)):
            it = x[int((time.time() - s_time) * 8000) + 1]
            if it < 0:
                it = 0
            with open("data/cache/cache.txt", "w") as cache_file:
                cache_file.write(str(float(it)))
            time.sleep(0.1)
    except:
        pass
    time.sleep(0.1)
    with open("data/cache/cache.txt", "w") as cache_file:
        cache_file.write("0")
            
def play_voice(path):  # 播放语音
    Thread(target=play_live2d).start()
    os.system('pkill "play"')
    os.system('./play.sh') 

def play_tts(text):  # 语音合成
    print('merge')
    async def ms_edge_tts():  # 使用edge_tts进行文本到语音的转换并保存到文件
        communicate = edge_tts.Communicate(text, voice=edge_speaker, rate=edge_rate, pitch=edge_pitch)
        await communicate.save(voice_path)
    text = text.split("</think>")[-1].strip()
    asyncio.run(ms_edge_tts())
    print("tts ok!")
    play_voice(voice_path)

def run_kokoro(text):  # 本地Kokoro-TTS
    global kokoro
    model_path = "data/model/TTS/Kokoro-82M/kokoro-v1.0.fp16.onnx"
    voice_list_path = "data/model/TTS/Kokoro-82M/voices-v1.0.bin"
    if kokoro is None:
        kokoro = Kokoro(model_path, voice_list_path)
    phonemes, _ = g2p(text)
    samples, sample_rate = kokoro.create(text=phonemes, voice="zf_xiaoyi", speed=0.8, is_phonemes=True)
    sf.write(wav_path, samples, sample_rate)
