import { CssBaseline, Container } from '@mui/material';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import StyledAppBar from '../components/StyledAppBar';
import ClickPointApp from '../pages/ClickPointApp';
import NotFound from '../pages/NotFound';
import SimulationApp from '../pages/SimulationApp';

const links = [
  { label: 'Android Click Helper', path: '/' },
  { label: 'Android Simulation', path: '/simulation' },
];

const App = () => (
  <BrowserRouter>
    <CssBaseline />
    <Container maxWidth="lg" fixed>
      <StyledAppBar links={links} />
      <Routes>
        <Route path="/" element={<ClickPointApp />} />
        <Route path="/simulation" element={<SimulationApp />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Container>
  </BrowserRouter>
);

export default App;
