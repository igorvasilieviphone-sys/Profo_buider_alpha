const pages = document.querySelectorAll('.page');
let explorerContainer, explorerFinishBtn, explorerResetBtn, progressBarFill, startAssessmentBtnHomepage;
let userInfoModal, showResultsBtn, userInfoInput;
let careerNameToDelete = null;
let testCompleted = false;

let excludedIds = [];
let isFetchingBackground = false;
let userContext = { topics: [], info: "" };

function showPage(pageId) {
    const chatWidget = document.getElementById('chatWidget');
    if (chatWidget) {
        if (pageId === 'homepage') chatWidget.classList.add('hidden');
        else chatWidget.classList.remove('hidden');
    }
    document.querySelectorAll('.page').forEach(page => {
        if (page.id === pageId) {
            page.classList.add('active');
            page.classList.remove('hidden');
        } else {
            page.classList.remove('active');
            page.classList.add('hidden');
        }
    });
    if (pageId === 'explorer') initExplorerPage();
}

function handleResultsNav() {
    if (testCompleted) showPage('results');
    else document.getElementById('noticeModal').classList.remove('hidden');
}

const ALL_EXPLORER_TOPICS = [
    { id: 'l1_1', label: 'Хочу создавать системы и инструменты', level: 1 },
    { id: 'l1_2', label: 'Хочу выражать идеи и вызывать эмоции', level: 1 },
    { id: 'l1_3', label: 'Хочу помогать другим и организовывать процессы', level: 1 },
    { id: 'l2_1', label: 'Хочу строить из логики и кода', level: 2, parentId: 'l1_1' },
    { id: 'l2_2', label: 'Хочу находить скрытые смыслы в информации', level: 2, parentId: 'l1_1' },
    { id: 'l2_3', label: 'Хочу проектировать надежные структуры', level: 2, parentId: 'l1_1' },
    { id: 'l2_4', label: 'Хочу облекать мысли в слова и образы', level: 2, parentId: 'l1_2' },
    { id: 'l2_5', label: 'Хочу рассказывать истории, которые увидят все', level: 2, parentId: 'l1_2' },
    { id: 'l2_6', label: 'Хочу создавать красоту своими руками', level: 2, parentId: 'l1_2' },
    { id: 'l2_7', label: 'Хочу вести людей к общей цели', level: 2, parentId: 'l1_3' },
    { id: 'l2_8', label: 'Хочу заботиться о благополучии других', level: 2, parentId: 'l1_3' },
    { id: 'l2_9', label: 'Хочу делиться знаниями и опытом', level: 2, parentId: 'l1_3' },
    { id: 'l3_1', label: 'Хочу, чтобы моим творением пользовались миллионы', level: 3, parentId: 'l2_1' },
    { id: 'l3_2', label: 'Хочу, чтобы сложные системы работали как часы', level: 3, parentId: 'l2_1' },
    { id: 'l3_3', label: 'Хочу предсказывать тренды и видеть будущее', level: 3, parentId: 'l2_2' },
    { id: 'l3_4', label: 'Хочу превращать данные в понятные выводы', level: 3, parentId: 'l2_2' },
    { id: 'l3_5', label: 'Хочу обеспечивать бесперебойную работу сервисов', level: 3, parentId: 'l2_3' },
    { id: 'l3_6', label: 'Хочу создавать непробиваемую защиту', level: 3, parentId: 'l2_3' },
    { id: 'l3_7', label: 'Хочу, чтобы интерфейсы были интуитивно понятными', level: 3, parentId: 'l2_4' },
    { id: 'l3_8', label: 'Хочу, чтобы бренды говорили на языке картинок', level: 3, parentId: 'l2_4' },
    { id: 'l3_9', label: 'Хочу формировать общественное мнение', level: 3, parentId: 'l2_5' },
    { id: 'l3_10', label: 'Хочу создавать ажиотаж вокруг продуктов и идей', level: 3, parentId: 'l2_5' },
    { id: 'l3_11', label: 'Хочу работать с физическими материалами', level: 3, parentId: 'l2_6' },
    { id: 'l3_12', label: 'Хочу рисовать в цифровом мире', level: 3, parentId: 'l2_6' },
    { id: 'l3_13', label: 'Хочу, чтобы проекты завершались в срок и успешно', level: 3, parentId: 'l2_7' },
    { id: 'l3_14', label: 'Хочу, чтобы бизнес рос и процветал', level: 3, parentId: 'l2_7' },
    { id: 'l3_15', label: 'Хочу помогать людям находить внутреннюю гармонию', level: 3, parentId: 'l2_8' },
    { id: 'l3_16', label: 'Хочу применять науку для улучшения здоровья', level: 3, parentId: 'l2_8' },
    { id: 'l3_17', label: 'Хочу находить таланты и строить команды', level: 3, parentId: 'l2_9' },
    { id: 'l3_18', label: 'Хочу делать сложное простым для других', level: 3, parentId: 'l2_9' },
];

