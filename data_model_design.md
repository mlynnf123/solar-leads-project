# Data Model Design for Solar Lead Generation System

## Overview

This document outlines the data model design for our solar lead generation system targeting Texas homeowners. The model is designed to efficiently store and process property data, utility information, and homeowner contact details to identify qualified solar leads.

## Core Entities

### Property
The central entity representing residential properties in Texas.

**Fields:**
- `property_id` (Primary Key): Unique identifier for the property
- `address_line_1`: Street address
- `address_line_2`: Apartment/unit number (if applicable)
- `city`: City name
- `county`: County name
- `state`: State (TX for Texas)
- `zip_code`: ZIP code
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude
- `property_type`: Type of property (single-family, multi-family, etc.)
- `year_built`: Year the property was constructed
- `square_footage`: Total living area in square feet
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `lot_size`: Size of the lot in square feet
- `assessed_value`: Property's assessed value
- `last_sale_date`: Date of last property sale
- `last_sale_price`: Price of last property sale
- `is_owner_occupied`: Boolean indicating if owner lives in the property
- `has_solar_installation`: Boolean indicating if property already has solar
- `has_solar_permit`: Boolean indicating if property has a recent solar permit
- `data_source`: Source of the property data
- `last_updated`: Timestamp of last data update

### Homeowner
Represents the property owner and their contact information.

**Fields:**
- `homeowner_id` (Primary Key): Unique identifier for the homeowner
- `property_id` (Foreign Key): Reference to the Property
- `first_name`: First name
- `last_name`: Last name
- `email`: Email address
- `phone_mobile`: Mobile phone number
- `phone_landline`: Landline phone number
- `mailing_address_line_1`: Mailing address (if different from property)
- `mailing_address_line_2`: Mailing address line 2
- `mailing_city`: Mailing address city
- `mailing_state`: Mailing address state
- `mailing_zip_code`: Mailing address ZIP code
- `length_of_ownership`: Duration of property ownership in years
- `skip_trace_status`: Status of skip tracing efforts
- `do_not_call`: Boolean indicating if on Do Not Call list
- `contact_preference`: Preferred contact method
- `data_source`: Source of the homeowner data
- `last_updated`: Timestamp of last data update

### Roof
Stores detailed information about the property's roof characteristics.

**Fields:**
- `roof_id` (Primary Key): Unique identifier for the roof
- `property_id` (Foreign Key): Reference to the Property
- `roof_type`: Type of roof (shingle, tile, metal, etc.)
- `roof_age`: Age of the roof in years
- `roof_condition`: Condition rating of the roof
- `total_roof_area`: Total roof area in square feet
- `usable_roof_area`: Usable area for solar panels in square feet
- `primary_orientation`: Primary roof orientation (N, S, E, W, etc.)
- `azimuth`: Roof azimuth angle
- `pitch`: Roof pitch/slope
- `shading_percentage`: Percentage of roof affected by shading
- `estimated_solar_potential`: Estimated solar generation potential (kWh/year)
- `data_source`: Source of the roof data
- `last_updated`: Timestamp of last data update

### Utility
Contains information about the utility provider and rate structure.

**Fields:**
- `utility_id` (Primary Key): Unique identifier for the utility record
- `property_id` (Foreign Key): Reference to the Property
- `utility_provider`: Name of the electricity provider
- `utility_rate_plan`: Name of the rate plan
- `base_rate`: Base electricity rate ($/kWh)
- `tdu_rate`: Transmission and Distribution Utility rate
- `has_net_metering`: Boolean indicating if net metering is available
- `net_metering_rate`: Rate paid for excess generation
- `estimated_monthly_bill`: Estimated monthly electricity bill
- `estimated_annual_usage`: Estimated annual electricity usage (kWh)
- `peak_demand`: Peak electricity demand (kW)
- `data_source`: Source of the utility data
- `last_updated`: Timestamp of last data update

### Lead
Represents a qualified lead for solar installation.

