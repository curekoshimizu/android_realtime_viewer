import { createSlice, PayloadAction } from '@reduxjs/toolkit';

const initialState : number = 0;

const slice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    addCounter: (status: number, action: PayloadAction<number>): number => status + action.payload,
  },
});

export const { actions } = slice;
export default slice.reducer;