let selectedTopicIds = new Set();

function saveCareerToLocal(careerData) {
    let saved = JSON.parse(localStorage.getItem('savedCareers')) || [];
    if (!saved.some(item => item.name === careerData.name)) {
        saved.push(careerData);
        localStorage.setItem('savedCareers', JSON.stringify(saved));
    }
}

function generateCardHTML(rec) {
    const labels = { logic: 'Логика', creativity: 'Креативность', social: 'Общение', routine: 'Рутина', art: 'Искусство' };
    let chartHtml = '<div class="chart-container"><h4>Навыки</h4>';
    if (rec.score_vector) {
        for (const [k, v] of Object.entries(rec.score_vector)) {
            chartHtml += `<div class="chart-bar-row"><span class="chart-label">${labels[k]||k}</span><div class="chart-bar-bg"><div class="chart-bar-fill" style="width:${(v/5)*100}%"></div></div></div>`;
        }
    }
    chartHtml += '</div>';
    return `<div class="card-content-wrapper"><div class="card-main-info"><h3>${rec.name}</h3><p class="card-industry"><b>${rec.industry}</b></p></div><div class="card-details-container"><div class="card-description-wrapper"><p class="card-ai-description">${rec.description||'...'}</p><div class="card-stats"><div class="stat-item"><span>//</span> <span>Зарплата: <b>${rec.junior_salary} ₽</b></span></div><div class="stat-item"><span>⚡️</span> <span>Рост: <b>${rec.growth_rate}</b></span></div></div></div><div class="card-hidden-details"><p><b>ВУЗы:</b> ${rec.university}</p>${chartHtml}<a href="${rec.link}" target="_blank" class="card-link">Подробнее</a></div></div><div class="card-footer"><div class="card-details-toggle">Подробнее</div></div></div>`;
}

function showSavedCards() {
    showPage('saved-cards');
    const container = document.getElementById('saved-cards-grid');
    const saved = JSON.parse(localStorage.getItem('savedCareers')) || [];
    container.innerHTML = saved.length ? '' : '<p class="description">У вас пока нет сохраненных карточек.</p>';
    saved.forEach(rec => {
        const item = document.createElement('div');
        item.className = 'explorer-block saved-item';
        const recStr = JSON.stringify(rec).replace(/'/g, "&apos;");
        item.innerHTML = `
            <div class="saved-item-content">
                <h3>${rec.name}</h3>
                <p>${rec.industry}</p>
            </div>
            <div class="saved-item-actions">
                <button class="btn-icon view" onclick='openFullCardModal(${recStr})'>Подробнее</button>
                <button class="btn-icon delete" onclick="removeSavedCareer('${rec.name}')">Удалить</button>
            </div>`;
        container.appendChild(item);
    });
}

function openFullCardModal(rec) {
    const modal = document.getElementById('cardModal');
    const container = document.getElementById('modal-card-container');
    container.innerHTML = '';
    const card = document.createElement('div');
    card.className = 'result-card static';
    card.innerHTML = generateCardHTML(rec);
    container.appendChild(card);
    modal.classList.remove('hidden');
}

window.removeSavedCareer = function(name) {
    careerNameToDelete = name;
    document.getElementById('deleteConfirmModal').classList.remove('hidden');
};

function initExplorerPage() {
    selectedTopicIds.clear();
    explorerContainer.innerHTML = '';
    renderExplorerBlocks(ALL_EXPLORER_TOPICS.filter(t => t.level === 1), false);
    updateFinishButtonState();
    updateProgressBar();
}

function renderExplorerBlocks(blocks, clear) {
    if (clear) explorerContainer.innerHTML = '';
    blocks.forEach(b => {
        const div = document.createElement('div');
        div.className = 'explorer-block';
        div.dataset.topicId = b.id;
        if (selectedTopicIds.has(b.id)) div.classList.add('selected');
        div.innerHTML = `<h3>${b.label}</h3>`;
        div.onclick = () => {
            if (selectedTopicIds.has(b.id)) selectedTopicIds.delete(b.id);
            else {
                selectedTopicIds.add(b.id);
                const children = ALL_EXPLORER_TOPICS.filter(t => t.parentId === b.id).slice(0, 3);
                if (children.length) renderExplorerBlocks(children, false);
            }
            div.classList.toggle('selected');
            updateFinishButtonState();
            updateProgressBar();
        };
        explorerContainer.appendChild(div);
    });
}

async function fetchCards(isInitial = false) {
    if (isFetchingBackground) return;
    isFetchingBackground = true;
    const container = document.getElementById('results-stack-container');
    const limit = isInitial ? 20 : 50;

    try {
        const res = await fetch('/api/generate_cards', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                selected_topics: Array.from(userContext.topics),
                additional_info: userContext.info,
                excluded_ids: excludedIds,
                limit: limit
            })
        });
        const data = await res.json();
        if (data && data.length) {
            data.forEach(c => excludedIds.push(c.id));
            if (isInitial) {
                container.innerHTML = '';
                testCompleted = true;
                data.forEach(rec => {
                    const card = document.createElement('div');
                    card.className = 'result-card';
                    card.dataset.careerData = JSON.stringify(rec);
                    card.innerHTML = generateCardHTML(rec);
                    container.appendChild(card);
                });
                initSwipeableCards('#results-stack-container');
                setTimeout(() => fetchCards(false), 500); 
            } else {
                data.forEach(rec => {
                    const card = document.createElement('div');
                    card.className = 'result-card';
                    card.dataset.careerData = JSON.stringify(rec);
                    card.innerHTML = generateCardHTML(rec);
                    container.appendChild(card);
                });
                if (window.syncCardStack) window.syncCardStack();
            }
        }
    } catch (e) {
        console.error(e);
    } finally {
        isFetchingBackground = false;
    }
}

