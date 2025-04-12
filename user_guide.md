# Solar Lead Generation System - User Documentation

## Overview

The Solar Lead Generation System is a comprehensive platform designed to identify and qualify homeowners in Texas who would benefit most from solar energy installations. The system combines property data, utility information, roof characteristics, and homeowner details to score and prioritize potential leads based on their suitability for solar energy.

## Key Features

1. **Lead Qualification**: Automatically identifies qualified leads based on:
   - Owner-occupied single-family homes
   - Estimated electric bills exceeding $120/month
   - Suitable roof characteristics (orientation, size, condition)
   - No existing solar permits

2. **Skip Tracing + Data Enrichment**: Fills in missing contact information for property owners and enriches property data with relevant characteristics.

3. **Net Metering Heat Map**: Visual representation of areas with the highest energy costs and solar potential.

4. **Lead Scoring Algorithm**: Comprehensive scoring system that evaluates leads based on:
   - Bill size (30%)
   - Roof suitability (25%)
   - Property value (15%)
   - Net metering benefits (20%)
   - Homeowner characteristics (10%)

5. **Interactive Dashboard**: User-friendly interface for managing and analyzing leads.

## Getting Started

### System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- User account with appropriate permissions

### Accessing the System

1. Open your web browser and navigate to the system URL
2. Log in with your credentials
3. You will be directed to the main dashboard

## Using the Dashboard

### Main Dashboard

The main dashboard provides an overview of your lead generation efforts with:

- **Summary Cards**: Total leads, qualified leads, average bill size, and average lead score
- **Lead Quality Distribution**: Pie chart showing the distribution of leads by quality category
- **Monthly Lead Acquisition**: Bar chart showing lead acquisition trends over time

### Lead Management

The Lead Management section allows you to:

1. **View Leads**: Browse all leads in a sortable, filterable table
2. **Filter Leads**: Filter by score, location, bill size, and other criteria
3. **View Lead Details**: Click on a lead to view comprehensive information including:
   - Property details
   - Homeowner information
   - Roof analysis
   - Utility data
   - Lead score breakdown
4. **Export Leads**: Export lead data to CSV for use in other systems

### Net Metering Heat Map

The Heat Map visualization helps identify areas with the highest potential for solar energy adoption:

1. **View Map**: See color-coded regions based on energy costs and solar potential
2. **Filter Map**: Apply filters for region, utility provider, lead score, and bill size
3. **View Details**: Click on map markers to see city-specific information

### Data Import

The Data Import section allows you to:

1. **Upload CSV**: Import property data from CSV files
2. **Connect to APIs**: Configure connections to external data sources
3. **Schedule Imports**: Set up recurring data imports

### Settings

The Settings section allows you to configure:

1. **Lead Scoring Parameters**: Adjust weights for different scoring components
2. **API Connections**: Manage connections to external data sources
3. **User Preferences**: Customize your dashboard experience

## Lead Scoring Explained

The system scores leads on a scale of 0-100 based on multiple factors:

### Score Categories

- **Excellent (80-100)**: Highly qualified leads with optimal conditions for solar
- **Good (65-79)**: Strong candidates with favorable conditions
- **Average (50-64)**: Potential candidates that may need further evaluation
- **Poor (35-49)**: Less favorable candidates with significant limitations
- **Unsuitable (<35)**: Not recommended for solar installation

### Scoring Components

1. **Bill Size Score (30%)**
   - Based on estimated monthly electric bill
   - Minimum qualifying bill: $120/month
   - Higher bills receive higher scores

2. **Roof Suitability Score (25%)**
   - Based on orientation, usable area, shading, and condition
   - South-facing roofs with large usable areas score highest
   - Heavily shaded or poor condition roofs score lowest

3. **Property Value Score (15%)**
   - Based on property type, value, and ownership status
   - Owner-occupied single-family homes score highest
   - Properties with existing solar installations are disqualified

4. **Net Metering Score (20%)**
   - Based on utility provider's net metering policies and rates
   - Areas with favorable net metering policies score highest
   - Higher utility rates increase the score

5. **Homeowner Score (10%)**
   - Based on contact information availability and ownership length
   - Homeowners with complete contact information score highest
   - Longer ownership periods receive higher scores

## Best Practices

1. **Focus on Excellent and Good Leads**: These leads have the highest conversion potential.
2. **Use the Heat Map for Targeted Marketing**: Concentrate efforts in areas with higher energy costs.
3. **Regularly Import Fresh Data**: Keep your lead database current with regular imports.
4. **Adjust Scoring Parameters**: Fine-tune the scoring algorithm based on your conversion results.
5. **Export Qualified Leads**: Use the export feature to share leads with your sales team.

## Troubleshooting

### Common Issues

1. **Data Import Errors**
   - Ensure CSV files match the expected format
   - Check for missing required fields
   - Verify file encoding (UTF-8 recommended)

2. **Map Not Loading**
   - Check your internet connection
   - Clear browser cache
   - Ensure you have permission to access the map feature

3. **Lead Scoring Discrepancies**
   - Verify that all required data is available for the property
   - Check the scoring parameters in Settings
   - Ensure utility rate data is current

### Getting Help

For additional assistance:
- Check the FAQ section
- Contact system administrator
- Submit a support ticket through the Help menu

## API Reference

The system provides several APIs for integration with other systems:

### Lead API

- `GET /api/leads`: Retrieve all leads
- `GET /api/leads/{id}`: Retrieve a specific lead
- `POST /api/leads/import`: Import leads from external source
- `GET /api/leads/export`: Export leads to CSV

### Property API

- `GET /api/properties`: Retrieve all properties
- `GET /api/properties/{id}`: Retrieve a specific property
- `POST /api/properties/search`: Search properties by criteria

### Utility API

- `GET /api/utilities`: Retrieve utility information
- `GET /api/utilities/rates`: Retrieve current utility rates

### Scoring API

- `POST /api/score`: Score a single lead
- `POST /api/score/batch`: Score multiple leads

## Privacy and Data Security

The system handles sensitive homeowner information and follows these practices:

1. **Data Encryption**: All personal data is encrypted in transit and at rest
2. **Access Controls**: User permissions restrict access to sensitive information
3. **Data Retention**: Information is retained according to company policy
4. **Compliance**: The system adheres to relevant data protection regulations

## Glossary

- **Lead**: A potential customer for solar installation
- **Skip Tracing**: The process of finding contact information for property owners
- **Net Metering**: A billing mechanism that credits solar energy system owners for electricity they add to the grid
- **TDU**: Transmission and Distribution Utility
- **Usable Roof Area**: The portion of a roof suitable for solar panel installation
- **Azimuth**: The compass direction that a roof surface faces
- **Lead Score**: A numerical value representing the quality of a lead
