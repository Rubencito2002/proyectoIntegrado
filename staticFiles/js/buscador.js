$(document).ready(function(){
    $('#search-query').on('keyup', function(){
        var query = $(this).val();
        $.ajax({
            url: '{% url "search_products" %}',
            data: {
                'query': query
            },
            success: function(data){
                $('#product-list').html(data.html);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});