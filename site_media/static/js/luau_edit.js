var editor;
$(function(){
    editor = CodeMirror.fromTextArea($("#id_body")[0], {
        mode: 'markdown',
        theme: 'monokai',
        matchBrackets: true,
        width:'700px',
        height:'700px',
        lineWrapping: true,
        extraKeys: {"F11": toggleFullscreenEditing, "Esc": toggleFullscreenEditing}
    });

    function toggleFullscreenEditing(){
        var editorDiv = $('.CodeMirror-scroll'),
            bodyBar = $('#actionbar'),
            toggleFS = $('#toggle_fs');
        if (!editorDiv.hasClass('fullscreen')) {
            toggleFullscreenEditing.beforeFullscreen = { height: editorDiv.height(), width: editorDiv.width() }
            editorDiv.addClass('fullscreen')
                .height($(window).height() - 40)
                .width('100%');
            bodyBar.addClass('fullscreenBar')
                .addClass('topbar-inner');
            toggleFS.addClass('danger');
            editor.refresh();
        }
        else {
            editorDiv.removeClass('fullscreen')
                .height(toggleFullscreenEditing.beforeFullscreen.height)
                .width(toggleFullscreenEditing.beforeFullscreen.width)
            bodyBar.removeClass('fullscreenBar')
                .removeClass('topbar-inner');
            toggleFS.removeClass('danger');
            editor.refresh();
        }
    }
    
    $('#toggle_fs').click(function(evt){
        evt.preventDefault();
        toggleFullscreenEditing();
    })
    
    $('#save_edit').click(function(evt){
        $('#save_edit').addClass('disabled')
        var data = {}
        $('#page_form input, #page_form textarea').each(function(){
            if($(this).attr('name')){
                data[$(this).attr('name')] = $(this).val();
            }
        })
        data['body'] = editor.getValue()
        $.post('.', data, function(result){
            $('#save_edit').removeClass('disabled')
        })
        evt.preventDefault();
    })
})