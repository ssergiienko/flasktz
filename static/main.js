$(document).ready(function() {
        var books_block = $('#books');
        $('#search_input').on('keyup', function (ev) {
            if (this.value != '') {
                $.getJSON(search_url, 'str=' + this.value, function (data) {
                    if (data[0]) {
                        books_block.text('Найдено:');
                        for (var i in data) {
                            var elem = document.createElement('p');
                            elem.innerHTML = data[i];
                            books_block.append(elem);
                        }
                    } else {
                        books_block.text('Ничего не найдено')
                    }
                })
            } else {
                books_block.text('');
            }
        });
        $('.book_delete').on('click', function(){
            $.ajax(delete_books_url + this.id, {
                type: 'DELETE',
                error: function(e) {alert(e.responseText)},
                success: function() {$('div#' + this.id).remove();}
            });
        });
    }
);