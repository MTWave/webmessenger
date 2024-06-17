
// Chats
function create_chat_bar(chat_data) {
	var chat_bar = document.createElement('div');
	chat_bar.setAttribute("class", "profile");
	chat_bar.setAttribute("onclick", `select_chat(${chat_data.chat_id})`);

	chat_bar.innerHTML = `
		<img src="PImg.jpg" alt="" width="100" height="100">
		<div class="name">
			${chat_data.user_name}
		</div>
		<div class="job">
			User
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
	// ToDo - params of url?
	if (message.chat_id != localStorage.getItem("current_chat"))
		return

	var message_bar = document.createElement('div');
	// ToDo: check is itself user
	

	// ToDo check is it current user == message.author_id
	var currentUser = false;

	if (currentUser) {
		message_bar.setAttribute("class", "wrapper");
		message_bar.innerHTML = `
                    <div class="item1L">
                        <div class="message">
                            <p class="message-text">${message.text}</p>
                          </div>
                    </div>
		`
	} else {

		message_bar.setAttribute("class", "wrapper1");
		message_bar.innerHTML = `
		            <div class="item1L">
                        <div class="message">
                            <p class="message-text">${message.text}</p>
                          </div>
                    </div>
		`
	}

	document.getElementById('messages_wrapper').appendChild(message_bar);
}

function add_messages(messages) {
	messages.forEach(item => add_message(item));
}

function select_chat(chat_id) {
	localStorage.setItem("current_chat", chat_id);

	messenger = document.getElementById("messages_wrapper");
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

function send_message() {
    //event.preventDefault(); // Отменяем стандартное поведение формы
    var formData = {
		chat_id: localStorage.getItem("current_chat"),
        message_text: document.getElementById('message_text').value
    };
    
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
}