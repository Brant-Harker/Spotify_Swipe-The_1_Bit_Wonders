import React from 'react';
import Music from "./Music";


export default function Album({ src }) {

  return (
<>
<div className='d-flex justify-content-center '>
          <h3 className="text-success mt-3 mb-4">Album Title</h3>
        </div>
        <div className='d-flex align-items-center flex-column'>
          <img src="placeholder.jpg" className='w-100' alt="placeholder" />
          <Music />
          
        </div>
</>


  );
}