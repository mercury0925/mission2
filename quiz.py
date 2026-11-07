class Quiz:
    """퀴즈 1개(문제, 선택지 4개, 정답 번호)를 표현한다."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1 ~ 4

    def display(self, number):
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        """JSON에서 읽은 dict를 검증해서 Quiz로 만든다. 형식이 틀리면 ValueError."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제가 비어 있습니다.")
        if (not isinstance(choices, list) or len(choices) != cls.CHOICE_COUNT
                or not all(isinstance(c, str) and c.strip() for c in choices)):
            raise ValueError("선택지는 4개의 문자열이어야 합니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) \
                or not 1 <= answer <= cls.CHOICE_COUNT:
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")
        return cls(question, choices, answer)