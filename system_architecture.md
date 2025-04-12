# Solar Lead Generation System - System Architecture Documentation

## System Overview

The Solar Lead Generation System is a comprehensive platform designed to identify and qualify homeowners in Texas who would benefit most from solar energy installations. The system integrates multiple data sources, applies sophisticated scoring algorithms, and provides visualization tools to help solar companies target their marketing efforts effectively.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                        Solar Lead Generation System                 │
│                                                                     │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────┤
│             │             │             │             │             │
│  Property   │  Utility    │    Roof     │ Homeowner   │    Lead     │
│    Data     │    Data     │    Data     │    Data     │  Management │
│   Module    │   Module    │   Module    │   Module    │   Module    │
│             │             │             │             │             │
├─────────────┴─────────────┴─────────────┴─────────────┴─────────────┤
│                                                                     │
│                        Data Integration Layer                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                        Lead Scoring Engine                          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                      Visualization & UI Layer                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Data Collection Modules

#### Property Data Module
- **Purpose**: Collects and processes property information from tax records and other sources
- **Key Components**:
  - Property data collector
  - Property type classifier
  - Ownership status validator
- **Data Sources**:
  - County tax assessor records
  - Property listing databases
  - Building permit records

#### Utility Data Module
- **Purpose**: Gathers utility rate information and estimates monthly bills
- **Key Components**:
  - Utility provider identifier
  - Rate plan analyzer
  - Bill estimator
- **Data Sources**:
  - NREL Utility Rate Database
  - ERCOT data
  - Utility provider APIs

#### Roof Data Module
- **Purpose**: Analyzes roof characteristics for solar suitability
- **Key Components**:
  - Roof orientation analyzer
  - Usable area calculator
  - Shading estimator
- **Data Sources**:
  - Google Maps Platform Solar API
  - Satellite imagery
  - Property dimensions

#### Homeowner Data Module
- **Purpose**: Performs skip tracing to obtain homeowner contact information
- **Key Components**:
  - Skip tracer
  - Contact validator
  - Do-not-call checker
- **Data Sources**:
  - Skip tracing services
  - Public records
  - Property ownership databases

### 2. Data Integration Layer

- **Purpose**: Integrates data from all sources into a unified database
- **Key Components**:
  - Data normalizer
  - Duplicate detector
  - Data quality validator
  - ETL pipeline
- **Technologies**:
  - SQLite database
  - Python data processing libraries

### 3. Lead Scoring Engine

- **Purpose**: Evaluates and scores potential leads based on multiple factors
- **Key Components**:
  - Bill size scorer
  - Roof suitability scorer
  - Property value scorer
  - Net metering benefit calculator
  - Homeowner profile scorer
  - Overall lead quality calculator
- **Technologies**:
  - Python scoring algorithms
  - NumPy for statistical analysis

### 4. Visualization & UI Layer

- **Purpose**: Provides user interface for interacting with the system
- **Key Components**:
  - Dashboard
  - Lead management interface
  - Net metering heat map
  - Data import tools
  - Settings panel
- **Technologies**:
  - HTML/CSS/JavaScript
  - Bootstrap for responsive design
  - Chart.js for data visualization
  - Leaflet.js for mapping

## Data Flow

1. **Data Collection**:
   - Property data is collected from tax records and property databases
   - Utility information is gathered from rate databases
   - Roof data is analyzed using satellite imagery and solar APIs
   - Homeowner information is obtained through skip tracing

2. **Data Integration**:
   - All data is normalized and validated
   - Records are linked by property ID
   - Integrated data is stored in the database

3. **Lead Scoring**:
   - Properties are evaluated based on multiple criteria
   - Component scores are calculated for each factor
   - Overall lead score is computed using weighted average
   - Leads are categorized by quality

4. **Visualization**:
   - Scored leads are displayed in the dashboard
   - Heat map shows geographic distribution of potential
   - Lead details are accessible through the UI

## Database Schema

### Properties Table
```
CREATE TABLE properties (
    property_id TEXT PRIMARY KEY,
    address_line_1 TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    latitude REAL,
    longitude REAL,
    year_built INTEGER,
    square_footage INTEGER,
    bedrooms INTEGER,
    bathrooms INTEGER,
    property_type TEXT,
    is_owner_occupied INTEGER,
    property_value INTEGER,
    has_solar_permit INTEGER,
    last_sale_date TEXT
)
```

### Homeowners Table
```
CREATE TABLE homeowners (
    homeowner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id TEXT,
    first_name TEXT,
    last_name TEXT,
    full_name TEXT,
    phone TEXT,
    email TEXT,
    ownership_years REAL,
    do_not_call INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties (property_id)
)
```

### Roofs Table
```
CREATE TABLE roofs (
    roof_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id TEXT,
    roof_type TEXT,
    roof_age INTEGER,
    total_roof_area INTEGER,
    usable_roof_area INTEGER,
    primary_orientation TEXT,
    azimuth INTEGER,
    pitch INTEGER,
    shading_percentage INTEGER,
    roof_condition TEXT,
    FOREIGN KEY (property_id) REFERENCES properties (property_id)
)
```

