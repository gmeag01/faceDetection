import cv2
from mtcnn_cv2 import MTCNN
import serial
from struct import pack

# mtcnn적용 및 bounding box 생성
def getCoorAndReturn(img):
    coor = detector.detect_faces(image)
    x, y, w, h = coor[0]['box']
    x2, y2 = x+w, y+h
    avg_x, avg_y = int((x+x2)/2), int((y+y2)/2)
    cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 4)

    return avg_x, avg_y

# 초기 변수 설정
detector = MTCNN()
cap = cv2.VideoCapture(cv2.CAP_DSHOW+0)
# cap = cv2.VideoCapture(0)  # 카메라 연결
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)  # 카메라 해상도 조절 (가로)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)  # 카메라 해상도 조절 (세로)

sl = serial.Serial('COM3', 14400, timeout=1)  # 아두이노와 시리얼 통신 연결

# 카메라 확인 및 영상 입력 / 입력된 영상에 mtcnn 적용
if not cap.isOpened : exit()
 
while (cap.isOpened):
    ret, image = cap.read()
    if ret:
        try:
            avg_x, avg_y = getCoorAndReturn(image)
            sl.write(pack('2i', avg_x, avg_y))
            # Print coordinate for serial bus test
            # print(str(sl.readline().decode()))
        except:
            pass

        # serial_read(ser, target_x, target_y)
        cv2.imshow('Image', image)
 
    if cv2.waitKey(30) > 0:
        break

cap.release()
cv2.destroyAllWindows()