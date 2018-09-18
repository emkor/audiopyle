API_HOST = 'http://localhost:8080';

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
        selected_request_details: null,
        requestPossible: false
    },
    methods: {
        fetchAudioDetails: function (event) {
            app.selected_file = event.currentTarget.name;
            app.requestPossible = app.selected_file != null && app.selected_plugin != null;
            let audioUrl = API_HOST + '/audio/' + app.selected_file;
            fetch(audioUrl)
                .then(function (response) {
                    response.json()
                        .then(value => app.selected_file_details = value)
                        .catch(reason => console.error("Could not parse response from " + audioUrl + ": " + reason));
                })
                .catch(error => console.error("Could not fetch details for " + app.selected_file + ": " + error));
        },
        fetchPluginDetails: function (event) {
            app.selected_plugin = event.currentTarget.name;
            app.requestPossible = app.selected_file != null && app.selected_plugin != null;
            let pluginUrl = API_HOST + '/plugin/' + app.selected_plugin.replace(/:/g, "/");
            fetch(pluginUrl)
                .then(function (response) {
                    response.json()
                        .then(value => app.selected_plugin_details = value)
                        .catch(reason => console.error("Could not parse response from " + pluginUrl + ": " + reason));
                })
                .catch(error => console.error("Could not fetch details for " + app.selected_plugin + ": " + error));
        },
        fetchRequestDetails: function (event) {
            app.selected_request = event.currentTarget.name;
            let requestStatusUrl = API_HOST + '/request/' + app.selected_request + '/status';
            fetch(requestStatusUrl)
                .then(function (response) {
                    response.json()
                        .then(function (value) {
                            app.selected_request_status = value.status;
                            if (app.selected_request_status === 'done') {
                                let requestDetailsUrl = API_HOST + '/request/' + app.selected_request;
                                fetch(requestDetailsUrl)
                                    .then(function (response) {
                                        response.json()
                                            .then(value => app.selected_request_details = value)
                                            .catch(reason => console.error("Could not parse response from " + requestDetailsUrl + ": " + reason));
                                    })
                                    .catch(error => console.error("Could not fetch details for " + app.selected_request + ": " + error));
                            } else {
                                console.info("Omitting fetching request details, because status is " + app.selected_request_status);
                            }

                        })
                        .catch(reason => console.error("Could not parse response from " + requestStatusUrl + ": " + reason));
                })
                .catch(error => console.error("Could not fetch status for " + app.selected_request + ": " + error));
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
        }
    }
});

function fetchInputFromApi(apiHost) {
    fetch(apiHost + '/')
        .then(function (response) {
            response.json()
                .then(value => app.api_status = value.status)
                .catch(reason => console.error("Could not parse API status: " + reason));
        })
        .catch(error => console.error("Could not fetch status: " + error));

    fetch(apiHost + '/audio')
        .then(function (response) {
            response.json()
                .then(value => app.audio_files = value)
                .catch(reason => console.error("Could not parse audio list: " + reason));
        })
        .catch(error => console.error("Could not fetch from /audio: " + error));

    fetch(apiHost + '/plugin')
        .then(function (response) {
            response.json()
                .then(value => app.vamp_plugins = value)
                .catch(reason => console.error("Could not parse plugin list: " + reason));
        })
        .catch(error => console.error("Could not fetch from /plugin: " + error));

    fetch(apiHost + '/request')
        .then(function (response) {
            response.json()
                .then(value => app.requests = value)
                .catch(reason => console.error("Could not parse request list: " + reason));
        })
        .catch(error => console.error("Could not fetch from /request: " + error));
}

fetchInputFromApi(API_HOST);