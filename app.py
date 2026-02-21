from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Example college data with branch-specific cutoffs and annual fees
colleges = {
    "College A": {
        "base_volatility": 5,
        "branches": {
            "Computer Science": {"cutoff": 85, "annual_fee": 450000},
            "Mechanical": {"cutoff": 82, "annual_fee": 350000},
            "Civil": {"cutoff": 78, "annual_fee": 300000},
            "Electrical": {"cutoff": 84, "annual_fee": 380000}
        }
    },
    "College B": {
        "base_volatility": 3,
        "branches": {
            "Computer Science": {"cutoff": 78, "annual_fee": 420000},
            "Mechanical": {"cutoff": 75, "annual_fee": 320000},
            "Civil": {"cutoff": 72, "annual_fee": 280000},
            "Electrical": {"cutoff": 77, "annual_fee": 350000}
        }
    },
    "College C": {
        "base_volatility": 4,
        "branches": {
            "Computer Science": {"cutoff": 92, "annual_fee": 500000},
            "Mechanical": {"cutoff": 88, "annual_fee": 380000},
            "Civil": {"cutoff": 85, "annual_fee": 320000},
            "Electrical": {"cutoff": 90, "annual_fee": 420000}
        }
    }
}

# both the root path and /admn render the same page; keeping everything on
# the Flask server means the front end (templates/static) and back end
# share the same port (5000 by default).

@app.route("/", methods=["GET", "POST"])
@app.route("/admn", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        # debug incoming data
        app.logger.debug("incoming form data: %s", request.form)

        try:
            score_val = request.form.get("score", None)
            score = float(score_val or 0)
        except (ValueError, TypeError):
            app.logger.debug("invalid score, defaulting to 0")
            score = 0

        try:
            budget_val = request.form.get("budget", None)
            budget = float(budget_val or 0)
        except (ValueError, TypeError):
            app.logger.debug("invalid budget, defaulting to 0")
            budget = 0

        category = request.form.get("category", "General")
        desired_college = request.form.get("college", None)
        desired_branch = request.form.get("branch", None)

        app.logger.debug("score=%s, budget=%s, college=%s, branch=%s", score, budget, desired_college, desired_branch)

        # if user selected a specific college and branch, compute probability
        if (desired_college and desired_college in colleges and 
            desired_branch and desired_branch in colleges[desired_college]["branches"]):
            
            college_data = colleges[desired_college]
            branch_data = college_data["branches"][desired_branch]
            
            cutoff = branch_data["cutoff"]
            annual_fee = branch_data["annual_fee"]
            volatility = college_data["base_volatility"]
            
            # improved probability logic:
            # - base is 50%
            # - add or subtract based on score vs cutoff, scaled by volatility
            # - apply category adjustment
            diff = score - cutoff
            cat_adjust = {"General": 0, "OBC": -5, "SC": -10, "ST": -10}
            
            # probability increases with score gap and volatility
            probability = 50 + diff * volatility + cat_adjust.get(category, 0)
            probability = max(min(probability, 100), 0)
            
            # if budget doesn't cover the fee, reduce probability slightly
            fee_feasible = budget >= annual_fee
            if not fee_feasible:
                probability *= 0.8  # 20% penalty if fee exceeds budget

            if probability > 70:
                risk = "Safe"
            elif probability > 40:
                risk = "Moderate"
            else:
                risk = "Risky"

            results = {
                "college_name": desired_college,
                "branch": desired_branch,
                "probability": round(probability, 1),
                "risk": risk,
                "cutoff": cutoff,
                "your_score": score,
                "fee_amount": annual_fee,
                "user_budget": budget,
                "fee_feasible": fee_feasible,
                "category": category
            }
        else:
            # backward compatibility: show all colleges if selection incomplete
            results = {}
            if desired_college and desired_college in colleges and desired_branch:
                results = {
                    "error": "Invalid college or branch selection. Please select a valid combination."
                }

    return render_template("index.html", results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)