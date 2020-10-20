$(document).ready(function(){
    $('select[name=data_input]').change(function(){
        $('select[name="script"]').empty()
        $('select[name="script"]').formSelect()
        let script_id = $(this).val();
        let request_url = 'get_scripts/' + script_id + '/';
        $.ajax({
            type: 'GET',
            url: request_url,
            success: function(data){
                $.each(JSON.parse(data), function(index, text){
                    console.log(data)
                    $('select[name="script"]').append(
                        $('<option></option>').val(index).html(text)
                    );
                    $('select[name="script"]').formSelect()
                });
            }
        });
        return false;
    })
});