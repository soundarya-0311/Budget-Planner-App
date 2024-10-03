from pydantic import BaseModel
from typing import Optional,List

class Investments(BaseModel):
    investment_types : str
    total_amount : int
    

class BudgetPlan(BaseModel):
    monthly_income : int
    eb_bill : int
    rent :  int
    groceries : int
    travel : int
    internet : int 
    EMIs : int
    existing_investments : bool
    investments : Optional[List[Investments]] = None