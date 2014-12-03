$(document).ready(function() {
        var books_block = $('#books');
        $('input.search').on('keyup', function (ev) {
            if (this.value != '') {
                $.getJSON(search_url + this.value, function (data) {
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
        $('.button_delete').on('click', function(){
            var obj_id = this.dataset.id;
            var url = $('a.obj' + obj_id).attr('href');
            $.ajax(url, {
                type: 'DELETE',
                error: function(e) {alert(e.responseText)},
                success: function() {$('div.obj' + obj_id).remove()}
            });
        });
    }
);