import Music from "./Music";

export default function Album({ src }) {
  return (
    <>
      <div className='d-flex justify-content-center '>
        <h3>Discovery Weekly</h3>
      </div>
      <div className='d-flex align-items-center flex-column'>
        <img src="placeholder.jpg" className='w-75' />
        <Music />
      </div>

    </>

  );
}