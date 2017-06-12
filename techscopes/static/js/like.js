$(document).ready(function() {
    $('.like-button').on('click', function(e){
        e.preventDefault();
        var elem = $(this);

        var counter = $(elem.data("counter"));
        var count = parseInt(counter.text());

        var url = elem.data("url");
        var content_type = elem.data("content_type");
        var object_id = elem.data("object_id");

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                content_type: content_type,
                object_id: object_id
            },
            success: function(response) {
                if(response.removed_like){
                    counter.text(count - 1);
                }
                if(response.added_like){
                    counter.text(count + 1);
                }
            },
        });
        e.stopPropagation();
    });
});