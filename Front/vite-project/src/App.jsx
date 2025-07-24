import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './views/home';
import General from './views/general';

function App() {

  return (
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/general" element={<General />} />
        </Routes>  
      </Router>

  );
}

export default App;