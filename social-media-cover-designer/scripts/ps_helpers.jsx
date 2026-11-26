#target photoshop
// Reusable ExtendScript helpers for cover layouts (tested Photoshop 2027).
// Include from a layout script:  $.evalFile(new File('<skill>/scripts/ps_helpers.jsx'));
// Pass all copy (Telugu/Hindi) via a UTF-8 JSON file: readJSON(path). Never hard-code Indic text in .jsx.
// Avoid naming a global variable `path` (it collides in ExtendScript).
app.displayDialogs = DialogModes.NO;
app.preferences.rulerUnits = Units.PIXELS;
app.preferences.typeUnits = TypeUnits.PIXELS;

function c2(s) { return charIDToTypeID(s); }
function readText(p) { var f = new File(p); f.encoding = 'UTF-8'; f.open('r'); var t = f.read(); f.close(); return t; }
function readJSON(p) { return eval('(' + readText(p) + ')'); }
function writeLog(p, s, append) { var f = new File(p); f.encoding = 'UTF-8'; f.open(append ? 'a' : 'w'); f.writeln(s); f.close(); }
function rgb(hex) { var c = new SolidColor(); c.rgb.hexValue = hex; return c; }
function rgbDesc(hex) { var c = rgb(hex), d = new ActionDescriptor(); d.putDouble(c2('Rd  '), c.rgb.red); d.putDouble(c2('Grn '), c.rgb.green); d.putDouble(c2('Bl  '), c.rgb.blue); return d; }
// fontOK scans the font list once (getByName throws an uncatchable 'No such element' inside nested evalFile)
var __FONTS = null;
function fontOK(ps) { if (!__FONTS) { __FONTS = {}; for (var i = 0; i < app.fonts.length; i++) __FONTS[app.fonts[i].postScriptName] = 1; } return !!__FONTS[ps]; }
function findFonts(substr) { fontOK(''); var r = []; for (var n in __FONTS) if (n.toLowerCase().indexOf(substr.toLowerCase()) >= 0) r.push(n); return r; }
function bnd(L) { var b = L.bounds; return [b[0].as('px'), b[1].as('px'), b[2].as('px'), b[3].as('px')]; }

function newDoc(w, h, name) { return app.documents.add(w, h, 72, name, NewDocumentMode.RGB, DocumentFill.TRANSPARENT); }

// Copy a PNG/JPG in as a new top layer (optionally scale %, then move to x,y top-left).
function placeImage(doc, file, name, scalePct, x, y) {
    var src = app.open(new File(file));
    if (src.activeLayer.isBackgroundLayer) src.activeLayer.isBackgroundLayer = false;
    src.activeLayer.duplicate(doc, ElementPlacement.PLACEATBEGINNING);
    src.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = doc;
    var L = doc.layers[0]; L.name = name;
    if (scalePct && scalePct !== 100) L.resize(scalePct, scalePct, AnchorPosition.TOPLEFT);
    if (x !== undefined) { var b = bnd(L); L.translate(x - b[0], y - b[1]); }
    return L;
}

// Layer FX on the active layer. o = {stroke:[hex,px], shadow:[hex,opacity,distance,size,spread,normalBlend], glow:[hex,opacity,size]}
function setFx(o) {
    var d = new ActionDescriptor(), r = new ActionReference();
    r.putProperty(c2('Prpr'), c2('Lefx')); r.putEnumerated(c2('Lyr '), c2('Ordn'), c2('Trgt'));
    d.putReference(c2('null'), r);
    var fx = new ActionDescriptor(); fx.putUnitDouble(c2('Scl '), c2('#Prc'), 100);
    if (o.stroke) {
        var s = new ActionDescriptor();
        s.putBoolean(c2('enab'), true); s.putEnumerated(c2('Styl'), c2('FStl'), c2('OutF'));
        s.putEnumerated(c2('PntT'), c2('FrFl'), c2('SClr')); s.putEnumerated(c2('Md  '), c2('BlnM'), c2('Nrml'));
        s.putUnitDouble(c2('Opct'), c2('#Prc'), 100); s.putUnitDouble(c2('Sz  '), c2('#Pxl'), o.stroke[1]);
        s.putObject(c2('Clr '), c2('RGBC'), rgbDesc(o.stroke[0])); fx.putObject(c2('FrFX'), c2('FrFX'), s);
    }
    if (o.shadow) {  // [hex, opacity, distance, size, spread, normalBlend]; normalBlend=true gives solid 2.5D extrusion
        var h = new ActionDescriptor();
        h.putBoolean(c2('enab'), true); h.putEnumerated(c2('Md  '), c2('BlnM'), c2(o.shadow[5] ? 'Nrml' : 'Mltp'));
        h.putObject(c2('Clr '), c2('RGBC'), rgbDesc(o.shadow[0])); h.putUnitDouble(c2('Opct'), c2('#Prc'), o.shadow[1]);
        h.putBoolean(c2('uglg'), false); h.putUnitDouble(c2('lagl'), c2('#Ang'), 100);
        h.putUnitDouble(c2('Dstn'), c2('#Pxl'), o.shadow[2]); h.putUnitDouble(c2('Ckmt'), c2('#Pxl'), o.shadow[4] || 0);
        h.putUnitDouble(c2('blur'), c2('#Pxl'), o.shadow[3]); fx.putObject(c2('DrSh'), c2('DrSh'), h);
    }
    if (o.glow) {  // outer glow, e.g. rim light ['FFB347', 25, 30]
        var g = new ActionDescriptor();
        g.putBoolean(c2('enab'), true); g.putEnumerated(c2('Md  '), c2('BlnM'), c2('Scrn'));
        g.putObject(c2('Clr '), c2('RGBC'), rgbDesc(o.glow[0])); g.putUnitDouble(c2('Opct'), c2('#Prc'), o.glow[1]);
        g.putUnitDouble(c2('blur'), c2('#Pxl'), o.glow[2]); fx.putObject(c2('OrGl'), c2('OrGl'), g);
    }
    d.putObject(c2('T   '), c2('Lefx'), fx);
    executeAction(c2('setd'), d, DialogModes.NO);
}

