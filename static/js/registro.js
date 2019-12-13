$(function(){
	$('#btnRegistro').click(function(){
		$.ajax({
			url: '/registro',
			data: $('form').serialize(),
            type: 'POST',
			success: function(response){
				alert('Usuario creado con éxito!');
				window.location.replace('verLogin');
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});