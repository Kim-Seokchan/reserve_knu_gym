
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime, timedelta
import time
import knu_gym_reserver as reserver

class ReserverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KNU 체육관 예약 시스템")
        self.geometry("600x750")

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main_frame, text="예약 정보 입력", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        self.entries = {}
        fields = {
            "id": "아이디", "password": "비밀번호",
            "gym_code": "체육관 코드(수정 금지)",
            "date": "예약 날짜 (YYYY-MM-DD)", "start_time": "시작 시간 (예: 9)",
            "duration": "사용 시간 (1 또는 2)", "contact": "연락처",
            "department": "소속", "student_id": "학번",
            "user_count": "이용자 수", "user_list": "이용자 명단 (인원수 * 3 자 이상)",
            "event_plan": "행사 계획 (15자 이상)"
        }

        default_values = {
            "id": "knsc135", "password": "",
            "gym_code": "&fc_grno=3&fc_sqno=47",
            "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "start_time": "9",
            "duration": "2", "contact": "010-1234-5678",
            "department": "약학과", "student_id": "2020123456",
            "user_count": "6", 
            "user_list": "김석찬 이유진 홍길동 호날두 바이든 트럼프",
            "event_plan": "배드민턴 카더가든 드리프트 유산소 운동 진행 후 주변 정리정돈"
        }

        for i, (field, label) in enumerate(fields.items()):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(input_frame, width=40, show="*" if field == "password" else "")
            entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)
            entry.insert(0, default_values.get(field, ""))
            self.entries[field] = entry
        
        i += 1
        ttk.Label(input_frame, text="예약 실행 시간(1초 지연)").grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.exec_time_frame = ttk.Frame(input_frame)
        self.exec_time_frame.grid(row=i, column=1, columnspan=2, sticky=tk.EW)

        self.exec_day_var = tk.StringVar()
        self.exec_day_combo = ttk.Combobox(self.exec_time_frame, textvariable=self.exec_day_var, values=["즉시", "오늘", "내일"], state="readonly")
        self.exec_day_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.exec_day_combo.set("오늘")
        self.exec_day_combo.bind("<<ComboboxSelected>>", self.toggle_time_selection)

        self.exec_hour_var = tk.StringVar()
        self.exec_hour_combo = ttk.Combobox(self.exec_time_frame, textvariable=self.exec_hour_var, values=[f"{h:02d}" for h in range(24)], width=5, state="readonly")
        self.exec_hour_combo.pack(side=tk.LEFT)
        
        ttk.Label(self.exec_time_frame, text="시").pack(side=tk.LEFT)

        self.exec_minute_var = tk.StringVar()
        self.exec_minute_combo = ttk.Combobox(self.exec_time_frame, textvariable=self.exec_minute_var, values=[f"{m:02d}" for m in range(60)], width=5, state="readonly")
        self.exec_minute_combo.pack(side=tk.LEFT)
        ttk.Label(self.exec_time_frame, text="분").pack(side=tk.LEFT)

        self.toggle_time_selection() 

        input_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.run_button = ttk.Button(button_frame, text="예약 실행", command=self.start_reservation_thread)
        self.run_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.clear_button = ttk.Button(button_frame, text="초기화", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        log_frame = ttk.LabelFrame(main_frame, text="실행 로그", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_area.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log_area.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.update_idletasks()

    def toggle_time_selection(self, event=None):
        if self.exec_day_var.get() in ["오늘", "내일"]:
            self.exec_hour_combo.config(state="readonly")
            self.exec_minute_combo.config(state="readonly")
            now = datetime.now()
            self.exec_hour_combo.set(f"{now.hour:02d}")
            self.exec_minute_combo.set(f"{(now.minute + 1):02d}")
        else:
            self.exec_hour_combo.config(state="disabled")
            self.exec_minute_combo.config(state="disabled")
            self.exec_hour_combo.set("")
            self.exec_minute_combo.set("")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.log("입력 필드를 초기화했습니다.")

    def start_reservation_thread(self):
        self.run_button.config(state=tk.DISABLED)
        self.log("예약 프로세스를 시작합니다.")
        
        config = {field: entry.get() for field, entry in self.entries.items()}
        config["exec_day"] = self.exec_day_var.get()
        config["exec_hour"] = self.exec_hour_var.get()
        config["exec_minute"] = self.exec_minute_var.get()

        if len(config["user_list"]) < int(config["user_count"]) * 3:
            self.log("[오류] 이용자 명단은 인원수 * 3 자 이상이어야 합니다.")
            self.run_button.config(state=tk.NORMAL)
            return
        if len(config["event_plan"]) < 15:
            self.log("[오류] 행사계획은 15자 이상이어야 합니다.")
            self.run_button.config(state=tk.NORMAL)
            return
        if not all([config["id"], config["password"]]):
            self.log("[오류] 아이디와 비밀번호를 입력해주세요.")
            self.run_button.config(state=tk.NORMAL)
            return
        if config["exec_day"] != "즉시" and not all([config["exec_hour"], config["exec_minute"]]):
            self.log("[오류] 예약 실행 시간을 선택해주세요.")
            self.run_button.config(state=tk.NORMAL)
            return

        thread = threading.Thread(target=self.run_reservation, args=(config,))
        thread.daemon = True
        thread.start()

    def run_reservation(self, config):
        driver = None
        try:
            self.log("웹 드라이버를 초기화합니다...")
            driver = reserver.initialize_driver()
            if not driver:
                self.log("오류: 웹 드라이버 초기화에 실패했습니다.")
                return

            self.log(f"{config['id']} 계정으로 로그인을 시도합니다...")
            login_success = reserver.login(driver, config['id'], config['password'])

            if not login_success:
                self.log("오류: 로그인에 실패했습니다. 아이디 또는 비밀번호를 확인하세요.")
                return

            self.log("로그인 성공.")

            result = reserver.reserve(driver, config, self.log)
            self.log(f"예약 시도 결과: {result}")

        except Exception as e:
            self.log(f"프로세스 중 예상치 못한 오류 발생: {e}")
        finally:
            if driver:
                self.log("10초 후 브라우저가 자동으로 닫힙니다.")
                time.sleep(10)
                driver.quit()
            self.run_button.config(state=tk.NORMAL)
            self.log("프로세스가 종료되었습니다.")

if __name__ == "__main__":
    app = ReserverApp()
    app.mainloop()
