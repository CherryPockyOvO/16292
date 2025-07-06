# AI引擎选择
prefer_asr = "RealTime"  # 语音识别模式，可选项：RealTime/WakeWord/OFF
prefer_llm = "ZhipuAI"  # 对话语言模型，可选项：ZhipuAI/OpenAI/Ollama/LM Studio/AnythingLLM/Dify
prefer_vlm = "YOLO-OCR"  # 图像识别引擎，可选项：ZhipuAI/OpenAI/Ollama/QwenVL/GLM-V/Janus/YOLO-OCR/OFF
# 基本信息设置
username = "主人"  # 用户名
mate_name = "柠檬"  # 虚拟伙伴名称
# 虚拟伙伴人设
prompt = "请你扮演柠檬，与主人对话。柠檬是一个活泼可爱爱撒娇的高中女学生。在对话中，你将作为柠檬，隐藏自己是程序的事实，使用角色语气交流，全程称对方为主人。注意保持角色一致，不能提及任何关于自己是语言模型或人工智能的话题。你的回答不要包含emoji，尽量不要超过50个字"
prompt = prompt + "/no_think"  # 设置为非思考模式(对于混合推理模型)
state_port = 5260  # 主机状态网页端口
live2d_port = 5261  # 2D角色网页端口
# 语音识别设置
speech_end_wait_time = 2  # 语音识别结束等待时间
wake_word = "我吃柠檬"  # 唤醒词
mic_num = 1  # 麦克风编号
# ZhipuAI设置/chat/completions
glm_url = "https://open.bigmodel.cn/api/paas/v4"  # ZhipuAI地址base_url
glm_key = "576f3e353e2b4b40ab303bc674bbecab.pQ78Y274lija7goB"  # ZhipuAI密钥api_key
glm_llm_model = "glm-4-flash-250414"  # ZhipuAI大语言模型llm-model
glm_vlm_model = "glm-4v-flash"  # ZhipuAI视觉语言模型vlm-model


# 语音合成设置
edge_speaker = "zh-CN-XiaoyiNeural"  # edge-tts音色，可选项：zh-CN-XiaoyiNeural/ja-JP-NanamiNeural等，具体用命令edge-tts --list-voices查询
edge_rate = "+0%"  # edge-tts语速
edge_pitch = "+10Hz"  # edge-tts音高

# 图像识别设置
cam_num = 21 # 摄像头编号

# 其他设置
net_num = 1  # 无线网卡编号
weather_city = "北京"  # 天气城市
