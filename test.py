from tkinter import *
import pyautogui as pag
import mediapipe as mp
import threading
import time
import math
import cv2

x8_output = 0
y8_output = 0
x5_output = 0
y5_output = 0
x4_output = 0
y4_output = 0
x6_output = 0
y6_output = 0
x12_output = 0
y12_output = 0

times = 0
drag = False

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pag.FAILSAFE = False


# 根據兩點的座標，計算角度
def vector_2d_angle(v1, v2):
    # 座標
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    #
    # 向量內積求角度
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    # noinspection PyBroadException
    except:
        angle_ = 180
    return angle_


# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []

    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )

    # 判斷手心手背
    # print((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1])))
    # if (round((int(hand_[0][0]) - int(hand_[2][0])), 0)) < 0:
    #     print("現在辨識為手背")
    # else:
    #     print("現在辨識為手心")

    angle_list.append(angle_)

    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)

    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)

    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)

    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)

    # 輸出手指間角度列表
    for num in range(0, 5):
        angle_list[num] = round(angle_list[num], 2)

    # print("手指間角度: " + str(angle_list))
    return angle_list


# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(fingers_angle):
    f1 = fingers_angle[0]  # 大拇指角度
    f2 = fingers_angle[1]  # 食指角度
    f3 = fingers_angle[2]  # 中指角度
    f4 = fingers_angle[3]  # 無名指角度
    f5 = fingers_angle[4]  # 小拇指角度
    # print(finger_angle)
    # 小於 90 表示手指伸直，大於等於 90 表示手指捲縮
    if f1 < 90 and f2 >= 90 and f3 >= 90 and f4 >= 90 and f5 >= 90:
        return 'good'
    elif f1 >= 90 and f2 >= 90 and f3 < 90 and f4 >= 90 and f5 >= 90:
        return 'fuck!!!'
    elif f1 < 90 and f2 < 90 and f3 >= 90 and f4 >= 90 and f5 < 90:
        return 'ROCK!'
    elif f1 >= 90 and f2 >= 90 and f3 >= 90 and f4 >= 90 and f5 >= 90:
        return '0'
    elif f1 >= 90 and f2 >= 90 and f3 >= 90 and f4 >= 90 and f5 < 90:
        return 'pink'
    elif f1 >= 90 and f2 < 90 and f3 >= 90 and f4 >= 90 and f5 >= 90:
        return '1'
    elif f1 >= 90 and f2 < 90 and f3 < 90 and f4 >= 90 and f5 >= 90:
        return '2'
    elif f1 >= 90 and f2 >= 90 and f3 < 90 and f4 < 90 and f5 < 90:
        return 'ok'
    elif f1 < 90 and f2 >= 90 and f3 < 90 and f4 < 90 and f5 < 90:
        return 'ok'
    elif f1 >= 90 and f2 < 90 and f3 < 90 and f4 < 90 and f5 > 90:
        return '3'
    elif f1 >= 90 and f2 < 90 and f3 < 90 and f4 < 90 and f5 < 90:
        return '4'
    elif f1 < 90 and f2 < 90 and f3 < 90 and f4 < 90 and f5 < 90:
        return '5'
    elif f1 < 90 and f2 >= 90 and f3 >= 90 and f4 >= 90 and f5 < 90:
        return '6'
    elif f1 < 90 and f2 < 90 and f3 >= 90 and f4 >= 90 and f5 >= 90:
        return '7'
    elif f1 < 90 and f2 < 90 and f3 < 90 and f4 >= 90 and f5 >= 90:
        return '8'
    elif f1 < 90 and f2 < 90 and f3 < 90 and f4 < 90 and f5 >= 90:
        return '9'
    else:
        return ''


def click(x1, x2, y1, y2):
    length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    # print(length)
    if length < 80:
        pag.click(clicks=1, button='left')


def right_click(x1, x2, y1, y2):
    length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    # print(length)
    if length < 70:
        pag.click(clicks=1, button='right')


def mouse_left_drag(x1, x2, y1, y2):
    global drag
    length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    print(length)
    if length < 50 and drag == False:
        drag = True
        pag.mouseDown()

    if length > 50 and drag == True:
        drag = False
        pag.mouseUp()


cap = cv2.VideoCapture(0)  # 讀取攝影機
fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
lineType = cv2.LINE_AA  # 印出文字的邊框
pTime = 0  # 開始時間初始化
cTime = 0  # 目前時間初始化


