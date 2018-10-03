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
        fetchAudioDetails: event => fetchAudioDetails(makeRequestApp, event.currentTarget.name),
        fetchPluginDetails: event => fetchPluginDetails(makeRequestApp, event.currentTarget.name),
        resetSelection: function (event) {
            makeRequestApp.selected_file = null;
            makeRequestApp.selected_file_details = null;
            makeRequestApp.selected_plugin = null;
            makeRequestApp.selected_plugin_details = null;
            makeRequestApp.selected_plugin_metrics = [];
        },
        sendRequest: event => sendExtractionRequest(makeRequestApp, v => makeRequestApp.resetSelection()),
        initData: function () {
            fetchAudioFiles(makeRequestApp);
            fetchPluginList(makeRequestApp);
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
        fetchRequestDetails: event => fetchRequest(viewResultsApp, event.currentTarget.name),
        fetchRequestMetricDetails: event => fetchRequestMetricValues(viewResultsApp, event.currentTarget.name),
        fetchRequests: event => fetchRequestList(viewResultsApp),
        initData: function () {
            this.fetchRequests();
        }
    }
});

makeRequestApp.initData();
viewResultsApp.initData();