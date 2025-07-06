import subprocess
import re
from threading import Thread
#from asr import recognize_audio, record_audio, voice_flag
import time
from deepchat import chat

def start_offline():
    chat()
    print("off")
