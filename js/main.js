// js/main.js

const pages = document.querySelectorAll('.page');
let explorerContainer, explorerFinishBtn, explorerResetBtn, progressBarFill, startAssessmentBtnHomepage;
let userInfoModal, closeModalBtn, showResultsBtn, userInfoInput;

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        if (page.id === pageId) {
            page.classList.add('active');
            page.classList.remove('hidden');
        } else {
            page.classList.remove('active');
            page.classList.add('hidden');
        }
    });
    if (pageId === 'explorer') { initExplorerPage(); }
}

const ALL_EXPLORER_TOPICS = [ { id: 'l1_1', label: 'Хочу создавать системы и инструменты', level: 1 }, { id: 'l1_2', label: 'Хочу выражать идеи и вызывать эмоции', level: 1 }, { id: 'l1_3', label: 'Хочу помогать другим и организовывать процессы', level: 1 }, { id: 'l2_1', label: 'Хочу строить из логики и кода', level: 2, parentId: 'l1_1' }, { id: 'l2_2', label: 'Хочу находить скрытые смыслы в информации', level: 2, parentId: 'l1_1' }, { id: 'l2_3', label: 'Хочу проектировать надежные структуры', level: 2, parentId: 'l1_1' }, { id: 'l2_4', label: 'Хочу облекать мысли в слова и образы', level: 2, parentId: 'l1_2' }, { id: 'l2_5', label: 'Хочу рассказывать истории, которые увидят все', level: 2, parentId: 'l1_2' }, { id: 'l2_6', label: 'Хочу создавать красоту своими руками', level: 2, parentId: 'l1_2' }, { id: 'l2_7', label: 'Хочу вести людей к общей цели', level: 2, parentId: 'l1_3' }, { id: 'l2_8', label: 'Хочу заботиться о благополучии других', level: 2, parentId: 'l1_3' }, { id: 'l2_9', label: 'Хочу делиться знаниями и опытом', level: 2, parentId: 'l1_3' }, { id: 'l3_1', label: 'Хочу, чтобы моим творением пользовались миллионы', level: 3, parentId: 'l2_1' }, { id: 'l3_2', label: 'Хочу, чтобы сложные системы работали как часы', level: 3, parentId: 'l2_1' }, { id: 'l3_3', label: 'Хочу предсказывать тренды и видеть будущее', level: 3, parentId: 'l2_2' }, { id: 'l3_4', label: 'Хочу превращать данные в понятные выводы', level: 3, parentId: 'l2_2' }, { id: 'l3_5', label: 'Хочу обеспечивать бесперебойную работу сервисов', level: 3, parentId: 'l2_3' }, { id: 'l3_6', label: 'Хочу создавать непробиваемую защиту', level: 3, parentId: 'l2_3' }, { id: 'l3_7', label: 'Хочу, чтобы интерфейсы были интуитивно понятными', level: 3, parentId: 'l2_4' }, { id: 'l3_8', label: 'Хочу, чтобы бренды говорили на языке картинок', level: 3, parentId: 'l2_4' }, { id: 'l3_9', label: 'Хочу формировать общественное мнение', level: 3, parentId: 'l2_5' }, { id: 'l3_10', label: 'Хочу создавать ажиотаж вокруг продуктов и идей', level: 3, parentId: 'l2_5' }, { id: 'l3_11', label: 'Хочу работать с физическими материалами', level: 3, parentId: 'l2_6' }, { id: 'l3_12', label: 'Хочу рисовать в цифровом мире', level: 3, parentId: 'l2_6' }, { id: 'l3_13', label: 'Хочу, чтобы проекты завершались в срок и успешно', level: 3, parentId: 'l2_7' }, { id: 'l3_14', label: 'Хочу, чтобы бизнес рос и процветал', level: 3, parentId: 'l2_7' }, { id: 'l3_15', label: 'Хочу помогать людям находить внутреннюю гармонию', level: 3, parentId: 'l2_8' }, { id: 'l3_16', label: 'Хочу применять науку для улучшения здоровья', level: 3, parentId: 'l2_8' }, { id: 'l3_17', label: 'Хочу находить таланты и строить команды', level: 3, parentId: 'l2_9' }, { id: 'l3_18', label: 'Хочу делать сложное простым для других', level: 3, parentId: 'l2_9' },];
let selectedTopicIds = new Set();
const MAX_PROGRESS_LEVEL = 4;
const ADJACENT_PARENTS = { 'l2_1': 'l2_2', 'l2_2': 'l2_3', 'l2_3': 'l2_1', 'l2_4': 'l2_5', 'l2_5': 'l2_6', 'l2_6': 'l2_4', 'l2_7': 'l2_8', 'l2_8': 'l2_9', 'l2_9': 'l2_7', };
function spawnChildBlocks(parentTopicId) { let newBlocks = []; const existingIds = new Set(Array.from(document.querySelectorAll('.explorer-block')).map(el => el.dataset.topicId)); let currentSearchId = parentTopicId; let originalSearchId = parentTopicId; let fallbackCount = 0; const parentTopic = ALL_EXPLORER_TOPICS.find(t => t.id === parentTopicId); if (!parentTopic) return []; if (parentTopic.level === 1) { let directChildren = ALL_EXPLORER_TOPICS.filter(topic => topic.parentId === parentTopicId).filter(topic => !existingIds.has(topic.id)); return directChildren.slice(0, 3); } while (newBlocks.length < 3) { let availableChildren = ALL_EXPLORER_TOPICS.filter(topic => topic.parentId === currentSearchId).filter(topic => !existingIds.has(topic.id)).filter(topic => !newBlocks.some(b => b.id === topic.id)); const needed = 3 - newBlocks.length; newBlocks.push(...availableChildren.slice(0, needed)); if (newBlocks.length === 3) break; if (ADJACENT_PARENTS[currentSearchId]) { currentSearchId = ADJACENT_PARENTS[currentSearchId]; } else { break; } fallbackCount++; if (currentSearchId === originalSearchId && fallbackCount > 2) break; } return newBlocks.slice(0, 3); }
function createBlockElement(block) { const div = document.createElement('div'); div.className = 'explorer-block'; div.dataset.topicId = block.id; if (selectedTopicIds.has(block.id)) { div.classList.add('selected'); } div.innerHTML = `<h3>${block.label}</h3>`; div.addEventListener('click', () => handleBlockClick(block.id)); return div; }
function renderExplorerBlocks(blocksToRender, clearExisting = true) { if (!explorerContainer) return; if (clearExisting) { explorerContainer.innerHTML = ''; } blocksToRender.forEach((block) => { const div = createBlockElement(block); explorerContainer.appendChild(div); }); }
function handleBlockClick(topicId) { const blockElement = document.querySelector(`[data-topic-id="${topicId}"]`); if (!blockElement) return; const isSelected = selectedTopicIds.has(topicId); const hasChildren = ALL_EXPLORER_TOPICS.some(t => t.parentId === topicId); if (isSelected) { selectedTopicIds.delete(topicId); blockElement.classList.remove('selected'); } else { selectedTopicIds.add(topicId); blockElement.classList.add('selected'); if (hasChildren) { const newBlocks = spawnChildBlocks(topicId); if (newBlocks.length > 0) { renderExplorerBlocks(newBlocks, false); } } } updateFinishButtonState(); updateProgressBar(); }
function updateProgressBar() { if (!progressBarFill) return; const count = selectedTopicIds.size; const progress = Math.min(count, MAX_PROGRESS_LEVEL) / MAX_PROGRESS_LEVEL * 100; progressBarFill.style.width = `${progress}%`; }
function updateFinishButtonState() { if (!explorerFinishBtn) return; const count = selectedTopicIds.size; explorerFinishBtn.textContent = `Продолжить к тесту (${count})`; explorerFinishBtn.disabled = count < 3; }
function initExplorerPage() { selectedTopicIds.clear(); const initialBlocks = ALL_EXPLORER_TOPICS.filter(t => t.level === 1); renderExplorerBlocks(initialBlocks, true); updateFinishButtonState(); updateProgressBar(); }

