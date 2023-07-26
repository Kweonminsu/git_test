from tkinter import Tk, ttk
from ctypes import windll


class app(Tk):
  def __init__(self, **args):
    super().__init__(**args)
    # init: 윈도우 기본 설정
    self.title("제목표시줄 교체")
    self.overrideredirect(True)
    self.iconbitmap("app.ico")
    self.minsize(300, 200)
    self.after(0, self._set_window)

    # init: 요소 정의하기
    titlebar = ttk.Frame(self, style="titlebar.TFrame")
    widget = ttk.Frame(self)
    title = ttk.Label(
        titlebar, text=self.title(), style="titlebar.TLabel")
    close = ttk.Button(
        titlebar, text='X', takefocus=False, command=self.on_exit)
    label = ttk.Label(
        widget, text="위젯영역")

    # init: 요소 배치하기
    titlebar.pack(side='top', fill='x', expand='no')
    widget.pack(side='bottom', fill='both', expand='yes')
    title.pack(side='left', fill='x', expand='yes', pady=4)
    close.pack(side='right')
    label.pack()

    # 요소에 함수 바인딩하기
    # <ButtonPress-1>: 마우스 왼쪽 버튼을 누름
    # <ButtonRelease-1>: 마우스 왼쪽 버튼을 뗌
    # <Double-Button-1>: 마우스 왼쪽 더블클릭
    # <B1-Motion>: 마우스를 클릭한 상태로 움직임
    title.bind("<ButtonPress-1>", self.start_move)
    title.bind("<ButtonRelease-1>", self.stop_move)
    title.bind("<Double-Button-1>", self.on_maximise)
    title.bind("<B1-Motion>", self.on_move)

  def on_maximise(self, event):
    # 창의 제목을 더블클릭
    # 최대화와 복원을 토글
    if self.state() == 'normal':
      self.state("zoomed")
    else:
      self.state("normal")

  def start_move(self, event):
    # 창의 제목을 클릭
    # 위치 변수 등록
    self.x = event.x
    self.y = event.y

  def stop_move(self, event):
    # 마우스를 뗌
    # 변수 초기화
    self.x = None
    self.y = None

  def on_move(self, event):
    # 마우스 드래그
    # 윈도우를 이동
    deltax = event.x - self.x
    deltay = event.y - self.y
    x = self.winfo_x() + deltax
    y = self.winfo_y() + deltay
    self.geometry("+%s+%s" % (x, y))

  def on_exit(self):
    # 종료 버튼 클릭
    # GUI를 끝냄
    self.destroy()

  def _set_window(self):
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    hwnd = windll.user32.GetParent(self.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    self.wm_withdraw()
    self.after(0, lambda: self.wm_deiconify())


if __name__ == "__main__":
  app().mainloop()