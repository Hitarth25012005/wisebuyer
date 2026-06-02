from flask import Flask, render_template, request, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "replace-with-your-secret-key"

@app.route("/", methods=["GET", "POST"])
def home():
    stocklist = []

    if request.method == "POST":
        q = request.form.get("nm", "").strip().lower()

        try:
            csv_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "flipkartandamazon.csv"
            )

            df = pd.read_csv(csv_path)

            filtered_df = df[
                df["Product_name_Flipkart"].astype(str).str.contains(
                    q, case=False, na=False
                ) |
                df["Product_name_Amazon"].astype(str).str.contains(
                    q, case=False, na=False
                )
            ]

            stocklist = filtered_df.values.tolist()

            if len(stocklist) == 0:
                flash("No matching products found.")

        except Exception as e:
            flash(f"An error occurred: {str(e)}")

    return render_template("index.html", stocklist=stocklist)

if __name__ == "__main__":
    app.run(debug=True)