### Utilities Table
```
CREATE TABLE utilities (
    utility_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id TEXT,
    utility_provider TEXT,
    residential REAL,
    estimated_monthly_bill REAL,
    net_metering_available INTEGER,
    rate_plan TEXT,
    FOREIGN KEY (property_id) REFERENCES properties (property_id)
)
```

### Leads Table
```
CREATE TABLE leads (
    lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id TEXT,
    lead_score INTEGER,
    qualification TEXT,
    bill_score INTEGER,
    roof_score INTEGER,
    property_score INTEGER,
    metering_score INTEGER,
    homeowner_score INTEGER,
    status TEXT,
    created_date TEXT,
    last_updated TEXT,
    notes TEXT,
    FOREIGN KEY (property_id) REFERENCES properties (property_id)
)
```

## API Endpoints

### Lead Management API

#### GET /api/leads
- **Purpose**: Retrieve all leads
- **Parameters**:
  - `limit`: Maximum number of leads to return
  - `offset`: Starting position for pagination
  - `sort_by`: Field to sort by
  - `sort_order`: "asc" or "desc"
  - `min_score`: Minimum lead score
  - `max_score`: Maximum lead score
  - `qualification`: Lead qualification category
- **Response**: JSON array of lead objects

#### GET /api/leads/{id}
- **Purpose**: Retrieve a specific lead
- **Parameters**:
  - `id`: Lead ID
- **Response**: JSON object with lead details

#### POST /api/leads/import
- **Purpose**: Import leads from external source
- **Parameters**:
  - `source`: Data source name
  - `file`: CSV or JSON file
- **Response**: Import status and summary

#### GET /api/leads/export
- **Purpose**: Export leads to CSV
- **Parameters**:
  - `format`: "csv" or "json"
  - `fields`: Comma-separated list of fields to include
- **Response**: CSV or JSON file

### Property API

#### GET /api/properties
- **Purpose**: Retrieve all properties
- **Parameters**: Similar to leads API
- **Response**: JSON array of property objects

#### GET /api/properties/{id}
- **Purpose**: Retrieve a specific property
- **Parameters**:
  - `id`: Property ID
- **Response**: JSON object with property details

#### POST /api/properties/search
- **Purpose**: Search properties by criteria
- **Parameters**:
  - `city`: City name
  - `zip_code`: ZIP code
  - `min_value`: Minimum property value
  - `max_value`: Maximum property value
  - `property_type`: Type of property
- **Response**: JSON array of matching properties

### Scoring API

#### POST /api/score
- **Purpose**: Score a single lead
- **Parameters**:
  - `property_data`: Property information
  - `utility_data`: Utility information
  - `roof_data`: Roof information
  - `owner_data`: Homeowner information
- **Response**: JSON object with score details

#### POST /api/score/batch
- **Purpose**: Score multiple leads
- **Parameters**:
  - `leads`: Array of lead data objects
- **Response**: JSON array with score details for each lead

## Technology Stack

### Backend
- **Language**: Python 3.10+
- **Database**: SQLite (development), PostgreSQL (production)
- **Key Libraries**:
  - NumPy for numerical operations
  - Pandas for data manipulation
  - SQLAlchemy for database operations
  - Flask for API endpoints

### Frontend
- **Languages**: HTML5, CSS3, JavaScript
- **Frameworks**:
  - Bootstrap 5 for responsive design
  - Chart.js for data visualization
  - Leaflet.js for mapping
  - jQuery for DOM manipulation

### Deployment
- **Development**: Local environment
- **Production**: Cloud-based hosting
- **CI/CD**: Automated testing and deployment pipeline

## Security Considerations

### Data Protection
- All personal data is encrypted in transit and at rest
- Database access is restricted by role-based permissions
- API endpoints require authentication and authorization

### Input Validation
- All user inputs are validated and sanitized
- API requests are validated against schema definitions
- Database queries use parameterized statements to prevent SQL injection

### Audit Logging
- All system actions are logged
- User activities are tracked for accountability
- Error logs are monitored for suspicious activity

## Performance Considerations

### Database Optimization
- Indexes on frequently queried fields
- Denormalization for performance-critical queries
- Query optimization for complex operations

### Caching Strategy
- Frequently accessed data is cached
- Heat map data is pre-calculated
- Lead scores are cached until underlying data changes

### Scalability
- Modular architecture allows for component scaling
- Database can be migrated to more powerful solutions
- API endpoints can be load-balanced

## Maintenance and Monitoring

### Monitoring
- System health metrics are collected
- Performance bottlenecks are identified
- Error rates are tracked

### Backup Strategy
- Database is backed up daily
- Configuration files are version-controlled
- Disaster recovery plan is documented

### Update Process
- Regular updates for data sources
- Scheduled maintenance windows
- Backward compatibility for API changes

## Future Enhancements

### Planned Features
- Machine learning model for lead scoring
- Integration with CRM systems
- Mobile application for field representatives
- Expanded geographic coverage beyond Texas
- Real-time utility rate updates

### Technical Improvements
- Microservice architecture
- Cloud-native deployment
- Advanced analytics dashboard
- Automated lead nurturing

## Conclusion

The Solar Lead Generation System architecture is designed to be modular, scalable, and maintainable. By separating concerns into distinct components and establishing clear interfaces between them, the system can evolve to meet changing business requirements while maintaining performance and reliability.
