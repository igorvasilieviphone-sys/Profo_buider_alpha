function initSwipeableCards(containerSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    container.querySelectorAll('.swipe-overlay').forEach(el => el.remove());
    const leftOverlay = document.createElement('div');
    leftOverlay.className = 'swipe-overlay left';
    const rightOverlay = document.createElement('div');
    rightOverlay.className = 'swipe-overlay right';
    container.appendChild(leftOverlay);
    container.appendChild(rightOverlay);

    let cards = [];

    window.syncCardStack = function() {
        cards = Array.from(container.querySelectorAll('.result-card'));
        updateCardStack();
    };

    function updateCardStack() {
        cards.forEach((card, index) => {
            card.style.zIndex = cards.length - index;
            card.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
            if (index < 3) {
                card.style.transform = `translateY(${index * -15}px) scale(${1 - index * 0.05})`;
                card.style.opacity = '1';
                card.style.pointerEvents = (index === 0) ? 'auto' : 'none';
            } else {
                card.style.opacity = '0';
                card.style.pointerEvents = 'none';
            }
        });

        if (cards.length > 0 && cards.length < 15 && !window.isFetchingBackground) {
            if (typeof fetchCards === 'function') fetchCards(false);
        }
    }

    function onDragStart(e) {
        const topCard = cards[0];
        if (!topCard || !topCard.contains(e.target)) return;
        if (e.target.closest('.card-details-toggle') || e.target.closest('a')) return;

        this.activeCard = topCard;
        this.isDragging = true;
        this.startX = e.pageX || e.touches[0].pageX;
        this.startY = e.pageY || e.touches[0].pageY;
        
        this.activeCard.style.transition = 'none';
        
        document.body.classList.add('is-dragging');
        window.getSelection().removeAllRanges(); 
    }

    function onDragMove(e) {
        if (!this.isDragging || !this.activeCard) return;
        if (e.cancelable) e.preventDefault();
        
        const x = (e.pageX || (e.touches && e.touches[0].pageX)) - this.startX;
        const y = (e.pageY || (e.touches && e.touches[0].pageY)) - this.startY;
        
        this.activeCard.style.transform = `translate(${x}px, ${y}px) rotate(${x/20}deg) scale(1.05)`;
        
        const op = Math.min(Math.abs(x) / 200, 0.5);
        if (x > 0) { 
            rightOverlay.style.opacity = op; 
            leftOverlay.style.opacity = 0; 
        } else { 
            leftOverlay.style.opacity = op; 
            rightOverlay.style.opacity = 0; 
        }
        
        window.getSelection().removeAllRanges();
    }

    function onDragEnd(e) {
        if (!this.isDragging || !this.activeCard) return;
        const x = (e.pageX || (e.changedTouches && e.changedTouches[0].pageX)) - this.startX;
        const card = this.activeCard;
        
        this.isDragging = false;
        this.activeCard = null;
        
        document.body.classList.remove('is-dragging');

        if (Math.abs(x) > 120) {
            const dir = x > 0 ? 1 : -1;
            if (dir === 1) saveCareerToLocal(JSON.parse(card.dataset.careerData));
            card.style.transition = 'transform 0.5s ease-out, opacity 0.5s';
            card.style.transform = `translate(${dir * 1000}px, 0) rotate(${dir * 45}deg)`;
            card.style.opacity = '0';
            setTimeout(() => {
                if (container.contains(card)) container.removeChild(card);
                cards.shift();
                updateCardStack();
                if (cards.length === 0) container.innerHTML = '<p class="description">Рекомендации закончились!</p>';
            }, 300);
        } else {
            card.style.transition = 'transform 0.3s ease';
            card.style.transform = 'translate(0,0) rotate(0) scale(1)';
        }
        leftOverlay.style.opacity = 0;
        rightOverlay.style.opacity = 0;
    }

    const state = { isDragging: false, activeCard: null, startX: 0, startY: 0 };
    container.addEventListener('mousedown', onDragStart.bind(state));
    container.addEventListener('touchstart', onDragStart.bind(state), { passive: false });
    document.addEventListener('mousemove', onDragMove.bind(state), { passive: false });
    document.addEventListener('touchmove', onDragMove.bind(state), { passive: false });
    document.addEventListener('mouseup', onDragEnd.bind(state));
    document.addEventListener('touchend', onDragEnd.bind(state));

    window.syncCardStack();
}