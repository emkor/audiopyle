function toMegabytes(bytes) {
    return (bytes / (1024 * 1024)).toFixed(2);
}

function fromIsoToHumanDate(isoDateString) {
    let dateObj = new Date(isoDateString);
    return dateObj.toLocaleString();
}

function roundStat(number) {
    return number.toFixed(3);
}


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