def virtual_mouse():
    # mediapipe 啟用偵測手掌
    with mp_hands.Hands(
            max_num_hands=2,  # 偵測手掌數量
            model_complexity=1,  # 模型複雜度
            min_detection_confidence=0.6,  # 最小偵測自信度
            min_tracking_confidence=0.6) as hands:  # 最小追蹤自信度

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        w, h = 640, 480  # 影像尺寸 width:640, height:480

        while True:
            global pTime
            global times
            ret, img = cap.read()
            img = cv2.resize(img, (w, h))  # 縮小尺寸，加快處理效率

            if not ret:
                print("Cannot receive frame")
                break

            # 影像翻轉
            img = cv2.flip(img, 1)

            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
            results = hands.process(img2)  # 偵測手勢

            # for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # for hand_landmarks in results.multi_hand_landmarks:

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    finger_points = []  # 記錄手指節點座標的串列

                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x * w
                        y = i.y * h

                        x8 = hand_landmarks.landmark[8].x * 1920  # 取得食指前端 X座標
                        y8 = hand_landmarks.landmark[8].y * 1080  # 取得食指前端 Y座標
                        x5 = hand_landmarks.landmark[5].x * 1920  # 取得食指前端 X座標
                        y5 = hand_landmarks.landmark[5].y * 1080  # 取得食指前端 Y座標
                        x4 = hand_landmarks.landmark[4].x * 1920  # 取得食指前端 X座標
                        y4 = hand_landmarks.landmark[4].y * 1080  # 取得食指前端 Y座標
                        x6 = hand_landmarks.landmark[6].x * 1920  # 取得食指第三端點 X座標
                        y6 = hand_landmarks.landmark[6].y * 1080  # 取得食指第三端點 Y座標
                        x12 = hand_landmarks.landmark[12].x * 1920  # 取得中指前端 X座標
                        y12 = hand_landmarks.landmark[12].y * 1080  # 取得中指前端 Y座標

                        finger_points.append((x, y))

                    finger_angle = hand_angle(finger_points)  # 計算手指角度，回傳長度為 5 的串列
                    # print(finger_angle)  # 印出角度

                    text = hand_pos(finger_angle)  # 取得手勢所回傳的內容

                    # print("斜率: " + str(m))
                    x8_output = round(x8, 0)
                    y8_output = round(y8, 0)
                    x5_output = round(x5, 0)
                    y5_output = round(y5, 0)
                    x4_output = round(x4, 0)
                    y4_output = round(y4, 0)
                    x6_output = round(x6, 0)
                    y6_output = round(y6, 0)

                    if finger_points and handedness.classification[0].label[0:] == 'Right':
                        thread1 = threading.Thread(target=pag.moveTo, args=(x8_output, y8_output))
                        thread1.start()
                        thread3 = threading.Thread(target=mouse_left_drag,
                                                   args=(x4_output, x8_output, y4_output, y8_output))
                        thread3.start()
                        thread4 = threading.Thread(target=right_click,
                                                   args=(x8_output, x12_output, y8_output, y12_output))
                        thread4.start()
                    if finger_points and handedness.classification[0].label[0:] == 'Right' and times % 6 == 0:
                        # length = math.sqrt((x6_output - x4_output)**2 + (y6_output - y4_output)**2)
                        # print(length)
                        thread2 = threading.Thread(target=click, args=(x4_output, x6_output, y4_output, y6_output))
                        thread2.start()
                        #
                        # thread3 = threading.Thread(target=window.mainloop())
                        # thread3.start()

                    # print(pag.position())

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 將節點和骨架繪製到影像中
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            # 將幀率顯示在影像上
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (600, 30), fontFace, 1, (0, 255, 0), 2, lineType)

            cv2.imshow('finger_recognition', img)

            times += 1

            # window.mainloop()
            # thread3 = threading.Thread(target=window.mainloop())
            # thread3.start()
            # 按下esc結束程式
            if cv2.waitKey(1) & 0xFF == 27:
                break


thread = threading.Thread(target=virtual_mouse)
thread.start()


def click_one():
    window.destroy()
    call(["python", "實驗.py"])


window = Tk()
window.geometry("1350x700")
window.geometry("+100+50")
window.resizable(width=0, height=0)
background = PhotoImage(file="D:/Python project/Ai_virtual_mouse_project/background4.png")
bg_label = Label(window,
                 image=background,
                 compound='bottom')
bg_label.pack()
button_left = Button(window,
                     width=10,
                     height=2,
                     text="遊戲1",
                     command=click_one,
                     font=('標楷體', 30),
                     fg="#BA55D3",
                     bg="#FFDAB9",
                     activeforeground="#800080",
                     activebackground="#FFEBCD"
                     )
button_left.place(x=20, y=450)

window.mainloop()

cap.release()
cv2.destroyAllWindows()
