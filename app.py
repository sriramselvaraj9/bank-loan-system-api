from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

loans = {}
transactions = {}

def calculate_interest(P, N, R):
    return (P * N * R) / 100

def calculate_total_amount(P, I):
    return P + I

@app.route("/lend", methods=["POST"])
def lend():
    data = request.get_json()
    customer_id = data["customer_id"]
    P = float(data["loan_amount"])
    N = float(data["loan_period"])
    R = float(data["rate_of_interest"])

    I = calculate_interest(P, N, R)
    A = calculate_total_amount(P, I)
    EMI = round(A / (N * 12), 2)

    loan_id = str(uuid4())
    loans[loan_id] = {
        "customer_id": customer_id,
        "loan_amount": P,
        "interest": I,
        "total_amount": A,
        "emi": EMI,
        "years": N,
        "paid": 0.0,
        "emi_paid_count": 0
    }
    transactions[loan_id] = []

    return jsonify({
        "loan_id": loan_id,
        "total_amount": A,
        "monthly_emi": EMI
    })

@app.route("/payment", methods=["POST"])
def payment():
    data = request.get_json()
    loan_id = data["loan_id"]
    payment_type = data["type"]
    amount = float(data["amount"])

    if loan_id not in loans:
        return jsonify({"error": "Loan ID not found"}), 404

    loan = loans[loan_id]
    loan["paid"] += amount
    if payment_type == "EMI":
        loan["emi_paid_count"] += 1

    transactions[loan_id].append({
        "type": payment_type,
        "amount": amount
    })

    return jsonify({"message": "Payment recorded successfully"})

@app.route("/ledger/<loan_id>", methods=["GET"])
def ledger(loan_id):
    if loan_id not in loans:
        return jsonify({"error": "Loan ID not found"}), 404

    loan = loans[loan_id]
    balance = round(loan["total_amount"] - loan["paid"], 2)
    emi_left = int((balance + loan["emi"] - 1) // loan["emi"])

    return jsonify({
        "transactions": transactions[loan_id],
        "balance": balance,
        "monthly_emi": loan["emi"],
        "emi_left": emi_left
    })

@app.route("/account-overview/<customer_id>", methods=["GET"])
def account_overview(customer_id):
    customer_loans = [
        {
            "loan_id": lid,
            "loan_amount": l["loan_amount"],
            "interest": l["interest"],
            "total_amount": l["total_amount"],
            "emi": l["emi"],
            "amount_paid": l["paid"],
            "emi_left": int(((l["total_amount"] - l["paid"]) + l["emi"] - 1) // l["emi"])
        }
        for lid, l in loans.items() if l["customer_id"] == customer_id
    ]
    return jsonify(customer_loans)
