from fastapi import FastAPI, HTTPException,APIRouter
from ..service.coinAnalysisService import addAnalysis,getAnalysisById,getAllAnalysis
from ..models.coinAnalysisModel import CoinAnalysisBase

router = APIRouter(
    prefix="/coin_ai_analysis"
)


@router.get("/coinanalysis")
async def get_coin_analysis():
    """
    Get all coin analysis.
    """
    try:
        analysis = await getAllAnalysis()
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/coinanalysis")
async def create_coin_analysis(coin_analysis: CoinAnalysisBase):
    """
    Create a new coin analysis.
    """
    try:
        analysis_id = await addAnalysis(coin_analysis)
        return {"id": analysis_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))