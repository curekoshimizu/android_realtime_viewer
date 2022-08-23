import React, { useState, useRef } from 'react';
import ReactCrop, {
  centerCrop,
  makeAspectCrop,
  Crop,
  PixelCrop,
} from 'react-image-crop';

import 'react-image-crop/dist/ReactCrop.css';

// This is to demonstate how to make and center a % aspect crop
// which is a bit trickier so we use some helper functions.
function centerAspectCrop(
  mediaWidth: number,
  mediaHeight: number,
  aspect: number,
) {
  return centerCrop(
    makeAspectCrop(
      {
        unit: '%',
        width: 90,
      },
      aspect,
      mediaWidth,
      mediaHeight,
    ),
    mediaWidth,
    mediaHeight,
  );
}

const imgSrc = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png';

const App = () => {
  const imgRef = useRef<HTMLImageElement>(null);
  const [crop, setCrop] = useState<Crop>();
  const [completedCrop, setCompletedCrop] = useState<PixelCrop>();
  const aspect = 16.0 / 9.0;

  function onImageLoad(e: React.SyntheticEvent<HTMLImageElement>) {
    if (aspect) {
      const { width, height } = e.currentTarget;
      setCrop(centerAspectCrop(width, height, aspect));
    }
  }

  return (
    <div className="App">
      {
          completedCrop && (
          <>
            <div>{completedCrop.x}</div>
            <div>{completedCrop.y}</div>
            <div>{completedCrop.width}</div>
            <div>{completedCrop.height}</div>
          </>
          )
      }
      <ReactCrop
        crop={crop}
        onChange={(c) => setCrop(c)}
        onComplete={(c) => setCompletedCrop(c)}
      >
        <img
          width={300}
          ref={imgRef}
          alt="Crop me"
          src={imgSrc}
          onLoad={onImageLoad}
        />
      </ReactCrop>
    </div>
  );
};

export default App;
