// Função para alternar entre formulários
function mostrarFormulario(formulario) {
    document.querySelectorAll('.formulario').forEach(function(section) {
        section.style.display = 'none';
    });
    document.getElementById(formulario).style.display = 'block';
}



//! Formulario adicionar Usuario
document.getElementById('formulariousuario').addEventListener('submit', function(event) {
    event.preventDefault();

    let nome = document.querySelector('#cadastrarUsuario input[name="nome"]').value;
    let email = document.querySelector('#cadastrarUsuario input[name="email"]').value;
    let tipo = document.querySelector('#cadastrarUsuario select[name="tipo"]').value;
    let senha = document.querySelector('#cadastrarUsuario input[name="senha"]').value;

    const usuario = { nome, email, tipo, senha };

    fetch('http://localhost:8000/usuarios/adicionar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(usuario)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        listarUsuarios(nome, email, tipo);
        document.getElementById('formulariousuario').reset();
        document.getElementById('feedbackusuario').innerHTML = 'Usuário adicionado com sucesso!';
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('feedbackusuario').innerHTML = `Erro ao adicionar usuário: ${error.message}`;
    });
});

//! Formulário para adicionar um veículo
document.getElementById('formularioveiculo').addEventListener('submit', function(event) {
    event.preventDefault();

    let placa = document.getElementById('placa').value;
    let modelo = document.getElementById('modelo').value;
    let marca = document.getElementById('marca').value;
    let cor = document.getElementById('cor').value;

    const veiculo = { placa, modelo, marca, cor };

    fetch('http://localhost:8000/veiculos/adicionar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(veiculo)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('formularioveiculo').reset(); // Limpa o formulário
        document.getElementById('feedbackveiculo').innerHTML = 'Veículo adicionado com sucesso!';
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('feedbackveiculo').innerHTML = `Erro ao adicionar veículo: ${error.message}`;
    });
});

// Submissão do formulário para adicionar um dispositivo
document.getElementById('formulariodispositivo').addEventListener('submit', function(event) {
    event.preventDefault();

    let nome = document.getElementById('nomedisp').value;
    let tipo = document.getElementById('tipodisp').value;
    let quantidade = document.getElementById('quantidadedisp').value;

    // Dados do dispositivo a serem enviados para o backend
    const dispositivo = { nome, tipo, quantidade };

    // Enviar os dados para o backend
    fetch('http://localhost:8000/dispositivos/adicionar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dispositivo)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // Aqui estamos assumindo que o backend retorna {"message": "Dispositivo adicionado com sucesso"}
        if (data.message) {
            document.getElementById('formulariodispositivo').reset();
            document.getElementById('feedbackdispositivo').innerHTML = 'Dispositivo adicionado com sucesso!';
        } else {
            document.getElementById('feedbackdispositivo').innerHTML = 'Erro ao adicionar dispositivo.';
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('feedbackdispositivo').innerHTML = `Erro ao adicionar dispositivo: ${error.message}`;
    });
});









function preencherFormulario(usuario) {
    document.getElementById('editUsuarioId').value = usuario.id;
    document.getElementById('editUsuarioNome').value = usuario.nome;
    document.getElementById('editUsuarioEmail').value = usuario.email;
    document.getElementById('editUsuarioTipo').value = usuario.tipo;
}


