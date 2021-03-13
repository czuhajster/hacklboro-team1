// Function to send form data to the server via JavaScript
function sendForm(data, method) {
    const XHR = new XMLHttpRequest();

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
    XHR.open(method, '/goals/data');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send(urlEncodedData);
}

// Function to update the percentage of a user's goal by sending a PUT request to the server
function changePercentage(id, percentage) {
    const data = {
        id: id,
        percentage: percentage
    };
    sendForm(data, "PUT");
}

// Suggest goal based on the dropdown given
function goalSuggestion(i) {
    let goalText = "";
    switch (i) {
        case 0:
            goalText = "Reduce meat consumption (at most 3 meat-based meals this week)";
            break;
        case 1:
            goalText = "Reduce car emissions (drive at most 5 times this week)";
            break;
        case 2:
            goalText = "Use environmentally friendly transport (use bicycle at least 5 times this week)";
            break;
    }

    const data = {
        name: goalText
    };

    sendForm(data, "POST");
}