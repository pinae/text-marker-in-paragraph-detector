window.onload = function () {
    var nativeCanvas = document.getElementById('cv9');
    var canvas = new fabric.Canvas(nativeCanvas);
    fabric.Image.fromURL('20191209144348468.pdf/9', function(oImg) {
        nativeCanvas.setAttribute('height', oImg.height);
        nativeCanvas.setAttribute('width', oImg.width);
        canvas.setHeight(oImg.height);
        canvas.setWidth(oImg.width);
        oImg.set({left: 0, top: 0, selectable: false});
        canvas.add(oImg);
        oImg.moveTo(-1);
        canvas.renderAll();
    });
    var rect = new fabric.Rect({
        left: 100,
        top: 100,
        fill: 'red',
        width: 20,
        height: 20
    });
    canvas.add(rect);
    canvas.renderAll();
};