// Text layer that shrinks to fit maxW x maxH; returns the layer. align 'L' | 'C'
function makeText(doc, str, font, size, hex, name, maxW, maxH) {
    var L = doc.artLayers.add(); L.kind = LayerKind.TEXT; L.name = name;
    var t = L.textItem; t.contents = str; t.font = font; t.size = new UnitValue(size, 'px');
    t.color = rgb(hex); t.antiAliasMethod = AntiAlias.STRONG; t.position = [0, size];
    var b = bnd(L), s = size;
    while (((b[2] - b[0]) > maxW || (maxH && (b[3] - b[1]) > maxH)) && s > 12) { s -= 2; t.size = new UnitValue(s, 'px'); b = bnd(L); }
    return L;
}
function centreAt(L, cx, cy) { var b = bnd(L); L.translate(cx - (b[0] + b[2]) / 2, cy - (b[1] + b[3]) / 2); }
function leftAt(L, x, cy) { var b = bnd(L); L.translate(x - b[0], cy - (b[1] + b[3]) / 2); }
function placeAbove(L, refTop, gap, cx) { var b = bnd(L); L.translate(cx - (b[0] + b[2]) / 2, (refTop - gap) - b[3]); return bnd(L)[1]; }
function placeBelow(L, refBottom, gap, cx) { var b = bnd(L); L.translate(cx - (b[0] + b[2]) / 2, (refBottom + gap) - b[1]); return bnd(L)[3]; }

// Filled shapes on a new pixel layer (polygon selection is reliable; PathItem fills can silently fail)
function fillPoly(doc, pts, hex, name) {
    var L = doc.artLayers.add(); L.name = name; doc.activeLayer = L;
    doc.selection.select(pts, SelectionType.REPLACE, 0, true); doc.selection.fill(rgb(hex)); doc.selection.deselect();
    return L;
}
function roundRectPts(x, y, w, h, r) {
    var pts = [], n = 10, cs = [[x + w - r, y + r, -90], [x + w - r, y + h - r, 0], [x + r, y + h - r, 90], [x + r, y + r, 180]];
    for (var c = 0; c < 4; c++) for (var i = 0; i <= n; i++) {
        var a = (cs[c][2] + 90 * i / n) * Math.PI / 180; pts.push([cs[c][0] + r * Math.cos(a), cs[c][1] + r * Math.sin(a)]);
    }
    return pts;
}
// Label bar behind an existing text layer (padding px), placed directly under it
function labelBar(doc, textLayer, hex, padX, padY, radius) {
    var b = bnd(textLayer);
    var L = fillPoly(doc, roundRectPts(b[0] - padX, b[1] - padY, (b[2] - b[0]) + 2 * padX, (b[3] - b[1]) + 2 * padY, radius || 0), hex, 'Label bar');
    L.move(textLayer, ElementPlacement.PLACEAFTER); return L;
}

function saveAll(doc, base) {  // base without extension -> .psd (layers) + .png
    var pso = new PhotoshopSaveOptions(); pso.layers = true; pso.embedColorProfile = true;
    doc.saveAs(new File(base + '.psd'), pso, true);
    var png = new PNGSaveOptions(); png.compression = 6;
    doc.saveAs(new File(base + '.png'), png, true);
}
function saveJPG(doc, file, quality) {
    var o = new JPEGSaveOptions(); o.quality = quality || 10; o.embedColorProfile = true;
    doc.saveAs(new File(file), o, true);
}
