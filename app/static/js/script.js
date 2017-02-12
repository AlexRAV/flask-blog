$(function () {
    $('.delete-article').on('click', function (e) {
        var href = $(e.currentTarget).data('href');
        $('#deleteArticle .delete').attr('href', href);
    });

    $('#newComment').on('submit', function (e) {
        e.preventDefault();
        var form = e.currentTarget;

        $.ajax({
            'url': form.action,
            'method': form.method,
            'data': {
                body: form.body.value,
                csrf_token: form.csrf_token.value
            },
            'success': function (response) {
                form.body.value = '';
                var template = $($('.comment')[0].outerHTML);
                template.find(".comment__author").text(response["author"]);
                template.find(".comment__date-publish-text").html(moment(response["created_at"]).format("HH:mm DD.MM.YYYY"));
                template.find(".comment__body").text(response["body"]);
                template.find(".comment__delete-container").html("<a href=" + response.url_for_delete + " class='col-lg-1 text-muted small comment__delete-btn'>Delete</a>");
                $('#comments tbody')[0].prepend(template[0]);
            }
        })
    });

    $('#comments').on('click', '.comment__delete-btn', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var link = e.target;

        $.ajax({
            'url': link.href,
            'method': 'POST',
            'success': function (resp) {
                if (resp.success == true) {
                    $(link).parents('tr.comment')[0].remove();
                }
            }
        })
    });

    $('#comments').on('click', '.comment__edit-btn', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var link = e.target;
        var comment = $(link).parents('tr.comment')[0];
        var body = $(comment).find('.comment__body')[0];
        var bodyText = $(body).text();

        $(link).text('Save');
        link.isEdited = true;
        body.contentEditable = true;
        body.focus();
        $(body).addClass('form-control');
        $(body).on('blur', function (e) {
            console.dir(e);
            $(this).removeClass('form-control');
            $(link).text('Edit');
            this.contentEditable = false;
            link.isEdited = false;

            if ($(e.relatedTarget).hasClass('comment__edit-btn')) {
                $.ajax({
                    'url': link.href,
                    'method': 'POST',
                    'data': {body: $(body).text()},
                    'success': function (resp) {
                        if (resp.success == true) {
                            console.log('Обновили');
                        }
                    }
                })
            }
            else {
                $(body).text(bodyText);
            }
        });
    })
});