$(function(){
	$('#btnSolicitar').click(function(){
		$.ajax({
			url: '/simular',
			data: $('form').serialize(),
            type: 'POST',
			success: function(response){
				alert("Solicitud enviada con éxito!");
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});