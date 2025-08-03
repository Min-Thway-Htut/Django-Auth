import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';


const ResetPassword = () => {
    const {uid, token} = useParams();
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleReset = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await axios.post(`http://localhost:8000/api/users/reset-password-confirm/${uid}/${token}/`, {
                new_password: newPassword,
                confirm_password: confirmPassword,
            });
            setMessage(res.data.success);
        } catch (err: any) {
            setMessage(err.response?.data?.error || "Something went wrong");
        }
    };

    return (
        <div>
            <h2>Reset Your Password</h2>
            <form onSubmit={handleReset}>
                <input type="password" placeholder="New Password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
                <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
                <button type="submit">Reset Password</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default ResetPassword;