import React from 'react';
import ChipsArray from './chips';
import Store from '../stores/store';

export default class RegionChip extends React.Component {

    constructor() {
        super();
        this.state  = {
            selectedRegions: Store.getSelectedRegions()
        }
    }
    
    componentDidMount() {
        Store.on('region-added', this.addRegion.bind(this));
        Store.on('chip-deleted', this.removeChip.bind(this));
    }

    componentWillUnmount() {
        Store.removeListener('region-added', this.addRegion.bind(this));
        Store.removeListener('chip-deleted', this.removeChip.bind(this));
    }
    
    removeChip() {
        this.setState({
            selectedRegions: Store.getSelectedRegions()
        })
    }

    addRegion() {
        this.setState({
            selectedRegions: Store.getSelectedRegions()
        })
    }

    render() {
        return (
            <ChipsArray chips={this.state.selectedRegions} />
        )
    }
}
