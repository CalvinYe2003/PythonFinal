''' Name:  Calvin Ye
CS230: Section 2
Data 3

Description:
The script loads data from a CSV file containing information about rest areas, including their names, locations, counties, cities, and facility amenities. It then provides different functionalities based on the selected page:

"Home": Displays a welcoming message along with an image of a rest area.
Comparing Locations": Allows users to compare post miles of selected rest areas.
"Map": Provides an interactive map for visualizing rest area locations.
"County & City": Enables users to explore rest areas based on county and city locations.
"Facilities": Allows users to filter rest areas based on the availability of RV stations and vending machines.

The code incorporates Streamlit's capabilities for creating user-friendly interfaces and visualizations, making it easy for users to explore and analyze California rest area data.
'''
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def load_data():
    data = pd.read_csv("RestArea.csv")
    return data

def compareLocations(data):
    st.header("Comparing Locations")
    selectLocations = st.multiselect("Select Locations", sorted(data['REST_AREA'].unique())) # ability to select multiple choices in a drop down
    if len(selectLocations) < 2: #Needs to choose more than two options so it can compare, if not there will be an error
        st.warning("Please select at least two locations.") 
    else:
        data_filtered = data[data['REST_AREA'].isin(selectLocations)]
        st.write(data_filtered)
        
    #Create a new figure and axis object
        fig, ax = plt.subplots() #ax adds multiple elements to your plot
        color = st.color_picker("Choose Graph Color:", '#9ed6f7')
        # Plot the filtered data
        ax.bar(data_filtered['REST_AREA'], data_filtered['POSTMILE'], color = color)
        
        # Set labels and title
        ax.set_xlabel("Rest Area")
        ax.set_ylabel("Post Mile")
        ax.set_title("Rest Areas based on their Post Mile")
        
        # Show plot in Streamlit
        st.pyplot(fig)

def showMap(data):
    show_map = st.checkbox("Click the button to Open Map", ["Open Map"])
    if show_map:
        st.title("Rest Area Map")
        locationName = st.multiselect("Select Locations", sorted(data['NAME'].unique())) #Choose one or multiple locations 
        filteredLocation = data[data['NAME'].isin(locationName)] 
        st.map(filteredLocation[['LATITUDE', 'LONGITUDE']])#outer bracket indexing the DataFrame and inner square bracket create a list containing what you selected
        for index, row in filteredLocation.iterrows(): #Print out the name, latitude, and longitude of the location you selcted
            st.write(row['NAME'], row['LATITUDE'], row['LONGITUDE'])

#County Rest Areas
def CountyAndCity(data):
    st.header("County Locations")
    selectCounties = st.multiselect("Select Counties", sorted(data['COUNTY'].unique()))
    if len(selectCounties) < 2:
        st.warning("Please select at least two counties.")
    else:
        countyFiltered = data[data['COUNTY'].isin(selectCounties)]
        st.write(countyFiltered)
    
        fig1, ax = plt.subplots()
        
        county_counts = countyFiltered['COUNTY'].value_counts()
        color = st.color_picker("Choose Graph Color:", '#9ed6f7')
        ax.bar(county_counts.index, county_counts.values, color = color) #index represents the category you are plotting, value is what you want to visualize which is the count
        ax.set_xlabel("County")
        ax.set_ylabel("Counts")
        ax.set_title("Number of Rest Area in that County") 
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(fig1)
    
    st.header("City Locations")
    selectCities = st.multiselect("Select Cities", sorted(data['CITY'].unique())) #unique extracts the values from CITY column from data, sort lines it up in alphabetical order
    if len(selectCities) < 2:
        st.warning("Please select at least two counties.")
    else:
        cityFiltered = data[data['CITY'].isin(selectCities)]
        st.write(cityFiltered)
    
        fig2, ax = plt.subplots()
        
        city_counts = cityFiltered['CITY'].value_counts()    
        ax.bar(city_counts.index, city_counts.values, color = color)
        ax.set_xlabel("City")
        ax.set_ylabel("Counts")
        ax.set_title("Number of Rest Areas in that City") 
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(fig2)

#Facilities
def filter_facilities(data):
    st.title("RV STATIONS")
    rvStations = st.radio("RV Stations:", ['Yes', 'No'])

    if rvStations == 'Yes':
        rvStationsAreas = data[data['RV_STATION']== 'Yes']
    else:
        rvStationsAreas = data[data['RV_STATION']== 'No']
    
    st.write("Filtered RV Stations:")
    st.write(rvStationsAreas)
    
    st.title("VENDING")
    vendingStations = st.radio("Vending Machines:", ['Yes', 'No']) #Radio gives you the choice to filter yes or no 
    
    if vendingStations == 'Yes':
        vendingStations = data[data['VENDING']== 'Yes']
    else:
        vendingStations = data[data['VENDING']== 'No']
    st.write("Filtered Vending: ")
    st.write(vendingStations)  #print out the filtered vending
    
def main():
    data = load_data()
    st.title("California Rest Area Data Analytics")
    page = st.sidebar.selectbox("Select Page", ["Home", "Comparing Locations", "Map","County & City", "Facilities"])#adds pages to the site
    
    st.sidebar.write("Would you like to rate this information?")
    st.sidebar.slider("Rate us from 1-10:", min_value = 0, max_value = 10)
    st.sidebar.text_input("Do you have any questions or comments?")
    submitButton = st.sidebar.button("Submit")
    
    if submitButton:
        st.sidebar.write("Thank you for your feedback!") #if the submit button is pressed then it will print out this
        
    
    if page == "Home":
        st.markdown("<h1 style='color: blue; font-size: 100px; text-align: center;'>Rest Area Information</h1>", unsafe_allow_html=True) #markdown allows css coding into streamlit
        st.markdown("<h2 style = 'text-align: center;'>Welcome to the Rest Area Information Website! This website consists of the traffic direction, county, and if they have an RV Station</h2>", unsafe_allow_html = True)
        st.markdown(f'<div style="display: flex; justify-content: center;">'
                    f'<img src="https://gr8traveltips.com/wp-content/uploads/2013/12/Mexico-2013-014-640x360.jpg" width="2000">'
                    f'</div>',unsafe_allow_html=True)

    elif page == "Comparing Locations":
        compareLocations(data)

    elif page == "Map":
        showMap(data)

    elif page == "County & City":
        CountyAndCity(data)

    elif page == "Facilities":
        filter_facilities(data) 

if __name__ == "__main__":
    main()

