import Dispatcher from "../dispatcher/dispatcher";


function parseRecords(response) {
    // const records = [];
    const records = response.user_records.map(res => {
        return {id: res.id, country: res.country, total: res.confirmed, active: res.active, deaths: res.deaths, recovered: res.recovered};
        // records.push(record);
    });
    return records;
}

export function addRegion(region) {
    Dispatcher.dispatch({
        region: region,
        type: 'addRegion'
    })

    const promise = fetch('http://192.168.0.14:5000/record', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(region)
    });
    promise.then(response => response.json()).then(response => {
        Dispatcher.dispatch({
            records: parseRecords(response),
            type: 'showRecords'
        })
    }).catch(err => {
        alert('no data found');
    });
    
}

export function showRecords() {
    const promise = fetch('http://192.168.0.14:5000/user-records');
    promise.then(response => response.json()).then(response => {
        Dispatcher.dispatch({
            records: parseRecords(response),
            type: 'showRecords'
        })
    }).catch(err => {
        alert('no data found');
    });
}

export function deleteRegion(region) {
    const promise = fetch('http://192.168.0.14:5000/remove-record', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(region)
    });
    promise.then(response => response.json()).then(response => {
        Dispatcher.dispatch({
            records: parseRecords(response),
            type: 'showRecords'
        })
    }).catch(err => {
        alert('no data found');
    });
}

export function removeChip(chipToDelete) {
    Dispatcher.dispatch({
        chipToDelete: chipToDelete,
        type: 'removeChip'
    })
}