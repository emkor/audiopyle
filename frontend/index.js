API_HOST = 'http://localhost:8080';

var app = new Vue({
    el: '#app',
    data: {
        api_status: 'not ok',
        audio_files: [],
        vamp_plugins: [],
        selected_file: null,
        selected_file_details: null,
        selected_plugin: null,
        selected_plugin_details: null
    },
    methods: {
        fetchAudioDetails: function (event) {
            app.selected_file = event.currentTarget.name;
            fetch(API_HOST + '/audio/' + app.selected_file)
                .then(function (response) {
                    response.json()
                        .then(value => app.selected_file_details = value)
                        .catch(reason => console.error("Could not parse API response for details of file " + app.selected_file + ": " + reason));
                })
                .catch(error => console.error("Could not fetch details for " + app.selected_file + ": " + error));
        },
        fetchPluginDetails: function (event) {
            app.selected_plugin = event.currentTarget.name;
            fetch(API_HOST + '/plugin/' + app.selected_plugin.replace(":", "/"))
                .then(function (response) {
                    response.json()
                        .then(value => app.selected_plugin_details = value)
                        .catch(reason => console.error("Could not parse API response for details of plugin " + app.selected_plugin + ": " + reason));
                })
                .catch(error => console.error("Could not fetch details for " + app.selected_plugin + ": " + error));
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
}

fetchInputFromApi(API_HOST);