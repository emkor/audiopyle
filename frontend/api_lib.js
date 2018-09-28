API_HOST = 'http://localhost:8080';

function fetchJson(url, responseJsonHandler, errorHandler) {
    // on success, calls responseJsonHandler() with response JSON, on failure - calls errorHandler() with error message
    fetch(url)
        .then(function (response) {
            if (response.ok) {
                response.json()
                    .then(value => responseJsonHandler(value))
                    .catch(function (reason) {
                        console.error("Could not parse response from " + url + ": " + reason);
                        errorHandler(reason);
                    });
            }
            else {
                console.error("Response from " + url + " was " + response.status + " (" + response.statusText + ")");
                errorHandler(response.statusText);
            }
        })
        .catch((function (reason) {
            console.error("Could not parse response from " + url + ": " + reason);
            errorHandler(reason);
        }));
}

function featchApiStatus() {
    makeRequestApp.api_status = "...";
    fetchJson(API_HOST + '/',
        v => makeRequestApp.api_status = v.status,
        e => makeRequestApp.api_status = "not ok! " + e);
}

function fetchAudioFiles() {
    makeRequestApp.audio_files = [];
    fetchJson(API_HOST + '/audio',
        v => makeRequestApp.audio_files = v,
        r => makeRequestApp.audio_files = []);
}

function fetchPluginList() {
    makeRequestApp.vamp_plugins = [];
    fetchJson(API_HOST + '/plugin',
        v => makeRequestApp.vamp_plugins = v,
        e => makeRequestApp.vamp_plugins = []);
}

function fetchRequestList() {
    viewResultsApp.requests = [];
    fetchJson(API_HOST + '/request',
        v => viewResultsApp.requests = v,
        e => viewResultsApp.requests = []);
}

function fetchAudioDetails(audioFileName) {
    makeRequestApp.selected_file = audioFileName;
    makeRequestApp.selected_file_details = null;
    makeRequestApp.selected_file_tags = null;
    fetchJson(API_HOST + '/audio/' + encodeURIComponent(makeRequestApp.selected_file),
        v => makeRequestApp.selected_file_details = v,
        e => makeRequestApp.selected_file_details = null);
    fetchJson(API_HOST + '/audio/' + encodeURIComponent(makeRequestApp.selected_file) + '/tag',
        v => makeRequestApp.selected_file_tags = v,
        e => makeRequestApp.selected_file_tags = null);
}

function fetchPluginDetails(pluginKey) {
    makeRequestApp.selected_plugin = pluginKey;
    makeRequestApp.selected_plugin_details = null;
    makeRequestApp.selected_plugin_metrics = [];
    makeRequestApp.selected_plugin_config = {};
    let encodedPluginUrl = encodeURIComponent(makeRequestApp.selected_plugin.replace(/:/g, "/"));
    fetchJson(API_HOST + '/plugin/' + encodedPluginUrl,
        function (v) {
            makeRequestApp.selected_plugin_details = v;
            fetchJson(API_HOST + '/config/plugin/' + encodedPluginUrl + "/metric",
                m => makeRequestApp.selected_plugin_metrics = m,
                e => makeRequestApp.selected_plugin_metrics = []);
            fetchJson(API_HOST + '/config/plugin/' + encodedPluginUrl,
                c => makeRequestApp.selected_plugin_config = c,
                e => makeRequestApp.selected_plugin_config = {})
        },
        e => makeRequestApp.selected_plugin_details = null);
}

function sendExtractionRequest(sendRequestUrl, payload, responseHandler) {
    let request = {
        method: "POST",
        headers: {"Content-Type": "application/json; charset=utf-8"},
        redirect: "follow",
        body: JSON.stringify(payload)
    };
    fetch(sendRequestUrl, request)
        .then(function (response) {
            response.json()
                .then(value => responseHandler(value))
                .catch(reason => console.error("Could not parse response from " + sendRequestUrl + ": " + reason));
        })
        .catch(error => console.error("Could not fetch request " + makeRequestApp.selected_request + ": " + error));
}

function fetchRequest(requestId) {
    viewResultsApp.selected_request = requestId;
    viewResultsApp.selected_request_details = null;
    viewResultsApp.selected_request_metrics = [];
    viewResultsApp.selected_request_selected_metric_name = null;
    viewResultsApp.selected_request_selected_metric_value = null;
    fetchJson(API_HOST + '/request/' + encodeURIComponent(viewResultsApp.selected_request) + '/status',
        function (value) {
            viewResultsApp.selected_request_status = value.status;
            if (viewResultsApp.selected_request_status === 'done') {
                fetchRequestDetails(viewResultsApp.selected_request);
                fetchRequestMetricNames(viewResultsApp.selected_request);
            }
            else {
                console.info("Omitting fetching request details, because status is " + viewResultsApp.selected_request_status);
            }
        },
        function (e) {
            viewResultsApp.selected_request = null;
            viewResultsApp.selected_request_details = null;
        });
}

function fetchRequestMetricValues(metric_name) {
    viewResultsApp.selected_request_selected_metric_name = metric_name;
    viewResultsApp.selected_request_selected_metric_value = null;
    let url = API_HOST
        + '/request/' + encodeURIComponent(viewResultsApp.selected_request)
        + '/metric/' + encodeURIComponent(viewResultsApp.selected_request_selected_metric_name);
    fetchJson(url,
        v => viewResultsApp.selected_request_selected_metric_value = v,
        e => viewResultsApp.selected_request_selected_metric_value = null)
}

function fetchRequestDetails(task_id) {
    fetchJson(API_HOST + '/request/' + task_id,
        v => viewResultsApp.selected_request_details = v,
        e => viewResultsApp.selected_request_details = null);
}

function fetchRequestMetricNames(task_id) {
    fetchJson(API_HOST + '/request/' + task_id + "/metric",
        v => viewResultsApp.selected_request_metrics = v,
        e => viewResultsApp.selected_request_metrics = []);
}
