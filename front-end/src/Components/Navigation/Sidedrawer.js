import React from 'react';
import { NavLink } from 'react-router-dom';

const sidedrawer = ( props ) => {

    let activeClass = ['navbar-side'];
    if ( props.show ) {
        activeClass = ['navbar-side', 'navbar-side-reveal'];
    }
  
    return (
        <React.Fragment>
            <ul className={activeClass.join(' ')} >
                <li className="navbar-side-item">
                    <NavLink to="/" className="side-link"><i className="fas fa-home"></i> Home</NavLink>
                </li>
                <li className="navbar-side-item">
                    <NavLink to="/" className="side-link"><i className="fas fa-book-open"></i> Menu</NavLink>
                </li>
            </ul>
        </React.Fragment>
  );
}

export default sidedrawer;
