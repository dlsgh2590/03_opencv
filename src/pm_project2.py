import cv2
import numpy as np

# 카메라 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("카메라 열기 실패")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패")
        break

    # 프레임을 복사해서 출력용으로 사용
    output = frame.copy()

    # ===== ① 그레이스케일 + 블러 =====
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # ===== ② 흑백으로 이진화 (검정 선 찾기 위해 반전) =====
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # ===== ③ 컨투어 찾기 =====
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:
            continue  # 너무 작은 건 무시 (노이즈 제거)

        # ===== ④ 외곽선 그리기 (초록색) =====
        cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)

        # ===== ⑤ 중심점 계산 후 표시 (빨간 점) =====
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)  # 빨간 점

    # ===== ⑥ 화면에 출력 =====
    cv2.imshow("Black Line Detection", output)

    # q 키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()