import React, { Component } from 'react';
import './App.css';

import Layout from './Components/Layout';

class App extends Component {
  render() {
    return (
      <div className="App">
        {/* the layout component gives me navbar and menu icon */}
        <Layout />
      </div>
    );
  }
}

export default App;
