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
                $('#comments tbody')[0].prepend(template[0]);
            }
        })
    })
});