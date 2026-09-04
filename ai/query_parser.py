import re


CATEGORIES = {
    "University": [
        "university",
        "universities",
        "college",
        "colleges",
        "engineering college",
        "engineering colleges"
    ],
    "Hospital": [
        "hospital",
        "hospitals",
        "clinic",
        "clinics"
    ],
    "School": [
        "school",
        "schools"
    ],
    "Hotel": [
        "hotel",
        "hotels"
    ],
    "Restaurant": [
        "restaurant",
        "restaurants",
        "food",
        "cafe",
        "cafes"
    ],
    "Bank": [
        "bank",
        "banks"
    ],
    "Tourist Place": [
        "tourist",
        "tourist place",
        "tourist places",
        "tourism",
        "attraction",
        "attractions"
    ]
}


LOCATIONS = [
    "Ahmedabad",
    "Mehsana",
    "Surat",
    "Vadodara",
    "Rajkot",
    "Gandhinagar",
    "Bhavnagar",
    "Anand",
    "Patan",
    "Kutch",
    "Gujarat"
]


REQUIREMENTS = {
    "Artificial Intelligence": [
        "ai",
        "artificial intelligence"
    ],
    "Machine Learning": [
        "ml",
        "machine learning"
    ],
    "Computer Science": [
        "computer science",
        "cse"
    ],
    "Information Technology": [
        "information technology",
        "it"
    ],
    "Cardiology": [
        "heart",
        "cardiology",
        "cardiac"
    ],
    "Cancer Treatment": [
        "cancer",
        "oncology"
    ],
    "Emergency": [
        "emergency",
        "emergency treatment"
    ]
}


def understand_query(query):

    query = query.lower().strip()

    result = {
        "original_query": query,
        "category": None,
        "location": None,
        "requirements": []
    }

    # -------------------------
    # CATEGORY DETECTION
    # -------------------------

    for category, keywords in CATEGORIES.items():

        for keyword in keywords:

            if keyword in query:

                result["category"] = category
                break

        if result["category"]:
            break


    # -------------------------
    # LOCATION DETECTION
    # -------------------------

    for location in LOCATIONS:

        if location.lower() in query:

            result["location"] = location
            break


    # -------------------------
    # REQUIREMENT DETECTION
    # -------------------------

    for requirement, keywords in REQUIREMENTS.items():

        for keyword in keywords:

            # Word boundary avoids matching "it"
            # inside unrelated words.
            if keyword == "it":

                if re.search(r"\bit\b", query):

                    result["requirements"].append(requirement)

                    break

            elif keyword in query:

                result["requirements"].append(requirement)

                break


    return result