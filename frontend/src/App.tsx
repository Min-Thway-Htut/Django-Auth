import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import LoginForm from './pages/LoginForm';
import RegisterForm from './pages/RegisterForm';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/signup" element={<RegisterForm />} />
        <Route path="/reset-password" element={<ForgotPassword />}/>
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />}/>
      </Routes>
    </Router>
  );
}

export default App;

