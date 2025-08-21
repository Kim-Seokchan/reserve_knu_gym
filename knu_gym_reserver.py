
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os

# ##############################################################################
# ##                           사용자 설정                                    ##
# ##############################################################################
USER_CONFIG = {
    # --- 로그인 정보 ---
    "id": "knsc135",  # 새로 입력하세요
    "password": "입력하세요",  # 새로 입력하세요

    # --- 예약 정보 ---
    "reservation_date": "2025-08-28",  # YYYY-MM-DD 형식
    "start_time": "9",  # 예약할 시작 시간 (예: "7", "8", "20")
    "usage_duration": "2",  # 사용 기간 (1시간 또는 2시간)

    # --- 예약 실행 시간 설정 ---
    # 스크립트가 예약을 시도할 시간을 설정합니다.
    # 예를 들어, 예약이 오전 9시에 열린다면, "08:59:58" 와 같이 약간의 여유를 두고 설정합니다.
    "reservation_trigger_time": "00:33:00", # HH:MM:SS 형식

    # --- 신청 정보 ---
    "contact_number": "010-1234-5678",
    "affiliation": "컴퓨터학부",
    "student_id": "2020123456",
    "num_users": "9",
    "user_list": "컴퓨터학부 홍길동 외 9명, 모두 개인 운동 목적임.", # 이용자수*3 자 이상
    "event_plan": "개인 근력 운동 및 유산소 운동 진행 후 주변 정리", # 15자 이상
}
# ##############################################################################

def wait_for_element(driver, by, value, timeout=10):
    """특정 요소가 나타날 때까지 기다리는 함수"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def login(driver, user_id, password):
    """로그인 페이지로 이동하여 로그인을 수행"""
    print("로그인 페이지로 이동합니다.")
    driver.get("https://sports.knu.ac.kr/pages/member/login.php")
    
    print(f"아이디: {user_id}")
    wait_for_element(driver, By.NAME, "id").send_keys(user_id)
    driver.find_element(By.NAME, "password").send_keys(password)
    
    print("로그인 버튼을 클릭합니다.")
    driver.find_element(By.CSS_SELECTOR, ".login").click()
    
    # 로그인 성공 확인 (URL 변경으로 판단)
    WebDriverWait(driver, 10).until(
        EC.url_changes("https://sports.knu.ac.kr/pages/member/login.php")
    )
    print("로그인 성공!")

def reserve_facility():
    """설정된 정보에 따라 체육관 예약을 진행"""
    
    # 스크립트의 실제 위치를 기준으로 chromedriver.exe 경로를 설정합니다.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    webdriver_path = os.path.join(script_dir, 'chromedriver.exe')
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # 1. 로그인
        login(driver, USER_CONFIG["id"], USER_CONFIG["password"])

        # 2. 예약 실행 시간까지 대기
        trigger_time_str = f"{datetime.now().strftime('%Y-%m-%d')} {USER_CONFIG['reservation_trigger_time']}"
        trigger_time = datetime.strptime(trigger_time_str, "%Y-%m-%d %H:%M:%S")
        
        print(f"예약 실행 시간({USER_CONFIG['reservation_trigger_time']})까지 대기합니다...")
        while datetime.now() < trigger_time:
            time.sleep(0.1)

        # 3. 예약 페이지로 직접 이동
        reservation_url = f"https://sports.knu.ac.kr/doc/class_info6_time.php?&tDATE={USER_CONFIG['reservation_date']}&fc_grno=1&fc_sqno=1#this"
        print(f"예약 시간이 되어 예약 페이지로 이동합니다: {reservation_url}")
        driver.get(reservation_url)

        # 4. 시작 시간 선택
        print(f"{USER_CONFIG['start_time']}시를 선택합니다.")
        # 동의 체크박스 클릭
        wait_for_element(driver, By.ID, "agree").click()

        # 시간 버튼 클릭
        start_time = USER_CONFIG['start_time']
        time_button_xpath = f"//a[@onclick=\"reserveFacility('{start_time}')\"]"
        wait_for_element(driver, By.XPATH, time_button_xpath).click()

        # 5. 예약 정보 입력
        print("예약 세부 정보를 입력합니다.")
        wait_for_element(driver, By.NAME, "HP_NO").send_keys(USER_CONFIG["contact_number"])
        driver.find_element(By.NAME, "BLNG_NM").send_keys(USER_CONFIG["affiliation"])
        driver.find_element(By.NAME, "EMNO").send_keys(USER_CONFIG["student_id"])
        
        # 사용 기간 선택 (Select dropdown)
        select = Select(driver.find_element(By.NAME, "use_time"))
        select.select_by_value(USER_CONFIG["usage_duration"])
        
        driver.find_element(By.NAME, "USER_QTY").send_keys(USER_CONFIG["num_users"])
        driver.find_element(By.NAME, "USER_LIST").send_keys(USER_CONFIG["user_list"])
        driver.find_element(By.NAME, "EVNT_PLAN").send_keys(USER_CONFIG["event_plan"])

        # 6. 다음 단계로 이동
        print("정보 입력을 완료하고 '다음단계' 버튼을 클릭합니다.")
        driver.find_element(By.XPATH, "//input[@value='다음단계']").click()

        # 7. 예약 신청 확인 및 완료
        # 첫 번째 확인창 (예약하시겠습니까?)
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        confirm_alert = driver.switch_to.alert
        print(f"확인창 메시지: {confirm_alert.text}")
        confirm_alert.accept()
        print("예약 신청을 확인했습니다.")

        # 두 번째 성공 메시지 창을 기다림
        # 웹사이트의 반응 속도에 따라 충분한 대기 시간을 주는 것이 중요
        time.sleep(2) # 알림창이 뜨는 시간을 고려하여 잠시 대기

        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            success_alert = driver.switch_to.alert
            final_message = success_alert.text
            print(f"최종 예약 성공! 메시지: {final_message}")
            success_alert.accept()
        except Exception as e:
            print("두 번째 확인창을 찾는 데 실패했습니다. 페이지의 현재 URL과 상태를 확인하세요.")
            print(f"현재 URL: {driver.current_url}")
            # 성공 또는 실패를 판단할 다른 요소가 있는지 확인 (예: 특정 텍스트)
            if "예약이 완료되었습니다" in driver.page_source:
                 print("페이지 소스에서 예약 완료 메시지를 확인했습니다.")
            else:
                 print("예약이 최종적으로 완료되었는지 확인하지 못했습니다.")


        print("프로그램을 초기화(종료)합니다.")

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
    finally:
        # driver.quit() # 문제 분석을 위해 브라우저를 닫지 않도록 주석 처리
        print("스크립트 실행이 완료되었습니다. 브라우저를 수동으로 닫아주세요.")


if __name__ == "__main__":
    # 입력값 유효성 검사
    if len(USER_CONFIG["user_list"]) < 27:
        print("[오류] 이용자 명단(user_list)은 15자 이상이어야 합니다.")
    elif len(USER_CONFIG["event_plan"]) < 15:
        print("[오류] 행사계획(event_plan)은 15자 이상이어야 합니다.")
    elif USER_CONFIG["id"] == "YOUR_ID" or USER_CONFIG["password"] == "YOUR_PASSWORD":
        print("[오류] USER_CONFIG의 id와 password를 자신의 정보로 수정해주세요.")
    else:
        reserve_facility()
