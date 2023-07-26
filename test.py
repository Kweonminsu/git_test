import getpass11
import os
import subprocess
import time
from tkinter import RIGHT, LEFT, BOTH, END, Y
import numpy as np
import tkinter as tk
import threading
import psutil
import pyautogui
import pyperclip
import pythoncom

timer_stop = False
initial_count = 7
username = getpass.getuser()

#경로
driver_path = r"C:\\Users\\{}\\Documents\\informer\\driver\\msedgedriver.exe".format(username)
messenger_path = "C:/"
save_path_log = r"C:\Users\{}\Documents\informer\log".format(username)
save_path = r"C:\\Users\\{}\\Documents\\informer\\img".format(username)
icon_path = "informer_icon.ico"
pythoncom.CoInitialize()
log = []

def close_excel():
    import psutil
    for proc in psutil.process_iter():
        try:
            if "excel.exe" in proc.name().lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

''''# 초기 위치 설정
def initial_pos():
    global root
    #기본 좌표로 이동
    messenger_path = "C:/m"
    subprocess.Popen(messenger_path)

    time.sleep(2)

    messenger = pyautogui.getWindowsWithTitle("K")[0]

    messenger.moveTo(0, 0)
'''
# run_program 개별 thread 구성 및 실행
def run_detection():
    global stop_program, save_path, root, timer_stop, timer_start, program_start

    if program_start :
        update_log("이미 실행 중입니다.")
    else :
        if timer_stop:
            resume_timer()

        #initial_pos()
        remove_all()
        program_start = True
        x1 = int(x1_entry.get())
        y1 = int(y1_entry.get())
        x2 = int(x2_entry.get())
        y2 = int(y2_entry.get())
        sec = int(entry_sec.get())
        update_log(f"{sec}초 간격으로 실행")
        time.sleep(2)
        # 프로그램 시작 전 변수들 초기화
        stop_program = False


        # 이미지 감지 스레드 시작
        run_program_thread = threading.Thread(target=run_program,
                                                  args=(sec, save_path, x1, y1, x2, y2)
                                                  , daemon=True)
        run_program_thread.start()

def resume_detection():
    global stop_program, save_path, root, timer_stop, run_program_thread


    x1 = int(x1_entry.get())
    y1 = int(y1_entry.get())
    x2 = int(x2_entry.get())
    y2 = int(y2_entry.get())
    sec = int(entry_sec.get())
    update_log(f"{sec}초 간격으로 재개")
    # 프로그램 시작 전 변수들 초기화
    stop_program = False
    run_program_thread = None
    # 이미지 감지 스레드 시작
    run_program_thread = threading.Thread(target=run_program,

                                          args=(sec, save_path, x1, y1, x2, y2)

                                          , daemon=True)

    run_program_thread.start()

def run_program(sec, save_path, x1, y1, x2, y2):
    from PIL import ImageGrab
    import time
    global stop_program

    ##while not stop_program:
    while not stop_program :
        try:
            # 현재 이미지 캡쳐
            current_image = ImageGrab.grab(bbox=(x1, y1, x2, y2)).convert('L')

            # 이전 이미지
            previous_image = current_image.copy()

            # 캡쳐 간격
            time.sleep(sec)

            # 현재 이미지 캡
            current_image = ImageGrab.grab(bbox=(x1, y1, x2, y2)).convert('L')

            # 두 이미지를 배열로 변환
            current_array = np.array(current_image)
            previous_array = np.array(previous_image)

            # 배열 요소간 차이 계산
            difference = np.sum(current_array != previous_array)

            # 라벨 위젯 생성
            log_label = tk.Label(root, text="")
            log_label.pack()

            # 이미지 변경 여부에 따라 로그 업데이트, infromer 작동 트리
            if difference == 0:
                update_log("프로그램 작동 중")
            else:
                ## timer 정지 ##
                stop_timer()
                ##          ##
                current_time = time.time()
                current_image_path = f"{save_path}/image_{current_time}.png"
                current_image.save(current_image_path)
                update_log("Informer 작동")
                informer()
                ## timer 시작
                resume_timer()

                # 지난 2개의 이미지 파일만 유지하도록 함
                files = os.listdir(save_path)

                if len(files) > 2:
                    oldest_file = min(files, key=lambda x: os.path.getctime(os.path.join(save_path, x)))
                    os.remove(os.path.join(save_path, oldest_file))

        except Exception as e:

            update_log("ERROR 발생")

            stop_timer()

            #pyperclip.copy("죄송해요..ERROR발생..")

            #data_send()

            close_excel()

            time.sleep(2)

            resume_timer()

            continue
    update_log("프로그램 중단")