**Fields:**
- `lead_id` (Primary Key): Unique identifier for the lead
- `property_id` (Foreign Key): Reference to the Property
- `homeowner_id` (Foreign Key): Reference to the Homeowner
- `lead_score`: Overall score indicating lead quality (0-100)
- `estimated_savings`: Estimated annual savings from solar
- `estimated_system_size`: Recommended solar system size (kW)
- `estimated_installation_cost`: Estimated cost of installation
- `estimated_payback_period`: Estimated payback period in years
- `lead_status`: Current status of the lead (new, contacted, qualified, etc.)
- `assigned_to`: User assigned to the lead
- `notes`: Additional notes about the lead
- `created_date`: Date the lead was created
- `last_updated`: Timestamp of last update

### User
System users who manage leads and access the platform.

**Fields:**
- `user_id` (Primary Key): Unique identifier for the user
- `username`: Username for login
- `email`: Email address
- `first_name`: First name
- `last_name`: Last name
- `role`: User role (admin, sales, analyst, etc.)
- `created_date`: Date the user was created
- `last_login`: Timestamp of last login
- `is_active`: Boolean indicating if the user account is active

## Relationships

1. **Property to Homeowner**: One-to-One
   - A property has one homeowner, and a homeowner owns one property (in this simplified model)

2. **Property to Roof**: One-to-One
   - A property has one roof record

3. **Property to Utility**: One-to-One
   - A property has one utility record

4. **Property to Lead**: One-to-One
   - A property can be associated with one lead

5. **Homeowner to Lead**: One-to-One
   - A homeowner can be associated with one lead

6. **User to Lead**: One-to-Many
   - A user can be assigned to multiple leads

## Derived Data and Calculations

### Lead Scoring Algorithm Factors
- **Bill Size Score**: Based on estimated monthly bill
- **Roof Suitability Score**: Based on orientation, size, and shading
- **Property Characteristics Score**: Based on age, size, and value
- **Net Metering Benefit Score**: Based on utility rates and policies
- **Overall Lead Score**: Weighted combination of individual scores

### Solar Potential Calculations
- **System Size Estimation**: Based on roof area, orientation, and electricity usage
- **Energy Production Estimation**: Based on system size, location, and roof characteristics
- **Savings Estimation**: Based on energy production and utility rates
- **ROI Calculation**: Based on installation cost and estimated savings

## Database Schema

