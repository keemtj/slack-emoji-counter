# 사내 슬랙에서 이모지 TOP 30 추출하기

기존 소스 코드에서 api 요청 및 변수 선언이 잘못된 부분이 있어 새로 수정한 소스코드입니다.

> 이전 코드 출처: https://qiita.com/leechungkyu/items/e822d8836b465a334fc9

### 이용 방법

1. python3 설치
2. requests, python-dotenv 모듈 설치
3. slack에서 발급받은 token을 .env에 저장
4. python3 get_emoji_count.py 실행
