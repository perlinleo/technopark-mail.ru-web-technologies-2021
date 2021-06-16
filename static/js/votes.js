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
        $('#rating-' + id).text(data.rating);
        
    });
    location.reload();
    console.log(type + " " + id + ": " + action);
})

$('.js-not-authorized').click(function(ev) {
    location.replace("/signup/")
})