// Funções para listar os itens nas listas
function listarUsuarios() {
    fetch('http://localhost:8000/usuarios/listar')
    .then(response => response.json())
    .then(data => {
        const lista = document.getElementById('listaUsuarios');
        const tituloLista = document.getElementById('tituloListaUsuarios');

        tituloLista.style.display = 'block';
        lista.style.display = 'block';
        lista.innerHTML = ''; 

        data.usuarios.forEach(usuario => {
            const li = document.createElement('li');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `usuario_${usuario.id}`;

            const label = document.createElement('label');
            label.htmlFor = `usuario_${usuario.id}`;
            label.textContent = `${usuario.nome} - ${usuario.email} (${usuario.tipo})`;

            const btnAlterar = document.createElement('button');
            btnAlterar.textContent = 'Alterar';
            btnAlterar.onclick = function() {
                mostrarFormulario('editarUsuario'); // Exibe o formulário de edição
                preencherFormulario(usuario); // Preenche os dados do usuário
            };

            const btnExcluir = document.createElement('button');
            btnExcluir.textContent = 'Excluir';
            btnExcluir.onclick = function() {
                excluirUsuario(usuario.id);
            };

            li.appendChild(checkbox);
            li.appendChild(label);
            li.appendChild(btnAlterar);
            li.appendChild(btnExcluir);

            lista.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Erro ao listar usuários:', error);
        document.getElementById('feedbackusuario').innerHTML = 'Erro ao listar usuários.';
    });
}


function listarVeiculos() {
    fetch('http://localhost:8000/veiculos/listar')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const lista = document.getElementById('listaVeiculos');
            const tituloLista = document.getElementById('tituloListaVeiculos');

            // Exibe o título e a lista
            tituloLista.style.display = 'block';
            lista.style.display = 'block';
            lista.innerHTML = ''; // Limpa a lista antes de adicionar novos itens

            // Adiciona cada veículo à lista
            data.veiculos.forEach(veiculo => {
                const li = document.createElement('li');
                li.textContent = `${veiculo.placa} - ${veiculo.modelo} (${veiculo.marca}, ${veiculo.cor})`;

                const btnAlterar = document.createElement('button');
                btnAlterar.textContent = 'Alterar';
                btnAlterar.onclick = function() {
                    mostrarFormularioVeiculo('editarVeiculo'); // Exibe o formulário de edição
                    preencherFormularioVeiculo(veiculo); // Preenche os dados do veículo
                };

                const btnExcluir = document.createElement('button');
                btnExcluir.textContent = 'Excluir';
                btnExcluir.onclick = function() {
                    excluirVeiculo(veiculo.id); // Chama a função para excluir o veículo
                };

                li.appendChild(btnAlterar);
                lista.appendChild(li);

                li.appendChild(btnExcluir);
                listaVeiculos.appendChild(li);
            
            });
        })
        .catch(error => {
            console.error('Erro ao listar veículos:', error);
            document.getElementById('feedbackveiculo').innerHTML = 'Erro ao listar veículos.';
        });
}

// Chame esta função no evento de clique
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('listarVeiculosLink').addEventListener('click', function() {
        listarVeiculos(); // Chama a função para listar veículos
    });
});

function listarDispositivos() {
    fetch('http://localhost:8000/dispositivos/listar')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const lista = document.getElementById('listaDispositivos');
            const tituloLista = document.getElementById('tituloListaDispositivos');

            // Exibe o título e a lista
            tituloLista.style.display = 'block';
            lista.style.display = 'block';
            lista.innerHTML = ''; // Limpa a lista antes de adicionar novos itens

            // Adiciona cada dispositivo à lista com botões de editar e excluir
            data.dispositivos.forEach(dispositivo => {
                const li = document.createElement('li');
                li.textContent = `${dispositivo.nome} - ${dispositivo.tipo} (Quantidade: ${dispositivo.quantidade})`;

                // Botão para editar o dispositivo
                const editarBtn = document.createElement('button');
                editarBtn.textContent = 'Editar';
                editarBtn.onclick = () => mostrarFormularioEdicaoDispositivo(dispositivo);

                // Botão para excluir o dispositivo
                const excluirBtn = document.createElement('button');
                excluirBtn.textContent = 'Excluir';
                excluirBtn.onclick = () => excluirDispositivo(dispositivo.id);

                li.appendChild(editarBtn);
                li.appendChild(excluirBtn);
                lista.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Erro ao listar dispositivos:', error);
            document.getElementById('feedbackdispositivo').innerHTML = 'Erro ao listar dispositivos.';
        });
}



// Chame esta função no evento de clique
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('listarDispositivosLink').addEventListener('click', function() {
        listarDispositivos(); // Chama a função para listar dispositivos
    });
});


//! EDITAR USUARIO

document.getElementById('formularioEditarUsuario').addEventListener('submit', function(event) {
    event.preventDefault();

    let id = document.getElementById('editUsuarioId').value;
    let nome = document.getElementById('editUsuarioNome').value;
    let email = document.getElementById('editUsuarioEmail').value;
    let tipo = document.getElementById('editUsuarioTipo').value;
    let senha = document.getElementById('editUsuarioSenha').value;

    const usuarioAtualizado = { nome, email, tipo, senha };

    fetch(`http://localhost:8000/usuarios/alterar/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(usuarioAtualizado)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        listarUsuarios(); // Atualiza a lista de usuários
        document.getElementById('editarUsuario').style.display = 'none'; // Esconde o formulário de edição
        document.getElementById('feedbackEdicaoUsuario').innerHTML = 'Usuário atualizado com sucesso!';
    })
    .catch(error => {
        console.error('Erro ao atualizar usuário:', error);
        document.getElementById('feedbackEdicaoUsuario').innerHTML = `Erro ao atualizar usuário: ${error.message}`;
    });
});

function mostrarFormulario(formId) {
    document.getElementById(formId).style.display = 'block';
}


// Função para preencher o formulário de edição com os dados do veículo
function preencherFormularioVeiculo(veiculo) {
    document.getElementById('editVeiculoId').value = veiculo.id;
    document.getElementById('editVeiculoPlaca').value = veiculo.placa;
    document.getElementById('editVeiculoModelo').value = veiculo.modelo;
    document.getElementById('editVeiculoMarca').value = veiculo.marca;
    document.getElementById('editVeiculoCor').value = veiculo.cor;
}

//! Função para editar um veículo
document.getElementById('formularioEditarVeiculo').addEventListener('submit', function(event) {
    event.preventDefault();

    let id = document.getElementById('editVeiculoId').value;
    let placa = document.getElementById('editVeiculoPlaca').value;
    let modelo = document.getElementById('editVeiculoModelo').value;
    let marca = document.getElementById('editVeiculoMarca').value;
    let cor = document.getElementById('editVeiculoCor').value;

    const veiculoAtualizado = { placa, modelo, marca, cor };

    fetch(`http://localhost:8000/veiculos/alterar/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(veiculoAtualizado)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        listarVeiculos(); // Atualiza a lista de veículos
        document.getElementById('editarVeiculo').style.display = 'none'; // Esconde o formulário de edição
        document.getElementById('feedbackEdicaoVeiculo').innerHTML = 'Veículo atualizado com sucesso!';
    })
    .catch(error => {
        console.error('Erro ao atualizar veículo:', error);
        document.getElementById('feedbackEdicaoVeiculo').innerHTML = `Erro ao atualizar veículo: ${error.message}`;
    });
});

