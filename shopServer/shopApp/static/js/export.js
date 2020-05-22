/*
* 参数 data 是导出的数据
* 参数 title 是导出的标题
* showLabel 表示是否显示表头 默认显示
*/
function JSONToCSVConvertor(obj) {
    var JSONData = obj['data'],
    ShowLabel = typeof obj['showLabel'] === 'undefined' ? true : obj['showLabel'],
    ReportTitle = obj['title']
    //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;
    var CSV = '';
    var ShowLabel = typeof ShowLabel === 'undefined' ? true : ShowLabel;
    //This condition will generate the Label/Header
    if (ShowLabel) {
        var row = "";
        //This loop will extract the label from 1st index of on array
        for (var index in arrData[0]) {
            //Now convert each value to string and comma-seprated
            row += index + ',';
        }
        row = row.slice(0, -1);
        //append Label row with line break
        CSV += row + '\r\n';
    }
    //1st loop is to extract each row
    for (var i = 0; i < arrData.length; i++) {
        var row = "";
        //2nd loop will extract each column and convert it in string comma-seprated
        for (var index in arrData[i]) {
            row += '"' + arrData[i][index] + '",';
        }
        row.slice(0, row.length - 1);
        //add a line break after each row
        CSV += row + '\r\n';
    }
    if (CSV == '') {
        console.error();
        ("Invalid data");
        return;
    }
    //this trick will generate a temp "a" tag
    var link = document.createElement("a");
    link.id = "lnkDwnldLnk";
    //this part will append the anchor tag and remove it after automatic click
    document.body.appendChild(link);
    var csv = CSV;
    // var blob = new Blob(['\ufeff' + csv], {
    //     type: 'text/csv'
    // });
    var csvUrl = _getDownloadUrl(csv); //window.webkitURL.createObjectURL(blob);
    var filename = ReportTitle || 'UserExport';
    filename = filename + '.csv';
    var linkDom = document.getElementById('lnkDwnldLnk');
    linkDom.setAttribute('download', filename);
    linkDom.setAttribute('href', csvUrl);
    linkDom.click();
    document.body.removeChild(link);
}

function _getDownloadUrl(text) {
    var BOM = "\uFEFF";
    // Add BOM to text for open in excel correctly
    if (window.Blob && window.URL && window.URL.createObjectURL) {
        var csvData = new Blob([BOM + text], {
            type: 'text/csv'
        });
        return URL.createObjectURL(csvData);
    } else {
        return 'data:attachment/csv;charset=utf-8,' + BOM + encodeURIComponent(text);
    }
}
