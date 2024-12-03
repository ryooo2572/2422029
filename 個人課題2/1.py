import requests
import flet as ft
from datetime import datetime

AREA_LIST_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"

def get_area_list():
    response = requests.get(AREA_LIST_URL)
    response.raise_for_status()
    area_data = response.json()
    areas = []

   
    for region_code, region_info in area_data['offices'].items():
        areas.append((region_code, region_info['name']))
    return areas

def get_weather_forecast(region_code):
    forecast_url = FORECAST_URL_TEMPLATE.format(region_code)
    response = requests.get(forecast_url)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
        return [{"date": "N/A", "weather": "取得エラー", "tempMax": "N/A", "tempMin": "N/A"}]

    forecast_data = response.json()

    weather_data = []

    try:
        area_forecasts = forecast_data[0]['timeSeries'][0]['areas']
        date_series = forecast_data[0]['timeSeries'][0]['timeDefines']

    
        temp_max_series = None
        temp_min_series = None
        for time_series in forecast_data:
            for series in time_series['timeSeries']:
                if 'tempsMax' in series['areas'][0]:
                    temp_max_series = series['areas'][0]['tempsMax']
                if 'tempsMin' in series['areas'][0]:
                    temp_min_series = series['areas'][0]['tempsMin']

    
        for i in range(3):  
            date = datetime.strptime(date_series[i], "%Y-%m-%dT%H:%M:%S%z").date()
            weather = area_forecasts[0]['weathers'][i]
            temp_max = temp_max_series[i] if temp_max_series and len(temp_max_series) > i else "N/A"
            temp_min = temp_min_series[i] if temp_min_series and len(temp_min_series) > i else "N/A"
            weather_data.append({
                "date": date,
                "weather": weather,
                "tempMax": temp_max,
                "tempMin": temp_min
            })

    except (IndexError, KeyError) as e:
        print(f"Data Error: {e}")
        return [{"date": "N/A", "weather": "データ取得エラー", "tempMax": "N/A", "tempMin": "N/A"}]

    return weather_data

def main(page: ft.Page):
    areas = get_area_list()

    dropdown = ft.Dropdown(
        label="地域を選択してください",
        hint_text="地域",
        options=[ft.dropdown.Option(key=code, text=name) for code, name in areas]
    )

    weather_info = ft.Row(wrap=True, spacing=10)   

    def on_area_select(e):
        region_code = dropdown.value
        print(f"Selected region code: {region_code}")  
        if region_code:
            weather_info.controls.clear()
            forecast = get_weather_forecast(region_code)
            for day in forecast:
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"日付: {day['date']}"),
                                ft.Text(f"天気: {day['weather']}"),
                                ft.Text(f"最高気温: {day['tempMax']}"),
                                ft.Text(f"最低気温: {day['tempMin']}"),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=10,
                    ),
                    elevation=5,
                )
                weather_info.controls.append(card)
            page.update()

    dropdown.on_change = on_area_select

    page.add(
        ft.Column(
            [
                ft.Text("天気予報アプリケーション", size=24, weight="bold"),
                dropdown,
                weather_info
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)