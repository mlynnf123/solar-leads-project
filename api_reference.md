# Solar Lead Generation System - API Reference

## Overview

This document provides detailed information about the APIs available in the Solar Lead Generation System. These APIs allow for programmatic access to the system's data and functionality, enabling integration with other systems and custom applications.

## Authentication

All API endpoints require authentication using an API key. The API key should be included in the request header as follows:

```
Authorization: Bearer YOUR_API_KEY
```

API keys can be generated and managed in the Settings section of the application.

## Base URL

All API endpoints are relative to the base URL:

```
https://api.solarleads.example.com/v1
```

## Response Format

All API responses are in JSON format and include the following standard fields:

- `success`: Boolean indicating whether the request was successful
- `data`: The response data (when success is true)
- `error`: Error details (when success is false)
- `meta`: Metadata about the response, such as pagination information

Example successful response:
```json
{
  "success": true,
  "data": {
    "lead_id": "LEAD-000123",
    "property_id": "PROP-000456",
    "lead_score": 85,
    "qualification": "excellent"
  },
  "meta": {
    "timestamp": "2025-04-11T23:16:56Z"
  }
}
```

Example error response:
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Lead with ID LEAD-999999 not found"
  },
  "meta": {
    "timestamp": "2025-04-11T23:16:56Z"
  }
}
```

## Rate Limiting

API requests are subject to rate limiting to ensure system stability. The current limits are:

- 100 requests per minute per API key
- 5,000 requests per day per API key

Rate limit information is included in the response headers:

- `X-RateLimit-Limit`: The maximum number of requests allowed per minute
- `X-RateLimit-Remaining`: The number of requests remaining in the current window
- `X-RateLimit-Reset`: The time at which the current rate limit window resets (Unix timestamp)

## Endpoints

### Lead Management API

#### GET /leads

Retrieves a list of leads based on the specified filters.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of leads to return (default: 50, max: 1000) |
| offset | integer | No | Starting position for pagination (default: 0) |
| sort_by | string | No | Field to sort by (default: "lead_score") |
| sort_order | string | No | Sort order: "asc" or "desc" (default: "desc") |
| min_score | integer | No | Minimum lead score (0-100) |
| max_score | integer | No | Maximum lead score (0-100) |
| qualification | string | No | Lead qualification category: "excellent", "good", "average", "poor", "unsuitable" |
| city | string | No | Filter by city |
| zip_code | string | No | Filter by ZIP code |
| utility_provider | string | No | Filter by utility provider |

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "lead_id": "LEAD-000123",
      "property_id": "PROP-000456",
      "address": "123 Main St, Austin, TX 78701",
      "lead_score": 85,
      "qualification": "excellent",
      "estimated_bill": 245.50,
      "created_date": "2025-04-01T12:00:00Z"
    },
    {
      "lead_id": "LEAD-000124",
      "property_id": "PROP-000457",
      "address": "456 Oak Ave, Houston, TX 77002",
      "lead_score": 78,
      "qualification": "good",
      "estimated_bill": 210.75,
      "created_date": "2025-04-02T14:30:00Z"
    }
  ],
  "meta": {
    "total": 247,
    "limit": 50,
    "offset": 0,
    "next_offset": 50
  }
}
```

#### GET /leads/{id}

Retrieves detailed information about a specific lead.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Lead ID |

**Response:**

```json
{
  "success": true,
  "data": {
    "lead_id": "LEAD-000123",
    "property_id": "PROP-000456",
    "lead_score": 85,
    "qualification": "excellent",
    "component_scores": {
      "bill_score": 90,
      "roof_score": 85,
      "property_score": 75,
      "metering_score": 95,
      "homeowner_score": 70
    },
    "property_data": {
      "address_line_1": "123 Main St",
      "city": "Austin",
      "state": "TX",
      "zip_code": "78701",
      "year_built": 1995,
      "square_footage": 2200,
      "bedrooms": 3,
      "bathrooms": 2,
      "property_type": "Single-Family",
      "is_owner_occupied": true,
      "property_value": 450000,
      "has_solar_permit": false,
      "last_sale_date": "2018-06-15"
    },
    "homeowner_data": {
      "first_name": "John",
      "last_name": "Smith",
      "phone": "(512) 555-1234",
      "email": "john.smith@example.com",
      "ownership_years": 7.2,
      "do_not_call": false
    },
    "roof_data": {
      "roof_type": "Asphalt Shingle",
      "roof_age": 8,
      "total_roof_area": 2500,
      "usable_roof_area": 1800,
      "primary_orientation": "S",
      "azimuth": 175,
      "pitch": 25,
      "shading_percentage": 12,
      "roof_condition": "good"
    },
    "utility_data": {
      "utility_provider": "Austin Energy",
      "residential": 0.1175,
      "estimated_monthly_bill": 245.50,
      "net_metering_available": true,
      "rate_plan": "Standard Residential"
    },
    "created_date": "2025-04-01T12:00:00Z",
    "last_updated": "2025-04-11T10:15:30Z",
    "status": "new",
    "notes": ""
  }
}
```

