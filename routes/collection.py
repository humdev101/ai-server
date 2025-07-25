from fastapi import FastAPI, HTTPException,APIRouter
from ..helpers.prompts import getCollectionReview
from ..service.collection import getCollection
from ..service.collectionReviewService import getCollectionReview1D
from pydantic import BaseModel

class CollectionBodyReview  ( BaseModel):
    key: str
    chain: str

router = APIRouter(
    prefix="/collection"
)



@router.get("/getCollection")
async def get_collec(key,chain):
    """
    Get Collection.
    """
    try:
        collection = await getCollection(key,chain)
        print("Collection: ",collection)
        return collection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getCollectionReview")
async def get_collection(key,chain):
    """
    Get Collection.
    """
    try:
        device_review = await getCollectionReview(key,chain,"llama3.1")
        return device_review
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/getCollectionReview")
async def get_collection(body:CollectionBodyReview):
    """
    Get Collection.
    """
    try:
        device_review = await getCollectionReview(body.key,body.chain,"llama3.1")
        return device_review
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/getCollectionReview1D")
async def get_collection(body:CollectionBodyReview):
    """
    Get Collection.
    """
    try:
        device_review = await getCollectionReview1D(body.key,body.chain)
        return device_review
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/getDeviceReview")
# async def get_device_review(body:DeviceReviewBody):
#     """
#     Get device.
#     """
#     try:
#         device = await getDeviceReview(body.deviceId)
#         return device
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
    