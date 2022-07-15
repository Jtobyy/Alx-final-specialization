function resetP() {
    div = document.createElement('div')
    div.classList = 'bg-success text-white text-center fixed-top p-3'
    div.innerHTML = 'Kindly contact the admin to reset your password'
    document.getElementsByTagName('body')[0].append(div)
    console.log(document.getElementsByClassName('my-group')[0])
}

function showPassword(e) {
    if (document.getElementById('id_password').type === 'password') {
        document.getElementById('id_password').type = 'text'
        document.getElementById('show').innerHTML = 'hide'
    }
    else {
        document.getElementById('id_password').type = 'password'
        document.getElementById('show').innerHTML = 'show'
    }    
}