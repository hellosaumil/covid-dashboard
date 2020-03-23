import React from 'react';
import RecordsTable from './recordTable';
import Store from '../stores/store';
import * as Actions from "../actions/action";

export default class Records extends React.Component {

    constructor(props) {
        super(props);
        this.state  = {
            records: Store.getRecords()
        }
    }

    UNSAFE_componentWillMount() {
        Actions.showRecords();
        this.showRecords();
    }

    componentDidMount() {
        Store.on('show-records', this.showRecords.bind(this));
    }

    componentWillUnmount() {
        Store.removeListener('show-records', this.showRecords.bind(this));
    }

    showRecords() {
        this.setState({
            records: Store.getRecords()
        })
    }

    render() {
        return (
            <RecordsTable rows={this.state.records}/>
        )
    }
}
