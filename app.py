import os
import sqlite3

from flask import Flask, render_template, request

from ai.query_parser import understand_query


app = Flask(__name__)


DATABASE = os.path.join(
    os.path.dirname(__file__),
    "database",
    "anyfind.db"
)


def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# SEARCH
# =========================

@app.route("/search")
def search():

    query = request.args.get("query", "").strip()

    interpreted_query = understand_query(query)

    print("Original query:", query)

    print("Interpreted query:", interpreted_query)


    connection = get_db_connection()


    category = interpreted_query["category"]

    location = interpreted_query["location"]

    requirements = interpreted_query["requirements"]


    sql = """
        SELECT *
        FROM places
        WHERE 1=1
    """


    parameters = []


    # =========================
    # CATEGORY FILTER
    # =========================

    if category:

        sql += " AND category LIKE ?"

        parameters.append(
            f"%{category}%"
        )


    # =========================
    # LOCATION FILTER
    # =========================

    if location:

        sql += """
            AND (
                city LIKE ?
                OR state LIKE ?
            )
        """

        parameters.append(
            f"%{location}%"
        )

        parameters.append(
            f"%{location}%"
        )


    # =========================
    # REQUIREMENT FILTER
    # =========================

    for requirement in requirements:

        sql += """
            AND (
                courses LIKE ?
                OR services LIKE ?
                OR specialties LIKE ?
                OR description LIKE ?
            )
        """

        parameters.extend([
            f"%{requirement}%",
            f"%{requirement}%",
            f"%{requirement}%",
            f"%{requirement}%"
        ])


    results = connection.execute(
        sql,
        parameters
    ).fetchall()


    connection.close()


    # =========================
    # RELEVANCE RANKING
    # =========================

    ranked_results = []


    for place in results:

        score = 0


        # Category match
        if category:

            if place["category"]:

                if category.lower() in place["category"].lower():

                    score += 30


        # Location match
        if location:

            if place["city"]:

                if location.lower() in place["city"].lower():

                    score += 30


            if place["state"]:

                if location.lower() in place["state"].lower():

                    score += 20


        # Requirement match
        for requirement in requirements:

            requirement = requirement.lower()


            fields = [

                place["courses"] or "",

                place["services"] or "",

                place["specialties"] or "",

                place["description"] or ""

            ]


            for field in fields:

                if requirement in field.lower():

                    score += 10

                    break


        ranked_results.append(
            (score, place)
        )


    # Highest score first
    ranked_results.sort(
        key=lambda item: item[0],
        reverse=True
    )


    final_results = [

        place

        for score, place

        in ranked_results

    ]


    return render_template(
        "results.html",

        query=query,

        results=final_results,

        interpreted_query=interpreted_query
    )


# =========================
# PLACE DETAILS
# =========================

@app.route("/place/<int:place_id>")
def place_details(place_id):

    connection = get_db_connection()


    place = connection.execute(
        """
        SELECT *
        FROM places
        WHERE id = ?
        """,
        (place_id,)
    ).fetchone()


    connection.close()


    if place is None:

        return "Place not found", 404


    return render_template(
        "details.html",
        place=place
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )