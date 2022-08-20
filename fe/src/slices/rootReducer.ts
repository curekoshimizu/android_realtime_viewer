import { combineReducers } from '@reduxjs/toolkit';

import counter from './counterSlices';

const rootReducer = combineReducers({
  counter,
});

export default rootReducer;
