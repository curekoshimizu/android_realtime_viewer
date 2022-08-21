import { Grid, Box, Typography } from '@mui/material';
import {
  MouseEvent, useState,
} from 'react';

interface Point {
  x: number;
  y: number;
}

const ClickPoint = ({ src }: { src: string }) => {
  const [point, setPoint] = useState<Point | null>(null);
  const originalHeight = 2340;
  const height = 1000;
  const scale = originalHeight / height;

  const handleMouseMove = (event : MouseEvent) => {
    const target = (event.target as HTMLButtonElement);

    setPoint({
      x: event.clientX - target.offsetLeft,
      y: event.clientY - target.offsetTop,
    });
  };

  return (
    <Grid container>
      <Grid item xs={8}>
        <Box
          display="flex"
          justifyContent="center"
        >

          <img
            height={height}
            onClick={handleMouseMove}
            alt="video_image"
            src={src}
          />
        </Box>
      </Grid>
      <Grid item xs={4}>
        <Box
          m="auto"
          display="flex"
          justifyContent="center"
        >
          {
          point && (
            <Typography variant="h4">
                {`click point : (${Math.round(point.x * scale)}, ${Math.round(point.y * scale)})`}
            </Typography>
          )
      }
        </Box>
      </Grid>
    </Grid>
  );
};

const ClickPointApp = () => (
  <ClickPoint src="/api/android/video" />
);

export default ClickPointApp;
