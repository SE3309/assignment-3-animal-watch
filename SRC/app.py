import streamlit as st
import mysql.connector
import os
import datetime

# ------------------------------------------------------------------
# 1. DATABASE CONNECTION MANAGER
# ------------------------------------------------------------------
def get_connection(db_name=None):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Captiva1816!", 
        database=db_name
    )

# ------------------------------------------------------------------
# 2. DATABASE SETUP FUNCTION
# ------------------------------------------------------------------
def init_database():
    status_placeholder = st.empty()
    status_placeholder.info("Starting Database Initialization...")
    
    try:
        conn = get_connection(db_name=None)
        cursor = conn.cursor()
        
        cursor.execute("DROP DATABASE IF EXISTS wildlifetraveldb")
        cursor.execute("CREATE DATABASE wildlifetraveldb")
        st.success("Database 'wildlifetraveldb' created.")
        
        cursor.close()
        conn.close()
        
        conn = get_connection(db_name="wildlifetraveldb")
        cursor = conn.cursor()

        base_dir = os.path.dirname(os.path.abspath(__file__))

        def run_file(filename):
            full_path = os.path.join(base_dir, filename)
            if not os.path.exists(full_path):
                st.error(f"File not found: {full_path}")
                return
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            commands = content.split(';')
            for cmd in commands:
                cmd = cmd.strip()
                if not cmd or cmd.upper().startswith('USE'):
                    continue
                try:
                    cursor.execute(cmd)
                    if cursor.with_rows:
                        cursor.fetchall() 
                except Exception as e:
                    pass 
            st.success(f"Executed: {filename}")

        run_file("ex2.sql")
        run_file("ex4.sql")
        
        conn.commit()
        st.success("SUCCESS: Database has been fully rebuilt and populated!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error during setup: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# ------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# ------------------------------------------------------------------
st.sidebar.title("Wildlife Watch App")
menu_option = st.sidebar.radio(
    "Choose an Action:",
    [
        "Home / Status",
        "DATABASE SETUP (Run First)",
        "Add New User",
        "Search Trips",
        "View Species",
        "Add a Review",
        "View Reviews",
        "Update Budgets",
        "Manage Sightings"  # <--- UPDATED NAME
    ]
)

# ------------------------------------------------------------------
# 4. PAGE LOGIC
# ------------------------------------------------------------------
st.title("Wildlife Travel Database System")

if menu_option == "Home / Status":
    st.write("Welcome to the Wildlife Travel System.")
    
    try:
        conn = get_connection("wildlifetraveldb")
        st.success("Successfully connected to 'wildlifetraveldb'!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM User")
        user_count = cursor.fetchone()[0]
        if cursor.with_rows: cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) FROM Trip")
        trip_count = cursor.fetchone()[0]
        if cursor.with_rows: cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) FROM Sighting")
        sighting_count = cursor.fetchone()[0]
        if cursor.with_rows: cursor.fetchall()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", user_count)
        col2.metric("Total Trips", trip_count)
        col3.metric("Total Sightings", sighting_count)
        
        conn.close()
    except Exception as e:
        st.error("Could not connect to the database.")
        st.warning("Go to 'DATABASE SETUP' and click Initialize.")

elif menu_option == "DATABASE SETUP (Run First)":
    st.warning("Warning: This will delete the existing database and rebuild it.")
    if st.button("Initialize Database"):
        init_database()

elif menu_option == "Add New User":
    st.subheader("Add a New User")
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_email = st.text_input("Email Address (Required)")
            new_fname = st.text_input("First Name")
        with col2:
            new_lname = st.text_input("Last Name")
            new_country = st.text_input("Country")
            
        submitted = st.form_submit_button("Save User to Database")
        
        if submitted:
            if not new_email:
                st.error("Error: Email Address is required.")
            else:
                try:
                    conn = get_connection("wildlifetraveldb")
                    cursor = conn.cursor()
                    query = "INSERT INTO User (userEmail, firstName, lastName, country, joinDate) VALUES (%s, %s, %s, %s, CURDATE())"
                    cursor.execute(query, (new_email, new_fname, new_lname, new_country))
                    conn.commit()
                    st.success(f"Success! User '{new_email}' has been added.")
                    cursor.close()
                    conn.close()
                except Exception as e:
                    st.error(f"Database Error: {e}")

