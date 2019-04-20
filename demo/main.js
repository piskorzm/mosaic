function requestImage() {
    var request = 'http://127.0.0.1:5000/mozaika?';

    var random = (document.getElementById('losowo').checked ? '1' : '0');
    var width = document.getElementById('width').value;
    var height = document.getElementById('height').value;
    var color = document.getElementById('color').value;
    var urls = [];

    for (var i = 1; i <= 8; i++) {
        var url = document.getElementById('url' + i).value;
        if (url.length) {
            urls.push(url);
        }
    }

    request += 'losowo=' + random + '&';

    if(width.length || height.length) {
        request += 'rozdzielczosc=' + width + 'x' + height + '&';
    }

    if(color.length) {
        request += 'kolor=' + color + '&';
    }

    request += 'zdjecia=' + urls.join(',');
    
    var image_window = window.open(request);
    image_window.location.reload(true);
}