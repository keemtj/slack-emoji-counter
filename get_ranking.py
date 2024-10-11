import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드
load_dotenv()

# 환경 변수에서 API 토큰과 채널 ID 가져오기
SLACK_API_RANKING_TOKEN = os.getenv('SLACK_API_RANKING_TOKEN') # your slack token
SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID') # your channel id

# 슬랙 API에서 메시지 가져오기
def fetch_channel_messages(channel_id, limit=1000):
    url = 'https://slack.com/api/conversations.history'
    headers = {'Authorization': f'Bearer {SLACK_API_RANKING_TOKEN}'}
    params = {'channel': channel_id, 'limit': limit}
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()
    if response_data.get('ok'):
        return response_data.get('messages', [])
    else:
        print(f"Error fetching messages: {response_data.get('error')}")
        return []

# 메시지 작성자별 메시지 수 카운트
def count_messages_by_user(messages):
    user_message_count = {}
    for message in messages:
        user = message.get('user')
        if user:
            user_message_count[user] = user_message_count.get(user, 0) + 1
    return user_message_count

# 이모지 반응 사용자별 카운트
def count_reactions_by_user(messages):
    user_reaction_count = {}
    for message in messages:
        reactions = message.get('reactions', [])
        for reaction in reactions:
            for user in reaction.get('users', []):
                user_reaction_count[user] = user_reaction_count.get(user, 0) + 1
    return user_reaction_count

# 이모지별 사용 횟수 카운트
def count_emoji_usage(messages):
    emoji_count = {}
    for message in messages:
        reactions = message.get('reactions', [])
        for reaction in reactions:
            emoji = reaction.get('name')
            emoji_count[emoji] = emoji_count.get(emoji, 0) + reaction.get('count', 0)
    return emoji_count

# 유저 ID를 이름으로 변환 (display_name 또는 real_name 사용)
def get_user_names(user_ids):
    url = 'https://slack.com/api/users.list'
    headers = {'Authorization': f'Bearer {SLACK_API_RANKING_TOKEN}'}
    response = requests.get(url, headers=headers)
    users = response.json().get('members', [])

    user_dict = {}
    for user in users:
        user_id = user['id']
        profile = user.get('profile', {})

        # real_name 또는 display_name을 사용
        user_name = profile.get('real_name') or profile.get('display_name') or 'Unknown User'

        user_dict[user_id] = user_name

    return {user_id: user_dict.get(user_id, 'Unknown User') for user_id in user_ids}

# 슬랙 데이터 분석 실행
def analyze_slack_channel():
    messages = fetch_channel_messages(SLACK_CHANNEL_ID)

    # 메시지 수 카운트
    user_message_count = count_messages_by_user(messages)
    sorted_users_by_message = sorted(user_message_count.items(), key=lambda x: x[1], reverse=True)

    # 이모지 반응 수 카운트
    user_reaction_count = count_reactions_by_user(messages)
    sorted_users_by_reactions = sorted(user_reaction_count.items(), key=lambda x: x[1], reverse=True)

    # 이모지 사용 횟수 카운트
    emoji_count = count_emoji_usage(messages)
    sorted_emojis = sorted(emoji_count.items(), key=lambda x: x[1], reverse=True)

    # 유저 이름 조회
    user_ids = set([user for user, _ in sorted_users_by_message] + [user for user, _ in sorted_users_by_reactions])
    user_names = get_user_names(user_ids)

    # 결과 출력
    print("\n가장 많이 게시글을 올린 사람 Top 10:")
    for user, count in sorted_users_by_message[:10]:
        print(f"{user_names[user]}: {count}개의 메시지")

    print("\n가장 많이 이모지를 단 사람 Top 10:")
    for user, count in sorted_users_by_reactions[:10]:
        print(f"{user_names[user]}: {count}개의 이모지 반응")

    print("\n가장 많이 사용된 이모지 Top 10:")
    for emoji, count in sorted_emojis[:10]:
        print(f":{emoji}: {count}번 사용됨")

# 분석 실행
analyze_slack_channel()