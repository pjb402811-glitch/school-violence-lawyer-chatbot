/**
 * 쏭비서 학폭 전문 AI 변호사 챗봇 - Vercel Serverless Web Client Logic (V2.1)
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소 캐싱
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const toggleIcon = sidebarToggle.querySelector('i');
    
    const accordionToggle = document.getElementById('accordion-toggle');
    const accordionContent = document.getElementById('accordion-content');
    const chevronIcon = accordionToggle.querySelector('.chevron-icon');
    
    const chatHistory = document.getElementById('chat-history');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const apiKeyInput = document.getElementById('api-key-input');
    const agentStatusDot = document.getElementById('agent-status-dot');
    const agentStatusText = document.getElementById('agent-status-text');
    
    const docSelector = document.getElementById('document-selector');
    const downloadBtn = document.getElementById('download-btn');
    
    // 4차 고도화: 가해자 핵심 취약점 설정 요소 캐싱
    const aggressorAge = document.getElementById('aggressor-age');
    const aggressorPrecedent = document.getElementById('aggressor-precedent');
    
    // 시뮬레이터 슬라이더 요소 캐싱
    const slides = {
        severity: document.getElementById('slide-severity'),
        duration: document.getElementById('slide-duration'),
        intent: document.getElementById('slide-intent'),
        repentance: document.getElementById('slide-repentance'),
        reconciliation: document.getElementById('slide-reconciliation')
    };
    
    const valOutputs = {
        severity: document.getElementById('val-severity'),
        duration: document.getElementById('val-duration'),
        intent: document.getElementById('val-intent'),
        repentance: document.getElementById('val-repentance'),
        reconciliation: document.getElementById('val-reconciliation')
    };
    
    const resultTotalScore = document.getElementById('result-total-score');
    const resultPredictedMeasure = document.getElementById('result-predicted-measure');

    // 대화 이력 메모리 (서버 API 통신용)
    let chatMemory = [
        { role: "assistant", content: "안녕하십니까, 피해 학생의 권리를 철저하게 사수하는 학교폭력 전문 AI 변호사입니다." }
    ];

    // ==========================================
    // 0. Vercel 서버 환경 변수 헬스체크 및 실시간 상태 감시
    // ==========================================
    let isServerEnvKeyConfigured = false;

    async function checkServerHealth() {
        if (!navigator.onLine) {
            updateStatusUI(false, "인터넷 미연결");
            return;
        }

        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                const data = await response.json();
                if (data.apiKeyConfigured) {
                    isServerEnvKeyConfigured = true;
                    // 사이드바 UI를 환경변수 연동 완료 상태로 업데이트
                    apiKeyInput.placeholder = "서버 환경 변수 연동 완료";
                    apiKeyInput.disabled = true;
                    apiKeyInput.style.borderColor = "#10b981"; // 녹색 테두리
                    apiKeyInput.style.boxShadow = "0 0 10px rgba(16, 185, 129, 0.15)";
                    
                    updateStatusUI(true);
                } else {
                    updateStatusUI(false, "미연결 (API 미설정)");
                }
            } else {
                updateStatusUI(false, "미연결");
            }
        } catch (err) {
            console.log("헬스체크 통신 지연 (로컬 환경 구동 중 또는 Vercel 부팅 중)");
            updateStatusUI(false, "미연결");
        }
    }

    function updateStatusUI(isOnline, text = "") {
        if (isOnline) {
            if (agentStatusDot) {
                agentStatusDot.className = "status-dot status-online";
                agentStatusDot.title = "AI 법률 에이전트 정상 가동 중";
            }
            if (agentStatusText) {
                agentStatusText.className = "status-text text-online";
                agentStatusText.innerText = "";
            }
        } else {
            if (agentStatusDot) {
                agentStatusDot.className = "status-dot status-offline";
                agentStatusDot.title = "연결 끊김";
            }
            if (agentStatusText) {
                agentStatusText.className = "status-text text-offline";
                agentStatusText.innerText = text;
            }
        }
    }

    // 실시간 브라우저 연결 상태 변경 리스너
    window.addEventListener('online', checkServerHealth);
    window.addEventListener('offline', () => updateStatusUI(false, "인터넷 미연결"));

    checkServerHealth();


    // ==========================================
    // 1. 모바일 사이드바 서랍 토글 로직
    // ==========================================
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (sidebar.classList.contains('open')) {
            toggleIcon.className = 'fa-solid fa-xmark';
        } else {
            toggleIcon.className = 'fa-solid fa-bars';
        }
    });

    // 화면 아무 데나 클릭 시 모바일 사이드바 닫기
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target) && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                toggleIcon.className = 'fa-solid fa-bars';
            }
        }
    });

    // ==========================================
    // 2. 학습 판례 아코디언 토글 로직
    // ==========================================
    accordionToggle.addEventListener('click', () => {
        accordionContent.classList.toggle('show');
        chevronIcon.classList.toggle('rotate');
    });

    // ==========================================
    // 3. 학폭위 예상 조치 시뮬레이터 로직 (실시간 API 연동 & Fallback)
    // ==========================================
    async function updateSimulation() {
        // 4차 고도화: 상습 재범 가중 락킹 (폭력의 지속성 4점 잠금 및 슬라이더 비활성화)
        if (aggressorPrecedent && aggressorPrecedent.checked) {
            slides.duration.value = 4;
            slides.duration.disabled = true;
            slides.duration.style.opacity = 0.5;
        } else if (slides.duration) {
            slides.duration.disabled = false;
            slides.duration.style.opacity = 1.0;
        }

        const values = {
            severity: parseInt(slides.severity.value),
            duration: parseInt(slides.duration.value),
            intent: parseInt(slides.intent.value),
            repentance: parseInt(slides.repentance.value),
            reconciliation: parseInt(slides.reconciliation.value)
        };

        // UI 숫자 렌더링
        for (const key in values) {
            if (key === 'duration' && aggressorPrecedent && aggressorPrecedent.checked) {
                valOutputs[key].innerText = "4 (상습 가중)";
            } else {
                valOutputs[key].innerText = values[key];
            }
        }

        try {
            const response = await fetch('/api/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(values)
            });
            
            if (response.ok) {
                const data = await response.json();
                resultTotalScore.innerText = data.score;
                resultPredictedMeasure.innerText = data.predictedMeasure;
                applyMeasureColor(data.score);
                return;
            }
        } catch (err) {
            console.warn("FastAPI 백엔드가 비활성 상태이므로 로컬 연산 엔진(Fallback)으로 대체 실행합니다.");
        }

        // 백엔드가 끊겼을 시의 로컬 시뮬레이션 공식
        const score = values.severity + values.duration + values.intent + values.repentance + values.reconciliation;
        resultTotalScore.innerText = score;
        
        let localMeasure = "";
        if (score <= 3) {
            localMeasure = "제1호(서면사과) 또는 제2호(접촉·협박 및 보복금지)";
        } else if (score <= 6) {
            localMeasure = "제3호(학교 봉사) 또는 제4호(사회봉사)";
        } else if (score <= 9) {
            localMeasure = "제5호(특별교육이수/심리치료) 또는 제6호(출석정지)";
        } else if (score <= 12) {
            localMeasure = "제7호(학급교체)";
        } else {
            localMeasure = "제8호(전학) 또는 제9호(퇴학처분 - 고등학생 한정)";
        }
        
        resultPredictedMeasure.innerText = localMeasure;
        applyMeasureColor(score);
    }

    function applyMeasureColor(score) {
        if (score <= 6) {
            resultPredictedMeasure.style.color = '#3b82f6'; 
        } else if (score <= 12) {
            resultPredictedMeasure.style.color = '#d4af37'; 
        } else {
            resultPredictedMeasure.style.color = '#ef4444'; 
        }
    }

    // 슬라이더 전원에 실시간 리스너 바인딩
    for (const key in slides) {
        slides[key].addEventListener('input', updateSimulation);
    }
    
    // 4차 고도화: 가해자 취약점 요소에도 실시간 시뮬레이터 갱신 이벤트 바인딩
    if (aggressorPrecedent) aggressorPrecedent.addEventListener('change', updateSimulation);
    if (aggressorAge) aggressorAge.addEventListener('change', updateSimulation);
    
    updateSimulation();

    // ==========================================
    // 4. 실전 법률 서식 원클릭 다운로드 로직
    // ==========================================
    downloadBtn.addEventListener('click', async () => {
        const selectedFile = docSelector.value;
        if (!selectedFile) {
            alert("다운로드할 서식을 먼저 선택하여 주십시오.");
            return;
        }

        try {
            const response = await fetch(`/${selectedFile}`);
            if (response.ok) {
                const text = await response.text();
                const blob = new Blob([text], { type: 'text/markdown;charset=utf-8;' });
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.setAttribute('download', selectedFile);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } else {
                alert("서식 파일 로드에 실패했습니다. 서버 내 파일 배치를 점검해 주십시오.");
            }
        } catch (err) {
            alert("서식 다운로드 네트워크 오류가 발생했습니다: " + err.message);
        }
    });

    // ==========================================
    // 5. RAG AI 챗봇 대화 로직
    // ==========================================
    function appendMessage(role, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role === 'user' ? 'user-msg' : 'bot-msg'}`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'avatar';
        avatarDiv.innerHTML = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-user-tie"></i>';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'bubble';
        
        if (role === 'assistant') {
            bubbleDiv.innerHTML = parseMarkdown(text);
        } else {
            bubbleDiv.innerText = text;
        }
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function parseMarkdown(text) {
        let parsed = text
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" style="color:#d4af37; text-decoration:underline; font-weight:bold;">$1</a>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/-\s(.*?)(<br>|$)/g, '• $1$2')
            .replace(/###\s(.*?)(<br>|$)/g, '<h3 style="color:#d4af37; margin:10px 0 5px 0; font-size:1rem;">$1</h3>$2')
            .replace(/⚠️/g, '<span style="color:#ef4444;">⚠️</span>')
            .replace(/⚖️/g, '<span style="color:#d4af37;">⚖️</span>');
        return parsed;
    }

    function showTypingIndicator() {
        const indicatorDiv = document.createElement('div');
        indicatorDiv.className = 'message bot-msg typing-container';
        indicatorDiv.id = 'typing-indicator';
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'avatar';
        avatarDiv.innerHTML = '<i class="fa-solid fa-user-tie"></i>';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'bubble';
        bubbleDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        indicatorDiv.appendChild(avatarDiv);
        indicatorDiv.appendChild(bubbleDiv);
        chatHistory.appendChild(indicatorDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    async function handleSendMessage() {
        const query = chatInput.value.trim();
        if (!query) return;

        appendMessage('user', query);
        chatInput.value = '';
        chatInput.style.height = 'auto';

        chatMemory.push({ role: 'user', content: query });
        showTypingIndicator();

        const apiKey = apiKeyInput.value.trim();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: query,
                    apiKey: apiKey || null,
                    history: chatMemory,
                    aggressorInfo: {
                        ageGroup: aggressorAge ? aggressorAge.value : 'criminal',
                        ageLabel: aggressorAge ? aggressorAge.options[aggressorAge.selectedIndex].text : '만 14세 이상 범죄소년 (형사처벌 대상)',
                        hasPrecedent: aggressorPrecedent ? aggressorPrecedent.checked : false
                    }
                })
            });

            removeTypingIndicator();

            if (response.ok) {
                const data = await response.json();
                appendMessage('assistant', data.response);
                chatMemory.push({ role: 'assistant', content: data.response });
            } else {
                const errMsg = "서버로부터 답변을 받아오지 못했습니다. Vercel 서버리스 가동 상태를 확인해 주십시오.";
                appendMessage('assistant', `⚠️ **오류 발생**: ${errMsg}`);
            }
        } catch (err) {
            removeTypingIndicator();
            const fallbackMsg = "네트워크 통신 중 오류가 발생했습니다. Vercel 서버가 아직 부팅 중이거나 배포 대기 상태일 수 있습니다.\n\n(사이드바의 예상 징계 조치 시뮬레이터와 법률 서식 퀵 다운로드 기능은 완전하게 정상 작동하므로 즉시 이용하실 수 있습니다.)";
            appendMessage('assistant', `⚠️ **연동 통신 불안정**\n\n${fallbackMsg}`);
        }
    }

    sendBtn.addEventListener('click', handleSendMessage);
    
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight - 10) + 'px';
    });

    // ==========================================
    // 3차 고도화: ⚡ 사후 대반격 로드맵 아코디언 및 퀵 질문 연동
    // ==========================================
    const roadmapBtns = document.querySelectorAll('.roadmap-btn');
    
    roadmapBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const panel = btn.nextElementSibling;
            const icon = btn.querySelector('i');
            
            // 토글 처리
            panel.classList.toggle('show');
            icon.classList.toggle('rotate');
            
            // 다른 아코디언을 닫아서 깔끔하게 조율 (쏭비서 오케스트레이션)
            roadmapBtns.forEach(otherBtn => {
                if (otherBtn !== btn) {
                    const otherPanel = otherBtn.nextElementSibling;
                    const otherIcon = otherBtn.querySelector('i');
                    otherPanel.classList.remove('show');
                    otherIcon.classList.remove('rotate');
                }
            });
        });
    });

    // 퀵 질문(Click-to-Ask) 버튼 연동
    const quickAskBtns = document.querySelectorAll('.quick-ask-btn');
    quickAskBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // 버블링으로 인한 패널 닫힘 예방
            const question = btn.getAttribute('data-question');
            if (question) {
                chatInput.value = question;
                
                // 모바일 환경일 경우, 질문이 잘 보이고 전송 화면으로 포커싱되도록 사이드바 닫기
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                    toggleIcon.className = 'fa-solid fa-bars';
                }
                
                // 챗봇 답변 프로세스 전격 기동
                handleSendMessage();
            }
        });
    });
});
