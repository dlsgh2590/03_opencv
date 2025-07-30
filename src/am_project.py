import cv2  
import os  
import numpy as np 
import matplotlib.pylab as plt 

# ========== 1. 웹캠으로 사진 촬영 ==========
cap = cv2.VideoCapture(0)  # 0번 웹캠(기본 카메라)을 킴

# 카메라로 찍을 사진의 크기를 가로 640, 세로 480으로 정함
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 사진을 저장할 파일 경로와 이름을 정함
img_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "img", "capture_histogram.png"))

print("'s'키를 누르면 사진이 찍히고 저장됩니다.")  # 안내 문구 보여주기
print("'q'키를 누르면 종료됩니다.")

if cap.isOpened():  # 카메라가 잘 켜졌는지 확인함
    while True:  # 계속 반복하면서 화면을 보여줌
        ret, frame = cap.read()  # 카메라에서 사진 한 장을 가져오기
        if ret:  # 사진을 제대로 받았는지 확인함
            cv2.imshow('Webcam - Press s to Save', frame)  # 화면에 사진 보여주기
            key = cv2.waitKey(1) & 0xFF  # 키보드에서 누른 키를 확인함

            # 만약 's' 키를 누르면
            if key == ord('s'):
                cv2.imwrite(img_filename, frame)  # 사진을 파일로 저장함
                print(f"Saved image to {img_filename}")  # 저장된 경로를 출력함
                break  # 반복을 멈추고 다음 단계로 넘어감

            # 만약 'q' 키를 누르면
            elif key == ord('q'):
                print("저장하지 않음.")
                cap.release()  # 카메라를 끄고
                cv2.destroyAllWindows()  # 열려 있는 창들을 닫고
                exit()  # 프로그램을 끝냄
        else:
            print("사진을 못 받음.")
            break
else:
    print("카메라가 안 켜짐")
    exit()

cap.release()  # 카메라를 끄고
cv2.destroyAllWindows()  # 화면 창 닫기

# ========== 2. 저장된 이미지 읽기 및 출력 ==========
img = cv2.imread(img_filename)  # 아까 저장한 사진을 다시 불러옴
if img is None:  # 사진이 잘 불러와졌는지 확인함
    print("이미지 파일을 불러오지 못함.")  # 실패했으면 알려줌
    exit()

cv2.imshow('Captured Image', img)  # 불러온 사진을 화면에 보여줌

# ========== 3. RGB 색상별 히스토그램 계산 및 출력 ==========
channels = cv2.split(img)  # 사진을 파랑, 초록, 빨강 색으로 나누기
colors = ('b', 'g', 'r')

plt.title('Color Histogram')
for ch, color in zip(channels, colors):
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256]) 
    plt.plot(hist, color=color)
    plt.xlim([0, 256])

plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.grid(True) 
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows() 