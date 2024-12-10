import logging
import httpx
from typing import Dict, Any
from fastapi import HTTPException

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


async def send_post_request(url: str, data: Dict[str, Any]) -> Dict:
    """
    비동기 POST 요청을 보내고 결과를 반환하는 함수
    """
    logger.info(f"Starting POST request to URL: {url}")
    logger.debug(f"Request data: {data}")

    try:
        logger.debug("Initializing httpx.AsyncClient")
        async with httpx.AsyncClient() as client:
            logger.info("Sending POST request")
            response = await client.post(url, json=data)

            logger.debug(f"Request headers: {response.request.headers}")
            logger.debug(f"Response status code: {response.status_code}")

            response.raise_for_status()
            logger.info(f"Request successful with status code: {response.status_code}")

            response_data = response.json()
            logger.debug(f"Response data: {response_data}")

            return response_data

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Status Error: {str(e)}")
        logger.error(f"Response content: {e.response.content}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"HTTP error: {str(e)}"
        )

    except httpx.RequestError as e:
        logger.error(f"Request Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Request error: {str(e)}"
        )

    except Exception as e:
        logger.critical(f"Unexpected error occurred: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


# # 작업 완료된 태스크를 처리하고 백엔드에 결과를 전송
# async def process_task(task_id: str):
#     if task_id not in tasks:
#         raise HTTPException(status_code=404, detail=f"Task ID '{task_id}' not found")
#
#     task = tasks[task_id]
#
#     # print("Task data:", task)  # task 전체 출력
#     if "result" not in task or task["result"] is None:
#         raise ValueError(f"Task ID '{task_id}' has invalid or missing 'result' data")
#
#     # 백엔드에 전달할 데이터 준비
#     payload = {
#         "requestId": task_id,
#         "blogUrl": task.get("result", {}).get("blogUrl", "Unknown"),
#         "summaryTitle": task.get("result", {}).get("summaryTitle", "Unknown"),
#         "summaryText": task.get("result", {}).get("summaryText", ""),
#         "score": task.get("result", {}).get("score", 0),
#         "evidence": task.get("result", {}).get("evidence", "No evidence found")
#     }
#
#     print('*** 2 : payload : ', payload, ' ***')
#     print('title : ', task.get("result", {}).get("summaryTitle", "Unknown"))
#     print('text : ', task.get("result", {}).get("summaryText", "Unknown"))
#
#     try:
#         # POST 요청 전송
#         response = await send_post_request(BACKEND_URL, payload)
#         print(f"Backend response: {response}")
#
#         return {"status": "COMPLETED", "response": response}
#
#     except HTTPException as e:
#         # 에러 발생 시 로깅 또는 상태 업데이트
#         print(f"?? Error while sending result for Task ID '{task_id}': {e}")
#         task["status"] = "ERROR"
#         task["result"]["error"] = e.detail
