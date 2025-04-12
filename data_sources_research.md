# Data Sources Research for Solar Lead Generation System

## Property Tax Records APIs

### TaxNetUSA
- **URL**: https://www.taxnetusa.com/data/web-service-api/
- **Coverage**: All of Texas and Florida (over 300 counties)
- **Data Types**:
  - Appraisal Data: Property owner/taxpayer information, square footage, year built, improvement sketches
  - Tax Collector/Delinquent Data: Up-to-date property tax data, delinquent tax bills, estimated annual taxes
  - GIS Parcel Data: Parcel shapefiles with property attributes
- **Access Methods**:
  - Real-time API access via web services (XML or JSON)
  - Bulk data downloads (state or county datasets)
  - List matching service (provide address list, get back with comprehensive data)
- **Relevance**: High - Provides comprehensive property data needed for identifying owner-occupied homes and property characteristics

### CoreLogic CLIP (CoreLogic Information Platform)
- **URL**: https://www.corelogic.com/360-property-data/clip/
- **Coverage**: National
- **Data Types**:
  - Property tax information
  - Property characteristics
  - Ownership data
- **Access Methods**:
  - API access
  - Mobile access to listings, tax, and client data
- **Relevance**: High - Provides property tax information and property characteristics

### Zillow Group Bridge Public Records API
- **URL**: https://www.zillowgroup.com/developers/api/public-data/public-records-api/
- **Coverage**: National
- **Data Types**:
  - Parcel data
  - Assessment data
  - Transactional county data (15 years history)
- **Access Methods**:
  - API access
- **Relevance**: High - Provides property characteristics and historical transaction data

### Texas Comptroller's Office
- **URL**: https://comptroller.texas.gov/taxes/property-tax/county-directory/
- **Coverage**: Texas
- **Data Types**:
  - Contact information for appraisal districts and county tax offices
  - Listing of taxing units
- **Access Methods**:
  - Directory access
  - Potential API access to specific county databases
- **Relevance**: Medium - Provides contact information for local tax authorities, but may not offer direct API access

## Utility Rate Data Sources

### NREL Utility Rate Database (URDB)
- **URL**: https://openei.org/wiki/Utility_Rate_Database
- **Coverage**: National (over 3,700 U.S. utilities)
- **Data Types**:
  - Rate structure information
  - Utility company information
  - Annual average utility rates ($/kWh) for residential, commercial, and industrial sectors
- **Access Methods**:
  - API access
  - Bulk download (CSV/JSON formats)
  - Web interface
- **Relevance**: High - Provides utility rate information needed to estimate electric bills

### NREL Utility Rates API
- **URL**: https://developer.nrel.gov/docs/electricity/utility-rates-v3/
- **Coverage**: National
- **Data Types**:
  - Annual average utility rates ($/kWh) for residential, commercial, and industrial sectors
  - Local utility name for specific locations
- **Access Methods**:
  - RESTful API (JSON/XML)
  - Geolocation-based queries (latitude/longitude)
- **Relevance**: High - Provides utility rate information based on location

### ERCOT (Electric Reliability Council of Texas)
- **URL**: https://www.ercot.com/services/mdt/data-portal
- **Coverage**: Texas
- **Data Types**:
  - Market prices
  - Grid data
  - Transmission and distribution utility (TDU) rates
- **Access Methods**:
  - Public API
  - Data portal
- **Relevance**: High - Texas-specific electricity market data

### Public Utility Commission of Texas
- **URL**: https://www.puc.texas.gov/industry/electric/rates/Default.aspx
- **Coverage**: Texas
- **Data Types**:
  - Monthly bill comparisons for residential and commercial customers
  - Utility rates for areas not open to retail competition
- **Access Methods**:
  - Web interface
  - Potential data downloads
- **Relevance**: Medium - Provides Texas-specific utility rate information

## Property Characteristics APIs

### Zillow MLS Listings API
- **URL**: https://www.zillowgroup.com/developers/api/mls-broker-data/mls-listings/
- **Coverage**: National (U.S. and Canada)
- **Data Types**:
  - MLS listing data
  - Property characteristics
  - Normalized to RESO data dictionary standard
- **Access Methods**:
  - RESTful API (JSON)
  - Password and access token authentication
- **Relevance**: High - Provides detailed property characteristics including square footage, year built, and roof type
- **Access Restrictions**: Invite-only platform, requires partnership with MLS

### Zillow Research Data
- **URL**: https://www.zillow.com/research/data/
- **Coverage**: National
- **Data Types**:
  - Zillow Home Value Index (ZHVI)
  - Market trends
  - Property characteristics
