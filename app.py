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
# HOME
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

    category = interpreted_query["category"]

    location = interpreted_query["location"]

    requirements = interpreted_query["requirements"]


    connection = get_db_connection()


    # Start with every place
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

        sql += """
            AND category LIKE ?
        """

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
                OR address LIKE ?
            )
        """

        parameters.extend([
            f"%{location}%",
            f"%{location}%",
            f"%{location}%"
        ])


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

        search_value = f"%{requirement}%"

        parameters.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])


    results = connection.execute(
        sql,
        parameters
    ).fetchall()


    connection.close()


    # =========================
    # AI RELEVANCE RANKING
    # =========================

    ranked_results = []


    for place in results:

        score = 0


        # -------------------------
        # CATEGORY SCORE
        # -------------------------

        if category:

            if place["category"]:

                if category.lower() in place["category"].lower():

                    score += 30


        # -------------------------
        # LOCATION SCORE
        # -------------------------

        if location:

            if place["city"]:

                if location.lower() == place["city"].lower():

                    score += 30

                elif location.lower() in place["city"].lower():

                    score += 20


            if place["state"]:

                if location.lower() == place["state"].lower():

                    score += 20


        # -------------------------
        # REQUIREMENT SCORE
        # -------------------------

        for requirement in requirements:

            requirement_lower = requirement.lower()


            fields = [

                place["courses"] or "",

                place["services"] or "",

                place["specialties"] or "",

                place["description"] or ""

            ]


            matched = False


            for field in fields:

                if requirement_lower in field.lower():

                    score += 10

                    matched = True

                    break


            if not matched:

                # Try individual words
                words = requirement_lower.split()

                for field in fields:

                    field_lower = field.lower()

                    if any(
                        word in field_lower
                        for word in words
                        if len(word) > 2
                    ):

                        score += 5

                        break


        ranked_results.append(
            {
                "place": place,
                "score": score
            }
        )


    # =========================
    # SORT RESULTS
    # =========================

    ranked_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    return render_template(
        "results.html",

        query=query,

        results=ranked_results,

        interpreted_query=interpreted_query
    )


# =========================
# DETAILS
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
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=True
    )