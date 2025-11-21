import random
import datetime
from pathlib import Path

# -------------------------------
# CONFIGURATION
# -------------------------------
# How many rows to generate
NUM_TRIPS = 300            # "hundreds"
NUM_SIGHTINGS = 2000       # "thousands"
NUM_REVIEWS = 2000         # "thousands"

# ID ranges chosen to avoid collision with your existing data:
# Trip: existing are 201–205, so we start at 3000
TRIP_START_ID = 3000

# Sighting: existing are 601–605, so start at 1000
SIGHTING_START_ID = 1000

# Review: existing are 701–708 and some 706–708 from ex3,
# so start high at 10000
REVIEW_START_ID = 10000

# Existing FK values from your ex4.sql
USER_EMAILS = [
    "emma@example.com",
    "liam@example.com",
    "sophia@example.com",
    "noah@example.com",
    "ava@example.com",
]

CORPORATE_ACCOUNTS = [101, 102, 103, 104, 105, None]  # allow NULL as well

DESTINATIONS = [
    "Tanzania", "Brazil", "Canada", "Ecuador", "Kenya",
    "Peru", "Costa Rica", "Namibia", "South Africa", "Australia"
]

LOCATION_IDS = [401, 402, 403, 404, 405]
SPECIES_IDS = [501, 502, 503, 504, 505]
ITINERARY_IDS = [301, 302, 303, 304, 305]

# Base dates for randomization
BASE_TRIP_DATE = datetime.date(2024, 1, 1)
BASE_SIGHTING_DATETIME = datetime.datetime(2024, 1, 1)
BASE_REVIEW_DATE = datetime.date(2024, 1, 1)

random.seed(42)  # for reproducible results

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

def random_trip_dates():
    """Return (startDate, endDate) as 'YYYY-MM-DD' strings."""
    start_offset_days = random.randint(0, 300)
    length_days = random.randint(3, 12)

    start_date = BASE_TRIP_DATE + datetime.timedelta(days=start_offset_days)
    end_date = start_date + datetime.timedelta(days=length_days)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def random_sighting_datetime():
    """Return observedAt as 'YYYY-MM-DD HH:MM:SS' string."""
    day_offset = random.randint(0, 300)
    hour_offset = random.randint(0, 23)
    minute_offset = random.randint(0, 59)

    dt = BASE_SIGHTING_DATETIME + datetime.timedelta(
        days=day_offset,
        hours=hour_offset,
        minutes=minute_offset
    )
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def random_review_date():
    """Return datePosted as 'YYYY-MM-DD' string."""
    day_offset = random.randint(0, 300)
    d = BASE_REVIEW_DATE + datetime.timedelta(days=day_offset)
    return d.strftime("%Y-%m-%d")


# -------------------------------
# MAIN GENERATION
# -------------------------------

def main():
    # Output file goes next to this script, called bulk_data_generated.sql
    out_path = Path(__file__).parent / "bulk_data_generated.sql"

    with out_path.open("w", encoding="utf-8") as f:
        f.write("-- Auto-generated bulk data for WildlifeTravelDB\n")
        f.write("USE WildlifeTravelDB;\n\n")

        # ---------------------------------------------
        # 1. TRIPS (hundreds of tuples)
        # ---------------------------------------------
        for i in range(NUM_TRIPS):
            trip_id = TRIP_START_ID + i
            user = random.choice(USER_EMAILS)
            c_acc = random.choice(CORPORATE_ACCOUNTS)
            trip_name = f"Auto Trip {trip_id}"
            dest = random.choice(DESTINATIONS)
            start_date, end_date = random_trip_dates()
            budget = round(random.uniform(800, 8000), 2)

            # Handle NULL vs integer for cAccountID
            if c_acc is None:
                c_acc_sql = "NULL"
            else:
                c_acc_sql = str(c_acc)

            sql = (
                "INSERT INTO Trip "
                "(tripID, userEmail, cAccountID, tripName, destination, startDate, endDate, budget) "
                f"VALUES ({trip_id}, '{user}', {c_acc_sql}, "
                f"'{trip_name}', '{dest}', '{start_date}', '{end_date}', {budget});\n"
            )
            f.write(sql)

        f.write("\n-- -----------------------------------------\n")
        f.write("-- Sightings (thousands of tuples)\n")
        f.write("-- -----------------------------------------\n\n")

        # ---------------------------------------------
        # 2. SIGHTINGS (thousands of tuples)
        # ---------------------------------------------
        for i in range(NUM_SIGHTINGS):
            sighting_id = SIGHTING_START_ID + i
            species_id = random.choice(SPECIES_IDS)
            location_id = random.choice(LOCATION_IDS)
            itinerary_id = random.choice(ITINERARY_IDS)
            observed_at = random_sighting_datetime()
            user = random.choice(USER_EMAILS)

            sql = (
                "INSERT INTO Sighting "
                "(sightingID, speciesID, locationID, itineraryID, observedAt, userEmail) "
                f"VALUES ({sighting_id}, {species_id}, {location_id}, "
                f"{itinerary_id}, '{observed_at}', '{user}');\n"
            )
            f.write(sql)

        f.write("\n-- -----------------------------------------\n")
        f.write("-- Reviews (thousands of tuples)\n")
        f.write("-- -----------------------------------------\n\n")

        # ---------------------------------------------
        # 3. REVIEWS (thousands of tuples)
        # ---------------------------------------------
        for i in range(NUM_REVIEWS):
            review_id = REVIEW_START_ID + i
            user = random.choice(USER_EMAILS)
            location_id = random.choice(LOCATION_IDS)
            rating = random.randint(3, 5)
            date_posted = random_review_date()
            helpful = random.randint(0, 50)

            review_text = f"Auto review {review_id} for location {location_id}"

            sql = (
                "INSERT INTO Review "
                "(reviewID, userEmail, locationID, rating, reviewText, datePosted, helpfulCount) "
                f"VALUES ({review_id}, '{user}', {location_id}, {rating}, "
                f"'{review_text}', '{date_posted}', {helpful});\n"
            )
            f.write(sql)

    print(f"Generated bulk data SQL at: {out_path}")


if __name__ == "__main__":
    main()
