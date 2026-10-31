const form_login = document.querySelector('#form_login')
const form_register = document.querySelector('#form_create_register')
const links_login = document.querySelector('#no_register_forgot_password')
const links_register = document.querySelector('#registered')
const titulo = document.querySelector('#titulo_acesso')

const open_registration_record = () => {
    form_login.hidden = true
    links_login.hidden = true
    form_register.hidden = false
    links_register.hidden = false
    titulo.textContent = 'Criar seu cadastro'
}

const open_login = () => {
    form_login.hidden = false
    links_login.hidden = false
    form_register.hidden = true
    links_register.hidden = true
    titulo.textContent = 'Login do cliente'
}

document.querySelector('#no_register')
    .addEventListener('click', open_registration_record)

document.querySelector('#btn_entrar')
    .addEventListener('click', open_login)
