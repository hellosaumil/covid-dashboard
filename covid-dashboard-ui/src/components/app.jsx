import React from 'react';
import ReactDOM from 'react-dom';
import Menus from '../views/menus';
import Records from '../views/records';

class App extends React.Component {
    render() {
        return(
            <div className="main">
                <Menus/>
                <Records />
            </div> 
        );
    }
}
ReactDOM.render(<App />, document.getElementById('container'));