#### POST /leads/import

Imports leads from an external source.

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source | string | Yes | Data source name |
| file | file | Yes | CSV or JSON file containing lead data |
| options | object | No | Import options |

**Response:**

```json
{
  "success": true,
  "data": {
    "import_id": "IMPORT-000123",
    "total_records": 100,
    "imported_records": 95,
    "skipped_records": 5,
    "error_records": [
      {
        "row": 12,
        "reason": "Missing required field: address"
      },
      {
        "row": 45,
        "reason": "Invalid ZIP code format"
      }
    ],
    "status": "completed",
    "timestamp": "2025-04-11T23:16:56Z"
  }
}
```

#### GET /leads/export

Exports leads to a CSV or JSON file.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| format | string | No | Export format: "csv" or "json" (default: "csv") |
| fields | string | No | Comma-separated list of fields to include |
| filters | object | No | Same filters as GET /leads |

**Response:**

The response is a file download with the appropriate Content-Type header.

### Property API

#### GET /properties

Retrieves a list of properties based on the specified filters.

**Query Parameters:**

Similar to the leads API, with property-specific filters.

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "property_id": "PROP-000456",
      "address_line_1": "123 Main St",
      "city": "Austin",
      "state": "TX",
      "zip_code": "78701",
      "year_built": 1995,
      "square_footage": 2200,
      "property_type": "Single-Family",
      "is_owner_occupied": true
    },
    {
      "property_id": "PROP-000457",
      "address_line_1": "456 Oak Ave",
      "city": "Houston",
      "state": "TX",
      "zip_code": "77002",
      "year_built": 2002,
      "square_footage": 1850,
      "property_type": "Single-Family",
      "is_owner_occupied": true
    }
  ],
  "meta": {
    "total": 1245,
    "limit": 50,
    "offset": 0,
    "next_offset": 50
  }
}
```

#### GET /properties/{id}

Retrieves detailed information about a specific property.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Property ID |

**Response:**

```json
{
  "success": true,
  "data": {
    "property_id": "PROP-000456",
    "address_line_1": "123 Main St",
    "city": "Austin",
    "state": "TX",
    "zip_code": "78701",
    "latitude": 30.2672,
    "longitude": -97.7431,
    "year_built": 1995,
    "square_footage": 2200,
    "bedrooms": 3,
    "bathrooms": 2,
    "property_type": "Single-Family",
    "is_owner_occupied": true,
    "property_value": 450000,
    "has_solar_permit": false,
    "last_sale_date": "2018-06-15"
  }
}
```

#### POST /properties/search

Searches for properties based on specific criteria.

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| city | string | No | City name |
| zip_code | string | No | ZIP code |
| min_value | integer | No | Minimum property value |
| max_value | integer | No | Maximum property value |
| property_type | string | No | Type of property |
| min_square_footage | integer | No | Minimum square footage |
| max_square_footage | integer | No | Maximum square footage |
| min_year_built | integer | No | Minimum year built |
| max_year_built | integer | No | Maximum year built |

**Response:**

Similar to GET /properties

### Utility API

#### GET /utilities

Retrieves utility information for properties.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| property_id | string | No | Filter by property ID |
| utility_provider | string | No | Filter by utility provider |
| net_metering_available | boolean | No | Filter by net metering availability |

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "utility_id": 123,
      "property_id": "PROP-000456",
      "utility_provider": "Austin Energy",
      "residential": 0.1175,
      "estimated_monthly_bill": 245.50,
      "net_metering_available": true,
      "rate_plan": "Standard Residential"
    },
    {
      "utility_id": 124,
      "property_id": "PROP-000457",
      "utility_provider": "CenterPoint Energy",
      "residential": 0.1150,
      "estimated_monthly_bill": 210.75,
      "net_metering_available": true,
      "rate_plan": "Standard Residential"
    }
  ],
  "meta": {
    "total": 1245,
    "limit": 50,
    "offset": 0,
    "next_offset": 50
  }
}
```

#### GET /utilities/rates

