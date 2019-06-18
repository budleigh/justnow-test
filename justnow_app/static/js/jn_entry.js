let editor = new FroalaEditor('#text', {
    events: {
        'keydown': handleSave,
    },
}, () => {
    editor.html.set(entryText);
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
    $.ajax({
        type: "POST",
        url: `/entry/${entryDate}/save`,
        data: {
            text: editor.html.get(true),
        },
        success: () => {
            $('#saved').text('Saved!');
        },
    });
}

$('#ask').submit((e) => {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: `/entry/${entryDate}/ask`,
        data: {
            question: $('#question-input').val()
        },
        success: () => {
            $('#question-input').val('');
        },
    });
});
