from base64 import b64encode
from ollama import Client
from rapidocr_openvino import RapidOCR
from function import *

cls_model, det_model, ocr = None, None, None


def glm_4v_cam(question):  # 多模态摄像头画面聊天
    cap = cv2.VideoCapture(cam_num)
    if not cap.isOpened():
        return "无法打开摄像头"
    ret, frame = cap.read()
    cap.release()
    base64_image = encode_image(frame)
    messages = [{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{base64_image}"}}]}]
    vlm_client = OpenAI(base_url=glm_url, api_key=glm_key)
    completion = vlm_client.chat.completions.create(model=glm_vlm_model, messages=messages)
    return completion.choices[0].message.content


def encode_image(image):  # 图片转base64
    _, buffer = cv2.imencode('.png', image)
    return b64encode(buffer).decode('utf-8')

