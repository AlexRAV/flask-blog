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
                form.body.value='';
                var template = $($('.comment')[0].outerHTML);
                template.find(".comment__author").text(response["author"]);
                template.find(".comment__date-publish-text").html(moment(response["created_at"]).format("HH:mm DD.MM.YYYY"));
                template.find(".comment__body").text(response["body"]);
                template.find(".comment__delete-container").html("<a href=" + response.url_for_delete + " class='col-lg-1 text-muted small comment__delete-btn'>Delete</a>");
                $('#comments tbody')[0].prepend(template[0]);
            }
        })
    });

    $('#comments').on('click.comment__delete-btn', function (e) {
        e.preventDefault();
        var link = e.target;
        window.testLink = link;

        $.ajax({
            'url': link.href,
            'method': 'POST',
            'success': function (resp) {
                if(resp.success == true) {
                    $(link).parents('tr.comment')[0].remove();
                }
            }
        })
    })
});