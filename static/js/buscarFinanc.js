$(function(){
    $.ajax({
        url : '/buscarFinanc',
        type : 'GET',
        success: function(res){
            var div = $('<div>')
            .attr('class', 'list-group')
            .append(
                $('<p>').attr('class', 'list-group-item active')
                .append(
                    $('<span>').attr('id', 'a1').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a2').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a3').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a4').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a5').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a6').attr('class', 'list-group-item-text spanlist')
                )
            );
            var div1 = $('<div>')
            .attr('class', 'list-group')
            .append(
                $('<p>').attr('class', 'list-group-item')
                .append(
                    $('<span>').attr('id', 'a1').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a2').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a3').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a4').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a5').attr('class', 'list-group-item-text spanlist'),
                    $('<span>').attr('id', 'a6').attr('class', 'list-group-item-text spanlist')
                )
            );

            var title = '';
            title = $(div).clone();
                $(title).find('span#a1').text('Valor Prestamo');
                $(title).find('span#a2').text('meses');
                $(title).find('span#a3').text('Mensua- lidad');
                $(title).find('span#a4').text('mes actual');
                $(title).find('span#a5').text('meses en retraso');
                $(title).find('span#a6').text('Valor en retraso');
                $('.jumbotron').append(title);
            
            var finObj = JSON.parse(res);
            var fin = '';
            
            $.each(finObj,function(index, value){
                fin = $(div1).clone();
                $(fin).find('span#a1').text(value.Total);
                $(fin).find('span#a2').text(value.meses);
                $(fin).find('span#a3').text(value.Mensualidad);
                $(fin).find('span#a4').text(value.mesActual);
                $(fin).find('span#a5').text(value.mesesRetraso);
                $(fin).find('span#a6').text(value.ImporteRetraso);
                $('.jumbotron').append(fin);
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
});