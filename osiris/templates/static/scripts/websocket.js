class WebSocketManager {
    constructor(url) {
      this.url = url;
      this.socket = null;
    }
  
    connect() {
      this.socket = new WebSocket(this.url);
  
      this.socket.onopen = () => {
        console.log("Соединение установлено");
      }
  
      this.socket.onmessage = (event) => {
        console.log("Получено сообщение:", event.data);
        handle_ws_message(JSON.parse(event.data));
        // Далее можно добавить обработку полученных сообщений
      }
  
      this.socket.onclose = (event) => {
        console.log("Соединение закрыто", event);
      }
  
      this.socket.onerror = (error) => {
        console.error("Произошла ошибка", error);
      }
    }
  
    sendMessage(message) {
      if (this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify(message));
      } else {
        console.error("Соединение не установлено");
      }
    }
  
    close() {
      this.socket.close();
    }
  }
  
  // Пример использования
  const wsManager = new WebSocketManager('ws://127.0.0.1:8081/chats/ws');
  wsManager.connect();
  
  // Отправка сообщения
  wsManager.sendMessage({ text: 'Привет, мир!' });
  
  // Закрытие соединения
  // wsManager.close();
  