import {
  Grid, Box, Button, Typography,
} from '@mui/material';
import {
  MouseEvent, useState,
  Dispatch,
  SetStateAction,
} from 'react';
import useEffectAsync from 'use-async-effect';

import { DefaultApi, Configuration } from '../client';

interface Record {
  x: number;
  y: number;
  unixTime: number;
  funcName: string;
}

interface ScriptListProp {
  records: Record[]
  setRecords: Dispatch<SetStateAction<Record[]>>
}

const ScriptList = ({ records, setRecords }: ScriptListProp) => {
  const [scriptNames, setScriptNames] = useState<string[]>([]);

  const click = async (script:string) => {
    const config = new Configuration({
      basePath: '',
    });
    const api = new DefaultApi(config);
    await api.androidRunScriptApiAndroidScriptsScriptPost({ script });
    const unixTime = (new Date()).getTime();
    setRecords([...records, {
      x: -1, y: -1, unixTime, funcName: script,
    }]);
  };

  useEffectAsync(async () => {
    const config = new Configuration({
      basePath: '',
    });
    const api = new DefaultApi(config);
    const ret = await api.androidScriptsApiAndroidScriptsGet();
    setScriptNames(ret);
  }, []);

  return (
    <>
      {
                scriptNames.map((name) => (
                  <Box m={2}>
                    <Button key={name} variant="contained" onClick={() => click(name)}>{name}</Button>
                  </Box>
                ))
            }
    </>
  );
};

const Script = ({ src }: { src: string }) => {
  const [records, setRecords] = useState<Record[]>([]);
  const [startTime, setStartTime] = useState<number | null>(null);
  const originalHeight = 2340;
  const height = 1000;
  const scale = originalHeight / height;

  const onClick = async (event : MouseEvent) => {
    const target = (event.target as HTMLButtonElement);

    const x = Math.round((event.clientX - target.offsetLeft) * scale);
    const y = Math.round((event.clientY - target.offsetTop) * scale);

    const config = new Configuration({
      basePath: '',
    });
    const api = new DefaultApi(config);
    await api.androidClickApiAndroidClickPost({ x, y });
    const unixTime = (new Date()).getTime();
    setRecords([...records, {
      x, y, unixTime, funcName: 'click',
    }]);
    if (!startTime) {
      setStartTime(unixTime);
    }
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
            onClick={onClick}
            alt="video_image"
            src={src}
          />
        </Box>
      </Grid>
      <Grid item xs={4}>
        <Box m={2}>
          <Button variant="contained" onClick={() => setRecords([])}>clear history</Button>
        </Box>
        <ScriptList records={records} setRecords={setRecords} />
        <Box>
          {
              records.map((record, i, arr) => {
                let delta = 0;
                if (i > 0) {
                  delta = arr[i].unixTime - arr[i - 1].unixTime;
                  delta = Math.round(delta / 100) * 100;
                }
                let note = `${record.funcName}()`;
                if (record.funcName === 'click') {
                  note = `click(${record.x}, ${record.y})`;
                }

                return (
                  <>
                    {delta > 0 && (
                      <Typography variant="h6">
                        {`sleep(${delta})`}
                      </Typography>

                    )}

                    <Typography variant="h6">
                      {note}
                    </Typography>
                  </>
                );
              })
}
        </Box>
      </Grid>
    </Grid>
  );
};

const ScriptApp = () => (
  <Script src="/api/android/video" />
);

export default ScriptApp;
