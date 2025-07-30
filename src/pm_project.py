import cv2
import os
import numpy as np
import matplotlib.pylab as plt

# ========== 1. 웹캠으로 사진 촬영 ==========
cap = cv2.VideoCapture(0)

# 해상도 설정 (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 파일 경로 설정
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "img"))
os.makedirs(base_dir, exist_ok=True)
full_img_path = os.path.join(base_dir, "full_capture.png")
roi_img_path = os.path.join(base_dir, "roi_capture.png")

print("'s'키를 누르면 사진이 찍히고 저장됩니다.")
print("'q'키를 누르면 종료됩니다.")

if cap.isOpened():
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Webcam - Press s to Save', frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                cv2.imwrite(full_img_path, frame)
                print(f"전체 이미지 저장 완료: {full_img_path}")
                break
            elif key == ord('q'):
                print("저장하지 않음.")
                cap.release()
                cv2.destroyAllWindows()
                exit()
        else:
            print("프레임을 읽지 못함.")
            break
else:
    print("카메라 연결 실패.")
    exit()

cap.release()
cv2.destroyAllWindows()

# ========== 2. 저장된 이미지 불러오기 ==========
img = cv2.imread(full_img_path)
if img is None:
    print("저장된 이미지를 불러올 수 없습니다.")
    exit()

# ========== 3. 관심 영역 지정 ==========
x, y, w, h = cv2.selectROI('Select ROI - 드래그 후 Enter', img, False)
cv2.destroyWindow('Select ROI - 드래그 후 Enter')

if w and h:
    roi = img[y:y+h, x:x+w]
    cv2.imshow('Cropped ROI', roi)
    cv2.moveWindow('Cropped ROI', 0, 0)
    cv2.imwrite(roi_img_path, roi)
    print(f"관심영역 이미지 저장 완료: {roi_img_path}")
else:
    print("영역이 선택되지 않았습니다.")
    exit()

# ========== 4. ROI 이미지의 RGB 히스토그램 출력 ==========
channels = cv2.split(roi)
colors = ('b', 'g', 'r')

plt.title('ROI Color Histogram')
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