# York Region Children's Service Locator

## Overview
The York Region Children's Service Locator is a Streamlit web application that helps residents of York Region, Ontario locate Children's Services in their area. The application provides an interactive map interface where users can:
- Input their home address
- View their location on the map
- See service area boundaries
- Determine which service area their address falls within

## Prerequisites
- Python 3.11 (tested)
- Git (for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd york-region-child-service-locator
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install streamlit pandas geopandas folium streamlit-folium geopy shapely
```

## Project Structure
```
york-region-child-service-locator/
├── README.md
├── app.py
├── requirements.txt
└── shapefile/
    ├── [shapefile_name].shp
    ├── [shapefile_name].dbf
    ├── [shapefile_name].shx
    └── [other shapefile components]
```

## Configuration
1. Place your shapefile components in the `shapefile/` directory
2. Ensure the shapefile contains the necessary service area boundaries and attributes
3. Update the `USER_AGENT` string in the code with your contact information:
```python
USER_AGENT = "YourApp_Name/1.0 (your.email@example.com)"
```

## Running the Application

1. Navigate to the project directory:
```bash
cd york-region-child-service-locator
```

2. Start the Streamlit application:
```bash
streamlit run main.py
```

3. The application will open in your default web browser (typically at `http://localhost:8501`)

## Usage

1. **Enter Your Address**:
   - Type your street number and name in the "Home Number and Street Name" field
   - Select your city/town from the dropdown menu
   - The province is automatically set to Ontario

2. **View the Map**:
   - Click "Show Location on Map" to display your address
   - Your location will be marked with a red home icon
   - Service areas are shown in blue with black borders
   - Hover over service areas to view additional information

3. **Service Area Information**:
   - The application will show how many service areas are available
   - If your address falls within a service area, details will be displayed below the map
   - You can explore different areas by hovering over the map

## Features
- Interactive map interface
- Address geocoding with retry mechanism
- Service area boundary visualization
- Address validation for York Region municipalities
- Tooltips showing service area information
- Automatic map centering based on search
- Cached shapefile loading for better performance

## Supported Municipalities
The application supports addresses in the following York Region locations:
- Aurora
- East Gwillimbury
- Georgina
- King
- Markham
- Newmarket
- Richmond Hill
- Vaughan
- Whitchurch-Stouffville
- And various communities within these municipalities

## Troubleshooting

### Common Issues:
1. **Address Not Found**:
   - Ensure the address is correctly formatted
   - Verify the address exists within York Region
   - Try adding more specific address details

2. **Shapefile Loading Error**:
   - Verify all shapefile components are present in the `shapefile/` directory
   - Check file permissions
   - Ensure the shapefile is in a compatible format

3. **Map Display Issues**:
   - Clear your browser cache
   - Try a different web browser
   - Check your internet connection

## Development

### Adding New Features
1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request



