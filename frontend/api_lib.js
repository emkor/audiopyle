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
    app.api_status = "...";
    fetchJson(API_HOST + '/',
        v => app.api_status = v.status,
        e => app.api_status = "not ok! " + e);
}

function fetchAudioFiles() {
    app.audio_files = [];
    fetchJson(API_HOST + '/audio',
        v => app.audio_files = v,
        r => app.audio_files = []);
}

function fetchPluginList() {
    app.vamp_plugins = [];
    fetchJson(API_HOST + '/plugin',
        v => app.vamp_plugins = v,
        e => app.vamp_plugins = []);
}

function fetchRequestList() {
    app.requests = [];
    fetchJson(API_HOST + '/request',
        v => app.requests = v,
        e => app.requests = []);
}

function fetchAudioDetails(audioFileName) {
    app.selected_file = audioFileName;
    app.selected_file_details = null;
    app.selected_file_tags = null;
    fetchJson(API_HOST + '/audio/' + encodeURIComponent(app.selected_file),
        v => app.selected_file_details = v,
        e => app.selected_file_details = null);
    fetchJson(API_HOST + '/audio/' + encodeURIComponent(app.selected_file) + '/tag',
        v => app.selected_file_tags = v,
        e => app.selected_file_tags = null);
}

function fetchPluginDetails(pluginKey) {
    app.selected_plugin = pluginKey;
    app.selected_plugin_details = null;
    let encodedPluginUrl = encodeURIComponent(app.selected_plugin.replace(/:/g, "/"));
    fetchJson(API_HOST + '/plugin/' + encodedPluginUrl,
        function (v) {
            app.selected_plugin_details = v;
            fetchJson(API_HOST + '/config/plugin/' + encodedPluginUrl + "/metric",
                m => app.selected_plugin_metrics = m,
                e => app.selected_plugin_metrics = []);
            fetchJson(API_HOST + '/config/plugin/' + encodedPluginUrl,
                c => app.selected_plugin_config = c,
                e => app.selected_plugin_config = {})
        },
        e => app.selected_plugin_details = null);
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
        .catch(error => console.error("Could not fetch details for " + app.selected_request + ": " + error));
}

function fetchRequestDetailsIfFinished(url) {
    if (app.selected_request_status === 'done') {
        fetchJson(url,
            v => app.selected_request_details = v,
            e => app.selected_request_details = null);
    } else {
        console.info("Omitting fetching request details, because status is " + app.selected_request_status);
    }
}

function fetchRequestDetails(requestId) {
    app.selected_request = requestId;
    app.selected_request_details = null;
    fetchJson(API_HOST + '/request/' + encodeURIComponent(app.selected_request) + '/status',
        function (value) {
            app.selected_request_status = value.status;
            fetchRequestDetailsIfFinished(API_HOST + '/request/' + app.selected_request);
        },
        function (e) {
            app.selected_request = null;
            app.selected_request_details = null;
        });
}

function resetSelection(event) {
    app.selected_file = null;
    app.selected_file_details = null;
    app.selected_plugin = null;
    app.selected_plugin_details = null;
}