import React, { useState, useMemo } from 'react'
import { ImageBackground, Text, View, Button } from 'react-native';
import logo from './logo.svg';
import TinderCard from 'react-tinder-card'
import './App.css';


// components
import Album from "./componets/Album";
import PlayButton from './componets/PlayButton';


const db = [
  {
    name: 'Richard Hendricks'
  },
  {
    name: 'Erlich Bachman'
  },
  {
    name: 'Monica Hall'
  },
  {
    name: 'Jared Dunn'
  },
  {
    name: 'Dinesh Chugtai'
  }
]

const alreadyRemoved = []
let charactersState = db

const App = () => {
  const [characters, setCharacters] = useState(db)
  const [lastDirection, setLastDirection] = useState()

  const childRefs = useMemo(() => Array(db.length).fill(1).map(i => React.createRef()), [])

  const swiped = (direction, nameToDelete) => {
    console.log('removing: ' + nameToDelete + ' to the ' + direction)
    setLastDirection(direction)
    alreadyRemoved.push(nameToDelete)
  }

  const outOfFrame = (name) => {
    console.log(name)
    charactersState = charactersState.filter(character => character.name !== name)
    setCharacters(charactersState)
  }

  const swipe = (dir) => {
    const cardsLeft = characters.filter(person => !alreadyRemoved.includes(person.name))
    if (cardsLeft.length) {
      const toBeRemoved = cardsLeft[cardsLeft.length - 1].name // Find the card object to be removed
      const index = db.map(person => person.name).indexOf(toBeRemoved) // Find the index of which to make the reference to
      alreadyRemoved.push(toBeRemoved) // Make sure the next card gets removed next time if this card do not have time to exit the screen
      childRefs[index].current.swipe(dir) // Swipe the card!
    }
  }



  const [value, setValue] = React.useState(30);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  return (
    <div className="">
      <header className="d-flex align-items-center flex-column ">
        <div className='d-flex flex-row justify-content-center mb-3 mt-3'>
          <img src={logo} className="App-logo" alt="logo" />
          <h3>
            1 Bit Wonders
          </h3>
        </div>
        <div className='w-75'>
          <div className='border d-flex flex-column align-items-center rounded'>
            <div className='w-75 d-flex flex-column align-items-center '>
            {characters.map((character, index) =>
            <TinderCard ref={childRefs[index]} key={character.name} onSwipe={(dir) => swiped(dir, character.name)} onCardLeftScreen={() => outOfFrame(character.name)}> 
            <div className='position-absolute'>
            <Album />

<div className='w-100 mb-3 mt-2'>
  <PlayButton />

</div>
            </div>
             
              </TinderCard>
              )}
            </div>
          </div>
        </div>


      </header>
    </div>
  );
}

export default App;
