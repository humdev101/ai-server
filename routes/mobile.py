from fastapi import FastAPI, HTTPException,APIRouter
from ..helpers.prompts import getMobilePhoneReview
from ..service.mobileReviewService import getDeviceReview
from pydantic import BaseModel

class DeviceReviewBody  ( BaseModel):
    deviceId: str

router = APIRouter(
    prefix="/mobile"
)


@router.get("/getDevice")
async def get_coin_analysis(id):
    """
    Get device.
    """
    try:
        device = await getMobilePhoneReview(id,"llama3.1")
        return device
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/getDeviceReview")
async def get_device_review(body:DeviceReviewBody):
    """
    Get device.
    """
    try:
        device = await getDeviceReview(body.deviceId)
        return device
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    