def message_del():

        import time

        import pyautogui

        import win32gui



        time.sleep(0.5)

        handle = win32gui.GetForegroundWindow()

        left, top, right, bottom = win32gui.GetWindowRect(handle)

        x, y = left, bottom

        x_offset, y_offset = 325, -205

        x += x_offset

        y += y_offset

        pyautogui.click(x, y, button='right')

        time.sleep(0.3)

        pyautogui.move(10, 100)

        time.sleep(0.3)

        pyautogui.click(button='left')

        time.sleep(0.3)

        pyautogui.press('enter')

def data_send():

        import pyautogui

        import subprocess

        import win32gui

        import time

        global messenger_path

        pass

        subprocess.Popen(messenger_path)

        time.sleep(1)

        K = pyautogui.getWindowsWithTitle('K')[0]

        x, y = K.left, K.top

        x_offset, y_offset = 130, 80

        x += x_offset

        y += y_offset

        pyautogui.click(x, y, button='left')

        pyautogui.doubleClick(x, y + 110, button='left')

        time.sleep(1)

        handle = win32gui.GetForegroundWindow()

        left, top, right, bottom = win32gui.GetWindowRect(handle)

        x, y = left, bottom

        x_offset, y_offset = 50, -70

        x += x_offset

        y += y_offset

        pyautogui.click(x, y, button='left')

        pyautogui.click(button='left')

        pyautogui.hotkey('ctrl', 'v')

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(2)

        pyautogui.press('enter')

        #대화 삭제

        message_del()

        pyautogui.press('esc')

        time.sleep(1)

        #사진 삭제

        remove_all()

        time.sleep(1)

def Hi_sending():

    import pyautogui

    import subprocess

    import win32gui

    import time

    global messenger_path



    subprocess.Popen(messenger_path)

    time.sleep(1)

    K = pyautogui.getWindowsWithTitle('K')[0]

    x, y = K.left, K.top

    x_offset, y_offset = 130, 80

    x += x_offset

    y += y_offset

    pyautogui.click(x, y, button='left')

    pyautogui.doubleClick(x, y + 110, button='left')

    time.sleep(1)

    handle = win32gui.GetForegroundWindow()

    left, top, right, bottom = win32gui.GetWindowRect(handle)

    x, y = left, bottom

    x_offset, y_offset = 50, -70

    x += x_offset

    y += y_offset

    pyautogui.click(x, y, button='left')

    pyautogui.click(button='left')

    pyperclip.copy("잠시만 기다려주세요 !\n최대 1분이 소요 됩니다.")

    pyautogui.hotkey('ctrl', 'v')

    time.sleep(1)

    pyautogui.press('enter')

    time.sleep(2)

    pyautogui.press('enter')

    pyautogui.press('esc')

    time.sleep(1)

