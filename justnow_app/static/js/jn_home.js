$('.datepicker').datepicker({
    todayHighlight: true,
    endDate: '1d',
    format: 'mm-dd-yyyy',
});

$('#form_entry_date').submit((e) => {
    e.preventDefault();
    window.location = `/entry/${$('.datepicker').val()}`;
});
