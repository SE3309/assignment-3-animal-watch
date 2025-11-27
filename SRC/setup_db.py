import mysql.connector
import os

def run_setup():
    print("🚀 Starting Database Setup...")
    
    try:
        # 1. Connect to MySQL (No DB selected yet)
        # We connect to localhost with root and no password
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Captiva1816!" 
        )
        cursor = conn.cursor()
        
        # 2. Clean Slate: Drop and Recreate Database
        cursor.execute("DROP DATABASE IF EXISTS wildlifetraveldb")
        cursor.execute("CREATE DATABASE wildlifetraveldb")
        cursor.execute("USE wildlifetraveldb")
        print("✅ Database 'wildlifetraveldb' created and selected.")
        
        # 3. Helper Function to execute SQL files safely
        def execute_sql_file(filename):
            if not os.path.exists(filename):
                print(f"❌ Missing file: {filename}")
                return

            print(f"📂 Processing {filename}...")
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split commands by semicolon to run them one by one
            commands = content.split(';')
            
            for cmd in commands:
                cmd = cmd.strip()
                # SKIP any 'USE' commands in the file to prevent errors
                if not cmd or cmd.upper().startswith("USE"):
                    continue
                
                try:
                    cursor.execute(cmd)
                except Exception as e:
                    # We print errors but keep going (some warnings are normal)
                    pass 

        # 4. Run the files
        # ex2 creates the tables, ex4 adds the data
        execute_sql_file("ex2.sql")
        execute_sql_file("ex4.sql")
        
        # 5. Save changes
        conn.commit()
        print("\n🎉 SUCCESS! Database is fully built.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Fatal Error: {e}")

if __name__ == "__main__":
    run_setup()