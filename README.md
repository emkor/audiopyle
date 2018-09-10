## audiopyle [![Build Status](https://travis-ci.com/emkor/audiopyle.svg?token=VJAwHN6qVcMdKUug57c9&branch=master)](https://travis-ci.com/emkor/audiopyle)
![audiopyle](http://i.imgur.com/NDGeQg5.png)

Docker-based app extracting features from audio files (preferably, music). Makes use of standard [VAMP plugins](https://www.vamp-plugins.org/) for feature extraction.

### Quick start
To start the app, follow these steps:
- make sure directories with music files (`.mp3`, `.flac` formats) and VAMP plugins (`.so` files in case of Linux) are mapped correctly in `scripts/docker-compose.yml` under sections:
    - `api/volumes`
    - `worker/volumes`
- do `make run` from the directory with `Makefile`
- docker should pull the audiopyle images now
- do `GET` on `http://localhost:8080/` to check the audiopyle status
- there's no UI available (*yet*), you can use REST API

### App REST API description
File `open_api_docs.yml` contains audiopyle API documentation compliant with OpenAPI / Swagger 2.0 spec (you may just paste file contents into [Swagger editor](https://editor.swagger.io/)
More convenient way is yet to come

### How it works (mental model)
- Extraction takes as input:
    - filename of an audio file (those are listed in `/audio` endpoint)
    - VAMP plugin full key - including plugin output (those are listen under `/plugin` endpoint)
    - optional: VAMP plugin config (if empty, defaults from `/config/plugin` for this plugin will be used)
    - optional: Metric config (if empty, defaults from `/config/metric` for this plugin will be used)
- Extraction outputs:
    - id3tag of an audio file, if included in the file
    - raw feature data; might be 1-, 2- or 3-dimensional; in constant or variable step format; see see [VAMP docs](https://www.vamp-plugins.org/vamp-programmer-presentation.pdf) for details
    - Metric values, if included in the request
- What is Metric?
    - **Metric value** is a bunch of statistics (mean, min, max, sum, variance etc.) over a vector of data selected from raw feature
    - **Metric definition** is a description of how to calculate vector mentioned above from raw feature data 
    - Default metric definitions are defined in `audiopyle/scripts/resources/config/metric.json`
    - Example: `bbc_intensity_lo_bass`
        - it's a Metric telling about sub-bass intensity of the track
        - Metric value is calculated from raw feature data produced by `bbc-vamp-plugins:bbc-intensity:intensity-ratio` VAMP plugin output 
        - the input vector is a first row of a 3-dimensional raw feature produced by the VAMP plugin output
        - standards statistics functions are applied over the vector, producing **Metric value**
- Automated extraction
    - `/request/automation` endpoint is triggered by empty POST request (see OpenAPI documentation for details)
    - the API creates Cartesian product of all available audio files and all available VAMP plugins excluding those blacklisted (`/config/blacklist` endpoint, `audiopyle/scripts/resources/config/blacklist.json` file))
    - plugin config and metric config are taken from their respective `/config` endpoints
    - all the requests are queued for execution, API responds with UUIDs (task_id) for each generated request
 
### Building from source
To build Docker images, follow these steps:
- do one-time setup: `make config`
- then, to trigger full-build and test procedure, do `make all`
- take a look at Makefile to see what build steps are doing