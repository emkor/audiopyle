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
        selected_plugin_config: {},
        selected_plugin_metrics: [],
        selected_request: null,
        selected_request_status: null,
        selected_request_details: null,
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
        fetchAudioDetails: event => fetchAudioDetails(event.currentTarget.name),
        fetchPluginDetails: event => fetchPluginDetails(event.currentTarget.name),
        fetchRequestDetails: event => fetchRequestDetails(event.currentTarget.name),
        sendRequest: event => sendExtractionRequest(API_HOST + '/request', {
            "audio_file_name": app.selected_file,
            "plugin_full_key": app.selected_plugin,
            "plugin_config": null,
            "metric_config": null
        }, function (event) { resetSelection(); }),
        resetSelection: event => resetSelection(),
        initData: function() {
            featchApiStatus();
            fetchAudioFiles();
            fetchPluginList();
            fetchRequestList();
        }
    }
});

app.initData();