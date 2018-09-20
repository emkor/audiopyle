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

var app = new Vue({
    el: '#app',
    data: {
        api_status: 'not ok',
        audio_files: [],
        vamp_plugins: [],
        requests: [],
        selected_file: null,
        selected_file_details: null,
        selected_plugin: null,
        selected_plugin_details: null,
        selected_request: null,
        selected_request_status: null,
        selected_request_details: null
    },
    computed: {
        requestNotPossible() {
            return this.selected_file == null || this.selected_plugin == null;
        },
        nothingSelected() {
            return this.selected_file == null && this.selected_plugin == null;
        }
    },
    methods: {
        fetchAudioDetails: function (event) {
            app.selected_file = event.currentTarget.name;
            app.selected_file_details = null;
            fetchJson(API_HOST + '/audio/' + app.selected_file,
                v => app.selected_file_details = v,
                e => app.selected_file_details = null);
        },
        fetchPluginDetails: function (event) {
            app.selected_plugin = event.currentTarget.name;
            app.selected_plugin_details = null;
            fetchJson(API_HOST + '/plugin/' + app.selected_plugin.replace(/:/g, "/"),
                v => app.selected_plugin_details = v,
                e => app.selected_plugin_details = null);
        },
        fetchRequestDetails: function (event) {
            app.selected_request = event.currentTarget.name;
            app.selected_request_details = null;
            fetchJson(API_HOST + '/request/' + app.selected_request + '/status',
                function (value) {
                    app.selected_request_status = value.status;
                    if (app.selected_request_status === 'done') {
                        fetchJson(API_HOST + '/request/' + app.selected_request,
                            v => app.selected_request_details = v,
                            e => app.selected_request_details = null);
                    } else {
                        console.info("Omitting fetching request details, because status is " + app.selected_request_status);
                    }
                },
                function (e) {
                    app.selected_request = null;
                    app.selected_request_details = null;
                });
        },
        sendRequest: function (event) {
            let sendRequestUrl = API_HOST + '/request';
            let payload = {
                "audio_file_name": app.selected_file,
                "plugin_full_key": app.selected_plugin,
                "plugin_config": null,
                "metric_config": null
            };
            let request = {
                method: "POST",
                headers: {"Content-Type": "application/json; charset=utf-8"},
                redirect: "follow",
                body: JSON.stringify(payload)
            };
            fetch(sendRequestUrl, request)
                .then(function (response) {
                    response.json()
                        .then(value => app.requests.push(value.task_id))
                        .catch(reason => console.error("Could not parse response from " + sendRequestUrl + ": " + reason));
                })
                .catch(error => console.error("Could not fetch details for " + app.selected_request + ": " + error));
        },
        resetSelection: function(event) {
            app.selected_file = null;
            app.selected_file_details = null;
            app.selected_plugin = null;
            app.selected_plugin_details = null;
        }
    }
});

function fetchInputFromApi(apiHost) {
    fetchJson(apiHost + '/',
        v => app.api_status = v.status,
        e => app.api_status = "not ok! " + e);

    fetchJson(apiHost + '/audio',
        v => app.audio_files = v,
        r => app.audio_files = []);

    fetchJson(apiHost + '/plugin',
        v => app.vamp_plugins = v,
        e => app.vamp_plugins = []);

    fetchJson(apiHost + '/request',
        v => app.requests = v,
        e => app.requests = []);
}

fetchInputFromApi(API_HOST);