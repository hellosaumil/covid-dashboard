import Dispatcher from "../dispatcher/dispatcher";
import {EventEmitter} from "events";

class Store extends EventEmitter {

    constructor() {
        super();
        this.records = [];
        this.selectedRegions = [{id: 0, name: 'Global'}];
    }

    handleAction(action) {
        switch(action.type) {
            case 'addRegion':
                this.addNewRegion(action.region);
                this.emit('region-added');
                break;
            case 'showRecords':
                this.showRecords(action.records);
                this.emit('show-records');
                break;
            case 'removeChip':
                this.removeChip(action.chipToDelete);
                this.emit('chip-deleted');
                break;
        }
    }

    removeChip(chipToDelete) {
        this.selectedRegions = this.selectedRegions.filter(chip => chip.name !== chipToDelete.name);
    }

    showRecords(records) {
        this.records = records;
    }

    addNewRegion(region) {
        this.selectedRegions.push(region);
    }

    getSelectedRegions() {
        return this.selectedRegions
    }

    getRecords() {
        return this.records;
    }

}

const store = new Store();
Dispatcher.register(store.handleAction.bind(store));
export default store;