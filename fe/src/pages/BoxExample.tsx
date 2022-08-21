import { Box, Typography } from '@mui/material';
import {
  MouseEvent, useState, useEffect,
} from 'react';

const width = 100;
const height = 200;

const App = () => {
  const [bgColor, setBgColor] = useState<string>('#888888');
  const [foColor, setFoColor] = useState<string>('#000000');

  const [png, setPng] = useState<string | null>(null);

  useEffect(() => {
    const canvasElem = document.createElement('canvas');
    canvasElem.width = width;
    canvasElem.height = height;

    const ctx = canvasElem && canvasElem.getContext('2d');
    if (!canvasElem || !ctx) return;

    // draw

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = '#33333333';
    ctx.fillRect(0, 0, width / 2, height / 2);

    // ctx.fillStyle = foColor;
    // ctx.fillText('Hello', width / 6, height / 2);

    setPng(canvasElem.toDataURL());
  }, [bgColor, foColor]);

  return (
    <div>
      <h3>画像生成</h3>
      <h4>背景色</h4>
      {['#f00', '#0f0', '#00f'].map((color) => (
        <button
          type="button"
          key={color}
          style={{ background: color }}
          onClick={() => setBgColor(color)}
        >
          {color}
        </button>
      ))}
      <h4>文字色</h4>
      {['#f00', '#0f0', '#00f'].map((color) => (
        <button
          type="button"
          key={color}
          style={{ color }}
          onClick={() => setFoColor(color)}
        >
          {color}
        </button>
      ))}
      <h4>生成</h4>
      {png && (
        <div className="comp" style={{ display: 'flex' }}>
          <img
            alt="video_image"
            src="/api/game/video"
          />
          <img alt="icon" src={png} />
          <img alt="round icon" src={png} />
        </div>
      )}
    </div>
  );
};

interface Point {
  x: number;
  y: number;
}

const MouseExample = () => {
  const [point, setPoint] = useState<Point | null>(null);

  const handleMouseMove = (event : MouseEvent) => {
    const target = (event.target as HTMLButtonElement);
    setPoint({
      x: event.clientX - target.offsetLeft,
      y: event.clientY - target.offsetTop,
    });
  };

  return (
    <>
      <Box
        display="flex"
        justifyContent="center"
      >
        <img
          onClick={handleMouseMove}
          alt="video_image"
          src="/api/game/video"
        />
      </Box>
      {
          point && (
          <div>
              {`(x, y) = (${point.x}, ${point.y})`}
          </div>
          )
      }
    </>
  );
};

const BoxExample = () => (
  <>
    <Typography variant="h4">Mouse Event</Typography>
    <MouseExample />
    <App />
    <img
      alt="video_image"
      src="/api/android/video"
    />
  </>
);

export default BoxExample;
