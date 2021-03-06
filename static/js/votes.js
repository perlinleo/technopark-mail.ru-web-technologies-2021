$('.js-votes').click(function(ev) {
    let $this = $(this),
        type = $this.data('type'),
        id = $this.data('id'),
        action = $this.data('action');
        
    $.ajax('/votes/', {
        method: 'POST',
        data: {
            type: type,
            id: id,
            action: action,
        },
    }).done(function(data) {
        location.reload()
    });
    
    console.log(type + " " + id + ": " + action);
    location.reload();
})

$('.js-not-authorized').click(function(ev) {
    location.replace("/signup/")
})