Retrieves current utility rates by provider and region.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| provider | string | No | Filter by utility provider |
| city | string | No | Filter by city |
| zip_code | string | No | Filter by ZIP code |

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "provider": "Austin Energy",
      "region": "Austin",
      "residential": 0.1175,
      "commercial": 0.1050,
      "net_metering_available": true,
      "net_metering_rate": 0.1175,
      "last_updated": "2025-03-15T00:00:00Z"
    },
    {
      "provider": "CenterPoint Energy",
      "region": "Houston",
      "residential": 0.1150,
      "commercial": 0.1025,
      "net_metering_available": true,
      "net_metering_rate": 0.0950,
      "last_updated": "2025-03-15T00:00:00Z"
    }
  ],
  "meta": {
    "total": 5,
    "limit": 50,
    "offset": 0
  }
}
```

### Scoring API

#### POST /score

Scores a single lead based on provided data.

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| property_data | object | Yes | Property information |
| utility_data | object | No | Utility information |
| roof_data | object | No | Roof information |
| owner_data | object | No | Homeowner information |

**Response:**

```json
{
  "success": true,
  "data": {
    "property_id": "PROP-000456",
    "overall_score": 85,
    "qualification": "excellent",
    "component_scores": {
      "bill_score": 90,
      "roof_score": 85,
      "property_score": 75,
      "metering_score": 95,
      "homeowner_score": 70
    },
    "disqualified": false,
    "disqualification_reason": null,
    "timestamp": "2025-04-11T23:16:56Z"
  }
}
```

#### POST /score/batch

Scores multiple leads in a single request.

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| leads | array | Yes | Array of lead data objects |

**Response:**

```json
{
  "success": true,
  "data": {
    "results": [
      {
        "property_id": "PROP-000456",
        "overall_score": 85,
        "qualification": "excellent",
        "component_scores": {
          "bill_score": 90,
          "roof_score": 85,
          "property_score": 75,
          "metering_score": 95,
          "homeowner_score": 70
        }
      },
      {
        "property_id": "PROP-000457",
        "overall_score": 78,
        "qualification": "good",
        "component_scores": {
          "bill_score": 80,
          "roof_score": 75,
          "property_score": 85,
          "metering_score": 80,
          "homeowner_score": 65
        }
      }
    ],
    "analysis": {
      "count": 2,
      "mean": 81.5,
      "median": 81.5,
      "std_dev": 4.95,
      "min": 78,
      "max": 85,
      "distribution": {
        "excellent": {
          "count": 1,
          "percentage": 50.0
        },
        "good": {
          "count": 1,
          "percentage": 50.0
        },
        "average": {
          "count": 0,
          "percentage": 0.0
        },
        "poor": {
          "count": 0,
          "percentage": 0.0
        },
        "unsuitable": {
          "count": 0,
          "percentage": 0.0
        }
      },
      "qualification_rate": 100.0
    }
  }
}
```

### Map API

#### GET /map/heatmap

Retrieves data for the net metering heat map.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| region | string | No | Filter by region (e.g., "Austin", "Houston") |
| utility_provider | string | No | Filter by utility provider |
| min_score | integer | No | Minimum lead score (0-100) |
| max_score | integer | No | Maximum lead score (0-100) |
| min_bill | number | No | Minimum estimated monthly bill |
| max_bill | number | No | Maximum estimated monthly bill |

**Response:**

```json
{
  "success": true,
  "data": {
    "points": [
      {
        "lat": 30.2672,
        "lng": -97.7431,
        "value": 95,
        "name": "Austin",
        "avg_bill": 237.50
      },
      {
        "lat": 29.7604,
        "lng": -95.3698,
        "value": 90,
        "name": "Houston",
        "avg_bill": 225.00
      },
      {
        "lat": 32.7767,
        "lng": -96.7970,
        "value": 85,
        "name": "Dallas",
        "avg_bill": 212.50
      }
    ],
    "meta": {
      "min_value": 65,
      "max_value": 95,
      "avg_value": 82.5
    }
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| UNAUTHORIZED | Authentication failed or API key is invalid |
| FORBIDDEN | The authenticated user does not have permission to access the requested resource |
| NOT_FOUND | The requested resource was not found |
| BAD_REQUEST | The request was malformed or contained invalid parameters |
| VALIDATION_ERROR | The request data failed validation |
| RATE_LIMIT_EXCEEDED | The API rate limit has been exceeded |
| INTERNAL_ERROR | An internal server error occurred |

## Webhooks

The system can send webhook notifications for various events. Webhooks can be configured in the Settings section of the application.

### Available Events

| Event | Description |
|-------|-------------|
| lead.created | A new lead has been created |
| lead.updated | A lead has been updated |
| lead.scored | A lead has been scored |
| import.completed | A data import has completed |
| export.completed | A data export has completed |

### Webhook Payload

```json
{
  "event": "lead.created",
  "timestamp": "2025-04-11T23:16:56Z",
  "data": {
    "lead_id": "LEAD-000123",
    "property_id": "PROP-000456",
    "lead_score": 85,
    "qualification": "excellent"
  }
}
```

## SDK Libraries

The following SDK libraries are available for common programming languages:

- [JavaScript/Node.js](https://github.com/example/solarleads-js)
- [Python](https://github.com/example/solarleads-python)
- [PHP](https://github.com/example/solarleads-php)
- [Ruby](https://github.com/example/solarleads-ruby)
- [Java](https://github.com/example/solarleads-java)

## Support

For API support, please contact:

- Email: api-support@solarleads.example.com
- Documentation: https://docs.solarleads.example.com
- Status Page: https://status.solarleads.example.com
