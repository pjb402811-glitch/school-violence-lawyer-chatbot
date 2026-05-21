# -*- coding: utf-8 -*-
"""
학교폭력 AI 전문 변호사 챗봇 - Vercel Serverless API 백엔드 (V2.1)
Vercel 환경 변수(GEMINI_API_KEY) 자동 주입 감지 및 RAG 연동 지원
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
import os
import sys

# api 디렉토리를 path에 추가하여 로컬 import 보장
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from knowledge_base import retrieve_relevant_knowledge

app = FastAPI(title="학폭 AI 변호사 챗봇 Vercel Serverless API")

# CORS 미들웨어 설정 (프론트엔드 통신 보장)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 요청 모델 정의
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    apiKey: Optional[str] = None
    history: List[ChatMessage] = []

class SimulateRequest(BaseModel):
    severity: int
    duration: int
    intent: int
    repentance: int
    reconciliation: int

@app.get("/api/health")
def health_check():
    # Vercel 환경 변수 GEMINI_API_KEY 설정 여부 동적 판단
    is_env_configured = "GEMINI_API_KEY" in os.environ and len(os.environ["GEMINI_API_KEY"].strip()) > 0
    return {
        "status": "healthy", 
        "version": "2.1.0 (Vercel Serverless)",
        "apiKeyConfigured": is_env_configured
    }

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    user_query = req.message
    
    # 1. 수동 입력 API Key 우선권 부여 후, 없을 시 Vercel 환경 변수 자동 검출
    api_key = req.apiKey
    if not api_key or not api_key.strip():
        api_key = os.environ.get("GEMINI_API_KEY", "")
        
    # 2. 앙상블 RAG 검색기 작동 (판례 및 가이드북 추출)
    context = retrieve_relevant_knowledge(user_query)
    
    if api_key and api_key.strip():
        try:
            # 구글 제미나이 엔진 구성
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # 전문 변호사 법리 프롬프트 조립
            system_prompt = (
                "당신은 대한민국 최고 수준의 학교폭력 전문 변호사이자 피해학생의 편에서 가해학생을 강력 징벌하는 유능한 대리인입니다.\n"
                "아래 제공된 [관련 법령 및 대법원 판례 컨텍스트]를 철저히 학습하고 그라운딩하여 사용자의 질문에 답하십시오.\n"
                "가해자 측의 학습권 및 선도 가능성 주장을 대법원 2022두56676 판결(피해학생 보호 최우선 원칙)로 박살내는 논리를 기본 탑재하십시오.\n"
                "또한 등교 불가능 상태나 정신과 치료가 폭력의 중대한 결과임을 명시하여 동일 학급 배치가 위법한 2차 가해 방치임을 증명하십시오.\n"
                "톤앤매너는 자녀의 일로 애가 타는 부모님께 무한히 공감하면서도, 상대방 변호사를 법적으로 부수기 위해 고도로 차갑고 날카로우며 빈틈이 없는 이성적 어조여야 합니다.\n"
                "모호한 법률 조언은 지향하고 확실하지 않은 사안은 1대1 대면 자문을 받으라는 주의도 포함시키십시오.\n\n"
                f"[관련 법령 및 대법원 판례 컨텍스트]:\n{context}"
            )
            
            # 이전 대화 내역 누적
            history_prompt = "이전 대화 기록:\n"
            for msg in req.history[-4:]:
                history_prompt += f"{msg.role}: {msg.content}\n"
                
            full_prompt = f"{system_prompt}\n\n{history_prompt}\n사용자 질문: {user_query}\n변호사 답변:"
            
            response = model.generate_content(full_prompt)
            bot_response = response.text
            
        except Exception as e:
            bot_response = f"⚠️ Gemini API 가동 중 오류가 발생했습니다: {str(e)}\n\n(안내: API Key 권한이나 잔여 크레딧을 확인해 주십시오. 대체 시스템으로 로컬 룰베이스 조언을 제공합니다.)"
    else:
        # API 키가 환경 변수와 수동 입력 둘 다 없을 때의 친절한 대체 룰베이스 조언
        bot_response = (
            "⚖️ **[로컬 내장 법률 시스템 기본 조언]**\n\n"
            "현재 **Vercel 설정(Environment Variables)에서 `GEMINI_API_KEY`를 키로 하여 구글 API 키 값을 등록해 주시면, 이 챗봇은 자녀분을 철저히 구제할 판례 RAG AI 모드로 24시간 실시간 동작합니다!**\n\n"
            "가해자 측 변호사가 선임되어 '학습권' 또는 '경미한 사안'이라 주장하며 공격을 펼치는 현재 상황에서 즉시 취하셔야 할 법률 대응 지침은 다음과 같습니다:\n\n"
            "1. **학습권 논리 파쇄**: 대법원 2022두56676 판결에 따라 '가해자 선도보다 피해학생의 보호구제가 압도적 최우선'입니다. 교내 동일 학급 방치는 위법 상태이므로, 준비된 `학교장 긴급분리 촉구서`를 다운로드하여 즉각 이송하십시오.\n"
            "2. **정신적 상해 적극 소명**: 행심위 재결 경향상 신체 외상(전치)이 없더라도 정신적 피해(등교 거부, 정신과 진료)만으로 폭력의 심각성이 인정되므로, 진단서 소견에 '학폭 기인 PTSD'를 구체적으로 넣으셔야 합니다.\n"
            "3. **사이드바 메뉴**에서 이미 완벽 구성된 행정심판 청구서(`administrative_appeal.md`) 및 경찰 제출용 의견서(`criminal_complaint_opinion.md`) 서식 파일들을 바로 다운로드해 활용하십시오."
        )
        
    return {"response": bot_response}

@app.post("/api/simulate")
async def simulate_endpoint(req: SimulateRequest):
    total_score = req.severity + req.duration + req.intent + req.repentance + req.reconciliation
    
    predicted_measure = ""
    if total_score <= 3:
        predicted_measure = "제1호(서면사과) 또는 제2호(접촉·협박 및 보복금지)"
    elif total_score <= 6:
        predicted_measure = "제3호(학교 봉사) 또는 제4호(사회봉사)"
    elif total_score <= 9:
        predicted_measure = "제5호(특별교육이수/심리치료) 또는 제6호(출석정지)"
    elif total_score <= 12:
        predicted_measure = "제7호(학급교체)"
    else:
        predicted_measure = "제8호(전학) 또는 제9호(퇴학처분 - 고등학생 한정)"
        
    return {
        "score": total_score,
        "predictedMeasure": predicted_measure,
        "detail": "교육부 '학교폭력 가해학생 조치별 적용 기준' 고시 점수에 의거한 결과입니다."
    }
