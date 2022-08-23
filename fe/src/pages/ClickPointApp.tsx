import {
  Grid, Box, Button, Typography, ToggleButton,
} from '@mui/material';
import {
  MouseEvent, useState, useRef,
  SetStateAction, Dispatch,
} from 'react';
import ReactCrop, {
  Crop,
  PixelCrop,
} from 'react-image-crop';
import { useAsyncEffect } from 'use-async-effect';

import { DefaultApi, Configuration, ImageResult } from '../client';
import { BoldDiv, BoldSpan } from '../components/BoldBox';

interface SnapShotImgProp {
  handleMouseClick: (event: MouseEvent) => void;
  height: number;
  cropMode: boolean;
  completedCrop?: PixelCrop,
  setCompletedCrop:Dispatch<SetStateAction< PixelCrop | undefined>>,
  imageResult?: ImageResult,
  setImageResult: Dispatch<SetStateAction< ImageResult | undefined>>,
}

const SnapShotImg = ({
  height,
  handleMouseClick,
  cropMode,
  completedCrop,
  setCompletedCrop,
  imageResult,
  setImageResult,
}: SnapShotImgProp) => {
  const imgRef = useRef<HTMLImageElement>(null);
  const [crop, setCrop] = useState<Crop>(completedCrop || {
    x: 10, y: 10, width: 80, height: 80, unit: '%',
  });

  useAsyncEffect(async () => {
    const config = new Configuration({
      basePath: '',
    });
    const api = new DefaultApi(config);
    const ret = await api.androidImageApiAndroidImageGet();
    setImageResult(ret);
  }, []);

  if (!imageResult) {
    return (<div />);
  }

  if (cropMode) {
    return (
      <ReactCrop
        crop={crop}
        keepSelection
        onChange={(c) => setCrop(c)}
        onComplete={(c) => setCompletedCrop(c)}
      >
        <img
          ref={imgRef}
          height={height}
          src={`data:image/webp;base64,${imageResult.base64}`}
          alt="captured_image"
        />
        <div>{completedCrop?.x}</div>
      </ReactCrop>
    );
  }

  return (
    <img
      height={height}
      src={`data:image/webp;base64,${imageResult.base64}`}
      onClick={handleMouseClick}
      alt="captured_image"
    />
  );
};

interface VideoProp {
  handleMouseClick: (event: MouseEvent) => void;
  height: number;
  src: string;
}

const Video = ({ height, handleMouseClick, src } : VideoProp) => (

  <img
    height={height}
    onClick={handleMouseClick}
    alt="video_image"
    src={src}
  />
);

interface Point {
  x: number;
  y: number;
}

const ClickPoint = ({ src }: { src: string }) => {
  const [imageResult, setImageResult] = useState<ImageResult >();
  const [snapShotMode, setSnapShotMode] = useState<boolean>(false);
  const [cropMode, setCropMode] = useState<boolean>(false);
  const [completedCrop, setCompletedCrop] = useState<PixelCrop>();
  const [point, setPoint] = useState<Point | null>(null);
  const originalHeight = 2340;
  const height = 1000;
  const scale = originalHeight / height;

  const handleMouseClick = (event : MouseEvent) => {
    const target = (event.target as HTMLButtonElement);

    setPoint({
      x: event.clientX - target.offsetLeft,
      y: event.clientY - target.offsetTop,
    });
  };

  return (
    <Grid container>
      <Grid item xs={4}>
        <Box m="auto" display="flex">
          <Box m="auto" display="flex" pt={5}>
            <Button variant="contained" onClick={() => setSnapShotMode(!snapShotMode)}>
              {(snapShotMode) ? 'REALTIME VIDEO' : 'SNAPSHOT'}
            </Button>
          </Box>
          <Typography variant="h6" pt={5}>
            <BoldDiv>
              {(snapShotMode) ? 'SNAPSHOT MODE' : 'REALTIME VIDEO MODE'}
            </BoldDiv>
          </Typography>
        </Box>
        {snapShotMode && (
        <Box m="auto" display="flex">
          <Box m="auto" display="flex" pt={5}>
            <ToggleButton
              value="check"
              selected={cropMode}
              onChange={() => setCropMode(!cropMode)}
            >
              CROP MODE
            </ToggleButton>
          </Box>
        </Box>
        ) }
        <Box
          m="auto"
          display="flex"
        >
          {
          point && (
            <Typography variant="h6" pt={10}>
              <BoldSpan>click point : </BoldSpan>
              <BoldSpan>{`(${Math.round(point.x * scale)}, ${Math.round(point.y * scale)})`}</BoldSpan>
            </Typography>
          )
      }
        </Box>
      </Grid>
      <Grid item xs={8}>
        <Box
          display="flex"
          justifyContent="center"
        >
          { snapShotMode && (
          <SnapShotImg
            height={height}
            handleMouseClick={handleMouseClick}
            cropMode={cropMode}
            completedCrop={completedCrop}
            setCompletedCrop={setCompletedCrop}
            imageResult={imageResult}
            setImageResult={setImageResult}
          />
          )}
          { !snapShotMode && (
          <Video src={src} height={height} handleMouseClick={handleMouseClick} />
          )}
        </Box>
      </Grid>
    </Grid>
  );
};

const ClickPointApp = () => (
  <ClickPoint src="/api/android/video" />
);

export default ClickPointApp;
