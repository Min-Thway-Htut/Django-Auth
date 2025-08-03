import React, { useState } from 'react';
import axios from 'axios';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/api/users/reset-password/', {email});
            setMessage(res.data.message);
        } catch (err: any) {
            setMessage(err.response?.data?.error || "Something went wrong");
        }
    };

    return (
        <div>
            <h2>Forgot Password</h2>
            <form onSubmit={handleSubmit}>
             <input 
             type="email"
             placeholder="Enter your registered email"
             value={email}
             onChange={(e) => setEmail(e.target.value)}
             required 
             />
             <button type="submit">Send Reset Link</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default ForgotPassword;