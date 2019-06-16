let editor = new FroalaEditor('#text', {
    events: {
        'keydown': handleSave,
    },
});
let typeTimeout = null;

function handleSave() {
    $('#saved').text('Editing...');
    clearTimeout(typeTimeout);
    typeTimeout = setTimeout(() => {
        save();
    }, 500)
}

function save() {
    $.post(`entry/${entryDate}/save`, {
        text: editor.html.get(true),
    }, () => {
        $('#saved').text('Saved!');
    }, 'json');
}
