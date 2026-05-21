# -*- coding: utf-8 -*-
"""
학교폭력 AI 전문 변호사 챗봇 - 지식 베이스(Knowledge Base) 고도화 모듈 (V2.0)
대법원 판례, 행정심판 재결례, 깃허브 오픈소스(LegaBot, osondoson-nlp) 로직 반영
"""

# 1. 학교폭력예방 및 대책에 관한 법률 (학폭법) 핵심 조항
LAW_PROVISIONS = [
    {
        "article": "제1조 (목적)",
        "content": "이 법은 학교폭력의 예방과 대책에 필요한 사항을 규정함으로써 피해학생의 보호, 가해학생의 선도·교육 및 피해학생과 가해학생 간의 분쟁조정을 통하여 학생의 인권을 보호하고 학생을 건전한 사회구성원으로 육성함을 목적으로 한다.",
        "keywords": ["목적", "피해학생 보호", "가해학생 선도", "인권 보호"]
    },
    {
        "article": "제16조 (피해학생의 보호조치)",
        "content": "① 학교장은 피해학생의 보호를 위하여 필요하다고 인정하는 경우 피해학생에 대하여 다음 각 호의 어느 하나에 해당하는 조치(수개의 조치를 병과하는 경우를 포함한다)를 취할 수 있다.\n"
                   "1. 학내외 전문가에 의한 심리상담 및 조언\n"
                   "2. 일시보호\n"
                   "3. 치료 및 치료를 위한 요양\n"
                   "4. 학급교체\n"
                   "6. 그 밖에 피해학생의 보호를 위하여 필요한 조치\n"
                   "② 학교장은 제1항에 따른 조치를 취하기 전에 피해학생 및 그 보호자의 의견을 들어야 한다.",
        "keywords": ["피해학생 보호조치", "심리상담", "일시보호", "치료 요양", "학급교체", "학교장 권한"]
    },
    {
        "article": "제17조 (가해학생에 대한 조치)",
        "content": "① 심의위원회는 피해학생의 보호와 가해학생의 선도·교육을 위하여 가해학생에 대하여 다음 각 호의 어느 하나에 해당하는 조치(수개의 조치를 병과하는 경우를 포함한다)를 할 것을 교육장에게 요청하여야 한다.\n"
                   "1. 피해학생에 대한 서면사과\n"
                   "2. 피해학생 및 신고·고발 학생에 대한 접촉, 협박 및 보복행위의 금지\n"
                   "3. 학교에서의 봉사\n"
                   "4. 사회봉사\n"
                   "5. 학내외 전문가에 의한 특별 교육이수 또는 심리치료\n"
                   "6. 출석정지\n"
                   "7. 학급교체\n"
                   "8. 전학\n"
                   "9. 퇴학처분(고등학교에 한함)",
        "keywords": ["가해학생 조치", "서면사과", "접촉금지", "보복금지", "출석정지", "학급교체", "전학", "퇴학"]
    },
    {
        "article": "제17조 (긴급조치 권한)",
        "content": "④ 학교장은 학교폭력 사안이 발생한 경우 피해학생의 보호와 가해학생의 선도·교육을 위하여 긴급하다고 인정하는 때에는 심의위원회 개최 전에 가해학생에 대하여 제1항 제1호부터 제3호까지, 제5호 및 제6호의 조치를 할 수 있다. 이 경우 심의위원회에 즉시 보고하여야 한다.",
        "keywords": ["학교장 긴급조치", "심의위 개최 전", "출석정지 긴급조치", "보호조치"]
    }
]

