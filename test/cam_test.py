

import cv2

# 选择摄像头索引（0=默认，1=外接摄像头1，2=外接摄像头2...）
camera_index = 21  # 修改此处切换设备

# 打开摄像头
cap = cv2.VideoCapture(camera_index)

# 检查是否成功打开
if not cap.isOpened():
    print(f"❌ 无法打开索引为 {camera_index} 的摄像头")
    exit()

# 实时显示视频流
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ 帧读取失败，可能摄像头断开")
            break
        
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 q 退出
            break
finally:
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
