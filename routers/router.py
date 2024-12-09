from fastapi import APIRouter
from aws_config import get_ssm_parameter
from schemas.review_check import ReviewCheckRequest

from utils.shared import tasks
from utils.task_logic import send_post_request

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