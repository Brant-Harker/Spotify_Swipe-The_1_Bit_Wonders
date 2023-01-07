import React from 'react';
import logo from './logo.svg';
import './App.css';


// components
import Album from "./componets/Album";
import PlayButton from './componets/PlayButton';

  
function App() {
  const [value, setValue] = React.useState(30);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  return (
    <div className="">
      <header className="d-flex align-items-center flex-column">
        <div className='d-flex flex-row justify-content-center'>
          <img src={logo} className="App-logo" alt="logo" />
          <h3>
            1 Bit Wonders
          </h3>
        </div>
        <div className='border w-75 d-flex flex-column '>
          <Album />
        <PlayButton />

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
