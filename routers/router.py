from fastapi import APIRouter
from aws_config import get_ssm_parameter
from schemas.review_check import ReviewCheckRequest

from utils.shared import tasks
from utils.task_logic import send_post_request

import logging
# 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 파일 핸들러 설정
file_handler = logging.FileHandler('logging.log')
file_handler.setLevel(logging.DEBUG)

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 포맷터 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 핸들러 추가
logger.addHandler(file_handler)
logger.addHandler(console_handler)

router = APIRouter()

# 실제 서버
backend_url_param = "/config/ktb22/backend.server.url"

# # 테스트
# backend_url_param = "/config/ktb22/backend.test.url"

# 각 파라미터 값 가져오기
BACKEND_URL = get_ssm_parameter(backend_url_param)

@router.post("/")
async def process_review_request(request: ReviewCheckRequest):
    # 작업 ID로 받은 requestID 사용
    task_id = request.requestId
    tasks[task_id] = {"status": "PENDING", "result": None}

    logger.info(f"1. Got request from: {request.blogUrl}")

    payload = {
      "requestId": "123e4567-e89b-12d3-a456-426614174000",
      "blogUrl": "https://blog.naver.com/example/12345",
      "summaryTitle": "Suspicious Review",
      "summaryText": "The review contains repetitive phrases and unnatural language patterns.",
      "score": 35,
      "evidence": "Identical review across multiple posts."
    }

    logger.info(f"2. input dummydata: {payload}")

    # await send_post_request(BACKEND_URL, payload)
    import asyncio
    asyncio.create_task(send_post_request(BACKEND_URL, payload))

    logger.info(f"3. : after send_post_request")

    return {"message": "Request received. Processing started.", "requestId": task_id}

if __name__ == "__main__":
    # 더미 데이터 생성
    task_id = "123e4567-e89b-12d3-a456-426614174000"