import React from 'react';
import { Link } from 'react-router-dom';

const navbar = ( props ) => {
  return (
    <React.Fragment>
        <nav className="navbar navbar-dark bg-dark">
            <Link className="navbar-brand" to="/">BoomBox</Link>
            <button className="navbar-toggler" onClick={props.clicked} type="button">
                <span className="navbar-toggler-icon"></span>
            </button>
        </nav>
    </React.Fragment>
  )
}

export default navbar;