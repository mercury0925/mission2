from default_quizzes import get_default_quizzes


class QuizGame:
    """퀴즈 목록과 최고 점수를 관리하고 게임 흐름을 진행한다."""

    MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]

    def __init__(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None  # 아직 한 번도 안 풀었으면 None

    # ---------- 입력 처리 ----------
    def input_text(self, prompt):
        """빈 문자열이 아닌 텍스트를 입력받는다."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈 입력입니다. 내용을 입력하세요.")

    def input_number(self, prompt, min_value, max_value):
        """min_value ~ max_value 범위의 정수를 입력받는다."""
        range_msg = f"{min_value}-{max_value} 사이의 숫자를 입력하세요."
        while True:
            value = input(prompt).strip()
            if not value:
                print(f"⚠️ 빈 입력입니다. {range_msg}")
                continue
            try:
                number = int(value)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {range_msg}")
                continue
            if not min_value <= number <= max_value:
                print(f"⚠️ 잘못된 입력입니다. {range_msg}")
                continue
            return number

    # ---------- 메뉴 ----------
    def show_menu(self):
        line = "=" * 40
        print(line)
        print("🎯 나만의 퀴즈 게임 🎯".center(36))
        print(line)
        for i, item in enumerate(self.MENU_ITEMS, start=1):
            print(f"{i}. {item}")
        print(line)

    # ---------- 실행 ----------
    def run(self):
        try:
            while True:
                print()
                self.show_menu()
                choice = self.input_number("선택: ", 1, len(self.MENU_ITEMS))
                if choice == 5:
                    print("\n👋 게임을 종료합니다.")
                    break
                print("\n🚧 준비 중인 기능입니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")