from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import csv
from youtube_transcript_api import YouTubeTranscriptApi

# .env 파일 로드
load_dotenv()

def generate_transcript_by_recipe_name(recipe_name):
    # API 키 설정
    api_key = os.getenv('YOUTUBE_API_KEY')

    # YouTube Data API v3 클라이언트 생성
    youtube = build('youtube', 'v3', developerKey=api_key)

    # 검색할 키워드 지정
    search_keyword = recipe_name

    # 검색 API 호출
    search_response = youtube.search().list(
        q=search_keyword,
        type='video',
        part='id',
        videoDuration='medium',  # 동영상 길이 짧은 것으로 제한
        maxResults=3  # 가져올 결과 수 (1, 2, 3위까지)
    ).execute()

    data_folder = 'data/'+recipe_name
    os.makedirs(data_folder, exist_ok=True)
    csv_file_path = os.path.join(data_folder, 'id.csv')
    video_data = []

    # 결과를 리스트에 추가
    for item in search_response['items']:
        video_id = item['id']['videoId']
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        with open('./'+data_folder+'/'+video_id+'.txt', 'w') as file:
            for line in transcript:
                file.write(line['text'] + '\n')
        video_data.append({'id': video_id})

    # CSV 파일에 데이터 쓰기
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 헤더 쓰기
        writer.writeheader()

        # 데이터 쓰기
        for data in video_data:
            writer.writerow(data)

    print(f'Data has been written to {csv_file_path}')
