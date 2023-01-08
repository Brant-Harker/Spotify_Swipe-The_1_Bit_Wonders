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
      <header className="d-flex align-items-center flex-column ">
        <div className='d-flex flex-row justify-content-center '>
          <img src={logo} className="App-logo" alt="logo" />
          <h3>
            1 Bit Wonders
          </h3>
        </div>
        <div className='w-75'>
          <div className='border d-flex flex-column align-items-center rounded'>
            <div className='w-75 d-flex flex-column align-items-center'>
              <Album />
              <div className='w-100 mb-3 mt-2'>
                <PlayButton />

              </div>
            </div>
          </div>
        </div>


      </header>
    </div>
  );
}

export default App;
