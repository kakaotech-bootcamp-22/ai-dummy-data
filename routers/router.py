from fastapi import APIRouter

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from aws_config import get_ssm_parameter
from schemas.review_check import ReviewCheckRequest
from utils.prediction_logic import process_and_predict_from_url

from utils.shared import tasks
from utils.task_logic import send_post_request

router = APIRouter()

# Selenium WebDriver 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# chrome_options = Options()
# chrome_options.add_argument("--headless")  # 헤드리스 모드
# chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
# chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안 함 (Docker에서 메모리 문제 해결)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#백엔드 서버 파라미터 경로
# backend_url_param = "/config/ktb22/backend.server.url"

## 실제 서버
# backend_url_param = "/config/ktb22/backend.server.url"

# 테스트
backend_url_param = "/config/ktb22/backend.test.url"

# 각 파라미터 값 가져오기
BACKEND_URL = get_ssm_parameter(backend_url_param)

@router.post("/")
async def process_review_request(request: ReviewCheckRequest):
    # 작업 ID로 받은 requestID 사용
    task_id = request.requestId
    tasks[task_id] = {"status": "PENDING", "result": None}

    payload = {
      "requestId": "123e4567-e89b-12d3-a456-426614174000",
      "blogUrl": "https://blog.naver.com/example/12345",
      "summaryTitle": "Suspicious Review",
      "summaryText": "The review contains repetitive phrases and unnatural language patterns.",
      "score": 35,
      "evidence": "Identical review across multiple posts."
    }

    await send_post_request(BACKEND_URL, payload)

    return {"message": "Request received. Processing started.", "requestId": task_id}

if __name__ == "__main__":
    # 더미 데이터 생성
    task_id = "123e4567-e89b-12d3-a456-426614174000"