```sql
-- Property Table
CREATE TABLE Property (
    property_id VARCHAR(36) PRIMARY KEY,
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    county VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    property_type VARCHAR(50),
    year_built INT,
    square_footage INT,
    bedrooms INT,
    bathrooms DECIMAL(3, 1),
    lot_size INT,
    assessed_value DECIMAL(12, 2),
    last_sale_date DATE,
    last_sale_price DECIMAL(12, 2),
    is_owner_occupied BOOLEAN,
    has_solar_installation BOOLEAN DEFAULT FALSE,
    has_solar_permit BOOLEAN DEFAULT FALSE,
    data_source VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Homeowner Table
CREATE TABLE Homeowner (
    homeowner_id VARCHAR(36) PRIMARY KEY,
    property_id VARCHAR(36) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone_mobile VARCHAR(20),
    phone_landline VARCHAR(20),
    mailing_address_line_1 VARCHAR(255),
    mailing_address_line_2 VARCHAR(255),
    mailing_city VARCHAR(100),
    mailing_state CHAR(2),
    mailing_zip_code VARCHAR(10),
    length_of_ownership DECIMAL(5, 2),
    skip_trace_status VARCHAR(50),
    do_not_call BOOLEAN DEFAULT FALSE,
    contact_preference VARCHAR(50),
    data_source VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);

-- Roof Table
CREATE TABLE Roof (
    roof_id VARCHAR(36) PRIMARY KEY,
    property_id VARCHAR(36) NOT NULL,
    roof_type VARCHAR(50),
    roof_age INT,
    roof_condition VARCHAR(50),
    total_roof_area DECIMAL(10, 2),
    usable_roof_area DECIMAL(10, 2),
    primary_orientation VARCHAR(20),
    azimuth INT,
    pitch DECIMAL(5, 2),
    shading_percentage DECIMAL(5, 2),
    estimated_solar_potential DECIMAL(10, 2),
    data_source VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);

-- Utility Table
CREATE TABLE Utility (
    utility_id VARCHAR(36) PRIMARY KEY,
    property_id VARCHAR(36) NOT NULL,
    utility_provider VARCHAR(100),
    utility_rate_plan VARCHAR(100),
    base_rate DECIMAL(6, 4),
    tdu_rate DECIMAL(6, 4),
    has_net_metering BOOLEAN,
    net_metering_rate DECIMAL(6, 4),
    estimated_monthly_bill DECIMAL(8, 2),
    estimated_annual_usage DECIMAL(10, 2),
    peak_demand DECIMAL(8, 2),
    data_source VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES Property(property_id)
);

-- Lead Table
CREATE TABLE Lead (
    lead_id VARCHAR(36) PRIMARY KEY,
    property_id VARCHAR(36) NOT NULL,
    homeowner_id VARCHAR(36) NOT NULL,
    lead_score INT,
    estimated_savings DECIMAL(10, 2),
    estimated_system_size DECIMAL(6, 2),
    estimated_installation_cost DECIMAL(10, 2),
    estimated_payback_period DECIMAL(5, 2),
    lead_status VARCHAR(50),
    assigned_to VARCHAR(36),
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES Property(property_id),
    FOREIGN KEY (homeowner_id) REFERENCES Homeowner(homeowner_id),
    FOREIGN KEY (assigned_to) REFERENCES User(user_id)
);

-- User Table
CREATE TABLE User (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Indexes
CREATE INDEX idx_property_location ON Property(latitude, longitude);
CREATE INDEX idx_property_zip ON Property(zip_code);
CREATE INDEX idx_property_owner_occupied ON Property(is_owner_occupied);
CREATE INDEX idx_homeowner_contact ON Homeowner(email, phone_mobile);
CREATE INDEX idx_lead_score ON Lead(lead_score);
CREATE INDEX idx_lead_status ON Lead(lead_status);
```

## Data Flow

1. **Data Collection**:
   - Import property data from tax records
   - Enrich with utility rate information
   - Add roof characteristics from Google Solar API
   - Perform skip tracing to add homeowner contact information

2. **Data Processing**:
   - Filter for owner-occupied single-family homes
   - Exclude properties with existing solar installations or permits
   - Calculate estimated electric bills based on square footage and utility rates
   - Analyze roof orientation and suitability

3. **Lead Scoring**:
   - Calculate individual component scores
   - Compute weighted overall lead score
   - Prioritize leads based on score

4. **Data Visualization**:
   - Generate heat maps of high-potential areas
   - Display lead details and property information
   - Track lead status and conversion metrics

## Data Security and Privacy Considerations

1. **Personal Information Protection**:
   - Encrypt sensitive homeowner data
   - Implement role-based access controls
   - Maintain compliance with data protection regulations

2. **Do Not Call Compliance**:
   - Flag and filter numbers on the Do Not Call registry
   - Implement contact preference management
   - Document consent for marketing communications

3. **Data Retention Policies**:
   - Define retention periods for different data categories
   - Implement data purging mechanisms
   - Provide data access and deletion capabilities

## Next Steps

1. **Database Implementation**:
   - Set up database server
   - Create tables and relationships
   - Implement indexes for performance optimization

2. **Data Integration**:
   - Develop API connectors for data sources
   - Create ETL processes for data import and transformation
   - Implement data validation and cleaning procedures

3. **Lead Scoring Algorithm Development**:
   - Define scoring weights and thresholds
   - Implement calculation logic
   - Test with sample data
