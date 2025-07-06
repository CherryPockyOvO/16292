import json
from datetime import datetime
from vlm import *
import os
with open('data/db/memory.db', 'r', encoding='utf-8') as memory_file:
    try:
        openai_history = json.load(memory_file)
    except:
        openai_history = []

def current_time():  # 当前时间
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def chat_llm(msg):  # 与大语言模型对话
    glm_client = OpenAI(base_url=glm_url, api_key=glm_key)
    openai_history.append({"role": "user", "content": msg})
    messages = [{"role": "system", "content": prompt}]
    messages.extend(openai_history)
    completion = glm_client.chat.completions.create(model=glm_llm_model, messages=messages)
    openai_history.append({"role": "assistant", "content": completion.choices[0].message.content})
    return completion.choices[0].message.content

def chat_preprocess(msg):  # 对话预处理
    try:
        global changeplay_flag
        if "几点" in msg or "多少点" in msg or "时间" in msg or "时候" in msg:
            msg = f"[当前时间:{current_time()}]{msg}"
        if "哈喽" in msg:
            res = f"{username}，我是{mate_name}，很高兴遇见你"
        elif ("画面" in msg or "图像" in msg or "看到" in msg or "看见" in msg or "照片" in msg or "摄像头" in msg or "图片" in msg) and prefer_vlm != "OFF":
            res = glm_4v_cam(msg)
            #res =yolo_ocr_cam(msg)
        elif "天气" in msg:
            res = get_weather()
        elif "切换模式" in msg:
            res = switch_asr_mode()
        elif "新闻" in msg:
            res = get_news(msg)
        elif "联网" in msg or "连网" in msg or "搜索" in msg or "查询" in msg or "查找" in msg:
            res = ol_search(msg)
        elif "信号" in msg or "强度" in msg:
            res = get_wifi_info()
        elif "网址" in msg or "地址" in msg or "端口" in msg:
            res = get_lan_url()
        elif "网络" in msg:
            res = get_net_info()
        elif "录入人脸" in msg:
            res = input_face(msg)
        elif "删除人脸" in msg:
            res = delete_face()
        elif "我是谁" in msg:
            res = recog_face()
        elif "切换" in msg and "语音" in msg:
            res = switch_asr_mode()
        elif "确认删除记忆" in msg or "确定删除记忆" in msg:
            res = clear_chat()
        elif "确定退出" in msg or "确认退出" in msg:
            exit_app()
            return
        elif "确认重新启动" in msg or "确定重新启动" in msg:
            reboot()
            return
        elif "确认关机" in msg or "确定关机" in msg:
            shutdown()
            return
        elif "停止播放" in msg:
            os.system('pkill "play"')
            return
        else:
            res = chat_llm(msg)
        with open('data/db/memory.db', 'w', encoding='utf-8') as f:
            json.dump(openai_history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        res = f"服务异常：{e}"
    try:
        res = res.replace("#", "").replace("*", "")
    except Exception as e:
        print(f"服务异常：{e}")
    print(f"{mate_name}：{res}")
    play_tts(res)

def clear_chat():  # 删除记忆
    global openai_history
    openai_history = []
    with open('data/db/memory.db', 'w', encoding='utf-8') as f:
        f.write("")
    return "记忆已清空"
