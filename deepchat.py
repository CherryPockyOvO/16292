import subprocess
import re
from threading import Thread
import time
from offline_tts import run_kokoro

exe_path = "./llm_demo"
model_path = "DeepSeek-R1-Distill-Qwen-1.5B_W8A8_RK3588.rkllm"
arg1 = "10000"
arg2 = "10000"
proc = subprocess.Popen([exe_path,model_path,arg1,arg2],  stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

input_access = True

def input_data():
    global proc, input_access
    print("---程序正在启动---")
    while input_access == True:
        text = input()        
        if '退出程序' in text:
            input_access = False
        proc.stdin.write(f"{text}\n")
        proc.stdin.flush()        


def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U00002600-\U000026FF"
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002702-\U000027B0"  
        u"\U0000FE00-\U0000FE0F" 
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

words = ""

def combine():
    global words
    words_last = ""
    while True:
        time.sleep(2)
        #print(words)
        if words != '' and words_last == words:
            print(words)
            if words != 'user:':
                run_kokoro(words)
            words_last = ""
            words = ""
        words_last = words

def chat():
    '''
    global proc, input_access
    Thread(target = input_data, daemon = True).start()
    Thread(target = combine, daemon = True).start()
    global words
    while input_access == True:
        if ch := proc.stdout.read(1):
            ch = remove_emojis(ch)
            words += ch
            print(ch, end='')           
    proc.terminate()
    proc.wait()
    input_access = False
    print("----程序已退出----\n")
    '''

