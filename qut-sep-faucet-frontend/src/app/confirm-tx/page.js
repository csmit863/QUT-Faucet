"use client";

import { useEffect, useState, useRef } from "react";
import { url } from "../page";

export default function ConfirmTx() {
    const [response, setResponse] = useState('');
    const isCalled = useRef(false);
    useEffect(() => {
        if (isCalled.current) return; // Prevent the API call if already made
        isCalled.current = true; // Mark as called

        const otp = window.location.hash.substring(1); // Remove the '#' from the start

        if (otp) {
            const sendOtp = async () => {
                try {
                    const response = await fetch(`${url}/api/get-eth`, {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                      },
                      body: JSON.stringify({data:otp})
                    });
                    if (!response.ok) {
                        console.log(response);
                        setResponse(response);
                        throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    console.log('Response data:', data);
                    setResponse(data);
                  } catch (error) {
                    console.error('Error:', error);
                  }
            }
            sendOtp();
        } else {
            console.error('No OTP found in URL');
        }
    }, []);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            {response ? (
                response.status !== 'success' ? (
                    <div>{response.status}: {response.statusText}</div>
                ) : (
                    <div>Transaction {response.status}, tx hash: {response.tx_hash}</div>
                )
            ) : (
                <div>Transaction pending...</div>   
            )}
            {/* Further implementation */}
        </div>
    );
}
