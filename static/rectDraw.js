function addRectSettingsToDOM(pageNo, color, coordText) {
    var container = document.getElementById('rects' + pageNo);
    var ulNode = container.children[0];
    var textNode = document.createTextNode(coordText);
    var liNode = document.createElement('LI');
    liNode.appendChild(textNode);
    liNode.style.backgroundColor = color;
    ulNode.appendChild(liNode);
}

function loadRects(canvas, rects, filename, pageNo) {
    var request = new XMLHttpRequest();
    request.open("GET","rects/" + filename + "/" + pageNo);
    request.addEventListener('load', function(event) {
        if (request.status >= 200 && request.status < 300) {
            var json_rects = JSON.parse(request.responseText);
            for (var i = 0; i < json_rects.length; i++) {
                var rectColor = '#0000FF77';
                if (json_rects[i]["type"] === "Titel") rectColor = '#FF000077';
                if (json_rects[i]["type"] === "Kasten") rectColor = '#FFFF0077';
                if (json_rects[i]["type"] === "Text") rectColor = '#00AA0077';
                var newRect = new fabric.Rect({
                    left: json_rects[i]["rect"][1],
                    top: json_rects[i]["rect"][0],
                    fill: rectColor,
                    width: json_rects[i]["rect"][3] - json_rects[i]["rect"][1],
                    height: json_rects[i]["rect"][2] - json_rects[i]["rect"][0]
                });
                rects.push(newRect);
                canvas.add(newRect);
                canvas.bringToFront(newRect);
                canvas.renderAll();
                addRectSettingsToDOM(pageNo, rectColor, json_rects[i]["rect"])
            }
        } else {
          console.warn(request.statusText, request.responseText);
        }
    });
    request.send();
}

function populateCanvas(filename, pageNo) {
    var nativeCanvas = document.getElementById('cv' + pageNo);
    var canvas = new fabric.Canvas(nativeCanvas);
    var rects = [];
    fabric.Image.fromURL('pdf/20191209144348468.pdf/' + pageNo, function(oImg) {
        nativeCanvas.setAttribute('height', oImg.height);
        nativeCanvas.setAttribute('width', oImg.width);
        canvas.setHeight(oImg.height);
        canvas.setWidth(oImg.width);
        oImg.set({left: 0, top: 0, selectable: false, preserveObjectStacking: true});
        canvas.add(oImg);
        oImg.moveTo(-1000);
        canvas.renderAll();
    });
    loadRects(canvas, rects, filename, pageNo);
    canvas.renderAll();
    return canvas;
}

window.onload = function () {
    populateCanvas('20191209144348468.pdf', 9);
};
