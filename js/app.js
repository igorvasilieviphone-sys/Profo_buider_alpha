document.addEventListener("DOMContentLoaded", () => {
    
    const chatToggle = document.getElementById("chatToggle");
    const chatWidget = document.getElementById("chatWidget");
    const closeChat = document.getElementById("closeChat");
    const chatInput = document.getElementById("chatInput");
    const chatMessages = document.getElementById("chatMessages");
    const sendMessageBtn = document.getElementById("sendMessage");
    
    // === ИЗМЕНЕНИЕ ЗДЕСЬ ===
    // Используем относительный путь, чтобы браузер сам определил домен
    const API_URL = "/api/chat";
    // === КОНЕЦ ИЗМЕНЕНИЯ ===

    const addMessage = (text, sender, isTyping = false) => {
        const messageWrapper = document.createElement("div");
        messageWrapper.className = `message-wrapper ${sender}`; 

        const messageContent = document.createElement("div");
        messageContent.textContent = text;
        messageContent.className = `message ${sender} ${isTyping ? 'typing-indicator' : ''} bg-gray-100 p-2 rounded-lg max-w-[80%]`; 

        if (sender === "bot") {
            const botLogo = document.createElement("img");
            botLogo.src = "img/chat_gpt_logo.png"; 
            botLogo.alt = "Профик";
            botLogo.className = "bot-avatar"; 
            
            messageWrapper.appendChild(botLogo);
            messageWrapper.appendChild(messageContent);
        } else {
            messageWrapper.appendChild(messageContent);
        }

        if (chatMessages) {
            chatMessages.appendChild(messageWrapper);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        return messageContent; 
    };

    if (chatToggle && chatWidget) {
        chatToggle.onclick = () => {
            chatWidget.classList.toggle("active"); 
        };
    }

    if (closeChat) {
        closeChat.onclick = () => {
            chatWidget.classList.remove("active");
        };
    }

    const sendMessage = async () => {
        if (chatInput && chatMessages) {
            const messageText = chatInput.value.trim();
            if (messageText !== "") {
                addMessage(messageText, "user");
                chatInput.value = "";
                
                const loadingMessage = addMessage("AI-Ассистент печатает...", "bot", true);
                
                try {
                    const response = await fetch(API_URL, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ message: messageText }),
                    });

                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({ error: 'Неизвестная ошибка сервера' }));
                        throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    loadingMessage.textContent = data.response; 
                    loadingMessage.classList.remove('typing-indicator');

                } catch (error) {
                    console.error("Error sending message:", error);
                    loadingMessage.textContent = "Произошла ошибка при получении ответа от ИИ. Проверьте, запущен ли Python-сервер.";
                    loadingMessage.classList.remove('typing-indicator');
                    loadingMessage.classList.add('error');
                }
            }
        }
    };

    if (sendMessageBtn) {
        sendMessageBtn.onclick = sendMessage;
    }

    if (chatInput) {
        chatInput.onkeydown = (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        };
    }
});