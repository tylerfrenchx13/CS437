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