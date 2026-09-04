def understand_query(query):

    query = query.lower()

    result = {
        "category": None,
        "location": None,
        "requirements": []
    }

    # CATEGORY DETECTION

    if "university" in query or "universities" in query or "college" in query or "colleges" in query:
        result["category"] = "University"

    elif "hospital" in query or "hospitals" in query:
        result["category"] = "Hospital"

    elif "school" in query or "schools" in query:
        result["category"] = "School"

    elif "hotel" in query or "hotels" in query:
        result["category"] = "Hotel"

    elif "restaurant" in query or "restaurants" in query:
        result["category"] = "Restaurant"


    # LOCATION DETECTION

    locations = [
        "ahmedabad",
        "mehsana",
        "surat",
        "vadodara",
        "rajkot",
        "gandhinagar",
        "gujarat"
    ]

    for location in locations:

        if location in query:
            result["location"] = location.title()
            break


    # REQUIREMENT DETECTION

    if "ai" in query or "artificial intelligence" in query:
        result["requirements"].append("Artificial Intelligence")

    if "machine learning" in query or "ml" in query:
        result["requirements"].append("Machine Learning")

    if "heart" in query or "cardiology" in query:
        result["requirements"].append("Cardiology")


    return result