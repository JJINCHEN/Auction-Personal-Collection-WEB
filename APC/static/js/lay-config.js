/**
 * date:2019/08/16
 * author:Mr.Chung
 * description:Layui custom extension here
 */

window.rootPath = (function (src) {
    src = document.scripts[document.scripts.length - 1].src;
    return src.substring(0, src.lastIndexOf("/") + 1);
})();

layui.config({
    base: rootPath + "lay-module/",
    version: true
}).extend({
    layuimini: "layuimini/layuimini", // layuimini extend
    step: 'step-lay/step', // Step by step form extension
    treetable: 'treetable-lay/treetable', //table Tree extension
    tableSelect: 'tableSelect/tableSelect', // table Select extension
    iconPickerFa: 'iconPicker/iconPickerFa', // fa Icon selection extension
    echarts: 'echarts/echarts', // echarts Chart extension
    echartsTheme: 'echarts/echartsTheme', // echarts Chart theme extension
    wangEditor: 'wangEditor/wangEditor', // wangEditor Rich text extension
    layarea: 'layarea/layarea', //  Three level linkage pull-down selector of provinces, cities, counties and districts
});