import { Box, Typography, Button } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useState } from 'react';
import useAsyncEffect from 'use-async-effect';

import { DefaultApi, Configuration, Response } from '../client';
import { actions } from '../slices/counterSlices';
import { useAppSelector, useAppDispatch } from '../store';

const CustomButton = styled(Button)({
  backgroundColor: 'royalblue',
});

const ReduxExampleApp = () => {
  const counter = useAppSelector((state) => state.counter);
  const [localCount, setLocalCount] = useState(0);
  const [responseArray, setResponseArray] = useState<Response[]>([]);
  const dispatch = useAppDispatch();

  useAsyncEffect(async () => {
    const config = new Configuration({
      basePath: '',
    });
    const api = new DefaultApi(config);
    const resp: Response[] = await api.pingApiPingGet();
    setResponseArray(resp);
  }, []);

  return (
    <>
      <Typography variant="h4">buttons</Typography>
      <Box p={10}>
        <CustomButton
          variant="contained"
          onClick={() => setLocalCount(localCount + 1)}
        >
          Local Counter:
          {' '}
          {localCount}
        </CustomButton>
      </Box>
      <Box p={10}>
        <CustomButton
          variant="contained"
          onClick={() => dispatch(actions.addCounter(1))}
        >
          Global Counter:
          {' '}
          {counter}
        </CustomButton>
      </Box>
      <Typography variant="h4">server response</Typography>
      <Box p={10}>
        {responseArray.map((e) => (
          <Box key={e.resp}>
            ・
            {e.resp}
          </Box>
        ))}
      </Box>
    </>
  );
};

export default ReduxExampleApp;
