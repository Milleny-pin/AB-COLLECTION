const form = document.getElementById('register-form');
const statusDiv = document.getElementById('status-message');
const registerButton = document.getElementById('register-button');

form.addEventListener('submit', async function(event){
    event.preventDefault();

    registerButton.disabled = true;
    registerButton.textContent = 'Aguarde...';
    statusDiv.style.display = 'none';

    const email = form.email.value;
    const password = form.password.value;

    const payload = {
        email: email,
        password: password
    };

    try{
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            }, 
            body: JSON.stringify(payload)
        });
        const data = await response.json();

                if (response.ok) {
                    statusDiv.textContent = data.message + " Redirecionando...";
                    statusDiv.style.backgroundColor = '#d4edda'; 
                    statusDiv.style.color = '#155724'; 
                    statusDiv.style.display = 'block';
                    
                   
                    setTimeout(() => {
                        window.location.href = '/'; 
                    }, 2000);

                } else {
                    statusDiv.textContent = 'Erro no cadastro: ' + (data.error || 'Ocorreu um erro desconhecido.');
                    statusDiv.style.backgroundColor = '#f8d7da'; 
                    statusDiv.style.color = '#721c24'; 
                    statusDiv.style.display = 'block';
                }

            } catch (error) {
                statusDiv.textContent = 'Erro de conexão: Não foi possível alcançar o servidor.';
                statusDiv.style.backgroundColor = '#f8d7da';
                statusDiv.style.color = '#721c24';
                statusDiv.style.display = 'block';
                console.error('Erro ao enviar formulário:', error);
            } finally {
              
                registerButton.disabled = false;
                registerButton.textContent = 'Cadastrar';
            }
        });