function updateProgressBar() {
    document.getElementById('progress-bar-fill').style.width = `${Math.min(selectedTopicIds.size, 4)/4*100}%`;
}

function updateFinishButtonState() {
    explorerFinishBtn.disabled = selectedTopicIds.size < 3;
    explorerFinishBtn.textContent = `Продолжить (${selectedTopicIds.size})`;
}

async function downloadPDF() {
    const saved = JSON.parse(localStorage.getItem('savedCareers')) || [];
    if (!saved.length) return alert("Список пуст");
    try {
        const res = await fetch('/api/export_pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ saved_careers: saved })
        });
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = "ProfoBuilder_Results.pdf"; a.click();
    } catch (e) { console.error(e); }
}

function closeAllModals() {
    document.querySelectorAll('.modal-overlay').forEach(modal => modal.classList.add('hidden'));
}

function setupEventListeners() {
    explorerContainer = document.getElementById('explorer-container');
    explorerFinishBtn = document.getElementById('explorer-finish-btn');
    explorerResetBtn = document.getElementById('explorer-reset-btn');
    startAssessmentBtnHomepage = document.getElementById('start-assessment-btn-homepage');
    userInfoModal = document.getElementById('userInfoModal');
    showResultsBtn = document.getElementById('showResultsBtn');
    userInfoInput = document.getElementById('userInfoInput');
    
    document.getElementById('download-pdf-btn').addEventListener('click', (e) => { e.preventDefault(); downloadPDF(); });
    explorerFinishBtn.addEventListener('click', () => userInfoModal.classList.remove('hidden'));
    explorerResetBtn.addEventListener('click', () => initExplorerPage());
    startAssessmentBtnHomepage.addEventListener('click', (e) => { e.preventDefault(); showPage('explorer'); });

    document.querySelectorAll('.modal-close-btn').forEach(btn => {
        btn.addEventListener('click', closeAllModals);
    });

    document.getElementById('closeNoticeBtn').addEventListener('click', () => {
        document.getElementById('noticeModal').classList.add('hidden');
        showPage('explorer');
    });

    document.getElementById('cancelDeleteBtn').addEventListener('click', closeAllModals);
    document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
        if (careerNameToDelete) {
            let saved = JSON.parse(localStorage.getItem('savedCareers')) || [];
            localStorage.setItem('savedCareers', JSON.stringify(saved.filter(i => i.name !== careerNameToDelete)));
            showSavedCards();
        }
        closeAllModals();
    });

    showResultsBtn.addEventListener('click', () => {
        userContext.info = userInfoInput.value;
        userContext.topics = ALL_EXPLORER_TOPICS.filter(t => selectedTopicIds.has(t.id));
        excludedIds = [];
        userInfoModal.classList.add('hidden');
        showPage('results');
        document.getElementById('results-stack-container').innerHTML = '<div class="loader-container"><div class="spinner"></div><p class="description">Загрузка...</p></div>';
        fetchCards(true);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeAllModals();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('homepage')) {
        setupEventListeners();
        showPage('homepage');
    }
    document.body.addEventListener('click', (e) => {
        if (e.target.classList.contains('card-details-toggle')) {
            const card = e.target.closest('.result-card');
            card.classList.toggle('expanded');
            e.target.textContent = card.classList.contains('expanded') ? 'Скрыть' : 'Подробнее';
        }
    });
});