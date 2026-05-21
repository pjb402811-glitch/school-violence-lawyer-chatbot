# -*- coding: utf-8 -*-
"""
학교폭력 전문 AI 변호사 챗봇 - '쏭비서 법률 오케스트레이션 V1.0'
Streamlit 기반 프리미엄 UI 및 RAG 검색 파이프라인 구현
"""
import streamlit as st
import google.generativeai as genai
import os
from knowledge_base import retrieve_relevant_knowledge, COURT_PRECEDENTS, LAW_PROVISIONS

# 페이지 설정
st.set_page_config(
    page_title="쏭비서 학폭 변호사 AI 챗봇",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. 프리미엄 CSS 커스텀 스타일링 (다크 테마, 글래스모피즘, 마이크로 애니메이션)
st.markdown("""
<style>
    /* 기본 다크 테마 */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #c9d1d9;
        font-family: 'Inter', 'Outfit', sans-serif;
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 2rem;
        border-radius: 16px;
        border-left: 6px solid #d4af37; /* 황금빛 포인트 */
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 2rem;
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
    }
    
    .main-header h1 {
        color: #f3f4f6;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0 0 8px 0;
    }
    
    .main-header p {
        color: #9ca3af;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* 글래스모피즘 박스 */
    .glass-card {
        background: rgba(22, 27, 34, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(212, 175, 55, 0.3); /* 황금빛 호버링 */
    }
    
    /* 챗 메시지 스타일링 */
    .chat-bubble {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        max-width: 80%;
        line-height: 1.5;
        font-size: 1rem;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: #ffffff;
        margin-left: auto;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    .bot-bubble {
        background: rgba(33, 38, 45, 0.85);
        color: #e6edf3;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }

    /* 사이드바 스타일 */
    .sidebar-title {
        color: #d4af37;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 2. 사이드바 - 제어판 & 예상 조치 시뮬레이터 (부모님용 초특급 도구)
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚖️ 쏭비서 법률 오케스트레이터</div>', unsafe_allow_html=True)
    st.write("피해 학생 부모님을 위한 실전 행정·사법 컨트롤 룸")
    
    # API 키 입력 필드
    api_key = st.text_input("Gemini API Key", type="password", help="Gemini API Key를 입력하여 초고성능 AI 조언을 활성화하세요.")
    if api_key:
        genai.configure(api_key=api_key)
        st.success("AI 엔진이 활성화되었습니다.")
    else:
        st.info("API Key 미입력 시, 로컬 내장 법률 시스템(시뮬레이터 및 서식 제공)으로 가동됩니다.")

    st.markdown("---")
    
    # 🧮 2024 교육부 사안처리 고시 기준 학폭위 조치 시뮬레이터
    st.markdown('<div class="sidebar-title">📊 학폭위 예상 처분 시뮬레이터</div>', unsafe_allow_html=True)
    st.write("가해학생의 예상 징계 수위를 교육부 채점표 기준으로 예측합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        v_severity = st.slider("폭력의 심각성", 0, 4, 2, help="0:없음 ~ 4:매우높음")
        v_duration = st.slider("폭력의 지속성", 0, 4, 2)
        v_intent = st.slider("폭력의 고의성", 0, 4, 2)
    with col2:
        v_repentance = st.slider("가해자 반성도", 0, 4, 2, help="0:높음(감점) ~ 4:없음(가점)")
        v_reconciliation = st.slider("피해자와의 화해", 0, 4, 2, help="0:높음(감점) ~ 4:없음(가점)")
        
    # 점수 계산
    total_score = v_severity + v_duration + v_intent + v_repentance + v_reconciliation
    
    # 징계 예측 매칭
    st.metric(label="총 산정 점수", value=f"{total_score} / 20 점")
    
    predicted_measure = ""
    if total_score <= 3:
        predicted_measure = "제1호(서면사과) 또는 제2호(접촉·협박 및 보복금지)"
    elif total_score <= 6:
        predicted_measure = "제3호(학교 봉사) 또는 제4호(사회봉사)"
    elif total_score <= 9:
        predicted_measure = "제5호(특별교육/치료) 또는 제6호(출석정지)"
    elif total_score <= 12:
        predicted_measure = "제7호(학급교체)"
    else:
        predicted_measure = "제8호(전학) 또는 제9호(퇴학처분 - 고등학생만)"
        
    st.markdown(f"**📢 예상 처분 결과:**\n<span style='color:#d4af37; font-weight:bold;'>{predicted_measure}</span>", unsafe_allow_html=True)
    st.markdown("*(교육부 공식 '학교폭력 가해학생 조치별 적용 기준'에 입각한 시뮬레이션입니다)*")

    st.markdown("---")
    st.markdown('<div class="sidebar-title">📄 실전 법률 서식 퀵 뷰어</div>', unsafe_allow_html=True)
    
    # 작성된 마크다운 파일들의 간편 보기 제공
    document_selected = st.selectbox("다운로드 및 보기를 원하는 문서", 
                                    ["선택하세요", "학교장 긴급분리 촉구서", "교육청 행정심판 청구서", "수사기관 엄벌의견서", "증거수집 가이드"])
    
    if document_selected != "선택하세요":
        filename_map = {
            "학교장 긴급분리 촉구서": "urgent_action_request.md",
            "교육청 행정심판 청구서": "administrative_appeal.md",
            "수사기관 엄벌의견서": "criminal_complaint_opinion.md",
            "증거수집 가이드": "evidence_and_defense_guide.md"
        }
        target_file = filename_map[document_selected]
        if os.path.exists(target_file):
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()
            st.download_button(
                label=f"📥 {document_selected} 다운로드",
                data=content,
                file_name=target_file,
                mime="text/markdown"
            )
        else:
            st.error("해당 문서 파일이 프로젝트 디렉토리에 없습니다.")

# 3. 메인 레이아웃 - 헤더
st.markdown("""
<div class="main-header">
    <h1>⚖️ 학교폭력 피해학생 수호 전문 AI 변호사</h1>
    <p>가해자 측의 악의적 법적 공세를 파쇄하고, 한 교실에 방치된 아이를 구제할 날카롭고 빈틈없는 1대1 법률/행정 조언</p>
</div>
""", unsafe_allow_html=True)

# 4. 기본 탑재 지식 베이스 안내 콜랩스
with st.expander("📚 학습 완료된 핵심 법령 및 대법원 판례 데이터 보기"):
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("🏛️ 대표 판례 요지")
        for prec in COURT_PRECEDENTS:
            st.markdown(f"**[{prec['case_no']}]**")
            st.markdown(f"- *요지*: {prec['summary']}")
            st.markdown(f"- *상세*: {prec['details']}")
            st.markdown("---")
    with col_r:
        st.subheader("⚖️ 핵심 학폭법 조항")
        for law in LAW_PROVISIONS:
            st.markdown(f"**{law['article']}**")
            st.markdown(f"*{law['content']}*")
            st.markdown("---")

# 5. 채팅 영역 초기화 및 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하십니까, 피해 학생의 권리를 철저하게 사수하는 학교폭력 전문 AI 변호사입니다. "
                                        "자녀분께서 처한 상황(가해학생과의 한 교실 방치, 상대방 대리인의 쌍방과실 주장, 보복 위협 등)을 말씀해 주시면, "
                                        "대법원 판례와 학폭법에 기초한 날카롭고 실전적인 법률·행정 구제 전략을 즉시 도출해 드리겠습니다."}
    ]

# 채팅 이력 출력
for msg in st.session_state.messages:
    role_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    st.markdown(f'<div class="chat-bubble {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# 6. 채팅 입력창 및 RAG 가동
user_query = st.chat_input("가해자 측 변호사의 주장 또는 현재 겪고 계신 애로사항을 입력하십시오...")

if user_query:
    # 1. 유저 메시지 렌더링 및 이력 저장
    st.markdown(f'<div class="chat-bubble user-bubble">{user_query}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # 2. 로컬 RAG 시스템 가동 - 판례/법령 컨텍스트 추출
    context = retrieve_relevant_knowledge(user_query)
    
    # 3. 답변 생성
    with st.spinner("법리 분석 및 방어 역공 시나리오 구성 중..."):
        if api_key:
            try:
                # Gemini API를 이용한 정밀 RAG 답변 생성
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                system_prompt = (
                    "당신은 대한민국 최고 수준의 학교폭력 전문 변호사이자 피해학생의 편에서 가해학생을 강력 징벌하는 유능한 대리인입니다.\n"
                    "아래 제공된 [관련 법령 및 대법원 판례 컨텍스트]를 철저히 학습하고 그라운딩하여 사용자의 질문에 답하십시오.\n"
                    "가해자 측의 학습권 및 선도 가능성 주장을 대법원 2022두56676 판결(피해학생 보호 최우선 원칙)로 박살내는 논리를 기본 탑재하십시오.\n"
                    "톤앤매너는 자녀의 일로 애가 타는 부모님께 무한히 공감하면서도, 상대방 변호사를 법적으로 부수기 위해 고도로 차갑고 날카로우며 빈틈이 없는 이성적 어조여야 합니다.\n"
                    "모호한 법률 조언은 지향하고 확실하지 않은 사안은 1대1 대면 자문을 받으라는 주의도 포함시키십시오.\n\n"
                    f"[관련 법령 및 대법원 판례 컨텍스트]:\n{context}"
                )
                
                # 대화 맥락 포함
                history_prompt = "이전 대화 기록:\n"
                for msg in st.session_state.messages[-3:-1]:  # 최근 2개의 대화 흐름
                    history_prompt += f"{msg['role']}: {msg['content']}\n"
                
                full_prompt = f"{system_prompt}\n\n{history_prompt}\n사용자 질문: {user_query}\n변호사 답변:"
                
                response = model.generate_content(full_prompt)
                bot_response = response.text
                
            except Exception as e:
                bot_response = f"⚠️ Gemini API 가동 중 오류가 발생했습니다: {str(e)}\n\n(안내: API Key 권한이나 잔여 크레딧을 확인해 주십시오. 대체 시스템으로 로컬 룰베이스 조언을 제공합니다.)"
        else:
            # API 키가 없을 때의 친절한 대체 룰베이스 법률 상담 로직
            bot_response = (
                "⚖️ **[로컬 내장 법률 시스템 기본 조언]**\n\n"
                "대표님(부모님), 현재 완벽한 AI 연동을 위해 **사이드바에 Gemini API Key를 주입해 주시면 본 학폭 챗봇은 대한민국 대법원 판례 데이터를 100% 흡수하여 실시간 초고도 조언을 출력합니다.**\n\n"
                "가해자 측 변호사가 선임되어 공세를 펼치는 상황에서 현재 가장 긴급하게 취하셔야 할 행동 강령은 아래와 같습니다:\n\n"
                "1. **학교장의 보호 의무 위반 고발**: 가해자에게 2호 접근금지가 나왔음에도 한 교실에 두는 것은 처분 위반의 방치입니다. 로컬 저장 폴더의 `urgent_action_request.md` 서식을 즉시 발송하여 압박하십시오.\n"
                "2. **행정심판 및 집행정지 신청**: 2호 조치가 결정된 날로부터 90일 이내에 교육청 행정심판위원회에 처분 변경 신청(`administrative_appeal.md` 서식 참조)을 하셔야 가해학생 전학이나 학급교체를 강제할 수 있습니다.\n"
                "3. **형사 조사 수사촉구의견서 제출**: 가해자는 중3으로 만 14세 이상 범죄소년에 해당하므로 형사 처벌 대상입니다. 경찰서 담당 수사관에게 `criminal_complaint_opinion.md` 서식을 제출하여 2차 가해를 차단하십시오.\n\n"
                "👉 *상세한 서식 다운로드 및 예상 조치 시뮬레이션은 사이드바 메뉴를 활용하십시오.*"
            )
            
        # 4. 봇 메시지 렌더링 및 이력 저장
        st.markdown(f'<div class="chat-bubble bot-bubble">{bot_response}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
