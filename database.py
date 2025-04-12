"""
Database module for the Solar Lead Generation System.
Handles database connection and schema creation.
"""

import sqlite3
import os
import uuid
from datetime import datetime

class Database:
    def __init__(self, db_path):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Connect to database
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_path}")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        try:
            # Property Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Property (
                property_id TEXT PRIMARY KEY,
                address_line_1 TEXT NOT NULL,
                address_line_2 TEXT,
                city TEXT NOT NULL,
                county TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                property_type TEXT,
                year_built INTEGER,
                square_footage INTEGER,
                bedrooms INTEGER,
                bathrooms REAL,
                lot_size INTEGER,
                assessed_value REAL,
                last_sale_date TEXT,
                last_sale_price REAL,
                is_owner_occupied INTEGER,
                has_solar_installation INTEGER DEFAULT 0,
                has_solar_permit INTEGER DEFAULT 0,
                data_source TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Homeowner Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Homeowner (
                homeowner_id TEXT PRIMARY KEY,
                property_id TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone_mobile TEXT,
                phone_landline TEXT,
                mailing_address_line_1 TEXT,
                mailing_address_line_2 TEXT,
                mailing_city TEXT,
                mailing_state TEXT,
                mailing_zip_code TEXT,
                length_of_ownership REAL,
                skip_trace_status TEXT,
                do_not_call INTEGER DEFAULT 0,
                contact_preference TEXT,
                data_source TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES Property(property_id)
            )
            ''')
            
            # Roof Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Roof (
                roof_id TEXT PRIMARY KEY,
                property_id TEXT NOT NULL,
                roof_type TEXT,
                roof_age INTEGER,
                roof_condition TEXT,
                total_roof_area REAL,
                usable_roof_area REAL,
                primary_orientation TEXT,
                azimuth INTEGER,
                pitch REAL,
                shading_percentage REAL,
                estimated_solar_potential REAL,
                data_source TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES Property(property_id)
            )
            ''')
            
            # Utility Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Utility (
                utility_id TEXT PRIMARY KEY,
                property_id TEXT NOT NULL,
                utility_provider TEXT,
                utility_rate_plan TEXT,
                base_rate REAL,
                tdu_rate REAL,
                has_net_metering INTEGER,
                net_metering_rate REAL,
                estimated_monthly_bill REAL,
                estimated_annual_usage REAL,
                peak_demand REAL,
                data_source TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES Property(property_id)
            )
            ''')
            
            # User Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                first_name TEXT,
                last_name TEXT,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT,
                is_active INTEGER DEFAULT 1
            )
            ''')
            
            # Lead Table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Lead (
                lead_id TEXT PRIMARY KEY,
                property_id TEXT NOT NULL,
                homeowner_id TEXT NOT NULL,
                lead_score INTEGER,
                estimated_savings REAL,
                estimated_system_size REAL,
                estimated_installation_cost REAL,
                estimated_payback_period REAL,
                lead_status TEXT,
                assigned_to TEXT,
                notes TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES Property(property_id),
                FOREIGN KEY (homeowner_id) REFERENCES Homeowner(homeowner_id),
                FOREIGN KEY (assigned_to) REFERENCES User(user_id)
            )
            ''')
            
            # Create indexes
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_property_location ON Property(latitude, longitude)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_property_zip ON Property(zip_code)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_property_owner_occupied ON Property(is_owner_occupied)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_homeowner_contact ON Homeowner(email, phone_mobile)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_lead_score ON Lead(lead_score)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_lead_status ON Lead(lead_status)')
            
            self.conn.commit()
            print("Database tables created successfully.")
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False
    
    def insert_property(self, property_data):
        """Insert a new property record."""
        try:
            property_id = str(uuid.uuid4())
            property_data['property_id'] = property_id
            
            # Set default timestamp if not provided
            if 'last_updated' not in property_data:
                property_data['last_updated'] = datetime.now().isoformat()
            
            # Build the SQL query dynamically based on available fields
            fields = ', '.join(property_data.keys())
            placeholders = ', '.join(['?' for _ in property_data])
            
            query = f"INSERT INTO Property ({fields}) VALUES ({placeholders})"
            self.cursor.execute(query, list(property_data.values()))
            self.conn.commit()
            
            print(f"Property inserted with ID: {property_id}")
            return property_id
        except Exception as e:
            print(f"Error inserting property: {e}")
            return None
    
    def insert_homeowner(self, homeowner_data):
        """Insert a new homeowner record."""
        try:
            homeowner_id = str(uuid.uuid4())
            homeowner_data['homeowner_id'] = homeowner_id
            
            # Set default timestamp if not provided
            if 'last_updated' not in homeowner_data:
                homeowner_data['last_updated'] = datetime.now().isoformat()
            
            # Build the SQL query dynamically based on available fields
            fields = ', '.join(homeowner_data.keys())
            placeholders = ', '.join(['?' for _ in homeowner_data])
            
            query = f"INSERT INTO Homeowner ({fields}) VALUES ({placeholders})"
            self.cursor.execute(query, list(homeowner_data.values()))
            self.conn.commit()
            
            print(f"Homeowner inserted with ID: {homeowner_id}")
            return homeowner_id
        except Exception as e:
            print(f"Error inserting homeowner: {e}")
            return None
    
    def insert_roof(self, roof_data):
        """Insert a new roof record."""
        try:
            roof_id = str(uuid.uuid4())
            roof_data['roof_id'] = roof_id
            
            # Set default timestamp if not provided
            if 'last_updated' not in roof_data:
                roof_data['last_updated'] = datetime.now().isoformat()
            
            # Build the SQL query dynamically based on available fields
            fields = ', '.join(roof_data.keys())
            placeholders = ', '.join(['?' for _ in roof_data])
            
            query = f"INSERT INTO Roof ({fields}) VALUES ({placeholders})"
            self.cursor.execute(query, list(roof_data.values()))
            self.conn.commit()
            
            print(f"Roof inserted with ID: {roof_id}")
            return roof_id
        except Exception as e:
            print(f"Error inserting roof: {e}")
            return None
    
    def insert_utility(self, utility_data):
        """Insert a new utility record."""
        try:
            utility_id = str(uuid.uuid4())
            utility_data['utility_id'] = utility_id
            
            # Set default timestamp if not provided
            if 'last_updated' not in utility_data:
                utility_data['last_updated'] = datetime.now().isoformat()
            
            # Build the SQL query dynamically based on available fields
            fields = ', '.join(utility_data.keys())
            placeholders = ', '.join(['?' for _ in utility_data])
            
            query = f"INSERT INTO Utility ({fields}) VALUES ({placeholders})"
            self.cursor.execute(query, list(utility_data.values()))
            self.conn.commit()
            
            print(f"Utility inserted with ID: {utility_id}")
            return utility_id
        except Exception as e:
            print(f"Error inserting utility: {e}")
            return None
    
    def insert_lead(self, lead_data):
        """Insert a new lead record."""
        try:
            lead_id = str(uuid.uuid4())
            lead_data['lead_id'] = lead_id
            
            # Set default timestamps if not provided
            if 'created_date' not in lead_data:
                lead_data['created_date'] = datetime.now().isoformat()
            if 'last_updated' not in lead_data:
                lead_data['last_updated'] = datetime.now().isoformat()
            
            # Build the SQL query dynamically based on available fields
            fields = ', '.join(lead_data.keys())
            placeholders = ', '.join(['?' for _ in lead_data])
            
            query = f"INSERT INTO Lead ({fields}) VALUES ({placeholders})"
            self.cursor.execute(query, list(lead_data.values()))
            self.conn.commit()
            
            print(f"Lead inserted with ID: {lead_id}")
            return lead_id
        except Exception as e:
            print(f"Error inserting lead: {e}")
            return None
    
    def get_property_by_id(self, property_id):
        """Get property by ID."""
        try:
            self.cursor.execute("SELECT * FROM Property WHERE property_id = ?", (property_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error getting property: {e}")
            return None
    
    def get_properties_by_zip(self, zip_code):
        """Get properties by ZIP code."""
        try:
            self.cursor.execute("SELECT * FROM Property WHERE zip_code = ?", (zip_code,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting properties by ZIP: {e}")
            return []
    
    def get_homeowner_by_property(self, property_id):
        """Get homeowner by property ID."""
        try:
            self.cursor.execute("SELECT * FROM Homeowner WHERE property_id = ?", (property_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error getting homeowner: {e}")
            return None
    
    def get_leads_by_score(self, min_score=0, max_score=100, limit=100):
        """Get leads by score range."""
        try:
            self.cursor.execute("""
                SELECT l.*, p.address_line_1, p.city, p.zip_code, h.first_name, h.last_name, h.phone_mobile, h.email
                FROM Lead l
                JOIN Property p ON l.property_id = p.property_id
                JOIN Homeowner h ON l.homeowner_id = h.homeowner_id
                WHERE l.lead_score BETWEEN ? AND ?
                ORDER BY l.lead_score DESC
                LIMIT ?
            """, (min_score, max_score, limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting leads by score: {e}")
            return []
    
    def update_property(self, property_id, update_data):
        """Update property record."""
        try:
            # Add last_updated timestamp
            update_data['last_updated'] = datetime.now().isoformat()
            
            # Build the SET clause for the SQL query
            set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
            values = list(update_data.values())
            values.append(property_id)  # Add property_id for the WHERE clause
            
            query = f"UPDATE Property SET {set_clause} WHERE property_id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
            
            print(f"Property updated: {property_id}")
            return True
        except Exception as e:
            print(f"Error updating property: {e}")
            return False
    
    def update_homeowner(self, homeowner_id, update_data):
        """Update homeowner record."""
        try:
            # Add last_updated timestamp
            update_data['last_updated'] = datetime.now().isoformat()
            
            # Build the SET clause for the SQL query
            set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
            values = list(update_data.values())
            values.append(homeowner_id)  # Add homeowner_id for the WHERE clause
            
            query = f"UPDATE Homeowner SET {set_clause} WHERE homeowner_id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
            
            print(f"Homeowner updated: {homeowner_id}")
            return True
        except Exception as e:
            print(f"Error updating homeowner: {e}")
            return False
    
    def update_lead_status(self, lead_id, status, notes=None):
        """Update lead status."""
        try:
            update_data = {
                'lead_status': status,
                'last_updated': datetime.now().isoformat()

(Content truncated due to size limit. Use line ranges to read in chunks)