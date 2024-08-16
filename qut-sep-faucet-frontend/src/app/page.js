"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';


/*
request body for POST /api/get-otp:
{
  "email": "user@qut.edu.au",
  "wallet_address": "0x94eabcdef01048"
}

TODO: address the email spoofing & wallet drainer risk
possible solution: using an email with @qut.edu.au domain
*/

export const url = "http://localhost:8000"

export default function Home() {
  const [email, setEmail] = useState('');
  const [walletAddress, setWalletAddress] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async () => {
    if (email && walletAddress) {
      console.log('Email:', email);
      console.log('Wallet Address:', walletAddress);
      try {
        const response = await fetch(`${url}/api/get-otp`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            address: walletAddress,
          }),
        });
      
        if (!response.ok) {
          const errorData = await response.json();
          if (errorData.detail && Array.isArray(errorData.detail)) {
            // Handle array of errors, e.g., from FastAPI validation
            const firstError = errorData.detail[0];
            setError(firstError.msg || 'An error occurred');
            throw new Error(firstError.msg || `Request failed with status ${response.status}`);
          } else if (typeof errorData.detail === 'string') {
            // Handle single error message
            setError(errorData.detail);
            throw new Error(errorData.detail || `Request failed with status ${response.status}`);
          } else {
            // Fallback for unexpected error format
            setError('An unexpected error occurred');
            throw new Error('An unexpected error occurred');
          }
        }
      
        const data = await response.json();
        console.log('Response data:', data);
        localStorage.setItem('OTP', data);
        router.push('/check-emails');
      } catch (error) {
        console.error('Error:', error);
        setError(error.message || 'An error occurred');
      }
      
    } else {
      setError('Must enter email and wallet address');
      console.log('Must enter an email and wallet address');
    }

  };
  

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Image src={`/blockchainclublogo.png`} alt="logo" width="256" height="256" />
      <div >QUT Blockchain Faucet</div>
      <div >Simply enter your email and wallet address, no need to connect your wallet!</div> 
      
      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="mb-4 p-2 border border-gray-300 rounded w-64 text-black"
      />
      
      <input
        type="text"
        placeholder="Wallet Address"
        value={walletAddress}
        onChange={(e) => setWalletAddress(e.target.value)}
        className="mb-6 p-2 border border-gray-300 rounded w-64 text-black"
      />

      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={handleSubmit}
      >
        Get testnet ETH
      </button>
      
      {error ? (
        <div>
          <p className="text-red-500">{error}</p>
        </div>
      ) : null}

    </div>
  );
}
