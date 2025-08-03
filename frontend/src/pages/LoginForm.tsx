// src/components/LoginForm.tsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {FaEye, FaEyeSlash} from 'react-icons/fa';
import { Link } from "react-router-dom";

interface LoginData {
  username: string;
  password: string;
}

const LoginForm: React.FC = () => {
  const [formData, setFormData] = useState<LoginData>({ username: '', password: '' });
  const [message, setMessage] = useState<string>('');
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/users/login/', formData);
      localStorage.setItem('token', res.data.token);
      setMessage('Login successful!');
      console.log('Login successful!')
      navigate('/home');
      console.log('After navigate call');
    } catch (err: any) {
      const error = err.response?.data?.error || 'Login failed.';
      setMessage(error);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  return (
    <div>
      <h2>Login</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <input 
        name="username" 
        placeholder="Username" 
        value={formData.username} 
        onChange={handleChange} 
        required 
        />
        <div style={{position: 'relative'}}>
        <input 
        name="password" 
        type={showPassword ? 'text' : 'password'} 
        placeholder="Password" 
        value={formData.password} 
        onChange={handleChange} 
        required
        style={{paddingRight: '2.5rem'}}
         />
         <span
          onClick={togglePasswordVisibility}
          style={{
             position: 'absolute',
             right: '0px',
             top: '50%',
             transform: 'translateY(-50%)',
             cursor: 'pointer',
          }}>
            {showPassword ? FaEyeSlash({})  : FaEye({})}
         </span>
        <button type="submit">Login</button>
        </div>
      </form>
      <Link to="/forgot-password">Forgot Password</Link>
    </div>
  );
};

export default LoginForm;

