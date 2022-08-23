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
  setCompletedCrop:Dispatch<SetStateAction< PixelCrop | undefined>>,
  imageResult?: ImageResult,
  setImageResult: Dispatch<SetStateAction< ImageResult | undefined>>,
}

const SnapShotImg = ({
  height,
  handleMouseClick,
  cropMode,
  setCompletedCrop,
  imageResult,
  setImageResult,
}: SnapShotImgProp) => {
  const imgRef = useRef<HTMLImageElement>(null);
  const [crop, setCrop] = useState<Crop>({
    x: 10, y: 10, width: 80, height: 80, unit: '%',
  });
  const [scaleWidth, setScaleWidth] = useState<number>();
  const [scaleHeight, setScaleHeight] = useState<number>();

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

  const onImageLoad = (e: React.SyntheticEvent<HTMLImageElement>) => {
    setScaleWidth(imageResult.width / e.currentTarget.width);
    setScaleHeight(imageResult.height / e.currentTarget.height);
  };

  if (cropMode) {
    return (
      <ReactCrop
        crop={crop}
        keepSelection
        onChange={(c) => setCrop(c)}
        onComplete={(c) => {
          if (!(scaleWidth && scaleHeight)) {
            return;
          }

          setCompletedCrop({
            x: Math.round(c.x * scaleWidth),
            y: Math.round(c.y * scaleHeight),
            width: Math.round(c.width * scaleWidth),
            height: Math.round(c.height * scaleHeight),
            unit: c.unit,
          });
        }}
      >
        <img
          ref={imgRef}
          height={height}
          src={`data:image/webp;base64,${imageResult.base64}`}
          alt="captured_image"
          onLoad={onImageLoad}
        />
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

  const onSave = async () => {
    if (!imageResult || !completedCrop) {
      return;
    }

    const config = new Configuration({
      basePath: '',
    });
    const api = new DefaultApi(config);
    const ret = await api.androidSaveCropImageApiAndroidImageCropSavePut({
      uuid: imageResult.uuid,
      name: 'hogehoge',
      x: completedCrop.x,
      y: completedCrop.y,
      width: completedCrop.width,
      height: completedCrop.height,
    });
    console.log(ret);
  };

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
            <Box p={2}>
              <ToggleButton
                value="check"
                selected={cropMode}
                onChange={() => setCropMode(!cropMode)}
              >
                CROP MODE
              </ToggleButton>
            </Box>

            <Box p={2}>
              <Button variant="contained" onClick={onSave}>
                save
              </Button>
            </Box>
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