function renderResults(recommendations) {
    const resultsContainer = document.getElementById('results-stack-container');
    if (!resultsContainer) return;
    resultsContainer.innerHTML = ''; 

    if (!recommendations || recommendations.length === 0) {
        resultsContainer.innerHTML = '<p class="description">К сожалению, мы не смогли подобрать для вас профессии. Попробуйте пройти тест еще раз.</p>';
        return;
    }

    const scoreVectorLabels = { logic: 'Логика', creativity: 'Креативность', social: 'Общение', routine: 'Рутина', art: 'Искусство' };
    
    recommendations.forEach(rec => {
        const card = document.createElement('div');
        card.className = 'result-card';

        let chartHtml = '<div class="chart-container"><h4>Требуемые навыки</h4>';
        if (rec.score_vector && Object.keys(rec.score_vector).length > 0) {
            for (const [key, value] of Object.entries(rec.score_vector)) {
                const label = scoreVectorLabels[key] || key;
                const barWidth = (value / 5) * 100;
                chartHtml += `<div class="chart-bar-row"><span class="chart-label">${label}</span><div class="chart-bar-bg"><div class="chart-bar-fill" style="width: ${barWidth}%;"></div></div></div>`;
            }
        } else {
            chartHtml += '<p>Данные о навыках отсутствуют.</p>';
        }
        chartHtml += '</div>';

        card.innerHTML = `
            <div class="card-content-wrapper">
                <div class="card-main-info">
                    <h3>${rec.name}</h3>
                    <p class="card-industry"><b>Отрасль:</b> ${rec.industry}</p>
                </div>
                
                <div class="card-details-container">
                    <div class="card-description-wrapper">
                        <p class="card-ai-description"><b>Описание:</b> ${rec.description || 'Узнайте больше об этой профессии.'}</p>
                        <div class="card-stats">
                            <div class="stat-item"><span>//</span> <span>Зарплата новичка: <b>${rec.junior_salary} ₽</b></span></div>
                            <div class="stat-item"><span>///</span> <span>Средняя зарплата: <b>${rec.avg_salary} ₽</b></span></div>
                            <div class="stat-item"><span>⚡️</span> <span>Темпы роста: <b>${rec.growth_rate}</b></span></div>
                        </div>
                    </div>

                    <div class="card-hidden-details">
                        <p><b>Примерные ВУЗы:</b> ${rec.university}</p>
                        ${chartHtml}
                        <a href="${rec.link}" target="_blank" class="card-link">Узнать больше на внешнем ресурсе</a>
                    </div>
                </div>

                <div class="card-footer">
                    <div class="card-details-toggle">Подробнее</div>
                </div>
            </div>
        `;
        resultsContainer.appendChild(card);
    });

    initSwipeableCards('#results-stack-container');
}

