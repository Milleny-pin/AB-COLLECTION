 const profileForm = document.getElementById('profile-form');
        const avatarInput = document.getElementById('avatar-input');
        const avatarPreview = document.getElementById('avatar-preview');
        const telefonesContainer = document.getElementById('telefones-container');
        const loadingElement = document.getElementById('loading');
        const uploadStatus = document.getElementById('upload-status');
        let currentProfileData = {};

        async function loadProfile() {
            loadingElement.classList.remove('hidden');
            profileForm.classList.add('hidden');

            try {
                const response = await fetch('/exibir_perfil');
                const data = await response.json();

                if (response.ok) {
                    currentProfileData = data;
                    
                    document.getElementById('full_name').value = data.nome_completo || '';
                    document.getElementById('email').value = data.email || 'Não informado';

                    if (data.image_url) {
                        avatarPreview.src = data.image_url;
                    }

                    telefonesContainer.innerHTML = ''; 
                    data.telefones.forEach(tel => addTelefoneField(tel));

                    profileForm.classList.remove('hidden');

                } else {
                    alert('Erro ao carregar perfil: ' + (data.erro || 'Desconhecido'));
                }

            } catch (error) {
                console.error('Falha na conexão:', error);
                alert('Falha ao conectar com o servidor para carregar o perfil.');
            } finally {
                loadingElement.classList.add('hidden');
            }
        }
        
        function addTelefoneField(telefone = { id: null, numero: '' }) {
            const index = telefonesContainer.children.length;
            const div = document.createElement('div');
            div.className = 'flex items-center space-x-2 mb-2';
            div.innerHTML = `
                <input type="text" 
                       placeholder="Número de telefone" 
                       value="${telefone.numero}"
                       data-id="${telefone.id || ''}"
                       class="telefone-input block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                <button type="button" onclick="removeTelefoneField(this)" class="p-2 text-red-500 hover:text-red-700 transition duration-150 text-sm font-semibold">Remover</button>
            `;
            telefonesContainer.appendChild(div);
        }

        function removeTelefoneField(button) {
            button.closest('div').remove();
        }

        avatarInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            uploadStatus.textContent = 'Enviando... Aguarde o upload.';
            
            avatarPreview.src = URL.createObjectURL(file);

            const formData = new FormData();
            formData.append('avatar_file', file);

            try {
                const response = await fetch('/upload_avatar', {
                    method: 'POST',
                    body: formData 
                });
                
                const data = await response.json();

                if (response.ok) {
                    uploadStatus.textContent = 'Foto atualizada com sucesso!';
                    avatarPreview.src = data.image_url; 
                    currentProfileData.image_url = data.image_url;
                } else {
                    uploadStatus.textContent = 'Erro no upload: ' + (data.erro || 'Falha desconhecida');
                    avatarPreview.src = currentProfileData.image_url || 'https://placehold.co/128x128/D1D5DB/4B5563?text=Avatar';
                }
            } catch (error) {
                console.error('Erro de rede durante o upload:', error);
                uploadStatus.textContent = 'Erro de conexão. Tente novamente.';
            }
        });

        profileForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            document.getElementById('save-button').textContent = 'Salvando...';
            document.getElementById('save-button').disabled = true;

            const telefones = Array.from(document.querySelectorAll('.telefone-input')).map(input => ({
                id: input.getAttribute('data-id') || null, 
                numero: input.value
            })).filter(t => t.numero.trim() !== ''); 
            
            const payload = {
                full_name: document.getElementById('full_name').value,
                telefones: telefones,
            };

            try {
                const response = await fetch('/editar_perfil', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (response.ok) {
                    alert('Sucesso: ' + data.mensagem);
                } else {
                    alert('Erro ao salvar: ' + (data.erro || 'Falha desconhecida'));
                }
            } catch (error) {
                console.error('Erro de rede ao salvar:', error);
                alert('Falha de conexão ao salvar.');
            } finally {
                document.getElementById('save-button').textContent = 'Salvar Alterações';
                document.getElementById('save-button').disabled = false;
            }
        });

        loadProfile();