// Função para exibir o formulário de edição
function mostrarFormularioVeiculo(formId) {
    document.getElementById(formId).style.display = 'block';
}

//! Editar dispositivo
function mostrarFormularioEdicaoDispositivo(dispositivo) {
    document.getElementById('editDispositivoId').value = dispositivo.id;
    document.getElementById('editDispositivoNome').value = dispositivo.nome;
    document.getElementById('editDispositivoTipo').value = dispositivo.tipo;
    document.getElementById('editDispositivoQuantidade').value = dispositivo.quantidade;

    document.getElementById('editarDispositivo').style.display = 'block';
}

document.getElementById('formularioEditarDispositivo').addEventListener('submit', function(event) {
    event.preventDefault();

    let id = document.getElementById('editDispositivoId').value;
    let nome = document.getElementById('editDispositivoNome').value;
    let tipo = document.getElementById('editDispositivoTipo').value;
    let quantidade = document.getElementById('editDispositivoQuantidade').value;

    const dispositivoAtualizado = { nome, tipo, quantidade };

    fetch(`http://localhost:8000/dispositivos/alterar/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dispositivoAtualizado)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        listarDispositivos(); // Atualiza a lista de dispositivos
        document.getElementById('editarDispositivo').style.display = 'none'; // Esconde o formulário de edição
        document.getElementById('feedbackEdicaoDispositivo').innerHTML = 'Dispositivo atualizado com sucesso!';
    })
    .catch(error => {
        console.error('Erro ao atualizar dispositivo:', error);
        document.getElementById('feedbackEdicaoDispositivo').innerHTML = `Erro ao atualizar dispositivo: ${error.message}`;
    });
});


//! EXCLUIR
function excluirUsuario(usuarioId) {
    if (confirm("Tem certeza que deseja excluir este usuário?")) {
        fetch(`http://localhost:8000/usuarios/excluir/${usuarioId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                listarUsuarios(); // Atualiza a lista após a exclusão
                document.getElementById('feedbackusuario').innerHTML = 'Usuário excluído com sucesso!';
            } else {
                throw new Error('Erro ao excluir usuário.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            document.getElementById('feedbackusuario').innerHTML = 'Erro ao excluir usuário.';
        });
    }
}


function excluirVeiculo(veiculoId) {
    if (confirm("Tem certeza que deseja excluir este veículo?")) {
        fetch(`http://localhost:8000/veiculos/excluir/${veiculoId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                listarVeiculos(); // Atualiza a lista de veículos após a exclusão
                document.getElementById('feedbackveiculo').innerHTML = 'Veículo excluído com sucesso!';
            } else {
                throw new Error('Erro ao excluir veículo.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            document.getElementById('feedbackveiculo').innerHTML = 'Erro ao excluir veículo.';
        });
    }
}


function excluirDispositivo(dispositivoId) {
    if (confirm("Tem certeza que deseja excluir este dispositivo?")) {
        fetch(`http://localhost:8000/dispositivos/excluir/${dispositivoId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao excluir dispositivo.');
            }
            listarDispositivos(); // Atualiza a lista após a exclusão
            document.getElementById('feedbackdispositivo').innerHTML = 'Dispositivo excluído com sucesso!';
        })
        .catch(error => {
            console.error('Erro:', error);
            document.getElementById('feedbackdispositivo').innerHTML = 'Erro ao excluir dispositivo.';
        });
    }
}