# Summary open, 메신저 데이터 확인, 엑셀 데이터 sorting, inform sending
def informer():

    # 임시 informer
    def terminate_process_by_name(process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                proc.terminate()

    # 계산기 실행
    calculator_process = psutil.Popen("notepad.exe")

    # 대기 시간 설정 (예: 10초)
    timeout = 3
    time.sleep(timeout)

    # 계산기 프로세스 종료
    terminate_process_by_name("notepad.exe")
    '''
    import win32com.client

    import re

    import time

    import pyautogui

    import pyperclip

    import datetime

    import win32gui

    import pythoncom

    global timeout



    def Summary_open():
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        import time
        import pythoncom
        global driver_path

        # excel 실행 여부 조회
        def is_excel_running():
            import psutil
            for proc in psutil.process_iter():
                try:
                    if "excel.exe" in proc.name().lower():
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return False

        # Excel 최소화
        def excel_minimize():
            import win32com.client
            excel = win32com.client.Dispatch('Excel.Application')
            excel.WindowState = 2
        close_excel()
        pythoncom.CoInitialize()
        # summary open
        url = "http://e"
        driver = webdriver.Edge(executable_path=driver_path)
        driver.get(url)


        try:

            # 최대 8초 기다림

            wait = WebDriverWait(driver, 8)

            button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".button_st1.btn_bgcolor_bl")))

            button.click()



        except:

            # 8초후 안열렸어 ? 다 끄고 다시 열어봐

            driver.quit()

            close_excel()

            time.sleep(1)

            pythoncom.CoInitialize()

            # summary open

            url = "http://e"

            driver = webdriver.Edge(executable_path=driver_path)

            driver.get(url)



            try:

                wait = WebDriverWait(driver, 8)

                button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".button_st1.btn_bgcolor_bl")))

                button.click()



            # 이거 실행 안될 것 같은데

            except :

                wait_time = 0

                while not is_excel_running():

                    time.sleep(1)

                    wait_time += 1

                    pythoncom.CoInitialize()

                    if wait_time > 8:

                        driver.quit()

                        close_excel()

                        break



        time.sleep(1)



        # 드라이버 종료

        driver.quit()

        time.sleep(4)

        excel_minimize()

    def Non_data_send():

        import pyautogui

        import subprocess

        import win32gui

        import time

        global messenger_path



        subprocess.Popen(messenger_path)

        time.sleep(1)

        pyautogui.press('enter')

        K = pyautogui.getWindowsWithTitle('K')[0]

        x, y = K.left, K.top

        x_offset, y_offset = 130, 80

        x += x_offset

        y += y_offset

        pyautogui.click(x, y, button='left')

        pyautogui.doubleClick(x, y + 110, button='left')

        time.sleep(1)

        handle = win32gui.GetForegroundWindow()

        left, top, right, bottom = win32gui.GetWindowRect(handle)

        x, y = left, bottom

        x_offset, y_offset = 50, -70

        x += x_offset

        y += y_offset

        pyautogui.click(x, y, button='left')

        pyautogui.click(button='left')

        time.sleep(2)

        pyautogui.hotkey('ctrl', 'v')

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(2)

        pyautogui.press('enter')

        message_del()

        pyautogui.press('esc')

        time.sleep(1)

        remove_all()

        time.sleep(1)

    # 메신저 실행, 대화방 입장

    def open_messenger_date():

        import subprocess

        import time

        import pyautogui

        import pythoncom



        global messenger_path

        pythoncom.CoInitialize()

        subprocess.Popen(messenger_path)

        time.sleep(3)

        pythoncom.CoInitialize()

        K = pyautogui.getWindowsWithTitle('K')[0]

        x, y = K.left, K.top

        x_offset, y_offset = 130, 80

        x += x_offset

        y += y_offset

        pyautogui.click(x, y, button='left')

        pyautogui.doubleClick(x, y + 110, button='left')
    # 요청 Data 변수에 저장

    def find_recent_date():

        global name



        time.sleep(2)

        time.sleep(1)

        handle = win32gui.GetForegroundWindow()

        left, top, right, bottom = win32gui.GetWindowRect(handle)



        # ---------------------------------------전체복사 방식----------------------------------

        x, y = left, bottom

        x_offset, y_offset = 100, -250

        x += x_offset

        y += y_offset

        pyautogui.click(x, y, button='left')

        pyautogui.click(x, y, button='left')

        time.sleep(1)

        time.sleep(1)

        pyautogui.hotkey('ctrl', 'a')

        time.sleep(2)

        pyautogui.hotkey('ctrl', 'c')

        time.sleep(1)

        pyautogui.hotkey('ctrl', 'c')

        # ---------------------------------------전체복사 방식----------------------------------



        text = pyperclip.paste()

        time.sleep(1)

        pyautogui.press('ESC')

        pyperclip.copy('')



        lines = text.split('\n')[-10:]

        lines_str = ''.join(lines)

        lines_str = lines_str.replace('\r', ' ')



        name_pattern = r"\[(.*?)\/"

        matches_names = re.findall(name_pattern, lines_str)



        pattern = r"\d{1,2}[/]\d{1,2}"

        matches = re.findall(pattern, lines_str)



        EQP_pattern = r"(?i)(\w{2}MC\d{2})"

        matches_EQP = re.findall(EQP_pattern, lines_str)



        EQP_Group = ['I']



        name = matches_names[0]



        try:

            # 날짜 o , 설비 o 둘다 요청한 경우 ERROR 발송

            if matches and matches_EQP:

                pyperclip.copy(f"{name} 님..설비(I), 날짜(4/12) 하나만 요청해주세요.\n")

                data_send()

                close_excel()



            # 날짜 o, 설비x

            elif matches and not matches_EQP:

                try:

                    recent_date = datetime.datetime.strptime(matches[-1], '%m/%d').date()

                    today = datetime.datetime.now().strftime('%m/%d')

                    today = datetime.datetime.strptime(today, '%m/%d').date()

                    if recent_date > today:

                        pyperclip.copy(f"{name} 님..미래의 인폼은 아직 작성되지 않았어요.\n")

                        data_send()

                        close_excel()

                    else:

                        return recent_date



                except ValueError:

                    pyperclip.copy(f"{name} 님..올바른 날짜 형식이 아니예요...\n")

                    data_send()

                    close_excel()



            # 날짜x, 설비o

            elif matches_EQP and not matches:

                if matches_EQP[-1].upper() in EQP_Group:

                    return matches_EQP[-1].upper()

                else:

                    pyperclip.copy(f"{name}님..{matches_EQP[-1]}는\nEQP gorup에 존재하지 않아요.\n")

                    data_send()

                    close_excel()



        # 에러

        except ValueError:

            pyperclip.copy(f"{name} 님..설비(I) 데이터또는 날짜(4/12) 데이터를 인식하지 못했어요."

                          f"\n 혹시 2개를 동시에 요청하셨다면 하나만 요청 해주세요.")

            data_send()

            close_excel()

    Hi_sending()
    Summary_open()
    pythoncom.CoInitialize()
    open_messenger_date()
    date_date = find_recent_date()



    # 날짜x, 설비x

    if date_date == None :

        pyperclip.copy(f"{name} 님..설비(I) 데이터또는 날짜(4/12) 데이터를 인식하지 못했어요."

                      f"\n 혹시 2개를 동시에 요청하셨다면 하나만 요청 해주세요.")

        data_send()

        close_excel()



    # 날짜 데이터인 경우

    elif re.match(r"\d{4}-\d{2}-\d{2}", str(date_date)):



        date_str_need = date_date.strftime('%#m/%#d')

        pythoncom.CoInitialize()

        excel = win32com.client.Dispatch('Excel.Application')

        workbook = excel.ActiveWorkbook

        sheet = workbook.Worksheets('MC Inform')

        date_col = sheet.Range('2:2').Find('날짜').Column

        last_row = sheet.UsedRange.Row + sheet.UsedRange.Rows.Count - 1

        row_data = ''

        data_to_copy = []

        for row in range(last_row, 3, -1):

            date_value = sheet.Cells(row, date_col).Value

            if isinstance(date_value, datetime.datetime):

                date_set = date_value.strftime('%Y-%m-%d')

                date_str = date_value.strftime('%#m/%#d')

                if date_str == date_str_need:

                    row_data = [date_set] + [str(sheet.Cells(row, col).Value) for col in range(3, 7)]

                    data_to_copy.insert(0, '\n'.join(row_data))

                    data_to_copy.insert(1, '----------------------------------------')

            else:

                if data_to_copy:

                    pyperclip.copy('\n'.join(data_to_copy))

                    data_to_copy = []

        row_text = str(pyperclip.paste())



        if not row_text:

            row_text = f"{name}님이 요청하신 \n{date_str_need}날짜의 inform 은 없습니다."

            pyperclip.copy(row_text)

            Non_data_send()



        row_text = f"{name}님이 요청하신 \n{date_str_need}날짜의 inform 입니다.\n\n {row_text}"

        row_text = row_text.replace('None', '')

        pyperclip.copy(row_text)

        data_send()

        close_excel()



    # 장비인 경우

    else :

        pythoncom.CoInitialize()

        excel = win32com.client.Dispatch('Excel.Application')

        workbook = excel.ActiveWorkbook

        sheet = workbook.Worksheets('MC Inform')

        date_col = sheet.Range('2:2').Find('날짜').Column

        EQP_col = sheet.Range('2:2').Find('EQP ID').Column

        last_row = sheet.UsedRange.Row + sheet.UsedRange.Rows.Count - 1

        EQP_to_copy = []

        for row in range(last_row, 3, -1):

            EQP_value = sheet.Cells(row, EQP_col).Value

            if EQP_value == date_date:



                date_value = sheet.Cells(row, date_col).Value

                date_set = date_value.strftime('%Y-%m-%d')

                merge_range = sheet.Cells(row, EQP_col).MergeArea



                # 병합된 셀의 경우

                if merge_range.MergeCells:

                    merge_row = merge_range.Rows.Count

                    EQP_to_copy_merge = []

                    for r in range(row, row + merge_row):

                        row_data = [date_set] + [str(sheet.Cells(r, col).Value) for col in range(3, 7)]

                        EQP_to_copy_merge.append('\n'.join(row_data))

                        EQP_to_copy_merge.append('')

                    EQP_to_copy.insert(0, '\n'.join(EQP_to_copy_merge))

                    EQP_to_copy.insert(1, 'ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')



                # 병합되지 않은 개별 셀인 경우

                else:

                    row_data = [date_set] + [str(sheet.Cells(row, col).Value) for col in range(3, 7)]

                    EQP_to_copy.insert(0, '\n'.join(row_data))

                    EQP_to_copy.insert(1, 'ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')

                if len(EQP_to_copy) >= 10:

                    break

            else:

                pass



        pyperclip.copy('\n'.join(EQP_to_copy))

        row_text = str(pyperclip.paste())



    if not row_text:

        row_text = f"{name}님이 요청하신 \n{date_date}호기의 inform 은 없습니다."

        pyperclip.copy(row_text)

        Non_data_send()

    row_text = f"{name}님이 요청하신 \n{date_date}호기의 inform 입니다.\n\n {row_text}"

    row_text = row_text.replace('None', '')

    pyperclip.copy(row_text)

    data_send()

    close_excel()
    '''

def remove_all():

    import os

    global save_path

    folder_path = save_path

    # 경로에 있는 모든 파일 목록 가져오기

    file_list = os.listdir(folder_path)

    # 모든 파일 삭제하기

    for file_name in file_list:

        file_path = os.path.join(folder_path, file_name)

        os.remove(file_path)

def update_log(message):

    global save_path_log

    current_time = time.strftime("%m/%d %H:%M:%S")

    log_message = f"{current_time} {message}"

    log.append(log_message)



    # 최근 3개만 출력

    ## 4로 변경 필요

    if len(log) > 15:

        log.pop(0)

    # 로그 출력

    log_text.delete('1.0', END)  # 기존 로그 삭제

    log_text.insert(END, "\n".join(log))



    # 스크롤바를 항상 마지막 로그로 이동

    log_text.yview_moveto(1.0)



    # 로그 파일에도 메시지를 기록

    log_file_path = os.path.join(save_path_log, "log.txt")



    if not os.path.exists(log_file_path):

        open(log_file_path, "w").close()  # 빈 파일 생성



    with open(log_file_path, "a") as f:



        f.write(f"{log_message}\n")

def stop_program_thread():
    global stop_program, program_start

    try :
        stop_program = True
        stop_timer()
        program_start = False

    except :
        pass
# Timeout shield 끝나고 실행되는 함수
def resume_program_thread():
    try :
        resume_detection()
        time.sleep(1)
    except :
        pass

def on_exit():

    root.quit()

    root.destroy()

# Timer count label
def update_timer_label():
    # 레이블에 타이머 시간 표시
    global count, initial_count, timer_stop, Timeout_shield_thread, timer_start, Timeout_end
    if  timer_stop == False :
        timer_label.config(text="Timeout 남은시간: {}초".format(count))
        count -= 1
        if count < 0 :
            ## shield 실행
            stop_program_thread()
            start_timeout_shield()
        elif count >= 0 :
            timer_label.after(1010, update_timer_label)

    else :
        timer_label.config(text="Timeout 일시 중지")

def stop_timer():
    global timer_stop
    timer_label.config(text="Timeout 일시 중지")
    timer_stop = True

def resume_timer() :
    global count, timer_stop
    count += 5
    timer_stop = False
    update_timer_label()

def reset_timer():

    global initial_count, count, timer_stop

    count = initial_count

    timer_stop = False

def start_timeout_shield():
    global Timeout_shield_thread
    Timeout_shield_thread = threading.Thread(target=Timeout_shield)
    Timeout_shield_thread.daemon = True
    Timeout_shield_thread.start()

# Knox logout 부수기
def Timeout_shield():
    # 계산기 실행 후 종료
    global Timeout_end
    def terminate_process_by_name(process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                proc.terminate()

    # 프로그램 완전 중지
    sec = int(entry_sec.get())
    sec += 1
    time.sleep(sec)

    update_log("Timeout 실행")
    # 계산기 실행
    calculator_process = psutil.Popen("calc.exe")
    # 대기 시간 설정 (예: 10초)
    timeout = 5
    time.sleep(timeout)

    # 계산기 프로세스 종료
    terminate_process_by_name("CalculatorApp.exe")

    ######## Resume조건들
    time.sleep(1)
    reset_timer()
    timer_label.after(1010, update_timer_label)

    resume_program_thread()

    '''
    import getpass
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    global count

    time.sleep(2)
    username = getpass.getuser()
    driver_path = r"C:\\Users\\{}\\Documents\\informer\\driver\\msedgedriver.exe".format(username)
    url = "https://w"
    time.sleep(1)

    try :
        driver = webdriver.Edge(executable_path=driver_path)
        driver.get(url)
        wait = WebDriverWait(driver, 13)
        time.sleep(2)
        button = wait.until(EC.element_to_be_clickable((By.ID, "g")))
        button.click()
        time.sleep(2)
        button = wait.until(EC.element_to_be_clickable((By.ID, "m")))
        button.click()
        time.sleep(2)
        button = driver.find_element_by_id("m")
        button.click()

    except:
        if driver is not None:
            driver.quit()
        time.sleep(2)
        driver = webdriver.Edge(executable_path=driver_path)
        driver.get(url)
        wait = WebDriverWait(driver, 13)
        button = wait.until(EC.element_to_be_clickable((By.ID, "m")))
        button.click()
        time.sleep(2)
        button = driver.find_element_by_id("m")
        button.click()


    driver.quit()
    '''
################# GUI ################
# Tk 객체 생
root = tk.Tk()
root.iconbitmap(icon_path)

# 윈도우 크기 조정
root.geometry("260x450")
# 윈도우 타이틀 설정
root.title("informer")

# x1, y1, x2, y2 값을 입력받기 위한 Entry 위젯 생성
label0 = tk.Label(root, text="X1,Y1,X2,Y2")
label0.pack(pady=0)
x1_entry = tk.Entry(root)
y1_entry = tk.Entry(root)
x2_entry = tk.Entry(root)
y2_entry = tk.Entry(root)
x1_entry.insert(0, "0")
y1_entry.insert(0, "0")
x2_entry.insert(0, "370")
y2_entry.insert(0, "400")
x1_entry.pack(padx=5, pady=0)
y1_entry.pack(padx=5, pady=0)
x2_entry.pack(padx=5, pady=0)
y2_entry.pack(padx=5, pady=0)

# 라벨 위젯 생성
label1 = tk.Label(root, text="시간 간격 (초)을 입력하세요")
label1.pack(pady=5)

# 엔트리 위젯 생성
entry_sec = tk.Entry(root)
entry_sec.pack(pady=0)
entry_sec.insert(0,"5")

# 실행 버튼
program_start = False
button = tk.Button(root, text="실행", command=run_detection, width=20, height=1)
button.pack(pady=2)

# 중단 버튼
button = tk.Button(root, text="중단", command=stop_program_thread, width=20, height=1)
button.pack(pady=2)

# 종료 버튼
exit_button = tk.Button(root, text="종료", command=on_exit, width=20, height=1)
exit_button.pack(pady=2)

# timer
timer_label = tk.Label(root, text="Timeout 남은시간: {}초".format(initial_count))
timer_label.pack(pady=5)
reset_timer()
update_timer_label()

################  Log 창  #####################
# 로그창을 담을 Text 위젯 생성
log_text = tk.Text(root)
log_text.pack(side=LEFT, fill=BOTH, expand=True, pady=5)
# 스크롤바를 담을 Scrollbar 위젯 생성
scrollbar = tk.Scrollbar(root, command=log_text.yview)
# 스크롤바와 Text 위젯 연결
log_text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
# 로그창에 텍스트 추가
log_text.insert(END, "작동 대기 중")
###############################################

root.mainloop()