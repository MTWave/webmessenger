
// Chats
function create_chat_bar(chat_data) {
	var chat_bar = document.createElement('div');
	chat_bar.setAttribute("class", "chat-tile");
	chat_bar.setAttribute("onclick", `select_chat(${chat_data.chat_id})`);

	chat_bar.innerHTML = `
        <div class="chat-avatar">
          <img src="static/imgs/PImg.jpg" alt="Chat Avatar">
        </div>
        <div class="chat-info">
          <div class="chat-name">Н${chat_data.name}</div>
          <div class="last-message">${chat_data.chat_id}</div>
        </div>
		`;

	document.getElementById('chat_list').appendChild(chat_bar);
}

function add_chat_bar(chats){
	chats.forEach(item => create_chat_bar(item));
}

function findMinId(jsonList) {
    // Инициализируем переменную с самым большим значением id
    let minId = jsonList[0].chat_id;

    // Итерируемся по каждому объекту в массиве
    jsonList.forEach(function(obj) {
        if (obj.chat_id < minId) {
            minId = obj.chat_id;
        }
    });

    return minId;
}

function init_chat_bar() {
	fetch(
		'chats/list', {
	method: 'GET'
	})
	.then(response => {
		if (!response.ok) {
		throw new Error('Network response was not ok');
		}
		return response.json()
	})
	.then(
		response_json => {
			console.log(response_json);
			add_chat_bar(response_json);
			select_chat(findMinId(response_json))
	})
}

// Messenger

function add_message(message) {
	/*
	add_message
	author
	text
	*/
	// ToDo - params of url?
	if (message.chat_id != localStorage.getItem("current_chat"))
		return

	var message_bar = document.createElement('div');
	// ToDo: check is itself user
	

	// ToDo check is it current user == message.author_id
	var current_user = localStorage.getItem("current_user");

	// ToDo autor_id
	if (message.author == current_user) {
		message_bar.setAttribute("class", "my-message-wrapper");
		message_bar.innerHTML = `
            <div class="my-message-bubble">
                <div class="message-text">${message.text}</div>
            </div>
		`
	} else {

		message_bar.setAttribute("class", "message-wrapper");
		message_bar.innerHTML = `
            <div class="message-bubble">
                <div class="message-sender">${message.author}</div>
                <div class="message-text">${message.text}</div>
            </div>
		`
	}

	document.getElementById('dialog_container').appendChild(message_bar);
}

function add_messages(messages) {
	messages.forEach(item => add_message(item));
}

function select_chat(chat_id) {
	localStorage.setItem("current_chat", chat_id);

	messenger = document.getElementById("dialog_container");
	messenger.innerHTML='';

	fetch(
		`chats/${chat_id}/messages`, {
		method: 'GET'
	})
	.then(response => {
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json()
	}).then(
		response_json => {
		console.log(response_json);
		add_messages(response_json);
	})
}

function send_message(event) {
    event.preventDefault(); // Отменяем стандартное поведение формы
    var formData = {
		msg_type: "create_msg",
		chat_id: localStorage.getItem("current_chat"),
        msg_text: document.getElementById('message_text').value
    };
    /*
    fetch(
        'chats/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    */
	wsManager.sendMessage(formData)
}

function handle_ws_message(msg) {
	if (msg.msg_type == "msg_created") {
		add_message(msg)
	}
}

document.getElementById("msg_sender").addEventListener('submit', send_message);