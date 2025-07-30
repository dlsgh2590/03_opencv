# OpenCV Contour & Line Tracer 실습

이 저장소는 OpenCV를 활용한 컨투어(Contour) 처리 및 라인트레이서 구현 실습 예제를 포함하고 있습니다. 각 파일은 특정한 컨투어 분석 기법을 다루며, 이미지 처리에 유용한 기능을 직접 실습하며 익힐 수 있습니다.

---

## 📁 파일 목록

### 1. `cntr_approximate.py`
- **설명**: 컨투어를 근사화하여 꼭짓점 수를 줄이는 방법을 실습합니다.
- **주요 함수**: `cv2.approxPolyDP`

---

### 2. `cntr_bound_fit.py`
- **설명**: 컨투어에 최소 크기의 경계 사각형과 타원을 그리는 실습입니다.
- **주요 함수**: `cv2.boundingRect`, `cv2.minAreaRect`, `cv2.fitEllipse`

---

### 3. `cntr_convexhull.py`
- **설명**: 컨투어의 볼록 껍질(Convex Hull)을 찾는 실습입니다.
- **주요 함수**: `cv2.convexHull`

---

### 4. `cntr_find.py`
- **설명**: 이미지에서 컨투어를 찾아서 출력하는 기본 예제입니다.
- **주요 함수**: `cv2.findContours`, `cv2.drawContours`

---

### 5. `cntr_heirach.py`
- **설명**: 컨투어 계층 구조(Hierarchy)를 분석하고 시각화합니다.
- **주요 개념**: 컨투어 간의 부모-자식 관계 이해

---

### 6. `linetracer.py`
- **설명**: 영상 내 선을 따라가며 라인을 추적하는 간단한 라인트레이서 예제입니다.
- **활용**: 로봇 비전, 경로 인식 등

---

## ✅ 실행 방법

```bash
pip install opencv-python
python cntr_find.py  # 원하는 파일명으로 실행

📸 웹캠 사진 촬영 후 색상 히스토그램 분석 프로젝트
이 프로젝트는 웹캠으로 사진을 찍고, 그 중 원하는 부분(관심 영역, ROI)을 선택해서 색상(RGB) 히스토그램을 그려주는 프로그램입니다.
사진을 찍고, 관심 부분을 선택하고, 그 부분에 어떤 색이 얼마나 있는지 시각적으로 확인할 수 있어요!

✅ 사용 도구
Python
OpenCV (이미지 처리)
Matplotlib (그래프 그리기)

📂 실행 흐름
웹캠으로 사진 찍기
프로그램을 실행하면 웹캠이 켜지고,
s 키를 누르면 사진이 저장되고,
q 키를 누르면 프로그램이 종료돼요.
사진에서 관심 영역(ROI) 선택하기
마우스로 원하는 부분을 드래그해서 선택해요.
선택된 부분이 잘렸고, 따로 저장돼요.
선택한 영역의 색 히스토그램 보기
파란색(Blue), 초록색(Green), 빨간색(Red)이 얼마나 들어있는지 그래프로 보여줘요.

📸 예시 이미지 저장 경로
전체 사진: ../img/full_capture.png
관심 영역: ../img/roi_capture.png

🧠 코드 구성 설명
1. 웹캠 설정 및 사진 저장
python
cap = cv2.VideoCapture(0)  # 웹캠 켜기
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 너비 설정
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 높이 설정
실시간으로 화면을 보여주고 s 누르면 사진이 저장돼요.

2. 사진 불러오기
python
img = cv2.imread(full_img_path)
아까 저장한 전체 사진을 불러와요.

3. 관심 영역(ROI) 선택
python
x, y, w, h = cv2.selectROI('Select ROI - 드래그 후 Enter', img, False)
roi = img[y:y+h, x:x+w]
마우스로 원하는 부분을 선택하고 잘라내요.

4. 색상 히스토그램 출력
python
channels = cv2.split(roi)
colors = ('b', 'g', 'r')
for ch, color in zip(channels, colors):
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256])
    plt.plot(hist, color=color)
파란색, 초록색, 빨간색이 몇 번씩 나오는지 그려주는 코드예요.

💾 결과 화면
히스토그램에는 X축이 색깔 밝기(0~255), Y축이 얼마나 자주 나왔는지를 보여줘요.

각 색의 분포를 한눈에 알 수 있어요!

# OpenCV 실습 정리 - 검은색 라인 추적 및 중심점 시각화

## 📸 실습 목표
- 웹캠을 이용해 실시간으로 이미지를 가져온 후
- 이미지에서 **검은색 라인(또는 도형)**을 감지하고
- 감지된 외곽선에 **초록색 테두리**를 그리고, 중심에 **빨간 점**을 표시하는 프로그램을 구현함.

---

## 🧪 사용된 기술
- **Python 3**
- **OpenCV (cv2)**
- **NumPy**

---

## 🔍 주요 기능 설명

### 1. 카메라 입력 받기
```python
cap = cv2.VideoCapture(0)
