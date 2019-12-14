window.onload = rotate;
var i = 0;
var images = new Array("../static/image/familia3.jpg", "../static/image/familia.jpg","../static/image/pareja.jpg","../static/image/parejaMayor.jpg","../static/image/familia2.jpg","../static/image/hombre_perro.jpg");

function rotate() {
     i++;
     if (i == images.length) {
        i = 0;
     }
     document.getElementById("imagen").src = images[i];
     setTimeout(rotate, 3 * 1000);
}