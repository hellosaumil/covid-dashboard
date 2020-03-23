import React from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import * as Actions from "../actions/action";

export default class RegionSelect extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            options: [],
        }
        this.onRegionSelect = this.onRegionSelect.bind(this);
    }

    componentWillMount() {
        const promise = fetch('http://192.168.0.14:5000/countries');
        promise.then(response => response.json()).then(response => {
            this.setState({
                options: response['countries']
            })
        }).catch(err => {
            alert('no data found');
        });
    }

    onRegionSelect(event, value) {
        if (value)
            Actions.addRegion(value);
    }

    render() {
        return (
            <Autocomplete
            id="combo-box-demo"
            options={this.state.options}
            onChange={this.onRegionSelect}
            getOptionLabel={option => option.name}
            style={{ width: 300 }}
            renderInput={params => <TextField {...params} label="Select Region" variant="outlined" />}
            />
        )
    }
}