- **Access Methods**:
  - Data downloads
  - Potential API access
- **Relevance**: Medium - Provides property value and market trend data

## Geospatial and Roof Orientation Data

### Google Maps Platform Solar API
- **URL**: https://developers.google.com/maps/documentation/solar/overview
- **Coverage**: Multiple countries (specific coverage details available)
- **Data Types**:
  - Building insights (location, dimensions, solar potential)
  - Data layers (raw solar information datasets)
  - GeoTIFF (rasters with encoded solar information)
  - Digital surface model
  - Aerial imagery
  - Annual and monthly flux maps
  - Hourly shade data
- **Access Methods**:
  - RESTful API
  - Three main endpoints: buildingInsights, dataLayers, geoTiff
- **Relevance**: High - Provides detailed roof orientation and solar potential data
- **Benefits**:
  - Remote solar power system design
  - Reduced site assessment time
  - Prioritization of installation locations
  - More accurate proposals

### Project Sunroof
- **URL**: https://sunroof.withgoogle.com/
- **Coverage**: Select areas in the U.S.
- **Data Types**:
  - Roof solar savings potential
  - Solar calculator
- **Access Methods**:
  - Web interface
  - Potential API access
- **Relevance**: Medium - Provides solar potential data but may have limited coverage

## Skip Tracing Services

### Datazapp
- **URL**: https://www.datazapp.com/skip-tracing-real-estate-marketing
- **Coverage**: National
- **Data Types**:
  - Cell phone numbers
  - Landline numbers
  - Email addresses
  - Property owner information
- **Access Methods**:
  - Bulk skip tracing service
  - Upload property lists and receive contact information
- **Pricing**: $0.03 per match (cell, landline, or email)
- **Relevance**: High - Provides contact information for property owners

### Accurate Append Skip Trace API
- **URL**: https://accurateappend.com/skip-tracing-api/
- **Coverage**: National
- **Data Types**:
  - Current addresses
  - Phone numbers
  - Email addresses
- **Access Methods**:
  - API integration
  - Batch processing
- **Relevance**: High - Provides API access for skip tracing integration

### Batch Skip Tracing
- **URL**: https://batchskiptracing.com/api
- **Coverage**: National
- **Data Types**:
  - Contact information
  - Property owner data
- **Access Methods**:
  - API solutions
  - Single and bulk skip tracing
- **Relevance**: High - Provides API access for skip tracing integration

### PropStream
- **URL**: https://www.propstream.com/skip-tracing
- **Coverage**: National
- **Data Types**:
  - Property owners' telephone numbers
  - Email addresses
- **Features**:
  - Free DNC (Do Not Call) scrubbing
  - No minimums
  - Instant access
- **Relevance**: High - Real estate-specific skip tracing service

### Tracerfy
- **URL**: https://tracerfy.com/skip-tracing-api
- **Coverage**: National
- **Data Types**:
  - Contact information
  - Property owner data
- **Access Methods**:
  - API access
  - Real estate lead generation
- **Relevance**: High - Specializes in real estate skip tracing

## Data Integration Considerations

1. **API Authentication and Access**:
   - Most APIs require authentication (API keys, OAuth, etc.)
   - Some services are invite-only or require partnerships
   - Budget considerations for paid APIs

2. **Data Normalization**:
   - Different data sources use different formats and standards
   - Need for data cleaning and normalization pipeline
   - RESO data dictionary standard for real estate data

3. **Geographic Coverage**:
   - Focus on Texas coverage for all data sources
   - Verify specific county/area coverage within Texas

4. **Update Frequency**:
   - Property data may be updated quarterly or annually
   - Utility rates may change seasonally
   - Need to implement regular data refresh mechanisms

5. **Data Privacy and Compliance**:
   - Handling of personal information (phone numbers, emails)
   - Compliance with regulations regarding contact information
   - DNC (Do Not Call) list compliance

## Recommended Data Sources for Implementation

1. **Property Data**: TaxNetUSA (Texas-specific coverage) or CoreLogic CLIP (national coverage)
2. **Utility Rates**: NREL Utility Rates API (geolocation-based) and ERCOT (Texas-specific)
3. **Property Characteristics**: Zillow MLS Listings API (if partnership available) or property tax records
4. **Roof Orientation**: Google Maps Platform Solar API (comprehensive solar data)
5. **Skip Tracing**: Datazapp (cost-effective) or Batch Skip Tracing API (for integration)
