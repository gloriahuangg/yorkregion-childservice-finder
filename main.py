import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from shapely.geometry import Point
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import random

# Set page configuration to wide mode
st.set_page_config(layout="wide", page_title="York Region Child Service Locator")

# Add custom CSS for width control
st.markdown("""
    <style>
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# York Region cities and towns
YORK_REGION_CITIES = [
    "Aurora", "East Gwillimbury", "Georgina", "King", "Markham",
    "Newmarket", "Richmond Hill", "Vaughan", "Whitchurch-Stouffville",
    "Holland Landing", "Mount Albert", "Keswick", "Sutton", "Pefferlaw",
    "King City", "Nobleton", "Schomberg", "Thornhill", "Maple",
    "Woodbridge", "Concord", "Kleinburg", "Sharon", "Queensville",
    "Ballantrae", "Unionville"
]

USER_AGENT = "YorkChildService_locator/1.0 (gloria.tian.huang@gmail.com)"

@st.cache_data
def load_shapefile():
    """Load and cache the shapefile data"""
    try:
        shapefile_path = "shapefile/"
        return gpd.read_file(shapefile_path)
    except Exception as e:
        st.error(f"Error loading shapefile: {str(e)}")
        return None

def geocode_address_with_retry(address, max_retries=3, delay=1):
    geolocator = Nominatim(user_agent=USER_AGENT)
    
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            else:
                st.error(f"Address not found: {address}")
                return None
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
            else:
                st.error(f"Failed to geocode after {max_retries} attempts: {address}")
                return None

def create_map(gdf, location=None):
    """Create a map with shapefile data and optional address marker"""
    # Create a map centered on York Region or the specified location
    york_region_center = [44.0, -79.5]  # Approximate center of York Region
    m = folium.Map(
        location=york_region_center if location is None else location,
        zoom_start=10 if location is None else 13
    )
    
    # Add the shapefile data to the map
    if gdf is not None:
        # Convert GeoDataFrame to GeoJSON
        folium.GeoJson(
            gdf,
            style_function=lambda x: {
                'fillColor': 'blue',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.2
            },
            tooltip=folium.GeoJsonTooltip(
                fields=gdf.columns[:-1].tolist(),  # Exclude geometry column
                aliases=gdf.columns[:-1].tolist(),
                style="font-size: 12px;"
            )
        ).add_to(m)
    
    if location:
        # Add marker for the searched address
        folium.Marker(
            location=location,
            popup='Your Address',
            icon=folium.Icon(color='red', icon='home')
        ).add_to(m)
    
    return m

def main():
    st.title("York Region Children's Service Locator")
    
    # Load shapefile data
    gdf = load_shapefile()
    
    # Create two columns for input and map
    col1, col2 = st.columns([1, 2])
    
    # Left column - Input Form
    with col1:
        st.header("Your Home Address")
        
        # Input fields
        home_number_street_name = st.text_input("Home Number and Street Name:")
        city = st.selectbox("York Region City/Town", options=sorted(YORK_REGION_CITIES))
        
        # Display province (hardcoded)
        st.text("Province: ON")
        
        # Submit button
        submit = st.button("Show Location on Map")
        
        # Display shapefile attributes if available
        if gdf is not None:
            st.write("Available Service Areas:", len(gdf))
    
    # Right column - Map Display
    with col2:
        if submit and home_number_street_name:
            address = f"{home_number_street_name}, {city}, ON"
            location = geocode_address_with_retry(address)
            
            if location:
                st.success(f"Address found: {address}")
                # Create map centered on the address with shapefile
                m = create_map(gdf, location)
                # Display the map
                folium_static(m)
                
                # If point is within any service area, display the information
                if gdf is not None:
                    point = Point(location[::-1])  # Convert to (longitude, latitude)
                    point_gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")
                    
                    # Check for intersections with service areas
                    for idx, area in gdf.iterrows():
                        if point_gdf.geometry.iloc[0].within(area.geometry):
                            st.info("Your address is within this service area:")
                            st.write(area.drop('geometry'))
            else:
                # If geocoding failed, show default map
                st.warning("Showing default map of York Region")
                m = create_map(gdf)
                #folium_static(m)
                folium_static(m)
        else:
            # Show default map centered on York Region
            m = create_map(gdf)
            #folium_static(m)
            folium_static(m)

if __name__ == "__main__":
    main()