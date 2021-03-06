import time, win32con, win32api, win32gui
import requests
from bs4 import BeautifulSoup
import schedule
#from apscheduler.schedulers.background import BackgroundScheduler


# # 카톡창 이름, (활성화 상태의 열려있는 창)
kakao_opentalk_name = '연습'


# # 채팅방에 메시지 전송
def kakao_sendtext(chatroom_name, text):
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow( None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx( hwndMain, None, "RICHEDIT50W", None)

    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwndEdit)


# # 엔터
def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


# # 채팅방 열기
def open_chatroom(chatroom_name):
    # # # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위하여)
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx( hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx( hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx( hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx( hwndkakao_edit2_2, None, "Edit", None)

    # # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
    win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(1)   # 안정성 위해 필요
    SendReturn(hwndkakao_edit3)
    time.sleep(1)


# # 혈액관리본부 혈액보유량 리턴
def bloodstockinfo():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    url = 'https://www.bloodinfo.net/bloodstats_stocks.do'
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.select('table.table.mb10 > tbody > tr:nth-of-type(3)')

    a = []
    a_list=[]
    for item in data:
        a.append(item.get_text())


    s = "\n".join(a)
    a_list = s.split()
    prints = {
        " 합계 ": a_list[1],
        " O형":   a_list[2],
        " A형":   a_list[3],
        " B형":   a_list[4],
        "AB형 ":  a_list[5],
    }

    return prints


# # 스케줄러 morning_1
def morning_1():
    p_time_ymd_hms = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}기준 적혈구제제 보유현황"


    open_chatroom(kakao_opentalk_name)  # 채팅방 열기
    stockinfo = bloodstockinfo()  # 혈액보유량 크롤링
    kakao_sendtext(kakao_opentalk_name, f"{p_time_ymd_hms}\n{stockinfo}")  # 메시지 전송, time/혈액보유량



def main():
    #sched = BackgroundScheduler()
    #sched.start()
    #sched.add_job(morning_1, 'cron', second='*/5', id="test_1")

    #매일 오전 10시 30분에 실행
    #schedule.every().day.at("10:30").do(morning_1)

    #10초에 한번씩 실행
    schedule.every(10).seconds.do(morning_1)

    count = 0
    while True:
        schedule.run_pending()
        print("실행중입니다.")
        time.sleep(1)


if __name__ == '__main__':
    main()