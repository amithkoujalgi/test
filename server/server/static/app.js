$(document).ready(function () {
    var editor1 = ace.edit("editor1");
    editor1.setTheme("ace/theme/monokai");
    editor1.session.setMode("ace/mode/yaml");
    editor1.setOption("showPrintMargin", false)
    editor1.setValue("base_image: razor-core:2.2.1", 1)

    var editor2 = ace.edit("editor2");
    editor2.setTheme("ace/theme/monokai");
    editor2.session.setMode("ace/mode/dockerfile");
    editor2.setOption("showPrintMargin", false)
    editor2.setValue("FROM razor-core:2.2.1", 1)

    editor1.getSession().on('change', function() {
        var val = editor1.getSession().getValue();

        let headers = {}
        let reqBody = {
            "yaml_file_content": val
        }
        httppost(
            '/generate-dockerfile',
            reqBody,
            headers,
            function (res) {
                let response = JSON.parse(res)
                editor2.setValue(response['result'], 1) // moves cursor to the end
            },
            function (jqXHR, tranStatus, errorThrown) {
                if (jqXHR.status >= 400 && jqXHR.hasOwnProperty("responseText")) {
                    alert(JSON.parse(jqXHR['responseText'])["detail"])
                } else {
                    console.log(jqXHR)
                    alert("Error: " + errorThrown)
                }
            }
        );
    });
});
$(".panel-left").resizable({
    handleSelector: ".splitter",
    resizeHeight: false
});

$(".panel-top").resizable({
    handleSelector: ".splitter-horizontal",
    resizeWidth: false
});

let baseUrl = location.protocol + "//" + $(location).attr('host')
function httppost(url, data, headers, successCallback, errorCallback) {
    $.ajax({
        url: baseUrl + url,
        headers: headers,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: 'text',
        success: successCallback,
        error: errorCallback
    });
}