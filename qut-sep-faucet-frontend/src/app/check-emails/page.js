"use client";

import { useState } from "react";

export default function CheckEmails() {
    const otp = localStorage.getItem('OTP');

    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <div>
                Please confirm faucet request sent to your email.
            </div>
            <div>
                link: <a href={`http://localhost:3000/confirm-tx#${otp}`}>Claim ETH</a>
            </div>
        </div>
    );
}
