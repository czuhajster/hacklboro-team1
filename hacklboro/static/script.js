function changePercentage(id, percentage) {
    const XHR = new XMLHttpRequest();

    const data = {
        id: id,
        percentage: percentage
    };

    let urlEncodedData = "",
        urlEncodedDataPairs = [],
        name;

    for (name in data) {
        urlEncodedDataPairs.push(encodeURIComponent(name) + '=' + encodeURIComponent(data[name]));
    }

    urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');
    XHR.addEventListener('load', function (event) {
        location.reload();
    });
    XHR.addEventListener('error', function (event) {
        alert('Oops! Something went wrong.');
    });
    XHR.open('PUT', '/goals/data');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send(urlEncodedData);
}