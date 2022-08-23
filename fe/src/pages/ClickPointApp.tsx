import {
  Grid, Box, Button, Typography,
} from '@mui/material';
import {
  MouseEvent, useState,
} from 'react';
import { useAsyncEffect } from 'use-async-effect';

import { DefaultApi, Configuration, ImageResult } from '../client';
import { BoldDiv, BoldSpan } from '../components/BoldBox';

interface SnapShotImgProp {
  handleMouseClick: (event: MouseEvent) => void;
  height: number;
}

const SnapShotImg = ({ height, handleMouseClick }: SnapShotImgProp) => {
  const [imageResult, setImageResult] = useState<ImageResult>();

  useAsyncEffect(async () => {
    const config = new Configuration({
      basePath: '',
    });
    const api = new DefaultApi(config);
    const ret = await api.androidImageApiAndroidImageGet();
    setImageResult(ret);
  }, []);

  return (
    <div>
      { imageResult && (
        <img
          height={height}
          src={`data:image/webp;base64,${imageResult.base64}`}
          onClick={handleMouseClick}
          alt="captured_image"
        />
      ) }
    </div>
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
  const [snapShotMode, setSnapShotMode] = useState<boolean>(false);
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
            <SnapShotImg height={height} handleMouseClick={handleMouseClick} />
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
