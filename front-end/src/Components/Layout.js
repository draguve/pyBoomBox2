import React, { Component } from 'react';

import Navbar from './Navigation/Navbar';
import SideDrawer from './Navigation/Sidedrawer';
import Backdrop from './Navigation/Backdrop';

class Layout extends Component {
    state = {
        showSideDrawer: false
    }

    sideDrawerToggler = () => {
        this.setState( ( prevState ) => {
            return {showSideDrawer: !prevState.showSideDrawer};
        });
    }

    render() {
    return (
        <React.Fragment>
            <Backdrop 
                show={this.state.showSideDrawer}
                clicked={this.sideDrawerToggler}
            />
            <Navbar 
                clicked={this.sideDrawerToggler}
            />
            <SideDrawer 
                show={this.state.showSideDrawer}
            />
        </React.Fragment>
    )
  }
}

export default Layout;