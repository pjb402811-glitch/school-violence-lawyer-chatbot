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
import base64

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

class AggressorInfo(BaseModel):
    ageGroup: str
    ageLabel: str
    hasPrecedent: bool

class AttachedFile(BaseModel):
    name: str
    type: str
    base64Data: str

class ChatRequest(BaseModel):
    message: str
    apiKey: Optional[str] = None
    history: List[ChatMessage] = []
    aggressorInfo: Optional[AggressorInfo] = None
    attachedFiles: Optional[List[AttachedFile]] = None

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
    
    # 3. 가해자 신상 취약점 정보 분석 및 법리 아킬레스건 동적 인젝션
    aggressor_strategy = ""
    if req.aggressorInfo:
        info = req.aggressorInfo
        precedent_text = "상습 재범 전학자" if info.hasPrecedent else "초범"
        aggressor_strategy += (
            f"\n★ [가해자 신상 취약점 핀포인트 저격 법리 적용]:\n"
            f"- 가해학생 연령 및 처벌 조건: {info.ageLabel}\n"
            f"- 가해학생 학폭 전과 여부: {precedent_text}\n"
        )
        
        if info.hasPrecedent:
            aggressor_strategy += (
                "- [상습범 가중처벌 법리]: 가해학생은 이전 학교에서도 학교폭력 이력으로 인해 강제 전학을 온 '상습 재범 가해자'입니다. "
                "학폭위 심의 시 교육부 고시 기준상 '폭력의 지속성' 항목은 즉시 최고점인 4점으로 고정되어야 하며, 반성도 또한 극히 낮으므로 가해자 측에 극히 불리한 점수가 책정되어야 함을 강력 피력하십시오. "
                "엄벌의견서와 행정심판 청구서에서 가해자의 '상습 학폭 성향'을 무자비하게 강조하여 제8호 전학(또는 고교의 경우 제9호 퇴학) 조치를 무조건 도출해 내야 합니다.\n"
                "- [교내 방치 위법성 경고]: 만일 학교가 가해학생과 피해학생을 즉각 분리(출석정지 또는 학급교체)하지 않고 동일 교실에 방치한다면, 이는 명백히 위법 상태이며 학교장 및 관할 교육청은 국가배상법 제2조에 따른 직무유기 손해배상 책임을 져야 함을 날카롭게 주장하십시오.\n"
            )
        else:
            aggressor_strategy += (
                "- [초범 대응 법리]: 비록 가해학생이 초범이라 주장하더라도 사안의 중대성과 정신적 상해의 지속성을 고려하여 즉각 제6호 출석정지 및 제7호 학급교체 이상의 분리 배제 조치를 적극 관철하십시오.\n"
            )
            
        if info.ageGroup == "criminal":
            aggressor_strategy += (
                "- [만 14세 이상 범죄소년 형사 단죄]: 가해학생은 형사책임 연령인 만 14세 이상 '범죄소년'입니다. "
                "촉법소년과 달리 실질적인 형사소송법상 피의자 신분으로 상해(정신과 PTSD 진단 포함), 공동폭행, 공동강요죄 등으로 정식 형사 고소가 가능하며, 기소 시 형사 전과기록(빨간 줄)이 남는 막강한 약점을 쥐고 흔들어야 합니다. 경찰서 형사팀에 즉각 고소장을 이송하십시오.\n"
                "- [민법 제755조 부모 압박 및 아파트 가압류]: 가해자 부모를 공동불법행위자로 묶어 민사소송을 제기하기 전, 가해 부모 명의의 아파트, 예금계좌 등을 선제 가압류하여 강력한 경제적 심리전 압박을 입히십시오. 이를 통해 합의의 Absolute Zone을 장악하십시오.\n"
                "- [징벌적 합의 조서 작성]: 합의 시 '비밀유지 조항 위반 시 건당 500만 원 위약벌 특약', '치료비 전액 실비 청구 단서', '상대방의 가해 인정 및 공식 사과'를 합의 조서에 핀포인트로 조율하십시오.\n"
            )
        elif info.ageGroup == "촉법":
            aggressor_strategy += (
                "- [만 10세 ~ 14세 촉법소년 소년원 송치 압박]: 가해학생은 형사미성년자(촉법소년)로 형사 처벌은 면제되나, 가정법원 소년부에 정식 송치되어 소년법 제32조에 따른 소년원 송치(최대 2년) 등의 보호처분이 고스란히 가능함을 알리십시오. "
                "수사 단계에서 경찰 수사관에게 '소년부 송치 강력의견서'를 제출해 숨통을 죄고, 가해자 부모를 상대로 민법 제755조 손해배상을 청구하십시오.\n"
            )
        else:
            aggressor_strategy += (
                "- [만 10세 미만 보호처분 외 조치]: 만 10세 미만은 소년법마저 배제되지만, 학폭법상 행정 조치(1호~8호 전학)는 100% 동등하게 처분되므로 학폭위 조치 수준을 최고 수위로 끌어올려야 합니다. "
                "동시에 부모에 대한 민사상 책임 추궁(치료비 및 위자료 손해배상)은 완벽히 가능하므로 가해 부모의 감독자 불법행위 책임 소송으로 대항하십시오.\n"
            )

    if api_key and api_key.strip():
        try:
            # 구글 제미나이 엔진 구성
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.5-flash")
            
            # 첨부 서류 텍스트 및 멀티모달 바이너리 추출
            attached_docs_context = ""
            multimodal_contents = []
            
            if req.attachedFiles:
                for file in req.attachedFiles:
                    # 1. 텍스트 성격의 파일은 직접 프롬프트 텍스트에 삽입 (신뢰성 극대화)
                    if "text/" in file.type or file.name.endswith(".txt") or file.name.endswith(".md") or file.name.endswith(".json"):
                        try:
                            b64_data = file.base64Data
                            if "," in b64_data:
                                b64_data = b64_data.split(",")[1]
                            decoded_text = base64.b64decode(b64_data).decode('utf-8', errors='ignore')
                            attached_docs_context += f"\n--- [첨부 서류: {file.name}] ---\n{decoded_text}\n"
                        except Exception as e:
                            print(f"텍스트 파일 디코딩 오류 ({file.name}): {str(e)}")
                    # 2. 이미지 및 PDF 등 바이너리 파일은 멀티모달 인라인 데이터 파트로 주입
                    else:
                        try:
                            b64_data = file.base64Data
                            if "," in b64_data:
                                b64_data = b64_data.split(",")[1]
                            file_bytes = base64.b64decode(b64_data)
                            multimodal_contents.append({
                                'mime_type': file.type,
                                'data': file_bytes
                            })
                        except Exception as e:
                            print(f"바이너리 파일 파싱 오류 ({file.name}): {str(e)}")
            
            # 전문 변호사 법리 프롬프트 조립 (2차 고도화 - 출처 명시 및 하이퍼링크 의무화)
            system_prompt = (
                "당신은 대한민국 최고 수준의 학교폭력 전문 변호사이자 피해학생의 편에서 가해학생을 강력 징벌하는 유능한 대리인입니다.\n"
                "아래 제공된 [관련 법령 및 대법원 판례 컨텍스트]를 철저히 학습하고 그라운딩하여 사용자의 질문에 답하십시오.\n"
                "가해자 측의 학습권 및 선도 가능성 주장을 '대법원 2022두56676 판결(피해학생 보호 최우선 원칙)'로 완벽하게 논파하는 법리를 기본 탑재하십시오.\n"
                "또한 등교 불가능 상태나 정신과 치료(PTSD)가 폭력의 중대한 결과임을 명시하여 동일 학급 배치가 위법한 2차 가해 방치임을 증명하십시오.\n"
                "★ [중요 - 대표 지시 규칙] 답변에 판례, 법률, 지침, 가이드 등을 인용할 때는 반드시 그 근거와 공식 출처를 명확히 명시하십시오. (예: '대법원 2022두56676 판결', '학교폭력예방 및 대책에 관한 법률 제16조', '교육부 학교폭력 사안처리 가이드북')\n"
                "★ [중요 - 하이퍼링크 활용] 컨텍스트에 수록된 공식 국가법령정보센터 및 판례 마크다운 하이퍼링크가 있을 경우, 본문 작성 시 반드시 해당 법률/판례 텍스트 뒤에 링크를 결합하여 제공하십시오. (예: [학교폭력예방 및 대책에 관한 법률 제17조](https://www.law.go.kr/법령/학교폭력예방및대책에관한법률/제17조))\n"
                "★ [합의 및 협상 전략 조언] 합의 또는 상대 변호사 대처 문의 시, 징벌적 위약벌 조항(비밀유지 위반 시 건당 500만 원 청구), 후유증 치료비 실비 청구 단서, 선결 조치 등 구체적인 실무 합의 조서 작성법과 상대 변호사를 압도하는 구두 스크립트를 포함하여 빈틈없이 조언해 주십시오.\n"
                "★ [첨부 서류 정밀 분석 지침] 만약 사용자가 진단서, 학폭위 결과서, 증언, 녹취록 등의 서류를 첨부한 경우, 해당 서류의 텍스트나 멀티모달 이미지/PDF 내용을 돋보기 들여다보듯 꼼꼼히 대조하여 사실관계를 입증하고, '첨부된 [서류명]을 분석한 결과...' 형태로 실전 법적 전술에 녹여내어 자녀의 피해 증빙과 상대방 가해의 악질성을 입체적으로 입증하십시오.\n"
                "톤앤매너는 자녀의 일로 애가 타는 부모님께 무한히 공감하면서도, 상대방 변호사를 법적으로 압도하기 위해 고도로 차갑고 날카로우며 빈틈이 없는 이성적 어조여야 합니다.\n"
                "모호한 법률 조언은 지향하고 확실하지 않은 사안은 1대1 대면 자문을 받으라는 주의도 포함시키십시오.\n\n"
            )
            
            if attached_docs_context:
                system_prompt += f"[사용자가 직접 첨부한 서류 본문 내용]:\n{attached_docs_context}\n\n"
                
            system_prompt += f"{aggressor_strategy}\n"
            system_prompt += f"[관련 법령 및 대법원 판례 컨텍스트]:\n{context}"
            
            # 이전 대화 내역 누적
            history_prompt = "이전 대화 기록:\n"
            for msg in req.history[-4:]:
                history_prompt += f"{msg.role}: {msg.content}\n"
                
            full_prompt = f"{system_prompt}\n\n{history_prompt}\n사용자 질문: {user_query}\n변호사 답변:"
            
            # 텍스트와 멀티모달 바이너리를 결합한 제미나이 앙상블 페이로드 빌드
            gemini_payload = [full_prompt]
            if multimodal_contents:
                gemini_payload.extend(multimodal_contents)
            
            response = model.generate_content(gemini_payload)
            bot_response = response.text
            
        except Exception as e:
            bot_response = f"⚠️ Gemini API 가동 중 오류가 발생했습니다: {str(e)}\n\n(안내: API Key 권한이나 잔여 크레딧을 확인해 주십시오. 대체 시스템으로 로컬 룰베이스 조언을 제공합니다.)"
    else:
        # API 키가 환경 변수와 수동 입력 둘 다 없을 때의 친절한 대체 룰베이스 조언
        local_aggressor_advice = ""
        if req.aggressorInfo:
            info = req.aggressorInfo
            local_aggressor_advice += f"\n🎯 **[가해자 취약점 맞춤 권고 - {info.ageLabel}]**\n"
            if info.hasPrecedent:
                local_aggressor_advice += (
                    "- **과거 학폭 이력이 확인된 상습 가해학생**: 지속성 4점 배점을 강력 주장하여 '제8호 강제 전학' 조치를 무조건 도출해 내야 합니다. 동일학급 방치 시 학교장의 의무 위반(국가배상 청구 예고)을 강력히 서면에 명시하십시오.\n"
                )
            if info.ageGroup == "criminal":
                local_aggressor_advice += (
                    "- **만 14세 이상 범죄소년 형사책임**: 소년원 수준이 아니라 정식 형사 고소를 통해 벌금형 및 전과기록(빨간 줄)을 형성할 수 있는 강력한 처벌 대상입니다. 경찰 고소를 즉시 진행해 징벌적 위약벌 특약이 포함된 합의 압박을 가하십시오.\n"
                )
            elif info.ageGroup == "촉법":
                local_aggressor_advice += (
                    "- **만 10~14세 촉법소년 대응**: 소년법 제32조에 따라 소년원 송치(최대 2년) 보호처분을 경찰 수사 의견으로 이송하도록 수사관을 압박하고, 부모를 상대로 민법 제755조 경제적 타격(손해배상 소송)을 개시하십시오.\n"
                )
            local_aggressor_advice += "\n"

        bot_response = (
            "⚖️ **[로컬 내장 법률 시스템 기본 조언]**\n\n"
            "현재 **Vercel 설정(Environment Variables)에서 `GEMINI_API_KEY`를 키로 하여 구글 API 키 값을 등록해 주시면, 이 챗봇은 자녀분을 철저히 구제할 판례 RAG AI 모드로 24시간 실시간 동작합니다!**\n\n"
            f"{local_aggressor_advice}"
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
