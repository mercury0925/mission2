from quiz import Quiz


def get_default_quizzes():
    return [
        Quiz("지도학습(Supervised Learning)에 해당하지 않는 것은?",
             ["선형 회귀", "로지스틱 회귀", "K-평균 군집화", "서포트 벡터 머신"], 3),
        Quiz("학습 데이터에는 잘 맞지만 새로운 데이터에서 성능이 떨어지는 현상은?",
             ["과소적합", "과적합", "정규화", "드롭아웃"], 2),
        Quiz("신경망에서 역전파(Backpropagation)가 계산하는 것은?",
             ["입력 데이터의 평균", "손실 함수에 대한 가중치의 기울기", "배치 크기", "학습률"], 2),
        Quiz("이진 분류 출력층에 주로 사용하는 활성화 함수는?",
             ["Sigmoid", "ReLU", "Tanh", "Linear"], 1),
        Quiz("Transformer 모델의 핵심 메커니즘은?",
             ["합성곱", "순환 연결", "풀링", "Self-Attention"], 4),
    ]