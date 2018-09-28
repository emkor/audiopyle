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