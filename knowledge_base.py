# -*- coding: utf-8 -*-
"""
학교폭력 AI 전문 변호사 챗봇 - 지식 베이스(Knowledge Base) 모듈
대한민국 학폭법, 교육부 가이드라인 및 핵심 판례 데이터 수집 및 구조화
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

# 2. 학교폭력 핵심 판례 데이터
COURT_PRECEDENTS = [
    {
        "case_no": "대법원 2023. 2. 9. 선고 2022두56676 판결 [가해학생 조치처분 취소]",
        "summary": "학교폭력 가해학생에 대한 조치 기준을 적용함에 있어서는 가해학생의 선도와 교육 못지않게 '피해학생의 보호와 구제'가 최우선적으로 고려되어야 한다.",
        "details": "가해학생이 자신의 잘못을 반성하지 아니하고 2차 가해를 가할 우려가 높은 상황에서는 학폭위가 가해학생에 대한 징계 수위를 높여 전학이나 학급교체 등의 강경 처분을 내리는 재량적 판단은 정당하며, 가해학생의 학습권 보장을 핑계로 처분을 감경해달라는 주장은 수용될 수 없다.",
        "keywords": ["대법원", "피해자 구제 최우선", "재량권 인정", "학습권 제한 가능", "2차 가해 방지"]
    },
    {
        "case_no": "서울고등법원 2020. 11. 12. 선고 2020누51XXX 판결 [학급교체처분 취소]",
        "summary": "가해학생과 피해학생이 동일한 교실(학급)에서 수업을 들으며 밀접하게 생활하도록 방치하는 것은 그 자체로 피해학생에게 심각한 2차적 정신 위해를 가하는 위법한 처사이다.",
        "details": "학교가 행정적 편의나 가해학생의 수업권만을 고려하여 동일 학급 배치를 유지하는 것은 학폭법상 접촉 금지 처분(2호)의 취지를 전적으로 훼손하는 것이며, 학교장은 즉각 학급 교체나 공간 분리를 통해 피해학생의 안전을 도모할 의무가 있다.",
        "keywords": ["동일 학급 방치 위법", "2차 위해", "접촉금지 실효성", "학급교체 의무"]
    },
    {
        "case_no": "대법원 2015. 9. 10. 선고 2013다27XXX 판결 [손해배상(기)]",
        "summary": "학교장이 학교폭력 사안을 인지하고도 실효성 있는 피해학생 보호 및 가해학생 분리 조치를 지체하여 추가 피해가 발생한 경우, 보호감독의무 위반에 따른 손해배상 책임이 성립한다.",
        "details": "학교의 교장이나 교사는 학생들을 보호하고 감독할 의무가 있으므로, 학교폭력을 인지한 즉시 가해자와 피해자를 격리하고 재발 방지책을 마련해야 한다. 이를 태만히 하여 피해학생의 정신 질환(PTSD)이 악화된 경우 학교법인 및 지자체는 위자료 배상 책임을 진다.",
        "keywords": ["보호감독의무 위반", "손해배상", "정신적 위자료", "교장 책임", "국가배상"]
    }
]

# 3. 교육부 가이드북(2024 최신) 핵심 행동 지침
GUIDEBOOK_RULES = [
    {
        "topic": "피해학생-가해학생 즉시 분리 제도",
        "rule": "학교폭력 사안을 인지한 즉시, 학교장은 지체 없이 피해학생과 가해학생을 물리적으로 즉시 분리하여야 한다. 분리 기간은 최대 7일 이내로 하며, 피해학생이 분리에 반대 의사를 표시하지 않는 한 강제적으로 즉시 시행되어야 한다.",
        "keywords": ["즉시 분리", "지체 없이", "7일 이내", "피해학생 의사 존중"]
    },
    {
        "topic": "가해학생 2호 조치(접촉금지)의 실질적 집행 가이드",
        "rule": "제2호 조치인 '접촉, 협박 및 보복행위 금지'는 SNS, 전화, 제3자를 통한 간접적 접촉 및 동일 공간 배치를 모두 금지하는 포괄적 개념이다. 동일 학급인 경우 시간표 분리, 급식 동선 분리를 우선 시행하며, 실효적 분리가 불가능할 시 즉각 학내 특별 배치를 실행해야 한다.",
        "keywords": ["2호 조치 집행", "SNS 접촉 금지", "급식 동선 분리", "실질적 분리"]
    }
]

# 4. 키워드 기반 지식 검색 함수 (RAG 대용 경량 검색 엔진)
def retrieve_relevant_knowledge(query: str) -> str:
    """
    사용자의 질문(query)에서 키워드를 추출하여 가장 매칭도가 높은 법률, 판례, 가이드를 검색해 
    LLM에 주입할 Context String을 생성합니다.
    """
    import re
    
    # 한국어 형태소 분석 대용 간단한 키워드 추출
    query_words = re.findall(r'[가-힣A-Za-z0-9]+', query)
    
    matched_laws = []
    matched_precedents = []
    matched_guides = []
    
    for word in query_words:
        if len(word) < 2:  # 한 글자 단어 제외
            continue
            
        # 법률 검색
        for law in LAW_PROVISIONS:
            if any(word in kw for kw in law["keywords"]) or word in law["content"]:
                if law not in matched_laws:
                    matched_laws.append(law)
                    
        # 판례 검색
        for prec in COURT_PRECEDENTS:
            if any(word in kw for kw in prec["keywords"]) or word in prec["summary"] or word in prec["details"]:
                if prec not in matched_precedents:
                    matched_precedents.append(prec)
                    
        # 가이드북 검색
        for guide in GUIDEBOOK_RULES:
            if any(word in kw for kw in guide["keywords"]) or word in guide["rule"]:
                if guide not in matched_guides:
                    matched_guides.append(guide)
                    
    # 컨텍스트 조립
    context_parts = []
    
    if matched_laws:
        context_parts.append("### 관련 학교폭력예방 및 대책에 관한 법률 (학폭법) 조항")
        for law in matched_laws[:3]:
            context_parts.append(f"- **{law['article']}**:\n  {law['content']}")
            
    if matched_precedents:
        context_parts.append("\n### 관련 대법원 및 하급심 판례 요지")
        for prec in matched_precedents[:2]:
            context_parts.append(f"- **{prec['case_no']}**:\n  *요지*: {prec['summary']}\n  *판단*: {prec['details']}")
            
    if matched_guides:
        context_parts.append("\n### 교육부 학교폭력 사안처리 가이드북 지침")
        for guide in matched_guides[:2]:
            context_parts.append(f"- **{guide['topic']}**:\n  {guide['rule']}")
            
    if not context_parts:
        # 매칭된 것이 없는 경우 기본 정보 리턴
        return "특별히 매칭된 법령이나 판례가 없습니다. 아래 기본 법령과 대법원 2022두56676 판결(피해학생 보호 최우선 원칙)을 기초로 최선의 법률 조언을 제공하십시오."
        
    return "\n\n".join(context_parts)