# 2. 학교폭력 핵심 판례 및 행정심판 재결례 데이터 (고도화 반영)
COURT_PRECEDENTS = [
    {
        "case_no": "대법원 2023. 2. 9. 선고 2022두56676 판결 [가해학생 조치처분 취소 기각]",
        "summary": "가해자의 학습권보다 피해자의 보호가 최우선이다.",
        "details": "가해학생 측 변호사들은 대개 '중학교 3학년은 고입을 앞둔 중요한 시기이므로 가해학생의 학습권과 전인적 발달을 위해 반 분리나 전학 등은 가혹하다'고 주장합니다. 하지만 대법원은 학교폭력예방법의 입법 취지상 '피해학생의 보호와 구제'가 최우선 고려되어야 하며, 가해학생의 학습권 보장이 피해학생이 안전하게 교육받을 권리보다 결코 우위에 설 수 없다고 판시했습니다. 따라서 반 분리(학급교체) 및 전학 조치는 정당합니다.",
        "keywords": ["가해자 학습권", "피해자 보호 최우선", "입법 취지", "반 분리 정당성", "대법원 2022두56676"]
    },
    {
        "case_no": "중앙행정심판위원회 및 행정법원 재결례 [정신적 위해 결과의 중대성 인정]",
        "summary": "피해학생의 '정신적 피해'와 '등교 불가능 상태'도 심각한 폭력 결과이다.",
        "details": "가해자 측은 '신체적 폭행이 없었고 단지 언어적 다툼이나 따돌림 수준이므로 반 분리는 과하다'고 주장하나, 사법부와 행심위는 학교폭력의 심각성을 판단할 때 외견상 전치 진단서 유무만을 기준으로 삼지 않습니다. 피해학생이 극심한 불안, 등교 거부, 정신과 치료(PTSD)를 요하는 상태에 이르렀다면 이는 가해행위의 심각성과 지속성이 최고 수준임을 증명하는 것입니다. 따라서 동일 학급 방치는 위법한 2차 가해 방치입니다.",
        "keywords": ["정신적 피해", "등교 불가능", "진단서 무관", "상당인과관계", "동일학급 방치 위법"]
    },
    {
        "case_no": "중앙행심위 재결례 [가해자 청구 기각 실제 성공 사례]",
        "summary": "가해자 측의 '학폭위 조치 취소 청구'를 기각시킨 실제 사례",
        "details": "가해학생 측이 '학급교체(반 분리) 처분이 너무 무거워 학습권이 침해된다'며 행정심판을 청구했으나, 위원회는 '피해학생이 가해자와 마주치는 것만으로도 정상적인 학교생활이 불가능하다고 호소하며 병원 치료를 받는 등 피해가 극심하므로 가해학생을 학급교체하여 격리하는 분리 조치는 정당하다'며 가해자 측의 행정심판 청구를 단호히 기각하고 원처분을 유지시켰습니다.",
        "keywords": ["가해자 청구 기각", "학급교체 정당", "마주치는 것만으로 고통", "실제 성공 사례"]
    }
]

# 3. 교육부 가이드북 및 공신력 있는 청소년 상담 지침
GUIDEBOOK_RULES = [
    {
        "topic": "교육부 학교폭력 사안처리 가이드북 (2025-2026 개정 반영)",
        "rule": "가장 중요한 매뉴얼로, 학교와 교육청 학폭위 위원들이 사안을 처리할 때 무조건 지켜야 하는 법적 백과사전입니다. 가이드북 지침에 따르면 피해-가해학생 즉시분리 기간은 최대 7일이며, 피해자의 반대 의사가 없는 한 학교장은 의무적으로 가해자를 임시 격리 또는 출석정지해야 합니다.",
        "keywords": ["가이드북", "업무 매뉴얼", "의무 분리", "즉시 분리 7일"]
    },
    {
        "topic": "푸른나무재단 & 청소년상담복지개발원 피해 증명 가이드",
        "rule": "피해 학생의 심리적 지지와 부모의 대처 요령을 제공합니다. 특히 법적 공방 시 자녀의 Wee클래스 상담 일지, 학교 상담 기록, 부모에게 보낸 심리 호소 메시지를 모두 누적하여 '피해의 고의성과 상해 상당인과관계'를 소명하는 입증 스펙트럼 구축이 필수적입니다.",
        "keywords": ["푸른나무재단", "상담 기록", "Wee클래스", "입증 스펙트럼", "피해 호소 기록"]
    }
]

