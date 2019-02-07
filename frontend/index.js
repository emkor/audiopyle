var app = new Vue({
    el: '#app',
    data: {
        api_status: 'not ok',
        audio_files: [],
        vamp_plugins: [],
        requests: [],
        selected_file: null,
        selected_file_details: null,
        selected_file_tags: null,
        selected_plugin: null,
        selected_plugin_details: null,
        selected_plugin_config: {},
        selected_plugin_metrics: [],
        selected_request: null,
        selected_request_status: null,
        selected_request_details: null,
        selected_request_metrics: [],
        selected_request_selected_metric_name: null,
        selected_request_selected_metric_value: null
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
        toMegabytes: function(bytes) {
            return (bytes/(1024*1024)).toFixed(2);
        },
        fromIsoToHumanDate: function(isoDateString) {
            let dateObj = new Date(isoDateString);
            return dateObj.toLocaleString();
        },
        roundStat: function(number) {
            return number.toFixed(3);
        },
        fetchAudioDetails: event => fetchAudioDetails(event.currentTarget.name),
        fetchPluginDetails: event => fetchPluginDetails(event.currentTarget.name),
        fetchRequestDetails: event => fetchRequest(event.currentTarget.name),
        fetchRequestMetricDetails: event => fetchRequestMetricValues(event.currentTarget.name),
        sendRequest: event => sendExtractionRequest(API_HOST + '/request', {
            "audio_file_name": app.selected_file,
            "plugin_full_key": app.selected_plugin,
            "plugin_config": app.selected_plugin_config,
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