import React, { useState } from 'react';
import axios from 'axios';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

interface RegisterData {
  username: string,
  email: string,
  password: string;
}

const RegisterForm: React.FC = () => {
  const [formData, setFormData] = useState<RegisterData>({
    username: '',
    email: '',
    password: '',
  });
  const [message, setMessage] = useState<string>('');
  const [showRules, setShowRules] = useState<boolean>(false);
  const [validations, setValidations] = useState({
    length: false,
    uppercase: false,
    specialChar: false,
  });
  const [showPassword, setShowPassword] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const {name, value} = e.target;
    setFormData({...formData, [e.target.name]: e.target.value});

    if (name === 'password') {
      setValidations({
         length: value.length >= 8,
         uppercase: /[A-Z]/.test(value),
         specialChar: /[!@#$%^&*]/.test(value),
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/users/register/', formData);
      setMessage(res.data.message || 'Registration submitted. Await admin approval.');
      setFormData({ username: '', email: '', password: '' });
    } catch (err: any) {
        const errors = err.response?.data;
        if (typeof errors === 'object') {
          setMessage(Object.values(errors).flat().join(', '));
        } else {
        setMessage('Registration failed.');
        }
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  }

  return (
    <div>
       <h2>Register</h2>
      {message && <p>{message}</p>}
       <form onSubmit={handleSubmit}>
        <input
         name="username" 
         placeholder="Username" 
         value={formData.username} 
         onChange={handleChange} 
         required />
        <input 
        name="email" 
        type="email" 
        placeholder="Email" 
        value={formData.email} 
        onChange={handleChange} 
        required />
        <div style={{position: 'relative'}}>
           <input 
        name="password" 
        type={showPassword ? 'text': 'password'}
        placeholder="Password" 
        value={formData.password} 
        onChange={handleChange} 
        onFocus={() => setShowRules(true)}
        onBlur={() => setShowRules(false)}
        required
        style={{paddingRight: '2.5rem'}} 
        />
        <span
        onClick={togglePasswordVisibility}
          style={{
              position: 'absolute',
              right: '10px',
              top: '50%',
              transform: 'translateY(-50%)',
              cursor: 'pointer',
            }}
        >
           {showPassword ? FaEyeSlash({})  : FaEye({})}
        </span>
        </div>

        {showRules && (
          <div style={{ marginTop: '10px', fontSize: '0.9em' }}>
            <p>Password must contain:</p>
            <ul>
              <li style={{ color: validations.length ? 'green' : 'red' }}>
                At least 8 characters
              </li>
              <li style={{ color: validations.uppercase ? 'green' : 'red' }}>
                At least one uppercase letter
              </li>
              <li style={{ color: validations.specialChar ? 'green' : 'red' }}>
                At least one special character (!@#$%^&*)
              </li>
            </ul>
          </div>
        )}
        <button type="submit">Register</button>
      </form>
    </div>
  )
}

export default RegisterForm;