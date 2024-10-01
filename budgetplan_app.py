import traceback
from fastapi import APIRouter,HTTPException,status
from fastapi.responses import JSONResponse
from schemas.schemas import BudgetPlan
from prompts.llm_prompts import BUDGET_PLANNER_PROMPT
from main import llm


router = APIRouter()

@router.post("/budget_planner")
def budget_planner(payload : BudgetPlan):
    try:
        if payload.existing_investments:
            investment_details = "\n".join([f"{inv.investment_types}: {inv.total_amount}" for inv in payload.investments])
        else:
            investment_details = "No existing investments"
            
        prompt = BUDGET_PLANNER_PROMPT.format(
            monthly_income = payload.monthly_income,
            eb_bill = payload.eb_bill,
            rent = payload.rent,
            groceries = payload.groceries,
            travel = payload.travel,
            internet = payload.internet,
            EMIs = payload.EMIs,
            existing_investments = payload.existing_investments,
            investment_details = investment_details
        )
        
        llm_response = llm.invoke([{"role":"system","content":prompt}])
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = llm_response.content
        )

    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = "Something Went Wrong"
        )