$("#Submit").on('click', function (e) {
    e.stopPropagation()

    alert("Submitted Fired");
    $(e.target).attr('id', 'Save');
    $(this).unbind('click');
})

$("body").on('click', '#Save', function (e) {
    alert("Save Event Fired");
})