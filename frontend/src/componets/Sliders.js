import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';


export default function Sliders() {
  const [value, setValue] = React.useState(30);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div className='d-flex justify-content-center'>
      <Box sx={{ width: 200 }}>

        <Slider defaultValue={0} aria-label="slider" />
      </Box>
    </div>

  );
}