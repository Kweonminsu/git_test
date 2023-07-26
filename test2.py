import pygetwindow as gw
import pywinauto

def run_notepad_in_background():
    # 메모장 실행
    app = pywinauto.Application(backend="uia").start('notepad.exe')

    # 메모장 창을 숨깁니다.
    app.top_window().minimize()

# 메모장 실행
run_notepad_in_background()
