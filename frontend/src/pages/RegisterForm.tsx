import React, { useState } from 'react';
import axios from 'axios';

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({...formData, [e.target.name]: e.target.value});
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

  return (
    <div>
       <h2>Register</h2>
      {message && <p>{message}</p>}
       <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
        <input name="email" type="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input name="password" type="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
        <button type="submit">Register</button>
      </form>
    </div>
  )
}

export default RegisterForm;