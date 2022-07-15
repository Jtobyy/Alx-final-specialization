var current
const arr = $('.dontclick')

$('document').ready(function () {
    if (sessionStorage.getItem('settings')) {
        customSettings(document.getElementById('settings'))
    }
    else {
    let url = new URL(window.location.href)
    for (let i = 0; i < arr.length; i++) {
        if (arr[i].href == url) {
            arr[i].parentElement.classList.add('active-section');
            arr[i].nextElementSibling.classList.remove('hidden');
            return
        }    
    }
    for (let i = 0; i < arr.length; i++) {
        if (arr[i].href == sessionStorage.getItem('currentPath')) {
            arr[i].parentElement.classList.add('active-section');
            arr[i].nextElementSibling.classList.remove('hidden');
            return
        }    
    }
    arr[0].parentElement.classList.add('active-section');
    arr[0].nextElementSibling.classList.remove('hidden');
    }
})

$('.dontclick').on('click', (e) => {    
    if (e == document.getElementById('settings'))    
        return
    sessionStorage.removeItem('settings')
    e.preventDefault()
    showSection(e)
})

function showSection(e) {
    if (e.target) {
        $(e.target).unbind('click')
        e.target.click()
        sessionStorage.setItem('currentPath', e.target.href);
        for (let i = 0; i < arr.length; i++) arr[i].parentElement.classList.remove('active-section');
        e.target.classList.add('active-section');
    }
    else if(e) {
        for (let i = 0; i < arr.length; i++) arr[i].parentElement.classList.remove('active-section');
        e.classList.add('active-section');
        e.firstElementChild.click(); e.firstElementChild.click();
    }

}

function customDashboard() {
    d = new Date()
    let month = $('#month').val()
    if (month == 0 || month == '') month = d.getMonth() + 1
    $.get('/cyberstickadmin/custom_dashboard/?month='+month, (res) => {    
        $('#content').html(res)
        $('.section-pointer').addClass('hidden');
        $('#dashboard-cell').next().removeClass('hidden');
        $('#month').val($('#month_value').val())
    })    
}

function customSettings(el) {    
    $.get('/cyberstickadmin/custom_settings', (res) => {
        $('#content').html(res)
        $('.section-pointer').addClass('hidden');
        $('dontclick').removeClass('active-section');
        el.parentElement.classList.add('active-section');
        el.nextElementSibling.classList.remove('hidden');
        sessionStorage.setItem('settings', 'true')
    })
}

function getIndex() {
    $('#dashboard-cell').click()
}

function linkBack() {
    window.location.href = sessionStorage.getItem('currentPath')
}