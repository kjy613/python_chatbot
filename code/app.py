from slack_sdk.rtm_v2 import RTMClient
from slack_sdk import WebClient
from weather_info_parser import WeatherInfoParser
from dotenv import load_dotenv
import os

load_dotenv()

rtm = RTMClient(token=os.getenv('slack_token'))
web_client = WebClient(token=os.getenv('slack_token'))
weather_info_parser = WeatherInfoParser()

# 채팅의 마지막 두 글자가 날씨로 끝나는지 확인
# httpx 모듈 사용해서 네이버에서 채팅글을 검색
# 요청에 대한 응답에서 필요한 데이터를 추출
# 추출한 데이터를 slack에 표시

@rtm.on("message")
def handle(client: RTMClient, event: dict):
    keyword: str = event['text']
    if  keyword.endswith('날씨'):
        weather_info = weather_info_parser.getWeatherInfo(keyword=keyword)

        channel_id = event['channel']

        client.web_client.chat_postMessage(
            channel=channel_id,
            blocks=[        #list 타입으로 데이터 전달받음 그 list는 dictionary 타입을 데이터로 가짐
                {'type':'divider'},
                {
                    'type':'section',
                    'text':{
                        'type':'plain_text',
                        'text':f'{weather_info.area}'
                    }
                },
                {'type':'divider'},
                                {
                    'type':'section',
                    'text':{
                        'type':'plain_text',
                        'text':f"""{weather_info.weather_today}
현재 기온 : {weather_info.temperature_now}
최고 기온 : {weather_info.temperature_high}
최저 기온 : {weather_info.temperature_low}
"""
                    }
                },
            ],
        )
        weather_info_parser.getScreenshot(keyword=keyword)

        web_client.files_upload_v2(
            channel=channel_id,
            file='info.png',
            title='날씨 정보',
        )

rtm.start() # 원래 connect로 되어있었는데 connect로 계속 두면 while문에서 connect함수 호출하도록 수정해줘야 함