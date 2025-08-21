
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSelectorException
import os

def initialize_driver():
    """웹 드라이버를 초기화하고 반환합니다."""
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        chrome_driver_path = os.path.join(script_dir, "chromedriver.exe")
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service)
        return driver
    except Exception as e:
        # GUI에 오류를 표시하기 위해 print 대신 예외를 발생시키거나 로깅하는 것이 더 나을 수 있습니다.
        print(f"드라이버 초기화 중 오류 발생: {e}")
        return None

def login(driver, user_id, password):
    """주어진 드라이버로 웹사이트에 로그인합니다."""
    try:
        wait = WebDriverWait(driver, 10)
        driver.get("https://sports.knu.ac.kr/pages/member/login.php")
        
        # ID, PW 입력 및 로그인 버튼 클릭
        wait.until(EC.presence_of_element_located((By.NAME, "id"))).send_keys(user_id)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "login").click()
        
        # 로그인 성공 확인 (로그인 페이지가 아닌 다른 페이지로 이동했는지 확인)
        wait.until(EC.url_changes("https://sports.knu.ac.kr/pages/member/login.php"))
        return True
    except TimeoutException:
        # 로그인 실패 시 (예: 비밀번호 오류) TimeoutException이 발생할 수 있음
        return False
    except Exception:
        return False

def reserve(driver, config, log_callback):
    """로그인된 드라이버를 사용하여 예약을 진행합니다."""
    try:
        # 1. 예약 실행 시간까지 대기
        if config["exec_day"] != "즉시":
            now = datetime.now()
            day = now.day
            if config["exec_day"] == "내일":
                day += 1
            
            trigger_time_str = f"{now.year}-{now.month:02d}-{day:02d} {config['exec_hour']}:{config['exec_minute']}:00"
            trigger_time = datetime.strptime(trigger_time_str, "%Y-%m-%d %H:%M:%S")
            
            log_callback(f"예약 실행 시간({trigger_time.strftime('%Y-%m-%d %H:%M:%S')})까지 대기합니다...")
            while datetime.now() < trigger_time:
                time.sleep(0.1)
            
            log_callback("정확한 예약 시작을 위해 1초 추가 대기합니다.")
            time.sleep(1)

        wait = WebDriverWait(driver, 10)

        # 2. 예약 페이지로 직접 이동
        target_url = f"https://sports.knu.ac.kr/doc/class_info6_time.php?&tDATE={config['date']}{config['gym_code']}#this"
        log_callback(f"예약 페이지로 이동합니다: {target_url}")
        driver.get(target_url)

        # 3. 동의 체크박스 클릭
        wait.until(EC.element_to_be_clickable((By.ID, "agree"))).click()

        # 4. 시작 시간 버튼 클릭
        time_button_xpath = f"//a[contains(@onclick, \"reserveFacility('{config['start_time']}')\")]"
        wait.until(EC.element_to_be_clickable((By.XPATH, time_button_xpath))).click()

        # 5. 정보 입력
        log_callback("예약 세부 정보를 입력합니다.")
        wait.until(EC.presence_of_element_located((By.NAME, "HP_NO"))).send_keys(config['contact'])
        driver.find_element(By.NAME, "BLNG_NM").send_keys(config['department'])
        driver.find_element(By.NAME, "EMNO").send_keys(config['student_id'])
        
        select = Select(driver.find_element(By.NAME, "use_time"))
        select.select_by_value(config['duration'])

        driver.find_element(By.NAME, "USER_QTY").send_keys(config['user_count'])
        driver.find_element(By.NAME, "USER_LIST").send_keys(config['user_list'])
        driver.find_element(By.NAME, "EVNT_PLAN").send_keys(config['event_plan'])

        # 6. 다음 단계 버튼 클릭
        driver.find_element(By.XPATH, "//input[@value='다음단계']").click()

        # 7. 첫 번째 알림창(확인) 처리
        confirm_alert = wait.until(EC.alert_is_present())
        log_callback(f"확인창 메시지: {confirm_alert.text}")
        confirm_alert.accept()

        # 8. 두 번째 알림창(최종 성공) 처리
        success_alert = wait.until(EC.alert_is_present())
        success_message = success_alert.text
        success_alert.accept()

        return f"성공: {success_message}"

    except (NoSuchElementException, TimeoutException):
        return "오류: 웹 페이지의 요소를 찾지 못했거나 시간이 초과되었습니다."
    except InvalidSelectorException:
        return f"오류: 시간 선택 버튼을 찾기 위한 XPath가 잘못되었습니다. 입력값: {config['start_time']}"
    except Exception as e:
        return f"알 수 없는 오류 발생: {e}"
