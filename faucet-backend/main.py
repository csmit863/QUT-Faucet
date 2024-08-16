from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from web3 import Web3
from otp.jwt_utils import create_jwt, decode_jwt
import time, jwt
from otp.send_email import send_email
from ethereum.send_eth import send_eth

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rpc_endpoint = ""

# Ethereum address validation function
def is_valid_ethereum_address(address: str) -> bool:
    return Web3.is_address(address)

valid_email = "@qut.edu.au"
# @connect.qut.edu.au ??

# Define a Pydantic model to validate the input data
class OTPRequest(BaseModel):
    email: EmailStr
    address: str


# In-memory store to track email and address combinations with timestamps
# Database would be better
used_combinations = set()

def checkClaimed(email, address):
    current_time = time.time()
    for entry in list(used_combinations):
        if entry[0] == email or entry[1] == address:
            if current_time - entry[2] < 12 * 60 * 60:  # 12 hours in seconds
                print('Wait 12 hours')
                raise HTTPException(status_code=400, detail="This email and address combination has already received funding within the last 12 hours")
            else:
                # Remove the old entry since it's expired
                used_combinations.remove(entry)


@app.post("/api/get-otp")
async def getotp(data: OTPRequest):
    email = data.email
    address = data.address
    #current_time = time.time()

    # create the key / lock pair (based on email and address)
    # 
    if is_valid_ethereum_address:

        checkClaimed(email, address)
        # Create JWT with a 5-minute expiry using the utility function
        otp = create_jwt(email, address)
        # send email with otp link

        # email spoofing risk --> click on malicious link & drain eth
        # issue: sending email to qut email is blocked by Proofpoint.
        # Would this still be the case with a vercel app?   
        # Sign in with QUT credentials would be superior
        # OR, send from official QUT email (e.g. ifb452@qut.edu.au)
        message = f"""
            Go to the following link to receive your sepolia ETH
            http://localhost:3000/confirm-tx#{otp}
            """
        subject = 'QUT Blockchain - Claim Sepolia ETH'
        send_email(email, message, subject)

        return otp
    else:
        raise HTTPException(status_code=422, detail='Not a valid Ethereum address')

class EthRequest(BaseModel):
    data: str

@app.post("/api/get-eth")
async def geteth(request: EthRequest):
    try:
        print(used_combinations)
        # Decode the OTP using the utility function
        decoded_otp = decode_jwt(request.data)
        email = decoded_otp['email']
        address = decoded_otp['address']
        current_time = time.time()
        checkClaimed(email, address)
        # Mark the combination as used with the current timestamp
        used_combinations.add((email, address, current_time))
        # Proceed with the transaction
        status, tx_hash = await send_eth(address)
        return {"status": status, "tx_hash": tx_hash}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="OTP has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid OTP")
