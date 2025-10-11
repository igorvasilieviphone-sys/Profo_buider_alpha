// js/block.js

function initSwipeableCards(containerSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    // --- НАЧАЛО ИЗМЕНЕНИЙ ---

    // 1. Создаем и добавляем оверлеи для фона
    const leftOverlay = document.createElement('div');
    leftOverlay.className = 'swipe-overlay left';
    container.appendChild(leftOverlay);

    const rightOverlay = document.createElement('div');
    rightOverlay.className = 'swipe-overlay right';
    container.appendChild(rightOverlay);

    // 2. Удаляем ненужные переменные и функции для цвета карточки
    // const initialColor = '#e67d37'; - больше не нужно в JS
    // const leftColor = '#ff4136'; - теперь в CSS
    // const rightColor = '#2cc295'; - теперь в CSS
    // function interpolateColor(...) - больше не нужна

    // --- КОНЕЦ ИЗМЕНЕНИЙ ---

    const flyAwayDuration = 400;
    const returnDuration = 300;

    const maxRotation = 15;
    const liftScale = 1.03;
    const decisionThreshold = window.innerWidth / 4;

    let activeCard = null;
    let startX, startY;
    let isDragging = false;
    let cards = Array.from(container.querySelectorAll('.result-card'));

    function updateCardStack() {
        cards.forEach((card, index) => {
            const zIndex = cards.length - index + 1; // +1 чтобы быть выше оверлея
            card.style.zIndex = zIndex;
            // Убираем background-color из transition
            card.style.transition = `transform ${returnDuration}ms cubic-bezier(0.175, 0.885, 0.32, 1.275)`;

            if (index < 3) {
                card.style.transform = `translateY(${index * -15}px) scale(${1 - index * 0.05})`;
                card.style.opacity = '1';
                card.style.pointerEvents = (index === 0) ? 'auto' : 'none';
            } else {
                card.style.opacity = '0';
                card.style.pointerEvents = 'none';
            }
        });
    }

    function onDragStart(e) {
        if (isDragging || !cards.length) return;
        const topCard = cards[0];
        
        if (!topCard || !topCard.contains(e.target)) return;

        activeCard = topCard;
        isDragging = true;
        
        activeCard.style.transition = 'none';
        activeCard.style.transform = `scale(${liftScale})`;

        // --- НАЧАЛО ИЗМЕНЕНИЙ ---
        // Сбрасываем transition у оверлеев на время перетаскивания
        leftOverlay.style.transition = 'none';
        rightOverlay.style.transition = 'none';
        // --- КОНЕЦ ИЗМЕНЕНИЙ ---

        startX = e.pageX || e.touches[0].pageX;
        startY = e.pageY || e.touches[0].pageY;

        e.preventDefault();
    }

    function onDragMove(e) {
        if (!isDragging || !activeCard) return;
        const currentX = e.pageX || e.touches[0].pageX;
        const currentY = e.pageY || e.touches[0].pageY;
        const deltaX = currentX - startX;
        const deltaY = currentY - startY;
        const progress = Math.max(-1, Math.min(1, deltaX / decisionThreshold));
        const rotation = maxRotation * progress;
        
        activeCard.style.transform = `translateX(${deltaX}px) translateY(${deltaY}px) scale(${liftScale}) rotate(${rotation}deg)`;
        
        // --- НАЧАЛО ИЗМЕНЕНИЙ ---
        // 3. Управляем прозрачностью оверлеев вместо цвета карточки
        if (progress < 0) { // Движение влево
            rightOverlay.style.opacity = 0;
            leftOverlay.style.opacity = -progress;
        } else { // Движение вправо
            leftOverlay.style.opacity = 0;
            rightOverlay.style.opacity = progress;
        }
        // activeCard.style.backgroundColor = newColor; // СТРОКА УДАЛЕНА
        // --- КОНЕЦ ИЗМЕНЕНИЙ ---
    }

    function onDragEnd(e) {
        if (!isDragging || !activeCard) return;
        
        const cardToAnimate = activeCard;
        isDragging = false;
        activeCard = null;

        const deltaX = (e.pageX || e.changedTouches[0].pageX) - startX;

        // --- НАЧАЛО ИЗМЕНЕНИЙ ---
        // Возвращаем transition оверлеям для плавного исчезновения
        leftOverlay.style.transition = `opacity ${returnDuration}ms ease`;
        rightOverlay.style.transition = `opacity ${returnDuration}ms ease`;
        // --- КОНЕЦ ИЗМЕНЕНИЙ ---


        if (Math.abs(deltaX) > decisionThreshold) {
            const direction = deltaX > 0 ? 1 : -1;
            cardToAnimate.style.transition = `transform ${flyAwayDuration}ms ease-out`;
            cardToAnimate.style.transform = `translateX(${direction * window.innerWidth}px) rotate(${direction * 30}deg)`;
            
            // --- НАЧАЛО ИЗМЕНЕНИЙ ---
            // 4. Убираем изменение цвета улетающей карточки
            // cardToAnimate.style.backgroundColor = direction === 1 ? rightColor : leftColor; // СТРОКА УДАЛЕНА

            // Плавно скрываем оверлеи после улетания карточки
            setTimeout(() => {
                leftOverlay.style.opacity = 0;
                rightOverlay.style.opacity = 0;
            }, returnDuration);
            // --- КОНЕЦ ИЗМЕНЕНИЙ ---

            cards.shift();
            updateCardStack();

            setTimeout(() => {
                if (container.contains(cardToAnimate)) {
                    container.removeChild(cardToAnimate);
                }
                if (cards.length === 0) {
                    const message = document.createElement('p');
                    message.textContent = 'Вы просмотрели все рекомендации!';
                    message.className = 'description';
                    container.appendChild(message);
                }
            }, flyAwayDuration);
        } else {
            // --- НАЧАЛО ИЗМЕНЕНИЙ ---
            // 5. Возвращаем карточку на место и скрываем оверлеи
            cardToAnimate.style.transition = `transform ${returnDuration}ms cubic-bezier(0.175, 0.885, 0.32, 1.275)`;
            cardToAnimate.style.transform = `translateX(0) translateY(0) rotate(0deg)`;
            // cardToAnimate.style.backgroundColor = initialColor; // СТРОКА УДАЛЕНА
            leftOverlay.style.opacity = 0;
            rightOverlay.style.opacity = 0;
            // --- КОНЕЦ ИЗМЕНЕНИЙ ---
        }
    }

    container.addEventListener('mousedown', onDragStart);
    container.addEventListener('touchstart', onDragStart, { passive: false });

    document.addEventListener('mousemove', onDragMove);
    document.addEventListener('touchmove', onDragMove, { passive: false });

    document.addEventListener('mouseup', onDragEnd);
    document.addEventListener('touchend', onDragEnd);

    updateCardStack();
}