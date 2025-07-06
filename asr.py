import wave
import pyaudio
import numpy as np
from funasr_onnx import SenseVoiceSmall
from config import speech_end_wait_time, mic_num
FORMAT = pyaudio.paInt16  # 16位深度
import os
CHANNELS = 2  # 单声道
RATE = 48000  # 采样率
CHUNK = 1024  # 每个缓冲区的帧数
SILENCE_DURATION = speech_end_wait_time  # 静音持续时间，单位秒
SILENCE_CHUNKS = SILENCE_DURATION * RATE / CHUNK  # 静音持续的帧数
p = pyaudio.PyAudio()
voice_flag = 0


try:
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=mic_num,frames_per_buffer=CHUNK)
    voice_flag = 1
    print("麦克风开启成功！")
   # os.system('bash ./clear.sh')
except Exception as e:
    print(f"麦克风配置错误，错误详情：{e}")	
    p.terminate()

cache_path = "data/cache/cache_record.wav"
model = SenseVoiceSmall("data/model/ASR/sensevoice-small-onnx-quant", batch_size=10, quantize=True)

def rms(data, eps=1e-10):
    if len(data) == 0:  # 空数据检查
        return 0.0
    samples = np.frombuffer(data, dtype=np.int16).astype(np.float64)
    if np.all(samples == 0):  # 全静音片段
        return 0.0
    squared = np.square(samples)  # 比**2更高效
    return np.sqrt(np.mean(squared) + eps)  # 加ε防负数

# 通用dBFS转换
def dbfs(rms_value, bit_depth=16):
    if rms_value <= 0:  # 静音保护
        return -np.inf  # 或返回自定义最小值如-120
    ref_value = 2 ** (bit_depth - 1)  # 动态参考值
    return 20 * np.log10(rms_value / ref_value)

def record_audio():  # 录音
    frames = []
    recording = True
    silence_counter = 0  # 用于记录静音持续的帧数
    while recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        current_rms = rms(data)
        current_dbfs = dbfs(current_rms)
#        print(current_dbfs)
        if current_dbfs < -40:
            silence_counter += 1  # 增加静音计数
            if silence_counter > SILENCE_CHUNKS:  # 判断是否达到设定的静音持续时间
                recording = False
        else:
            silence_counter = 0  # 重置静音计数
    return b''.join(frames)

def recognize_audio(audiodata):  # 保存录音到临时文件
    with wave.open(cache_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audiodata)
    with wave.open(cache_path, 'rb') as wf:
        n_frames = wf.getnframes()
        duration = n_frames / RATE
    if duration < SILENCE_DURATION + 0.5:
        return ""
    res = model(cache_path, language="auto", use_itn=False)
    # 提取语种、情感、事件和文本结果
    info = res[0].split('<|')[1:]  # 分割文本信息
    emotion = info[1].split('|>')[0]  # 情感
    event = info[2].split('|>')[0]  # 事件
    text = info[3].split('}')[0].split('|>')[1]  # 文本结果
    emotion_dict = {"HAPPY": "[开心]", "SAD": "[伤心]", "ANGRY": "[愤怒]", "DISGUSTED": "[厌恶]",
                    "SURPRISED": "[惊讶]", "NEUTRAL": "", "EMO_UNKNOWN": ""}
    event_dict = {"BGM": "[背景音乐]", "Applause": "[鼓掌]", "Laughter": "[大笑]", "Cry": "[哭]",
                  "Sneeze": "[打喷嚏]", "Cough": "[咳嗽]", "Breath": "[深呼吸]", "Speech": "", "Event_UNK": ""}
    emotion = emotion_dict.get(emotion, emotion)
    event = event_dict.get(event, event)
    result = event + text + emotion
    return result
