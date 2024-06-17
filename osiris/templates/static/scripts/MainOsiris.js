(function(){

  document.getElementById('login_form').addEventListener('submit', function() {
    // ToDo use formData object
    var formData = {
      login: document.getElementById('username').value,
      password: document.getElementById('password').value
    };
   
    fetch(
        'auth/sign_in', {
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
    .then(data => {
      console.log(data);
      window.location.href = '/chat'; // Редирект на другую страницу после успешной авторизации
    })
    .catch(error => {
      console.error('Error:', error);
      const input1 = document.getElementById('username');
      const input2 = document.getElementById('password');
      input1.style.borderColor = 'red';
      input2.style.borderColor = 'red';
    });
  });

})();
