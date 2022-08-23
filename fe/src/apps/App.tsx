import { CssBaseline, Container } from '@mui/material';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import StyledAppBar from '../components/StyledAppBar';
import ClickPointApp from '../pages/ClickPointApp';
import ExampleCrop from '../pages/ExampleCrop';
import NotFound from '../pages/NotFound';
import ScriptApp from '../pages/ScriptApp';

const links = [
  { label: 'Android Click Helper', path: '/' },
  { label: 'Android Scripts', path: '/script' },
];

const App = () => (
  <BrowserRouter>
    <CssBaseline />
    <Container maxWidth="lg" fixed>
      <StyledAppBar links={links} />
      <Routes>
        <Route path="/" element={<ClickPointApp />} />
        <Route path="/script" element={<ScriptApp />} />
        <Route path="/example_crop" element={<ExampleCrop />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Container>
  </BrowserRouter>
);

export default App;
