$('.query-input').on('input', function(event){
    if(this.value.length == 0)
    {
        $('.suggestion-list').empty()
        return
    }
    if(this.value[this.value.length-1] == " ")
    {
        $.ajax({url: "/query_suggestion/" + this.value, success: function(result){
            $('.suggestion-list').empty()
            
            $.each( result, function( i, r ) {
                $('.suggestion-list').append('<a href="#" class="list-group-item">'+r+'</a>')
            });
        }});
    }
}); 


/* KEYDOWN ON ENTER DO SEARCH */
$('.query-input').on('keydown', function(event){
    if(event.which == 13) {
        location.href = "/search/"+$('.query-input').val();
    }
})

/* CLICK SEARCH BUTTON DO SEARCH */
$('.submit-btn').on('click', function(event){
     location.href = "/search/"+$('.query-input').val();
});