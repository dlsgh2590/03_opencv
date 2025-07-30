import cv2
import os
import numpy as np
import matplotlib.pylab as plt

# ========== 1. 웹캠으로 사진 촬영 ==========
cap = cv2.VideoCapture(0)  # 0번 웹캠(기본 카메라)을 킴

# 해상도 설정 (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 이미지 저장 경로 설정
img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "img"))
os.makedirs(img_dir, exist_ok=True)
full_img_path = os.path.join(img_dir, "capture_for_roi.png")      # 전체 사진 저장 경로
roi_img_path = os.path.join(img_dir, "roi_capture.png")           # ROI 저장 경로

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
                print(f"[✔] 사진 저장 완료: {full_img_path}")
                break
            elif key == ord('q'):
                print("저장하지 않음.")
                cap.release()
                cv2.destroyAllWindows()
                exit()
        else:
            print("사진을 읽지 못했습니다.")
            break
else:
    print("카메라 연결 실패.")
    exit()

cap.release()
cv2.destroyAllWindows()

# ========== 2. 저장된 이미지에서 관심영역(ROI) 선택 ==========
img = cv2.imread(full_img_path)  # 저장된 이미지 불러오기
if img is None:
    print("이미지를 불러올 수 없습니다.")
    exit()

# ROI 선택 (마우스로 드래그 후 Enter 누르기)
x, y, w, h = cv2.selectROI("ROI 영역 지정 - 드래그 후 Enter", img, False)
cv2.destroyWindow("ROI 영역 지정 - 드래그 후 Enter")

if w and h:
    roi = img[y:y+h, x:x+w]            # ROI 부분 잘라내기
    roi_copy = roi.copy()              # ROI 복사본 생성
    cv2.imwrite(roi_img_path, roi_copy)  # ROI 이미지 저장
    print(f"[✔] ROI 영역 저장 완료: {roi_img_path}")

    # 선택한 영역에 녹색 사각형 표시
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # ========== 3. 이미지 출력 ==========
    cv2.imshow("전체 이미지 (ROI 표시됨)", img)
    cv2.imshow("ROI 영역만 출력", roi_copy)
else:
    print("선택된 영역이 없습니다.")
    exit()

# ========== 4. ROI 이미지의 RGB 히스토그램 출력 ==========
channels = cv2.split(roi_copy)  # B, G, R 채널 분리
colors = ('b', 'g', 'r')        # 색상 이름 정의

plt.title('ROI Color Histogram')  # 그래프 제목 설정
for ch, color in zip(channels, colors):
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256])  # 각 채널의 히스토그램 계산
    plt.plot(hist, color=color)  # 해당 색으로 그리기
    plt.xlim([0, 256])           # x축 범위 설정

plt.xlabel('Pixel Value')  # x축 라벨
plt.ylabel('Frequency')    # y축 라벨
plt.grid(True)             # 격자 표시
plt.show()                 # 그래프 표시

cv2.waitKey(0)
cv2.destroyAllWindows()