import requests
import json
import time
import sys
from dotenv import load_dotenv
import os

load_dotenv()

def get_channel_list(headers):
    r = requests.get("https://slack.com/api/conversations.list", headers=headers)
    json = r.json()

    # Public Channel ID를 저장
    channels = []

    # 최대 100개의 채널까지
    for channel in json["channels"]:
        channels.append(channel["id"])

    time.sleep(1)
    print("사내 공개 채널 수: ", len(channels))
    return channels


def count_emoji(channels, headers):
    # 이모지 저장
    emojis = {}
    channel_count = 0
    for channel in channels:
        param = {}
        param.update(count=1000, channel=channel, inclusive=1)
        r = requests.get("https://slack.com/api/conversations.history", headers=headers, params=param)
        json = r.json()

        # 메시지가 없을 때
        if "messages" in json == False:
            continue

        # 채널의 메시지 (최대 1000개 메시지까지)
        for message in json["messages"]:
            if "reactions" in message:
                # 종류
                for reaction in message["reactions"]:
                    # 집계 목록
                    if reaction["name"] in emojis:
                        emojis[reaction["name"]] += reaction["count"]
                    else:
                        emojis[reaction["name"]] = reaction["count"]

        # 1초 슬립
        channel_count += 1
        print(f"현재 {int(round(channel_count / len(channels) * 100))}% 완료",)
        time.sleep(1)

    print("이모지 추출 성공!")
    print("이모지 수: ", len(emojis))
    return emojis

# ------------------------
# 사용 횟수가 많은 순서로 이모티콘 30개 정렬
# ------------------------
def sort_30(emojis):
    emojis_sorted = sorted(emojis.items(), key=lambda x: x[1], reverse=True)[:30]
    return emojis_sorted

if __name__ == '__main__':
    # slack user token
    token = os.getenv("TOKEN")

    if token is None:
        print("환경변수에 토큰이 설정되어 있지 않습니다.")
    else:
        print("불러온 토큰 값:", token)
        params = {"token": token}
        headers = {
            "Authorization":  f"Bearer {params['token']}"
        }
        channels = get_channel_list(headers)
        emojis = count_emoji(channels, headers)
        emojis_sorted = sort_30(emojis)

        # 결과 파일로 출력
        print('결과 파일로 출력 중')
        time.sleep(1)
        print('결과 파일로 출력 중.')
        time.sleep(1)
        print('결과 파일로 출력 중..')
        time.sleep(1)
        print('결과 파일로 출력 중...')
        time.sleep(1)
        f = open('result.txt', 'w')
        for data in emojis_sorted:
            f.write(str(data).replace("'",":") + "\n")
        f.close()
        time.sleep(1)
        print('결과 파일로 출력 완료!')
