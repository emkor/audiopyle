var makeRequestApp = new Vue({
    el: '#makeRequest',
    data: {
        audio_files: [],
        vamp_plugins: [],
        selected_file: null,
        selected_file_details: null,
        selected_file_tags: null,
        selected_plugin: null,
        selected_plugin_details: null,
        selected_plugin_config: {},
        selected_plugin_metrics: []
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
        resetSelection: function (event) {
            makeRequestApp.selected_file = null;
            makeRequestApp.selected_file_details = null;
            makeRequestApp.selected_plugin = null;
            makeRequestApp.selected_plugin_details = null;
            makeRequestApp.selected_plugin_metrics = [];
        },
        sendRequest: event => sendExtractionRequest(API_HOST + '/request', {
            "audio_file_name": makeRequestApp.selected_file,
            "plugin_full_key": makeRequestApp.selected_plugin,
            "plugin_config": makeRequestApp.selected_plugin_config,
            "metric_config": null
        }, e => makeRequestApp.resetSelection()),
        initData: function () {
            fetchAudioFiles();
            fetchPluginList();
        }
    }
});

var viewResultsApp = new Vue({
    el: '#browseResults',
    data: {
        requests: [],
        selected_request: null,
        selected_request_status: null,
        selected_request_details: null,
        selected_request_metrics: [],
        selected_request_selected_metric_name: null,
        selected_request_selected_metric_value: null
    },
    methods: {
        fetchRequestDetails: event => fetchRequest(event.currentTarget.name),
        fetchRequestMetricDetails: event => fetchRequestMetricValues(event.currentTarget.name),
        fetchRequests: event => fetchRequestList(),
        initData: function () {
            this.fetchRequests();
        }
    }
});

makeRequestApp.initData();
viewResultsApp.initData();