elif menu_option == "Search Trips":
    st.subheader("Search for Trips")
    search_term = st.text_input("Search by Trip Name or Destination:")
    
    if search_term:
        try:
            conn = get_connection("wildlifetraveldb")
            cursor = conn.cursor()
            query = """
                SELECT tripName, destination, startDate, budget, userEmail 
                FROM Trip 
                WHERE tripName LIKE %s OR destination LIKE %s
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            columns = [col[0] for col in cursor.description] 
            data = cursor.fetchall()
            
            if data:
                st.success(f"Found {len(data)} trips matching '{search_term}':")
                st.table([dict(zip(columns, row)) for row in data])
            else:
                st.warning("No trips found matching that search.")
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

elif menu_option == "View Species":
    st.subheader("View Species Details")
    try:
        conn = get_connection("wildlifetraveldb")
        cursor = conn.cursor()
        cursor.execute("SELECT commonName FROM Species")
        species_list = [row[0] for row in cursor.fetchall()]
        
        selected_species = st.selectbox("Select a Species to view:", species_list)
        
        if selected_species:
            cursor.execute("SELECT specificName, conservationStatus, description FROM Species WHERE commonName = %s", (selected_species,))
            data = cursor.fetchone()
            if data:
                st.info(f"**Scientific Name:** {data[0]}")
                st.write(f"**Status:** {data[1]}")
                st.write(f"**Description:** {data[2]}")
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

elif menu_option == "Add a Review":
    st.subheader("Write a Review")
    try:
        conn = get_connection("wildlifetraveldb")
        cursor = conn.cursor()
        
        cursor.execute("SELECT userEmail FROM User")
        users = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT locationID, name FROM Location")
        locations = cursor.fetchall()
        loc_options = {f"{loc[1]} (ID: {loc[0]})": loc[0] for loc in locations}
        
        with st.form("review_form"):
            selected_user = st.selectbox("Select User:", users)
            selected_loc_name = st.selectbox("Select Location:", list(loc_options.keys()))
            rating = st.slider("Rating (1-5):", 1, 5, 5)
            review_text = st.text_area("Write your review here:")
            
            submit_review = st.form_submit_button("Submit Review")
            
            if submit_review:
                cursor.execute("SELECT MAX(reviewID) FROM Review")
                max_id = cursor.fetchone()[0]
                new_id = max_id + 1 if max_id else 1
                
                loc_id = loc_options[selected_loc_name]
                insert_query = """
                    INSERT INTO Review (reviewID, userEmail, locationID, rating, reviewText, datePosted, helpfulCount)
                    VALUES (%s, %s, %s, %s, %s, CURDATE(), 0)
                """
                cursor.execute(insert_query, (new_id, selected_user, loc_id, rating, review_text))
                conn.commit()
                st.success(f"Review #{new_id} added successfully!")
                st.info("Go to 'View Reviews' to see it!")
                
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

elif menu_option == "View Reviews":
    st.subheader("Read Reviews by Location")
    try:
        conn = get_connection("wildlifetraveldb")
        cursor = conn.cursor()
        
        cursor.execute("SELECT locationID, name FROM Location")
        locations = cursor.fetchall()
        loc_options = {f"{loc[1]} (ID: {loc[0]})": loc[0] for loc in locations}
        
        selected_loc_label = st.selectbox("Select a Location:", list(loc_options.keys()))
        
        if selected_loc_label:
            loc_id = loc_options[selected_loc_label]
            cursor.execute("""
                SELECT rating, reviewText, userEmail, datePosted 
                FROM Review 
                WHERE locationID = %s 
                ORDER BY reviewID DESC
            """, (loc_id,))
            reviews = cursor.fetchall()
            
            if reviews:
                st.success(f"Found {len(reviews)} reviews:")
                for rev in reviews:
                    with st.expander(f"Rating: {rev[0]}/5 - {rev[2]} ({rev[3]})"):
                        st.write(rev[1])
            else:
                st.info("No reviews found for this location yet.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

elif menu_option == "Update Budgets":
    st.subheader("Update Trip Budget")
    try:
        conn = get_connection("wildlifetraveldb")
        cursor = conn.cursor()
        
        cursor.execute("SELECT tripID, tripName, budget FROM Trip ORDER BY tripID DESC LIMIT 50")
        trips = cursor.fetchall()
        trip_options = {f"{t[1]} (ID: {t[0]}) - Current: ${t[2]}": t[0] for t in trips}
        
        selected_trip_label = st.selectbox("Select a Trip to Update:", list(trip_options.keys()))
        trip_id = trip_options[selected_trip_label]
        
        new_budget = st.number_input("Enter New Budget ($):", min_value=0.0, step=100.0)
        
        if st.button("Update Budget"):
            update_query = "UPDATE Trip SET budget = %s WHERE tripID = %s"
            cursor.execute(update_query, (new_budget, trip_id))
            conn.commit()
            st.success(f"Budget for Trip {trip_id} updated to ${new_budget}")
            st.info("You can verify this in the 'Search Trips' tab.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

# ------------------------------------------------------------------
# NEW FEATURE: MANAGE SIGHTINGS (Add & Delete)
# ------------------------------------------------------------------
elif menu_option == "Manage Sightings":
    st.subheader("Manage Sightings")
    
    # Tabs for Add vs Delete
    tab1, tab2 = st.tabs(["➕ Add New Sighting", "🗑️ Delete Old Sightings"])
    
    # --- TAB 1: ADD SIGHTING ---
    with tab1:
        st.write("Record a new animal sighting on a trip.")
        
        try:
            conn = get_connection("wildlifetraveldb")
            cursor = conn.cursor()
            
            # 1. Get Users
            cursor.execute("SELECT userEmail FROM User")
            users = [row[0] for row in cursor.fetchall()]
            
            # 2. Get Species
            cursor.execute("SELECT speciesID, commonName FROM Species")
            species_raw = cursor.fetchall()
            species_options = {f"{s[1]}": s[0] for s in species_raw} # "Lion": 501
            
            # 3. Get Locations
            cursor.execute("SELECT locationID, name FROM Location")
            loc_raw = cursor.fetchall()
            loc_options = {f"{l[1]}": l[0] for l in loc_raw}
            
            # 4. Get Trips (Itineraries)
            # We join Itinerary and Trip to show useful names like "Kenya Safari (ID: 301)"
            cursor.execute("""
                SELECT I.itineraryID, T.tripName, T.destination 
                FROM Itinerary I 
                JOIN Trip T ON I.tripID = T.tripID
            """)
            itin_raw = cursor.fetchall()
            itin_options = {f"{i[1]} - {i[2]} (Itinerary #{i[0]})": i[0] for i in itin_raw}
            
            with st.form("add_sighting_form"):
                sel_user = st.selectbox("Who saw it?", users)
                sel_species = st.selectbox("What species?", list(species_options.keys()))
                sel_loc = st.selectbox("Where (Location)?", list(loc_options.keys()))
                sel_trip = st.selectbox("On which Trip?", list(itin_options.keys()))
                
                obs_date = st.date_input("Date Observed", datetime.date.today())
                obs_time = st.time_input("Time Observed", datetime.time(12, 00))
                
                submitted = st.form_submit_button("Record Sighting")
                
                if submitted:
                    # Get IDs
                    s_id = species_options[sel_species]
                    l_id = loc_options[sel_loc]
                    i_id = itin_options[sel_trip]
                    
                    # Generate new Sighting ID
                    cursor.execute("SELECT MAX(sightingID) FROM Sighting")
                    max_id = cursor.fetchone()[0]
                    new_sight_id = max_id + 1 if max_id else 1
                    
                    # Combine Date and Time
                    final_datetime = datetime.datetime.combine(obs_date, obs_time)
                    
                    # Insert
                    query = """
                        INSERT INTO Sighting (sightingID, speciesID, locationID, itineraryID, observedAt, userEmail)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (new_sight_id, s_id, l_id, i_id, final_datetime, sel_user))
                    conn.commit()
                    st.success(f"✅ Sighting #{new_sight_id} recorded successfully!")
            
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error loading form data: {e}")

    # --- TAB 2: DELETE SIGHTINGS ---
    with tab2:
        st.warning("Admin Zone: Remove sightings based on date.")
        
        try:
            conn = get_connection("wildlifetraveldb")
            cursor = conn.cursor()
            
            delete_date = st.date_input("Delete sightings BEFORE this date:", key="del_date")
            status_to_delete = st.selectbox("Delete for species with status:", ["Least Concern", "Vulnerable", "Endangered"], key="del_status")
            
            st.write("---")
            st.write("**Preview:**")
            
            preview_query = """
                SELECT S.sightingID, S.observedAt, Sp.commonName, Sp.conservationStatus 
                FROM Sighting S
                JOIN Species Sp ON S.speciesID = Sp.speciesID
                WHERE S.observedAt < %s AND Sp.conservationStatus = %s
                LIMIT 50
            """
            cursor.execute(preview_query, (delete_date, status_to_delete))
            columns = [col[0] for col in cursor.description]
            preview_data = cursor.fetchall()
            
            if preview_data:
                st.dataframe([dict(zip(columns, row)) for row in preview_data])
                st.warning(f"⚠️ Found {len(preview_data)} sightings matching criteria.")
                
                if st.button("Confirm Delete"):
                    delete_query = """
                        DELETE FROM Sighting 
                        WHERE observedAt < %s 
                        AND speciesID IN (SELECT speciesID FROM Species WHERE conservationStatus = %s)
                    """
                    cursor.execute(delete_query, (delete_date, status_to_delete))
                    count = cursor.rowcount
                    conn.commit()
                    st.success(f"✅ Deleted {count} sightings.")
            else:
                st.info("No sightings match these criteria.")
                
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")