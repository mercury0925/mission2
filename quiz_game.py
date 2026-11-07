import json
import os

from quiz import Quiz
from default_quizzes import get_default_quizzes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.json")


class QuizGame:
    """퀴즈 목록과 최고 점수를 관리하고 게임 흐름을 진행한다."""

    MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]

    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file
        self.quizzes = []
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

    # ---------- 파일 저장/불러오기 ----------
    def load(self):
        """state.json을 읽어 퀴즈와 최고 점수를 복원한다."""
        if not os.path.exists(self.state_file):
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self._reset_to_default()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data.get("best_score")
            if best_score is not None and (isinstance(best_score, bool)
                                           or not isinstance(best_score, int)):
                raise ValueError("best_score 형식 오류")
        except (KeyError, TypeError, ValueError, AttributeError):
            # JSONDecodeError, UnicodeDecodeError도 ValueError의 하위 클래스
            print("⚠️ state.json이 손상되어 기본 데이터로 복구합니다. (기존 파일은 state.json.bak)")
            self._backup_broken_file()
            self._reset_to_default()
            return
        except OSError as e:
            print(f"⚠️ 데이터 파일을 읽을 수 없습니다: {e}")
            self.quizzes = get_default_quizzes()
            self.best_score = None
            return

        self.quizzes = quizzes
        self.best_score = best_score
        score_text = "기록 없음" if best_score is None else f"{best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")

    def save(self):
        """퀴즈와 최고 점수를 state.json에 저장한다. 성공하면 True."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        tmp_path = self.state_file + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.state_file)  # 쓰다가 중단돼도 원본이 안 깨지게
            return True
        except OSError as e:
            print(f"⚠️ 저장에 실패했습니다: {e}")
            return False

    def _reset_to_default(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.save()

    def _backup_broken_file(self):
        try:
            os.replace(self.state_file, self.state_file + ".bak")
        except OSError:
            pass

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
            self.load()
            while True:
                print()
                self.show_menu()
                choice = self.input_number("선택: ", 1, len(self.MENU_ITEMS))
                if choice == 5:
                    self.save()
                    print("\n👋 게임을 종료합니다. 데이터가 저장되었습니다.")
                    break
                print("\n🚧 준비 중인 기능입니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 종료합니다.")
            self.save()