# 4. 키워드 기반 지식 검색 함수 (LegaBot의 RAG 검색 핵심 아키텍처 반영 - 앙상블 검색 흉내)
def retrieve_relevant_knowledge(query: str) -> str:
    """
    milistu/LegaBot RAG 및 osondoson-nlp 또래상담 감정 분류 흐름을 모사한 앙상블 검색기.
    질문 속에서 '감정(우울, 등교거부)', '법리(학습권, 반분리)' 등의 유형을 파악하고 최적의 처방 지식을 매칭합니다.
    """
    import re
    
    query_words = re.findall(r'[가-힣A-Za-z0-9]+', query)
    
    matched_laws = []
    matched_precedents = []
    matched_guides = []
    
    # osondoson-nlp NLP 분류 패턴 매칭 (감정 및 정황 분류)
    is_emotional_distress = any(kw in query for kw in ["우울", "힘들어", "죽고싶", "정신과", "불안", "등교거부", "진단서"])
    is_legal_argument = any(kw in query for kw in ["학습권", "가혹", "변호사", "취소", "행정심판", "쌍방", "맞고소"])
    
    for word in query_words:
        if len(word) < 2:
            continue
            
        # 1. 법령 검색
        for law in LAW_PROVISIONS:
            if any(word in kw for kw in law["keywords"]) or word in law["content"]:
                if law not in matched_laws:
                    matched_laws.append(law)
                    
        # 2. 판례 검색 (가중치 적용)
        for prec in COURT_PRECEDENTS:
            if any(word in kw for kw in prec["keywords"]) or word in prec["summary"] or word in prec["details"]:
                if prec not in matched_precedents:
                    matched_precedents.append(prec)
                    
        # 3. 가이드 검색
        for guide in GUIDEBOOK_RULES:
            if any(word in kw for kw in guide["keywords"]) or word in guide["rule"]:
                if guide not in matched_guides:
                    matched_guides.append(guide)
                    
    # 컨텍스트 조립
    context_parts = []
    
    # NLP 다중 분류 가중치 피드백 강제 주입
    if is_emotional_distress:
        context_parts.append("📢 [감정 분석 알림] 사용자의 자녀가 등교 거부, 우울 및 심각한 PTSD(외상후스트레스장애) 등의 정신적 극단 위해에 처해 있습니다. 법률 소견서 작성 시 정신과 진단 인과관계 극대화 지침을 최우선 연용하여 주치의 특약 소견 구성을 강조하십시오.")
        # 관련 정신적 위해 판례 강제 주입
        matched_precedents.insert(0, COURT_PRECEDENTS[1])
        
    if is_legal_argument:
        context_parts.append("📢 [법리 분석 알림] 상대방 대리인(가해자 변호사)이 '가해학생의 학습권 보장' 또는 '학폭위 조치 과다에 따른 취소 청구'를 논거로 들고 나왔습니다. 대법원 2022두56676 판결의 '피해자보호 압도적 우선 원칙' 및 실제 행심위 기각 성공사례를 즉각 인용하여 역공하십시오.")
        # 관련 대법원 판례 강제 주입
        matched_precedents.insert(0, COURT_PRECEDENTS[0])
        matched_precedents.append(COURT_PRECEDENTS[2])
        
    if matched_laws:
        context_parts.append("### ⚖️ 대한민국 학교폭력예방법 조문")
        for law in matched_laws[:3]:
            context_parts.append(f"- **{law['article']}**:\n  {law['content']}")
            
    if matched_precedents:
        # 중복 제거
        unique_precedents = []
        for p in matched_precedents:
            if p not in unique_precedents:
                unique_precedents.append(p)
                
        context_parts.append("\n### 🏛️ 핵심 대법원 판례 및 행정심판 재결례")
        for prec in unique_precedents[:3]:
            context_parts.append(f"- **{prec['case_no']}**:\n  *핵심 논리*: {prec['summary']}\n  *상세 법리*: {prec['details']}")
            
    if matched_guides:
        context_parts.append("\n### 📋 교육부 및 공신력 있는 단체 가이드라인")
        for guide in matched_guides[:2]:
            context_parts.append(f"- **{guide['topic']}**:\n  {guide['rule']}")
            
    if not context_parts:
        return "대표 기본 컨텍스트: 대법원 2022두56676 판결(피해학생 보호 최우선), 학폭법 제16조(피해학생 보호조치 권한)에 입각하여 고도의 법률 가이드를 작성하십시오."
        
    return "\n\n".join(context_parts)
