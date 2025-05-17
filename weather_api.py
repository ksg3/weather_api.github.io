import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

API_KEY = "여기에 api_key"


LOCATION_GRID = {
    "서울": (60, 127),
    "부산": (98, 76),
    "대구": (89, 90),
    "광주": (58, 74),
    "대전": (67, 100),
    "춘천": (73, 134),
    "제주": (52, 38),
}

def get_weather_data(x, y):
    # 오늘 날짜 및 기준 시간 설정
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = "0500"  # 단기예보 API는 3시간 간격으로 제공됨 (예: 0500, 0800 등)

    url = (
        f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
        f"?serviceKey={API_KEY}"
        f"&pageNo=1&numOfRows=1000&dataType=JSON"
        f"&base_date={base_date}&base_time={base_time}"
        f"&nx={x}&ny={y}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data['response']['body']['items']['item']
        weather_info = {}

        for item in items:
            category = item['category']
            fcst_time = item['fcstTime']
            fcst_value = item['fcstValue']
            if fcst_time not in weather_info:
                weather_info[fcst_time] = {}
            weather_info[fcst_time][category] = fcst_value
        return weather_info
    else:
        return None

def show_weather():
    city = city_var.get()
    x, y = LOCATION_GRID.get(city, (60, 127))  
    weather_data = get_weather_data(x, y)

    if weather_data:
        output_text.delete(1.0, tk.END)
        for time, values in sorted(weather_data.items()):
            output_text.insert(tk.END, f"[{time[:2]}시 예보]\n")
            tmp = values.get("TMP", "N/A")   # 기온
            pty = values.get("PTY", "0")     # 강수형태 (0: 없음, 1: 비, 2: 비/눈, 3: 눈)
            pty_dict = {"0": "없음", "1": "비", "2": "비/눈", "3": "눈", "4": "소나기"}
            sky = values.get("SKY", "1")     # 하늘상태 (1: 맑음, 3: 구름많음, 4: 흐림)
            sky_dict = {"1": "맑음", "3": "구름많음", "4": "흐림"}
            output_text.insert(tk.END, f"  기온: {tmp}℃\n")
            output_text.insert(tk.END, f"  강수: {pty_dict.get(pty, '알수없음')}\n")
            output_text.insert(tk.END, f"  하늘: {sky_dict.get(sky, '알수없음')}\n\n")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "날씨 정보를 가져올 수 없습니다.")

# GUI 설정
root = tk.Tk()
root.title("기상청 날씨 앱")

tk.Label(root, text="지역 선택:").pack()
city_var = tk.StringVar()
city_dropdown = ttk.Combobox(root, textvariable=city_var)
city_dropdown['values'] = list(LOCATION_GRID.keys())
city_dropdown.set("서울")
city_dropdown.pack()

tk.Button(root, text="날씨 조회", command=show_weather).pack()

output_text = tk.Text(root, height=25, width=50)
output_text.pack()

root.mainloop()
