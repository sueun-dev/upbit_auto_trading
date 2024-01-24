import requests
from bs4 import BeautifulSoup
from news_analyzer import analyze_sentiment
import schedule
import datetime
import time

sentiment_counts = {
    'Neutral': 0,
    'Negative': 0,
    'Positive': 0
}

# ┌─────────────────────────────────────────────────────────────────┐
# │ fetch_page_content 함수                                          │
# │ - 주어진 URL에서 웹 페이지의 HTML 내용을 가져오기                         │
# │ - requests를 사용하여 웹 페이지에 요청을 보내고, 받은 응답을                │
# │   BeautifulSoup 객체로 파싱하여 반환                                 │
# └─────────────────────────────────────────────────────────────────┘
def fetch_page_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

# ┌─────────────────────────────────────────────────────────────────┐
# │ parse_news_article 함수                                          │
# │ - 개별 뉴스 기사를 파싱하여 필요한 정보(제목, 링크, 요약, 시간)를 추출         │                                               │
# │ - 기존에 저장된 제목들과 비교하여 중복되면 None을 반환하여                   │
# │   중복 기사 스킵                                                   │
# └─────────────────────────────────────────────────────────────────┘
def parse_news_article(article, existing_titles):
    """
    개별 뉴스 기사를 파싱하여 필요한 정보를 추출
    기존의 제목들과 비교하여 중복되면 None을 반환
    """
    title_tag = article.find('h3', class_='zBAuLc')
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    # "No Title" 제목의 기사는 skip
    if title == "No Title" or title in existing_titles:
        return None

    link_tag = article.find('a', href=True)
    link = link_tag['href'][link_tag['href'].find('http'):link_tag['href'].find('&')] if link_tag else "No Link"

    summary_tag = article.find('div', class_='BNeawe')
    summary = summary_tag.get_text(strip=True) if summary_tag else "No Summary"

    time_tag = article.find('span', class_='r0bn4c')
    time_posted = time_tag.get_text(strip=True) if time_tag else "No Time Info"

    sentiment_title = analyze_sentiment(title)
    sentiment_summary = analyze_sentiment(summary)
    
    sentiment_counts[sentiment_title] += 1
    sentiment_counts[sentiment_summary] += 1
    
    return {
        'title': title,
        'link': link,
        'summary': summary,
        'time_posted': time_posted,
        'sentiment_title': sentiment_title,
        'sentiment_summary': sentiment_summary
    }

# ┌─────────────────────────────────────────────────────────────────┐
# │ get_existing_titles 함수                                         │
# │ - coinNews.txt 파일에서 기존에 저장된 기사 제목들을 가져오기               │
# │ - 파일이 존재하지 않을 경우 빈 리스트를 반환                              │
# └─────────────────────────────────────────────────────────────────┘
def get_existing_titles():
    titles = []
    try:
        with open("coinNews.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('Title: '):
                    titles.append(line.replace('Title: ', '').strip())
    except FileNotFoundError:
        pass  # 파일이 없으면 빈 리스트를 반환
    return titles

# ┌─────────────────────────────────────────────────────────────────┐
# │ write_article_to_file 함수                                       │
# │ - 주어진 기사 정보를 coinNews.txt 파일의 맨 위에 작성                    │
# │ - 파일을 읽고, 내용을 임시 저장한 후, 새로운 기사를 파일의 맨 위에 작성         │                                                    │
# └─────────────────────────────────────────────────────────────────┘
def write_article_to_file(article):
    with open("coinNews.txt", "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write('Title: ' + article['title'] + '\n')
        f.write('Link: ' + article['link'] + '\n')
        f.write('Summary: ' + article['summary'] + '\n')
        f.write('Time Posted: ' + article['time_posted'] + '\n')
        f.write('Sentiment Title: ' + article['sentiment_title'] + '\n')
        f.write('Sentiment Summary: ' + article['sentiment_summary'] + '\n\n')
        f.write(content)

# ┌─────────────────────────────────────────────────────────────────┐
# │ fetch_bitcoin_news 함수                                          │
# │ - Bitcoin 뉴스를 최대 2페이지까지만 가져와서 처리                         │
# │ - 각 페이지에서 새로운 기사를 찾아 파일에 저장하고, 2페이지에서                │
# │   더 이상 새로운 기사가 없으면 검색 중단                                 │
# └─────────────────────────────────────────────────────────────────┘
# 매개변수에 bitcoin, etheruem등 유동적으로 집어넣을 수 있게 수정해야함
def fetch_bitcoin_news():
    existing_titles = get_existing_titles()
    new_articles = []
    max_pages = 2

    for page in range(1, max_pages + 1):  # 최대 2페이지까지 순회
        start_index = (page - 1) * 10
        url = f"https://www.google.com/search?q=bitcoin&tbm=nws&tbs=sbd:1&start={start_index}"
        soup = fetch_page_content(url)

        for article in soup.find_all('div', class_='Gx5Zad'):
            parsed_article = parse_news_article(article, existing_titles)
            if parsed_article:
                new_articles.append(parsed_article)
                write_article_to_file(parsed_article)

    if not new_articles:
        print("No new articles found.")
        return

# ┌─────────────────────────────────────────────────────────────────┐
# │ schedule_fetching 함수                                           │
# │ - 15분마다 fetch_bitcoin_news 함수를 실행하는 스케줄을 설정              │
# │ - 프로그램 시작 시 첫 번째 뉴스 수집을 즉시 실행                           │
# └─────────────────────────────────────────────────────────────────┘
def schedule_fetching():
    # 30분마다 뉴스 소스에 직접 접근
    schedule.every(30).minutes.do(fetch_bitcoin_news)

    # 프로그램 시작 시 첫 번째 뉴스 수집을 즉시 실행
    fetch_bitcoin_news()

    while True:
        # 10분마다 깨어나 스케쥴러 확인, 만약 30분이 지났다면 해당 함수 자동 실행
        schedule.run_pending()
        print("WAIT - Program Running")
        time.sleep(600)

# 프로그램 실행
schedule_fetching()

# 프로그램 실행 예시:
# 1. 프로그램을 실행하면 schedule_fetching 함수가 호출됩니다.
# 2. schedule_fetching 함수는 30분마다 fetch_bitcoin_news 함수를
#    실행하도록 스케줄을 설정합니다.
# 3. fetch_bitcoin_news 함수는 Google 뉴스에서 최신 Bitcoin 뉴스를
#    최대 2페이지까지 검색하여 분석하고, coinNews.txt 파일에 저장합니다.
# 4. 파일에 저장된 기사 제목들은 중복 검사에 사용되어, 같은 기사가
#    반복적으로 저장되는 것을 방지합니다.


# 추가해야할 아이디어
# 하루에 4번 작동하며, 각각 txt 파일을 나눠서 관리
# - 이유 : 많은 양의 scrape은 ban 될 수 있음
# 이후 마지막 23:59분에 Today Final txt 파일 생성해서 총 Neutral, negative, positive 퍼센트 관리
# Neutral인 경우 gpt api 사용해서 전달 후 결과값 가져오기!