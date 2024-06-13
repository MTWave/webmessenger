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
      localStorage.setItem('jwtToken', data["access_token"])
      //window.location.href = '/dashboard'; // Редирект на другую страницу после успешной авторизации
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    });
  });

})();