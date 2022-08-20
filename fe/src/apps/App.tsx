import { CssBaseline, Container } from '@mui/material';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import StyledAppBar from '../components/StyledAppBar';
import BoxExample from '../pages/BoxExample';
import ReduxExampleApp from '../pages/ReduxExample';
import NotFound from "../pages/NotFound";

const links = [
  { label: 'box example', path: '/' },
  { label: 'redux example', path: '/redux_example' },
];

const App = () => (
  <BrowserRouter>
    <CssBaseline />
    <Container maxWidth="lg" fixed>
      <StyledAppBar links={links} />
      <Routes>
        <Route path="/" element={<BoxExample />} />
        <Route path="/redux_example" element={<ReduxExampleApp />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Container>
  </BrowserRouter>
);

export default App;
