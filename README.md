## Streamlit Application Link
[Explore the Streamlit App](https://environmentaljustice.streamlit.app/)

## Introduction
Hey! Over the past year, I've been involved in researching Environmental Justice Areas in North Carolina. My primary focus has been on replicating other state agencies' Environmental Justice Indexes, which calculate the extent of environmental injustice a geography faces, and implementing them for North Carolina. This application was inspired by two recent discoveries: firstly, a racial dot density/redlining website created by FiveThirtyEight, and secondly, a 36-indicator EJ index developed by the CDC. I've melded the two into this application!

The 36-Indicator Shapefile includes environmental, demographic, health, and social concerns, ranking every tract in the US from 0 - 1 based on their level of Environmental Injustice concern. In my app, I've focused exclusively on North Carolina; trying to do all of the US would involve a very large dataset and make the functionality of this app decrease.

The app displays two maps: the first showcases the racial dot density of a selected county alongside a level of Environmental Injustice. Users can choose an EJI Concern Level, which categorizes U.S. Census Tracts into quartiles based on that 36-indicator ranking:
Minor (0-0.25), Moderate (0.25-0.5), Major (0.5-0.75), and Severe (0.75-1). The second map displays the racial dot density distribution within whichever county selected. Below these maps are stacked bar charts that display the racial percentage compositions. I was interested to see the relationship between EJI Concern Levels and % Non-White Populations. As seen with many counties, as the EJI Concern Level increases so does the % minority.

## Data Sources

I utilized data from several different sources for this project:

1. **CDC Environmental Justice Index**: [CDC EJI](https://www.atsdr.cdc.gov/placeandhealth/eji/index.html)
   - This source provided the 36 different indicators and the overall concern level for each area.

2. **US Census TIGERLINE**:
   - I used this to obtain state, county, and census tract boundaries.

There wasn't too much data prep before throwing it into python. While in Python I spliced up some of the data only getting the important stuff such as in the Census_Tract shapefile only pulling North Carolina ones. 

## Future Work
Currently, the app is only for North Carolina counties. The application is focused only on North Carolina due to some challenges I encountered in loading the maps. My goal is to expand this to cover every county in the US. However, before I can do that, I need to find ways to speed up the process, especially considering the large volume of data involved. This optimization will be my primary focus in the next phase of development. I am also running into a problem with the map1 output; some of the county + ej combo's do not show the dot density mapping... not sure why have been messing around for the past day, but will continue to look at this for the future. 
