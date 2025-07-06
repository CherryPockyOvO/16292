import pygame 
import os
import pyaudio
FORMAT = pyaudio.paInt16  # 16位深度
CHANNELS = 2  # 单声道
RATE = 48000  # 采样率
CHUNK = 1024  # 每个缓冲区的帧数
p = pyaudio.PyAudio()


