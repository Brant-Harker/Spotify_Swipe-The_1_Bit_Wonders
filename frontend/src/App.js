import React from 'react';
import logo from './logo.svg';
import './App.css';



function App() {
  return (
    <div className="">
      <header className="d-flex align-items-center flex-column">
        <div className='d-flex flex-row justify-content-center'>
          <img src={logo} className="App-logo" alt="logo" />
          <h3>
            1 Bit Wonders
          </h3>
        </div>
        <div className='border w-75'>
          <div className='d-flex justify-content-center '>
            <h3>Discovery Weekly</h3>
          </div>
          <div className='d-flex justify-content-center'>
          <img src="placeholder.jpg" className='w-75' />

          </div>
          
        </div>

        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
