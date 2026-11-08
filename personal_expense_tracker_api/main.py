from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

expenses = [
    {"id": 1, "title": "Lunch", "amount": 150, "category": "food", "description": "Lunch at college"},
    {"id": 2, "title": "Python Crash Course", "amount": 750, "category": "education", "description": "Programming book"},
    {"id": 3, "title": "Coffee", "amount": 120, "category": "food", "description": "Evening coffee with friends"},
    {"id": 4, "title": "Groceries", "amount": 1200, "category": "shopping", "description": "Weekly essentials"},
    {"id": 5, "title": "Movie Ticket", "amount": 350, "category": "entertainment", "description": "Weekend movie night"},
    {"id": 6, "title": "Electricity Bill", "amount": 850, "category": "bills", "description": "Monthly utility payment"}
]


# POST
class ExpenseCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category: str
    description: str

@app.post("/expenses", status_code=201)
def add_expense(expense: ExpenseCreate):
    new_expense = {
        "id": len(expenses) + 1,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description
    }
    expenses.append(new_expense)
    return new_expense


# GET ALL EXPENSES (with query parameters for filtering and limits)
@app.get("/expenses")
def get_expenses(
    category: str | None = None, 
    limit: int | None = None, 
    keyword: str | None = None
    ):
    res = expenses

    if category:
        res = [i for i in res if i["category"].lower() == category.lower()]

    if keyword:
        kw = keyword.lower()
        res = [
            i for i in res
            if kw in i["title"].lower() or kw in i["description"].lower()
        ]
    if limit is not None:
        res = res[:limit]

    return res


# GET SUMMARY 
@app.get("/expenses/summary")
def get_expense_summary():
    total = sum(expense["amount"] for expense in expenses)
    return {
        "total_spending": total,
        "total_items": len(expenses)
    }


# GET EXPENSE BY ID
@app.get("/expenses/{expense_id}")
def get_expense_by_id(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


# PATCH
class ExpensePatch(BaseModel):
    title: str | None = None
    amount: float | None = None
    category: str | None = None
    description: str | None = None

@app.patch("/expenses/{expense_id}")
def expenses_patch(expense_id: int, updated_expense: ExpensePatch):
    for expense in expenses:
        if expense["id"] == expense_id:
            update_data = updated_expense.model_dump(exclude_unset=True)
            expense.update(update_data)
            return expense

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


# PUT
class ExpenseUpdate(BaseModel):
    title: str
    amount: float
    category: str
    description: str

@app.put("/expenses/{expense_id}")
def update_entire_expense(expense_id: int, updated_expense: ExpenseUpdate):
    for expense in expenses:
        if expense["id"] == expense_id:
            expense["title"] = updated_expense.title
            expense["amount"] = updated_expense.amount
            expense["category"] = updated_expense.category
            expense["description"] = updated_expense.description
            return expense

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


# DELETE
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            return {"message": "Expense deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )