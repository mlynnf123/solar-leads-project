/**
 * Dashboard JavaScript for Solar Lead Generation System
 * Handles UI interactions, chart rendering, and map visualization
 */

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize navigation
    initNavigation();
    
    // Initialize charts
    initCharts();
    
    // Initialize heat map
    initHeatMap();
    
    // Initialize range sliders
    initRangeSliders();
});

/**
 * Initialize navigation between different sections
 */
function initNavigation() {
    // Get all navigation links
    const dashboardLink = document.getElementById('dashboard-link');
    const leadsLink = document.getElementById('leads-link');
    const mapLink = document.getElementById('map-link');
    const importLink = document.getElementById('import-link');
    const settingsLink = document.getElementById('settings-link');
    
    // Get all content sections
    const dashboardContent = document.getElementById('dashboard-content');
    const leadsContent = document.getElementById('leads-content');
    const mapContent = document.getElementById('map-content');
    const importContent = document.getElementById('import-content');
    const settingsContent = document.getElementById('settings-content');
    
    // Add click event listeners to navigation links
    dashboardLink.addEventListener('click', function(e) {
        e.preventDefault();
        showContent(dashboardContent);
        setActiveLink(dashboardLink);
        document.querySelector('main h1').textContent = 'Dashboard';
    });
    
    leadsLink.addEventListener('click', function(e) {
        e.preventDefault();
        showContent(leadsContent);
        setActiveLink(leadsLink);
        document.querySelector('main h1').textContent = 'Lead Management';
    });
    
    mapLink.addEventListener('click', function(e) {
        e.preventDefault();
        showContent(mapContent);
        setActiveLink(mapLink);
        document.querySelector('main h1').textContent = 'Net Metering Heat Map';
        // Refresh map when shown to ensure proper rendering
        if (heatMap) {
            heatMap.invalidateSize();
        }
    });
    
    importLink.addEventListener('click', function(e) {
        e.preventDefault();
        showContent(importContent);
        setActiveLink(importLink);
        document.querySelector('main h1').textContent = 'Import Data';
    });
    
    settingsLink.addEventListener('click', function(e) {
        e.preventDefault();
        showContent(settingsContent);
        setActiveLink(settingsLink);
        document.querySelector('main h1').textContent = 'Settings';
    });
    
    // Add event listeners for lead detail buttons
    const viewButtons = document.querySelectorAll('.btn-outline-primary');
    viewButtons.forEach(button => {
        if (button.textContent.trim() === 'View') {
            button.addEventListener('click', function() {
                const leadDetailModal = new bootstrap.Modal(document.getElementById('leadDetailModal'));
                leadDetailModal.show();
                initLeadDetailCharts();
            });
        }
    });
}

/**
 * Show the selected content section and hide others
 */
function showContent(contentToShow) {
    // Get all content sections
    const contentSections = document.querySelectorAll('.content-section');
    
    // Hide all content sections
    contentSections.forEach(section => {
        section.classList.add('d-none');
    });
    
    // Show the selected content section
    contentToShow.classList.remove('d-none');
}

/**
 * Set the active navigation link
 */
function setActiveLink(activeLink) {
    // Get all navigation links
    const navLinks = document.querySelectorAll('#sidebar .nav-link');
    
    // Remove active class from all links
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to the selected link
    activeLink.classList.add('active');
}

/**
 * Initialize charts on the dashboard
 */
function initCharts() {
    // Lead Quality Distribution Chart
    const leadQualityCtx = document.getElementById('leadQualityChart').getContext('2d');
    const leadQualityChart = new Chart(leadQualityCtx, {
        type: 'pie',
        data: {
            labels: ['Excellent (80-100)', 'Good (65-79)', 'Average (50-64)', 'Poor (35-49)', 'Unsuitable (<35)'],
            datasets: [{
                data: [42, 86, 65, 32, 22],
                backgroundColor: [
                    '#28a745', // Green for excellent
                    '#17a2b8', // Teal for good
                    '#ffc107', // Yellow for average
                    '#fd7e14', // Orange for poor
                    '#dc3545'  // Red for unsuitable
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'Lead Quality Distribution'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} leads (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
    
    // Monthly Lead Acquisition Chart
    const leadAcquisitionCtx = document.getElementById('leadAcquisitionChart').getContext('2d');
    const leadAcquisitionChart = new Chart(leadAcquisitionCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                {
                    label: 'Total Leads',
                    data: [32, 45, 58, 75, 62, 47],
                    backgroundColor: 'rgba(13, 110, 253, 0.5)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Qualified Leads',
                    data: [18, 24, 32, 42, 35, 28],
                    backgroundColor: 'rgba(40, 167, 69, 0.5)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Leads'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Lead Acquisition'
                }
            }
        }
    });
}

/**
 * Initialize charts in the lead detail modal
 */
function initLeadDetailCharts() {
    // Monthly Bill Chart
    const monthlyBillCtx = document.getElementById('monthlyBillChart').getContext('2d');
    const monthlyBillChart = new Chart(monthlyBillCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Monthly Bill ($)',
                data: [210, 195, 185, 205, 240, 290, 345, 330, 275, 230, 205, 220],
                backgroundColor: 'rgba(255, 193, 7, 0.2)',
                borderColor: 'rgba(255, 193, 7, 1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Bill Amount ($)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Bill: $${context.raw}`;
                        }
                    }
                }
            }
        }
    });
    
    // Initialize property map in lead detail modal
    initPropertyMap();
}

/**
 * Initialize the heat map
 */
let heatMap = null;
function initHeatMap() {
    // Create map if the element exists
    const heatMapElement = document.getElementById('heatMap');
    if (heatMapElement) {
        // Initialize the map centered on Texas
        heatMap = L.map('heatMap').setView([31.0, -100.0], 6);
        
        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(heatMap);
        
        // Sample data for Texas cities with energy costs
        const heatData = [
            {lat: 30.2672, lng: -97.7431, value: 95, name: 'Austin'}, // Austin
            {lat: 29.7604, lng: -95.3698, value: 90, name: 'Houston'}, // Houston
            {lat: 32.7767, lng: -96.7970, value: 85, name: 'Dallas'}, // Dallas
            {lat: 29.4241, lng: -98.4936, value: 80, name: 'San Antonio'}, // San Antonio
            {lat: 31.7619, lng: -106.4850, value: 75, name: 'El Paso'}, // El Paso
            {lat: 32.7555, lng: -97.3308, value: 82, name: 'Fort Worth'}, // Fort Worth
            {lat: 30.6280, lng: -96.3344, value: 78, name: 'College Station'}, // College Station
            {lat: 33.9137, lng: -98.4934, value: 70, name: 'Wichita Falls'}, // Wichita Falls
            {lat: 27.8006, lng: -97.3964, value: 88, name: 'Corpus Christi'}, // Corpus Christi
            {lat: 31.5493, lng: -97.1467, value: 76, name: 'Waco'}, // Waco
            {lat: 32.4487, lng: -99.7331, value: 72, name: 'Abilene'}, // Abilene
            {lat: 33.5779, lng: -101.8552, value: 68, name: 'Lubbock'}, // Lubbock
            {lat: 26.2034, lng: -98.2300, value: 92, name: 'McAllen'}, // McAllen
            {lat: 32.4487, lng: -94.7677, value: 74, name: 'Longview'}, // Longview
            {lat: 30.0802, lng: -94.1266, value: 86, name: 'Beaumont'}, // Beaumont
            {lat: 35.2220, lng: -101.8313, value: 65, name: 'Amarillo'}, // Amarillo
            {lat: 28.8639, lng: -96.9819, value: 80, name: 'Victoria'}, // Victoria
            {lat: 31.1171, lng: -97.7278, value: 78, name: 'Killeen'}, // Killeen
            {lat: 29.9888, lng: -90.0414, value: 84, name: 'New Orleans'}, // New Orleans (for reference)
            {lat: 35.4676, lng: -97.5164, value: 70, name: 'Oklahoma City'} // Oklahoma City (for reference)
        ];
        
        // Create heat layer
        const heatPoints = heatData.map(point => [point.lat, point.lng, point.value / 100]);
        const heat = L.heatLayer(heatPoints, {
            radius: 25,
            blur: 15,
            maxZoom: 10,
            gradient: {
                0.4: 'blue',
                0.5: 'lime',
                0.6: 'yellow',
                0.7: 'orange',
                0.8: 'red'
            }
        }).addTo(heatMap);
        
        // Add markers with city names and values
        heatData.forEach(point => {
            const marker = L.marker([point.lat, point.lng]).addTo(heatMap);
            marker.bindPopup(`<b>${point.name}</b><br>Energy Cost Index: ${point.value}<br>Avg. Bill: $${Math.round(point.value * 2.5)}`);
        });
    }
}

/**
 * Initialize the property map in the lead detail modal
 */
function initPropertyMap() {
    // Create map if the element exists
    const propertyMapElement = document.getElementById('propertyMap');
    if (propertyMapElement) {
        // Initialize the map centered on the property (Austin for demo)
        const propertyMap = L.map('propertyMap').setView([30.2672, -97.7431], 16);
        
        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(propertyMap);
        
        // Add marker for the property
        const marker = L.marker([30.2672, -97.7431]).addTo(propertyMap);
        marker.bindPopup("<b>123 Main St</b><br>Austin, TX 78701<br><b>Lead Score:</b> 92").openPopup();
        
        // Add a circle to represent solar potential
        L.circle([30.2672, -97.7431], {
            color: '#28a745',
            fillColor: '#28a745',
            fillOpacity: 0.2,
            radius: 50
        }).addTo(propertyMap);
    }
}

/**
 * Initialize range sliders with value display
 */
function initRangeSliders() {
    // Score range slider
    const scoreRange = document.getElementById('scoreRange');
    const scoreValue = document.getElementById('scoreValue');
    if (scoreRange && scoreValue) {
        scoreRange.addEventListener('input', function() {
            scoreValue.textContent = this.value;
        });
    }
    
    // Bill weight slider
    const billWeight = document.getElementById('billWeight');
    const billWeightValue = document.getElementById('billWeightValue');
    if (billWeight && billWeightValue) {
        billWeight.addEventListener('input', function() {
            billWeightValue.textContent = this.value + '%';
        });
    }
    
    // Roof weight slider
    const roofWeight = document.getElementById('roofWeight');
    const roofWeightValue = document.getElementById('roofWeightValue');
    if (roofWeight && roofWeightValue) {
        roofWeight.addEventListener('input', function() {
            roofWeightValue.textContent = this.value + '%';
        });
    }
    
    // Property weight slider
    const propertyWeight = document.getElementById('propertyWeight');
    const propertyWeightValue = document.getElementById('propertyWeightValue');
    if (propertyWeight && propertyWeightValue) {
        propertyWeight.addEventListener('input', function() {
            propertyWeightValue.textContent = this.value + '%';
        });
    }
    
    // Metering weight slider
    const meteringWeight = document.getElementById('meteringWeight');
    const meteringWeightValue = document.getElementById('meteringWeightValue');
    if (meteringWeight && meteringWeightValue) {
        meteringWeight.addEventListener('input', function() {
            meteringWeightValue.textContent = this.value + '%';
        });
    }
    
    // Homeowner weight slider
    const homeownerWeight = document.getElementById('homeownerWeight');
    const homeownerWeightValue = document.getElementById('homeownerWeightValue');
    if (homeownerWeight && homeownerWeightValue) {
        homeownerWeight.addEventListener('input', function() {
            homeownerWeightValue.textContent = this.value + '%';
        });
    }
}

/**
 * Fetch and display lead data
 * This would normally connect to the backend API
 */
function fetchLeadData() {
    // This is a placeholder for actual API calls
    // In a real implementation, this would fetch data from the backend
    console.log('Fetching lead data...');
    
    // Simulate API call delay
    setTimeout(() => {
        console.log('Le
(Content truncated due to size limit. Use line ranges to read in chunks)