function setupEventListeners() {
    explorerContainer = document.getElementById('explorer-container');
    explorerFinishBtn = document.getElementById('explorer-finish-btn');
    explorerResetBtn = document.getElementById('explorer-reset-btn');
    progressBarFill = document.getElementById('progress-bar-fill');
    startAssessmentBtnHomepage = document.getElementById('start-assessment-btn-homepage');
    
    userInfoModal = document.getElementById('userInfoModal');
    closeModalBtn = document.getElementById('closeModalBtn');
    showResultsBtn = document.getElementById('showResultsBtn');
    userInfoInput = document.getElementById('userInfoInput');

    if (explorerFinishBtn) { explorerFinishBtn.addEventListener('click', () => { if (selectedTopicIds.size < 3) { alert("Пожалуйста, выберите как минимум 3 темы."); return; } userInfoModal.classList.remove('hidden'); }); }
    if (explorerResetBtn) { explorerResetBtn.addEventListener('click', () => initExplorerPage()); }
    if (startAssessmentBtnHomepage) { startAssessmentBtnHomepage.addEventListener('click', (e) => { e.preventDefault(); showPage('explorer'); }); }
    if (closeModalBtn) { closeModalBtn.addEventListener('click', () => userInfoModal.classList.add('hidden')); }

    if (showResultsBtn) {
        showResultsBtn.addEventListener('click', async () => {
            const additionalInfo = userInfoInput.value;
            const selectedTopics = ALL_EXPLORER_TOPICS.filter(topic => selectedTopicIds.has(topic.id));
            userInfoModal.classList.add('hidden');
            showPage('results');
            const resultsContainer = document.getElementById('results-stack-container');
            resultsContainer.innerHTML = `<div class="loader-container"><div class="spinner"></div><p class="description">Подбираем профессии для вас...</p><p class="description small-text">AI-ассистент генерирует персональные рекомендации. Обычно это занимает не более 10 секунд.</p></div>`;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/generate_cards', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ selected_topics: selectedTopics, additional_info: additionalInfo }),
                });
                if (!response.ok) { const errorData = await response.json(); throw new Error(errorData.error || 'Ошибка при получении рекомендаций.'); }
                const recommendations = await response.json();
                renderResults(recommendations);
            } catch (error) {
                console.error('Error fetching recommendations:', error);
                resultsContainer.innerHTML = `<p class="description error">Не удалось загрузить рекомендации. Пожалуйста, попробуйте еще раз. ${error.message}</p>`;
            }
        });
    }

    const resultsContainer = document.getElementById('results-stack-container');
    if(resultsContainer) {
        resultsContainer.addEventListener('click', function(event) {
            if (event.target.classList.contains('card-details-toggle')) {
                const card = event.target.closest('.result-card');
                if (card) {
                    card.classList.toggle('expanded');
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    document.querySelectorAll('.page').forEach(page => {
        if (!page.classList.contains('active')) { page.classList.add('hidden'); }
    });
    if (document.querySelector('.page.active')?.id === 'explorer') { initExplorerPage(); }
});