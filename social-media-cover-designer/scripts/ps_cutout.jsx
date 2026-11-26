#target photoshop
// Batch Remove Background -> transparent PNGs. Tested on Photoshop 2027 (Windows).
// Usage: write a tiny runner .jsx and launch it with Photoshop.exe <runner.jsx> while Photoshop is open:
//   var CUT_JOBS_FILE = 'C:/proj/covers/cut_jobs.json';   // [["C:/in/a.png","C:/out/a_cut.png"], ...]
//   var LOG_FILE      = 'C:/proj/covers/ps_log.txt';
//   $.evalFile(new File('C:/Users/hello/.claude/skills/social-media-cover-designer/scripts/ps_cutout.jsx'));
app.displayDialogs = DialogModes.NO;
function _read(p) { var f = new File(p); f.encoding = 'UTF-8'; f.open('r'); var t = f.read(); f.close(); return t; }
var jobs = eval('(' + _read(CUT_JOBS_FILE) + ')');
var out = [];
for (var i = 0; i < jobs.length; i++) {
    var d = null;
    try {
        d = app.open(new File(jobs[i][0]));
        if (d.activeLayer.isBackgroundLayer) d.activeLayer.isBackgroundLayer = false;
        executeAction(stringIDToTypeID('removeBackground'), undefined, DialogModes.NO);
        // apply the layer mask
        var desc = new ActionDescriptor(), ref = new ActionReference();
        ref.putEnumerated(charIDToTypeID('Chnl'), charIDToTypeID('Chnl'), charIDToTypeID('Msk '));
        desc.putReference(charIDToTypeID('null'), ref); desc.putBoolean(charIDToTypeID('Aply'), true);
        executeAction(charIDToTypeID('Dlt '), desc, DialogModes.NO);
        var png = new PNGSaveOptions(); png.compression = 6;
        d.saveAs(new File(jobs[i][1]), png, true);
        d.close(SaveOptions.DONOTSAVECHANGES);
        out.push('ok ' + jobs[i][1]);
    } catch (e) {
        out.push('ERR ' + jobs[i][0] + ': ' + e + ' line ' + e.line);
        try { if (d) d.close(SaveOptions.DONOTSAVECHANGES); } catch (_) {}
    }
}
var lf = new File(LOG_FILE); lf.encoding = 'UTF-8'; lf.open('w'); lf.write(out.join('\n')); lf.close();
