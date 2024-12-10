from fastapi import FastAPI
from routers import router  # 라우터 임포트

from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers.router import BACKEND_URL

app = FastAPI()
print("백엔드 url : ", BACKEND_URL)

"""# CORS 미들웨어 설정
origins = [
    "http://localhost:8080",  # React 로컬 개발 서버
    "http://ac18f3f52dac84eb48de27e653868baf-739259397.ap-northeast-2.elb.amazonaws.com",  # 클라우드 배포 URL
    "http://ac18f3f52dac84eb48de27e653868baf-739259397.ap-northeast-2.elb.amazonaws.com/review-check"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)
"""
# 라우터 등록 : 앞 쪽 router가 파일명
app.include_router(router.router, prefix="/review-check", tags=["Prediction"])  # tags=["Prediction"] : OpenAPI 문서화 및 API 탐색을 용이하게 하기 위한 메타데이터, 없어도 되는 인자이긴 함

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# ai -> backend 테스트 하기 위한 api (테스트가 가능한거?)
@app.post("/review-check/response")
async def receive_response():

    result = '!!!! got response !!!!!'

    return result
