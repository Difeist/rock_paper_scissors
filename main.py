# Import library
import cv2
import mediapipe as mp
import math

org = (50, 50)
fontScale = 1
color = (0, 255, 0)
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX


cap = cv2.VideoCapture(1)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

status = 1
status_1 = 1
status_2 = 1
# Создаем цикл

while True:
    rep, image = cap.read()
    image = cv2.flip(image, 1)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(w * lm.x), int(h * lm.y)
                if id == 6:
                    ax, ay = cx, cy
                elif id == 5:
                    bx, by = cx, cy
                elif id == 10:
                    dx, dy = cx, cy
                elif id == 4:
                    px, py = cx, cy
                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
            cv2.circle(image, (ax, ay), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(image, (bx, by), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(image, (dx, dy), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(image, (px,py), 10, (184, 22, 58), cv2.FILLED)

            AB = (bx - ax, by - ay)
            DB = (bx - dx, by - dy)
            PA = (ax - px, ay - py)

            scy = (AB[0] * DB[0]) + (AB[1] * DB[1])
            scy_1 = (AB[0] * PA[0]) + (AB[1] * PA[1])

            lenAB = math.sqrt(AB[0] ** 2 + AB[1] ** 2)
            lenDB = math.sqrt(DB[0] ** 2 + DB[1] ** 2)
            lenPA = math.sqrt(PA[0] ** 2 + PA[1] ** 2)

            cosABD = scy / (lenAB * lenDB)
            cosPAA = scy_1 / (lenAB * lenPA)

            angle_rad = math.acos(cosABD)
            angle = (180 / math.pi) * angle_rad

            angle_rad_1 = math.acos(cosPAA)
            angle_1 = (180 / math.pi) * angle_rad_1

            print(angle_1)

            if int(angle) > 40:
                status = 0
                status_2 = 2 
            else:
                status = 1
            if int(angle_1) < 80:
                status_1 = 0
                status = 1
            else:
                status_1 = 2
        if status == 0:
            image = cv2.putText(image,'scissors gesture', org, font, fontScale, color, thickness, cv2.LINE_AA)
        if angle < 25:
            image = cv2.putText(image, 'scissors paper', org, font, fontScale, color, thickness, cv2.LINE_AA)
        if status_1 == 0:
            image = cv2.putText(image, 'scissors rock', org, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow('Angle', image)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()