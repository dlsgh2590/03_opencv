import cv2
import numpy as np

# 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
img = cv2.imread("../img/lightning.png")
if img is None:
    print("이미지를 불러오지 못했습니다. 경로를 확인하세요.")
    exit()

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)

# 컨투어 찾기 (OpenCV 4.x 버전 기준)
contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 컨투어가 있는지 확인
if len(contours) == 0:
    print("컨투어가 없습니다.")
    exit()

contr = contours[0]  # 첫 번째 컨투어 사용

# 감싸는 사각형 표시(검정색)
x, y, w, h = cv2.boundingRect(contr)
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)

# 최소한의 사각형 표시(초록색)
rect = cv2.minAreaRect(contr)
box = cv2.boxPoints(rect)
box = box.astype(int)  # np.int0 → 안전한 방식으로 수정
cv2.drawContours(img, [box], -1, (0, 255, 0), 3)

# 최소한의 원 표시(파랑색)
(center_x, center_y), radius = cv2.minEnclosingCircle(contr)
cv2.circle(img, (int(center_x), int(center_y)), int(radius), (255, 0, 0), 2)

# 최소한의 삼각형 표시(분홍색)
ret, tri = cv2.minEnclosingTriangle(contr)
cv2.polylines(img, [np.int32(tri)], True, (255, 0, 255), 2)

# 최소한의 타원 표시(노랑색)
if len(contr) >= 5:  # 타원을 그릴 때는 최소 5개 이상의 포인트가 필요함
    ellipse = cv2.fitEllipse(contr)
    cv2.ellipse(img, ellipse, (0, 255, 255), 3)

# 중심점 통과하는 직선 표시(빨강색)
[vx, vy, x0, y0] = cv2.fitLine(contr, cv2.DIST_L2, 0, 0.01, 0.01)
rows, cols = img.shape[:2]

# 두 점 계산 (float → int 변환)
left_y = int((-x0 * vy / vx) + y0)
right_y = int(((cols - 1 - x0) * vy / vx) + y0)

cv2.line(img, (0, left_y), (cols - 1, right_y), (0, 0, 255), 2)

# 결과 출력
cv2.imshow('Bound Fit shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()