import sys
import subprocess
import re
#ALL CODE BELOW IS DONE THROUGH ITERATIONS WITH CHATGPT
import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import pycountry
import sys
import scipy
import time
import statsmodels.formula.api as smf


# Set page configuration
st.set_page_config(page_title="Wastrade", layout="wide")

#Colors
PRIMARY_COLOR = "#0A2342"    # Deep ocean blue
ACCENT_COLOR = "#4CAF50"     # Eco-green
SECONDARY_ACCENT = "#FF6B6B" # Coral
BACKGROUND_COLOR = "#F8F9FA" # Off-white
TEXT_COLOR = "#212529"       # Dark charcoal

# Replace lines 17-41 with this updated CSS block
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

/* Apply to all text */
* {{
    font-family: 'Space Grotesk', sans-serif !important;
}}

/* Specific header enhancements */
h1, h2, h3 {{
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
}}

/* Sidebar text */
.sidebar .stRadio label div {{
    font-weight: 600 !important;
    color: {ACCENT_COLOR} !important; /* Change sidebar text color to theme green */
}}

:root {{
    --font-primary: 'Space Grotesk', sans-serif;
    --primary-color: {PRIMARY_COLOR};
    --accent-color: {ACCENT_COLOR};
    --secondary-accent: {SECONDARY_ACCENT};
}}

/* Full page background color (updated variable) */
.css-18e3th9, .css-1d391kg, .main, .block-container {{
    background-color: {BACKGROUND_COLOR};
}}

/* Sidebar background in white (keep existing) */
.sidebar .sidebar-content {{
    background-color: white;
}}

/* Link styling (updated color) */
a {{
    color: {PRIMARY_COLOR};
    text-decoration: none;
}}

/* New Navigation Styles */
.st-emotion-cache-1kyxreq {{
    background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {ACCENT_COLOR} 100%)!important;
    border-radius: 8px!important;
    padding: 8px 12px!important;
    margin: 0 auto 24px!important;
    max-width: 1200px!important;
}}

.st-emotion-cache-1dgmtq3 {{
    font-family: var(--font-primary)!important;
    font-weight: 500!important;
    transition: all 0.2s ease!important;
    margin: 0 12px!important;
    color: white!important;
}}

.st-emotion-cache-r421ms {{
    background: {SECONDARY_ACCENT}!important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15)!important;
    border-radius: 6px!important;
}}

/* Enhanced Components */
.streamlit-expanderHeader {{
        background-color: #007BFF !important;
        color: white !important; /* Text color */
        border-radius: 8px !important; /* Rounded corners */
        padding: 12px 16px !important; /* Padding around the text */
        font-weight: 700 !important; /* Bold font weight */
        letter-spacing: -0.03em !important; /* Adjust letter spacing */
        font-size: 20px !important; /* Font size to match subheader */
    }}

.stMetric {{
    border: 1px solid {ACCENT_COLOR}55!important;
    border-radius: 12px;
    padding: 16px!important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

.stProgress > div > div {{
    background: {ACCENT_COLOR}!important;
}}

/* Typography Overrides */
body {{
    font-family: var(--font-primary)!important;
}}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    font-family: var(--font-primary)!important;
    color: {PRIMARY_COLOR}!important;
}}

.stMetricLabel {{
    font-family: var(--font-primary)!important;
    font-weight: 600!important;
    color: {PRIMARY_COLOR}!important;
}}

.st-emotion-cache-1v0mbdj {{
    font-family: var(--font-primary)!important;
}}

/* Replace existing border declarations with: */
div[data-testid="stExpander"] {{
    outline: none !important;
    box-shadow: none !important;
    border-style: none !important;
}}

/* Add this for sidebar expander specifically */
.sidebar .streamlit-expander {{
    background: {PRIMARY_COLOR}15 !important;
    border-radius: 12px !important;
    padding: 8px !important;
}}

/* Style for multiselect containers */
div[data-baseweb="select"] {{
    background: {PRIMARY_COLOR}15 !important; /* Light tint of primary color */
    border: none !important;
    border-radius: 12px !important;
    padding: 8px !important;
    box-shadow: none !important;
}}

/* Style for multiselect tags (selected options) */
span[data-baseweb="tag"] {{
    background-color: {ACCENT_COLOR} !important; /* Accent color for tags */
    color: white !important; /* White text for tags */
    border-radius: 8px !important;
    padding: 4px 8px !important;
}}

/* Adjust font size and alignment for multiselect dropdown */
div[data-baseweb="select"] > div {{
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px !important;
}}

/* Smooth transition for sidebar */
.sidebar .sidebar-content {{
    transition: all 0.3s ease-in-out !important;
}}

/* Fade-in animation for content */
.stApp {{
    animation: fadeIn 0.5s ease;
}}

@keyframes fadeIn {{
    from {{ opacity: 0.7; }}
    to {{ opacity: 1; }}
}}

/* Make the option_menu container full width */
    div[data-testid="stHorizontalBlock"] > div:first-child {{
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        border-radius: 0px !important;
    }}
    /* Optional: Remove border-radius for a flush look */
    .st-emotion-cache-1kyxreq {{
        border-radius: 0px !important;
    }}

/* Your existing CSS above... */

body, .stApp, .stMarkdown, #root, div {{
    color: {TEXT_COLOR} !important;
}}

.sidebar .streamlit-expanderHeader::before,
.sidebar .streamlit-expanderHeader svg,
.sidebar [data-testid="stExpander"] > details > summary::before {{
    font-size: 0px !important;
}}
.sidebar .streamlit-expanderHeader {{
    min-height: 0px !important;
    padding: 4px 8px !important;
}}


</style>
""", unsafe_allow_html=True)



# Horizontal Menu
from streamlit_option_menu import option_menu

# Horizontal Navigation Bar
horizontal_menu = option_menu(
    menu_title=None,
    options=["Introduction", "Maps", "The Project's Purpose", "About Me", "More Resources"],
    icons=["house", "map", "info-circle", "person-circle", "book"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "#e8f5e9"  # Light green background
        },
        "icon": {"color": "#5f8b55", "font-size": "20px"},
        "nav-link": {
            "font-size": "18px",
            "--hover-color": "#c8e6c9"  # Hover color for links
        },
        "nav-link-selected": {
            "background-color": f"{ACCENT_COLOR}",  # Use your defined accent color
            "color": "#FFFFFF"  # Text color for selected item
        }
    }
)


# Conditional Rendering Based on Selection
if horizontal_menu == "Introduction":
    st.title("Welcome to Wastrade")

    # Add the content sections

    # Introductory paragraph
    st.write(
        "*This website serves as a resource for exploring the complexities of the European Union’s waste export practices. It critically examines the mainstream narrative of the EU as a global leader in climate action and shows somewhat overlooked aspects of its waste management policies. It hopes to create a more nuanced discussion about environmental justice and sustainability.*"
    )
    st.markdown("---")

    st.subheader("The Other Side of the EU’s Green Story")
    st.write(
        "The European Union is often celebrated as a global leader in climate action. From regulations on plastics and automobiles to initiatives promoting green innovation, the EU positions itself as a global leader in environmental stewardship. While these actions are true, how this dominant narrative has shaped global perceptions casts the EU as the ultimate sustainability champion. However, having a singular lens is dangerous. Moreover, the lens through which the EU is viewed—that it takes climate change more seriously than other regions, such as the United States [1]—creates the false impression that the EU’s environmental practices are flawless and universally leading. This impression overlooks critical gaps in its policies and practices, particularly in waste management."
    )

    st.write(
        "Sweep your own doorstep before you sweep someone else's. Before the EU critiques others for their climate inaction, it should examine its own environmental practices critically. Is the EU analyzing the right data and metrics to estimate its true environmental performance? These questions become especially relevant when we focus on the EU’s handling of waste, specifically the export of waste to other regions."
    )

    with st.expander("A Question of Responsibility"):
        st.write(
            "A question to ask is if the EU is the global leader in climate and environment, why does it not process 100% of its waste? Instead of addressing waste fully within its borders, the EU ships some of it to other countries. It transfers the responsibility for disposal and recycling to regions less well-equipped to handle the burden than the EU is. This raises a critical question: "
            "if the EU claims climate leadership, why does it outsource the negative consequences of its consumption?"
        )

        st.markdown("### Waste as a Market Externality")

        st.write(
            "**Waste generation is an externality in most markets, as producing goods inevitably results in waste.** Some markets generate more waste than others. For example, the real estate market creates substantial waste during the construction of new buildings, much of which we still lack proper methods to dispose of [2]. Another example is food production, which generates significant waste due to plastic packaging. This particular issue has likely received more attention than any other form of waste generation since food packaging is the biggest plastic pollutant [3]. Neither consumers nor producers directly bear the costs of waste disposal. Instead, this burden often falls on municipalities [4]. **This classifies it as a negative externality of production.**"
        )

        st.write(
            "Examining waste creation as a market externality highlights challenges similar to those posed by other externalities. **One key issue with externalities is that different markets produce varying amounts of waste with differing impacts on the world [5].** For instance, we can agree that producing hazardous waste is objectively worse than producing non-hazardous waste when considering scale and consequences."
        )

        st.write(
            "**Waste treatment facilities themselves also create various negative externalities.** Landfills produce leachate (a significant environmental concern discussed here) and emit landfill gases like CO2 and CH4 [6]. Other waste management facilities, such as incinerators, also contribute to environmental externalities through air pollution. However, these facilities generate more than just environmental issues. **Property values decrease in areas near waste treatment facilities is another key issue discussed here.** This happens due to occurrences of odor, dust, wind-blown litter, or increased occurrences of animals such as seagulls near landfills [6]. Additionally, there are indirect factors that significantly contribute to property devaluation, such as the fear of negative health impacts and concerns about a reduced quality of life for those living nearby (which leads to a decreased demand for such property)."
        )

        col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths as needed
        with col2:
            st.image(
                "externalities02.png",
                caption="A picture demonstrating negative externalities of production, modeling the effect of waste production as a social cost.",
                width=400
            )

        st.write(
            "Given the cumulative negative externalities associated with waste and its treatment, waste trade becomes a layered issue. When waste is sold, the paying party (the one selling it) essentially pays for disposal at a market-determined price where demand and supply meet equilibrium (as seen in the picture). However, this price does not account for social costs like leachate management or property value loss. **These unaccounted-for costs (the externalities of waste management) are instead borne by surrounding communities and municipalities responsible for environmental cleanup.** Ideally, these costs should be borne by the payer (the seller), which is why many countries impose taxes on waste imports to mitigate these externalities. However, some costs remain uncovered, such as property devaluation and reduced quality of life for surrounding communities. That means these costs became burdens of already disadvantaged populations. Furthermore, corruption within the industry exacerbates this issue [7]; sometimes, the funds paid by the payer are not used to address social costs at all."
        )

        st.markdown("### Extended Producer Responsibility (EPR) and Remaining Challenges")

        st.write(
            "**From the EU’s side, Extended Producer Responsibility (EPR) policies are set to begin in 2025 to address these issues.** EPR shifts the financial and operational responsibility for waste disposal from municipalities to producers and aims to help meet EU recycling targets [8]. **This policy represents progress by redistributing responsibility, a step forward in terms of accountability as outlined in the Social Connectivity Model.** However, it does not directly regulate how waste is disposed of, but only who is responsible for it within EU borders. Without addressing disposal methods comprehensively, this policy risks inadvertently incentivizing waste exports, which could exacerbate existing inequalities."
        )

        st.markdown(
            "> The persistence of waste exports from the EU reflects an interplay of economic power dynamics, a 'Not In My Backyard' (NIMBY) mentality, and ongoing challenges in achieving safe and sustainable waste management. These systemic issues demand solutions that go beyond simple redistribution of responsibility."
        )

    st.subheader("Waste as a Commodity")
    st.write(
        "To understand the complexities of EU waste management, this project investigates the trade of waste by material types, including plastic, metal, and hazardous waste. Metal waste is further categorized into ferrous and non-ferrous, while hazardous waste is classified by treatment type, such as recovery, disposal, or unspecified processes. Using Eurostat data, these classifications help illuminate the distinct handling requirements and responsibilities associated with each waste type."
    )

    st.write(
        "This analysis prioritizes key variables to identify broader trends, revealing the unequal distribution of responsibility in global waste flows. By tracking specific waste streams, the project highlights the systemic inequities exported along with the materials themselves."
    )

    st.subheader("Mapping the Unknown")
    st.write(
        "Global waste trade operates through complex and often not transparent networks. Waste exports frequently go through multiple countries, making it difficult to know their ultimate destinations and fates. For instance, Malaysia is commonly reported as a destination for U.S. waste, yet evidence shows it also receives waste originating in China and Indonesia [9]. Given that Indonesia imports waste from the EU, it is unclear whether this waste is processed locally or further exported to countries like Malaysia. These convoluted pathways make it nearly impossible to ascertain where the waste ends up or how it is handled."
    )

    st.subheader("The Waste-Income Paradox")
    st.write(
        "There is a strong positive correlation between a country’s income level and its waste generation per capita[10] as seen in the graph below."
    )
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths as needed
    with col2:
        st.image(
            "income_waste04.png",
            caption="Figure from Kaza et al. (2018) describing waste generation per capita aggregated based on country’s GDP per capita",
            width=400
        )
    st.write("Higher-income countries produce more waste per capita but also have better waste collection systems and higher rates of recycling and incineration (controlled incineration). In contrast, upper-middle-income countries rely heavily on landfills, while lower-middle-income and low-income countries often depend on open dumping."
    )

    st.write(
        "This disparity highlights a paradox: Despite having the infrastructure to manage their waste, high-income countries export significant portions to lower-income countries, where infrastructure is often inadequate. This practice not only shifts the burden of waste management but also amplifies environmental risks in regions less equipped to handle them."
    )

    st.subheader("Moving Forward")
    st.write(
        "The story of the EU’s climate leadership is far more complex than the mainstream narrative suggests. By critically examining its waste management practices, we uncover contradictions that demand attention. This is not just an exploration of data—it’s a call to question assumptions, address imbalances, and reimagine what true environmental leadership looks like in a deeply interconnected world."
    )

    # Divider for references
    st.markdown("---")
    # Add references
    st.markdown(
        """
        <h4 style="font-size: 16px;">References</h4>
        <p style="font-size: 12px;">
        1. Rosenthal, E. (2009). What Makes Europe Greener than the U.S.? Yale E360. Retrieved from 
        <a href="https://e360.yale.edu/features/what_makes_europe_greener_than_the_us">https://e360.yale.edu/features/what_makes_europe_greener_than_the_us</a>
        </p>
        <p style="font-size: 12px;">
        2. Ragossnig AM. Construction and demolition waste – Major challenges ahead! Waste Management & Research. 2020;38(4):345-346. 
        <a href="https://journals.sagepub.com/doi/full/10.1177/0734242X20910309">https://journals.sagepub.com/doi/full/10.1177/0734242X20910309</a>
        </p>
        <p style="font-size: 12px;">
        3. Ncube, L. K., Ude, A. U., Ogunmuyiwa, E. N., Zulkifli, R., & Beas, I. N. (2020). Environmental Impact of Food Packaging Materials: A Review of Contemporary Development from Conventional Plastics to Polylactic Acid Based Materials. Materials (Basel, Switzerland), 13(21), 4994. 
        <a href="https://doi.org/10.3390/ma13214994">https://doi.org/10.3390/ma13214994</a>
        </p>
        <p style="font-size: 12px;">
        4. Bishop, A. (2017). Examining waste as an economic externality. Discard Studies: Social Studies of Waste, Pollution & Externalities. Retrieved from 
        <a href="https://discardstudies.com/2017/10/30/examining-waste-as-an-economic-externality/">https://discardstudies.com/2017/10/30/examining-waste-as-an-economic-externality/</a>
        </p>
        <p style="font-size: 12px;">
        5. Frischmann, B. M., & Ramello, G. B. (2023). Externalities, scarcity, and abundance. Frontiers in research metrics and analytics, 7, 1111446. 
        <a href="https://doi.org/10.3389/frma.2022.1111446">https://doi.org/10.3389/frma.2022.1111446</a>
        </p>
        <p style="font-size: 12px;">
        6. Eshet, T., Ayalon, O., & Shechter, M. (2006). Valuation of externalities of selected waste management alternatives: A comparative review and analysis. Resources, Conservation and Recycling, 46(4), 335–364. 
        <a href="https://doi.org/10.1016/j.resconrec.2005.08.004">https://doi.org/10.1016/j.resconrec.2005.08.004</a>
        </p>
        <p style="font-size: 12px;">
        7. DW Planet A. (2021, December 24). Your plastic waste might be traded by criminals [Video]. 
        <a href="https://www.youtube.com/watch?v=tID-AChSg7o">https://www.youtube.com/watch?v=tID-AChSg7o</a>
        </p>
        <p style="font-size: 12px;">
        8. Europen. (2024). Extended producer responsibility. The European Organization for Packaging and the Environment. Retrieved from 
        <a href="https://www.europen-packaging.eu/policy-area/extended-producer-responsibility/">https://www.europen-packaging.eu/policy-area/extended-producer-responsibility/</a>
        </p>
        <p style="font-size: 12px;">
        9. Latiff, R. (2024). Malaysia opens anti-dumping duty probe on plastic imports from China, Indonesia. Reuters. Retrieved from 
        <a href="https://www.reuters.com/sustainability/malaysia-opens-anti-dumping-duty-probe-plastic-imports-china-indonesia-2024-08-09/">https://www.reuters.com/sustainability/malaysia-opens-anti-dumping-duty-probe-plastic-imports-china-indonesia-2024-08-09/</a>
        </p>
        <p style="font-size: 12px;">
        10. Kaza, S., Yao, L. C., Bhada Tata, P., & Van Woerden, F. (2018). What a Waste 2.0: A Global Snapshot of Solid Waste Management to 2050. World Bank Group. Retrieved from 
        <a href="http://documents.worldbank.org/curated/en/697271544470229584/What-a-Waste-2-0-A-Global-Snapshot-of-Solid-Waste-Management-to-2050">http://documents.worldbank.org/curated/en/697271544470229584/What-a-Waste-2-0-A-Global-Snapshot-of-Solid-Waste-Management-to-2050</a>
        </p>
        """,
        unsafe_allow_html=True
    )
elif horizontal_menu == "Maps":
    # Sidebar for Maps Navigation
    with st.spinner("Loading map view..."):
         time.sleep(0.5)  # Short delay for visual transition
    st.sidebar.title("Map Navigation")
    
    page = st.sidebar.selectbox(
        "Select waste category",
        ["General", "Plastic", "Metal", "Hazardous Waste"],
        index=0,
        key="waste_category"
    )



    # Load shapefile for world map
    shapefile_path = r'110m_cultural/ne_110m_admin_0_countries.shp' #File from Natural Earth » 1:110m Cultural Vectors—Free vector and raster map data at 1:10m, 1:50m, and 1:110m scales. (n.d.).
                                                                    #from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/


    # Main Content
    if page == "General":
        st.title("General Export")
        st.header("Export Map Overview")
        st.write("Explore what data says on EU's waste export.")
        st.info(
            "This interactive map shows the amounts of waste exported from the EU to specific countries with shading based on amount."
            "\n\n*Feel free to adjust the selections on the side to explore different years, material types, and export reasons.*"
        )

            # Load datasets
        all_data = pd.read_csv("data03.csv")
        country_codes = pd.read_csv("countries_codes_and_coordinates.csv", encoding="latin1") #File from Artur. (n.d.). ISO 3166 Countries with Regional Codes [CSV file].
                                                                                              #Retrieved December 12, 2024, from https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv

        # Merge the Alpha-3 codes directly into the plastic dataset
        all_data = all_data.merge(
            country_codes[['Country', 'Alpha-3 code']],
            left_on='partner',
            right_on='Country',
            how='left'
        )

        # Drop the redundant 'Country' column from the merge
        all_data.drop(columns=['Country'], inplace=True)

        # Save or display the updated dataset
        #all_data.to_csv("data03_with_alpha3.csv", index=False)
        #print("Updated file saved as 'data03_with_alpha3.csv'")

        # Sidebar to choose the year
        st.sidebar.title("Select Year")
        year = st.sidebar.slider(
            "Year",
            min_value=int(all_data['TIME_PERIOD'].min()),
            max_value=int(all_data['TIME_PERIOD'].max()),
            value=int(all_data['TIME_PERIOD'].max()),  # Default to max year
        )

        # Filter data for the selected year
        filtered_data = all_data[all_data['TIME_PERIOD'] == year]
        
        # Load shapefile for world map
        world = gpd.read_file(shapefile_path)
        
        # Merge with the country export data on Alpha-3 codes
        world['SOV_A3'] = world['SOV_A3'].replace('CH1', 'CHN')
        world['SOV_A3'] = world['SOV_A3'].replace('KA1', 'KAZ')
        world['SOV_A3'] = world['SOV_A3'].replace('US1', 'USA')
        world['SOV_A3'] = world['SOV_A3'].replace('AU1', 'AUS')
        world = world.merge(filtered_data, how='left', left_on='SOV_A3', right_on='Alpha-3 code')
        world['OBS_VALUE'].fillna(0, inplace=True)
        # Get the maximum OBS_VALUE for scaling
        max_obs_value = world['OBS_VALUE'].max()

        # Define a function to determine the color based on OBS_VALUE
        def get_custom_shade(obs_value, max_value):
            if obs_value == 0:
                return [150, 150, 150]  # Gray for zero
            elif obs_value / max_value < 0.1:
                return [173, 216, 230]  # Light blue
            elif obs_value / max_value < 0.2:
                return [135, 206, 235]  # Sky blue
            elif obs_value / max_value < 0.3:
                return [100, 149, 237]  # Cornflower blue
            elif obs_value / max_value < 0.4:
                return [65, 105, 225]  # Royal blue
            elif obs_value / max_value < 0.5:
                return [30, 144, 255]  # Dodger blue
            elif obs_value / max_value < 0.6:
                return [0, 191, 255]  # Deep sky blue
            elif obs_value / max_value < 0.7:
                return [0, 0, 255]  # Blue
            elif obs_value / max_value < 0.8:
                return [0, 0, 205]  # Medium blue
            elif obs_value / max_value < 0.9:
                return [0, 0, 139]  # Dark blue
            else:
                return [0, 0, 100]  # Navy

        # Apply the function to create the `fill_color` column
        world['fill_color'] = world['OBS_VALUE'].apply(lambda x: get_custom_shade(x, max_obs_value))
        # Add a formatted OBS_VALUE column for tooltip
        world['formatted_OBS_VALUE'] = world['OBS_VALUE'].apply(lambda x: f"{x:,.0f}")
        # Update your tooltip to include this information
        tooltip_html = """
        <b>{SOV_A3}</b>: {formatted_OBS_VALUE} tonnes/year
        """
        # Set up the Pydeck layer with precomputed colors
        layer = pdk.Layer(
            "GeoJsonLayer",
            world.__geo_interface__,
            pickable=True,
            opacity=0.8,               # Increase opacity to make colors more visible
            stroked=True,
            filled=True,
            get_fill_color="properties.fill_color",  # Use the precomputed color
            get_line_color=[255, 255, 255],  # Border color in white
            auto_highlight=False         # Disable auto-highlight to keep colors consistent
            )
        # View configuration
        view_state = pdk.ViewState(latitude=10, longitude=20, zoom=1)
        #Display map with enhanced tooltip
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": tooltip_html,
                "style": {
                    "backgroundColor": "aliceblue",
                    "color": "white",
                    "maxWidth": "300px",
                    "padding": "10px"
                }
            },
            map_style="light"
        )
        with st.spinner("Generating export visualization..."):
            st.pydeck_chart(r, use_container_width=True)
        st.write(
                    "Data Source:"
                    "Eurostat. (2024). *Trade in waste by type of material and partner* [Online data set]. DOI: "
                    "[10.2908/env_wastrdmp](https://doi.org/10.2908/env_wastrdmp)"
                )
         # Add custom country information box here
         # Create a selectbox below the map for more information about specific countries
        selected_country = st.selectbox(
            "Countries importing EU's waste the most:",
            ["Select a country for more information:", "Turkey", "India"],
            index=0
        )

         # Display additional information based on selection
        if selected_country == "Turkey":
            st.subheader("About Turkey")
            st.write("Turkey is the largest recipient of EU waste exports, importing approximately 12 million tonnes of total waste from the EU in 2023. The country is particularly prominent in steel scrap imports. However, Turkey struggles with proper waste management, with studies showing that imported plastic waste often ends up in illegal dumpsites or is openly burned, releasing toxic chemicals.")
            st.info("*Did you know?* A 2022 Greenpeace study documented irreversible environmental damage in Adana, Turkey, where dangerous chemicals and heavy metals from plastic waste imported from the UK and Germany were detected at levels thousands of times higher than in uncontaminated soil, posing significant risks to soil, water sources, and the food chain in the region.")
        elif selected_country == "India":
            st.subheader("About India")
            st.write("India has become a major destination for EU waste exports, especially following China's 2018 waste import ban. The country faces significant challenges in waste management infrastructure, with much of the imported waste ending up in informal recycling.")
            st.info("*Did you know?* India followed the Basel Convention in 2016, making all imports of waste for disposal illegal and introducing stricter documentation requirements for recycling and recovery.")
        
        # Divider for visual separation
        st.markdown("---")

        # Add the content sections
        st.subheader("The EU's Role in the Global Waste Trade")
        st.write(
            "The European Union is a major player in the global waste trade. While much of the EU's waste trade occurs internally, "
            "the region continues to export large volumes of waste outside its borders, making it one of the largest global waste exporters. "
            "Moreover, while the EU mostly imports waste from other high-income countries, it exports mostly to middle-income to low-income ones. "
            "However, the trends in these exports have shifted notably in recent years, particularly following China's 2018 ban on the import of "
            "plastic waste, which disrupted established trade routes."
        )

        st.subheader("Shifting Destinations Post-2018")
        st.write(
            "In 2016, the EU exported substantial volumes of waste to China—almost as much as it currently exports to Turkey, its largest "
            "waste destination. India, by contrast, received far less EU waste before 2018 than it does today. Despite the policy changes, "
            "the total volume of EU waste exports has not decreased; rather, it has continued to grow, with destinations shifting toward "
            "countries like Turkey and India."
        )

        st.subheader("Practical Implications of Waste Redirection")
        st.write(
            "Practical trends inferred from maps and trade data indicate clear increases in waste exports to Turkey and India. These shifts "
            "highlight the need to examine the implications of growing exports to specific regions, even if the changes cannot be attributed "
            "solely to the ban. Importantly, the overall trend reflects a steady increase in waste exports outside the EU, raising questions "
            "about the EU's ability to manage its waste domestically."
        )

        st.subheader("Ethical and Environmental Concerns")
        st.write(
            "This persistent reliance on external markets for waste disposal is particularly concerning given the limited infrastructure in many "
            "recipient countries. For instance, in South Asia, 75% of waste disposal occurs via open dumping [1], which "
            "poses significant environmental and health risks. These dynamics highlight the ethical and environmental challenges of the EU's "
            "waste trade practices, particularly as waste continues to flow to regions less equipped to handle it sustainably. Such trends "
            "emphasize the importance of critically evaluating the EU's role in global waste management and the broader implications for "
            "environmental equity."
        )

        # Divider for references
        st.markdown("---")

        # Add references
        st.markdown(
            """
            <h4 style="font-size: 16px;">References</h4>
            <p style="font-size: 12px;">
            1. Kaza, Silpa; Yao, Lisa Congyuan; Bhada Tata, Perinaz; Van Woerden, Frank; Martin, Thierry Michel Rene; Serrona, Kevin Roy B.; Thakur, Ritu; Pop, Flaviu; Hayashi, Shiko; Solorzano, Gustavo; Alencastro Larios, Nadya Selene; Poveda, Renan Alberto; Ismail, Anis. What a Waste 2.0 : A Global Snapshot of Solid Waste Management to 2050 (English). Urban Development Series Washington, D.C.: World Bank Group. 
            <a href="http://documents.worldbank.org/curated/en/697271544470229584/What-a-Waste-2-0-A-Global-Snapshot-of-Solid-Waste-Management-to-2050">http://documents.worldbank.org/curated/en/697271544470229584/What-a-Waste-2-0-A-Global-Snapshot-of-Solid-Waste-Management-to-2050</a>
            </p>
            """,
            unsafe_allow_html=True
        )

    elif page == "Plastic":
        st.title("Plastic")
        st.write("Explore the definition and nuances of plastic waste")
        st.info(
            "This interactive map shows the amounts of plastic waste exported from the EU to specific countries. "
            "\n\n*Feel free to adjust the selections on the side to explore different years, material types, and export reasons.*"
        )
            # Load datasets
        plastic_data = pd.read_csv("plastic01.csv")
        country_codes = pd.read_csv("countries_codes_and_coordinates.csv", encoding="latin1")

        # Merge the Alpha-3 codes directly into the plastic dataset
        plastic_data = plastic_data.merge(
            country_codes[['Country', 'Alpha-3 code']],
            left_on='partner',
            right_on='Country',
            how='left'
        )

        # Drop the redundant 'Country' column from the merge
        plastic_data.drop(columns=['Country'], inplace=True)

        # Save or display the updated dataset
        #plastic_data.to_csv("plastic01_with_alpha3.csv", index=False)
        #print("Updated file saved as 'plastic01_with_alpha3.csv'")

        # Sidebar to choose the year
        st.sidebar.title("Select Year")
        year = st.sidebar.slider(
            "Year",
            min_value=int(plastic_data['TIME_PERIOD'].min()),
            max_value=int(plastic_data['TIME_PERIOD'].max()),
            value=int(plastic_data['TIME_PERIOD'].max()),  # Default to max year
        )

        # Filter data for the selected year
        filtered_data = plastic_data[plastic_data['TIME_PERIOD'] == year]

           # Merge the filtered data with the world shapefile using SOV_A3 (shapefile) and Alpha-3 code (filtered_data)
        world_copy = gpd.read_file(shapefile_path)
        world_copy['SOV_A3'] = world_copy['SOV_A3'].replace('CH1', 'CHN')
        world_copy['SOV_A3'] = world_copy['SOV_A3'].replace('KA1', 'KAZ')
        world_copy['SOV_A3'] = world_copy['SOV_A3'].replace('US1', 'USA')
        world_copy['SOV_A3'] = world_copy['SOV_A3'].replace('AU1', 'AUS')
        world_copy = world_copy.merge(
            filtered_data, how='left', left_on='SOV_A3', right_on='Alpha-3 code'
        )

        # Fill missing values in AMOUNT
        if 'AMOUNT' in world_copy.columns:
            world_copy['AMOUNT'].fillna(0, inplace=True)
        else:
            st.error("'OBS_VALUE' column is missing after the merge.")
            st.stop()


        # Define the color gradient
        max_obs_value = world_copy['AMOUNT'].max()

        def get_custom_shade(obs_value, max_value):
            if obs_value == 0:
                return [150, 150, 150]  # Gray for zero
            elif obs_value / max_value < 0.1:
                return [173, 216, 230]  # Light blue
            elif obs_value / max_value < 0.2:
                return [135, 206, 235]  # Sky blue
            elif obs_value / max_value < 0.3:
                return [100, 149, 237]  # Cornflower blue
            elif obs_value / max_value < 0.4:
                return [65, 105, 225]  # Royal blue
            elif obs_value / max_value < 0.5:
                return [30, 144, 255]  # Dodger blue
            elif obs_value / max_value < 0.6:
                return [0, 191, 255]  # Deep sky blue
            elif obs_value / max_value < 0.7:
                return [0, 0, 255]  # Blue
            elif obs_value / max_value < 0.8:
                return [0, 0, 205]  # Medium blue
            elif obs_value / max_value < 0.9:
                return [0, 0, 139]  # Dark blue
            else:
                return [0, 0, 100]  # Navy

        # Apply the function to create the `fill_color` column
        world_copy['fill_color'] = world_copy['AMOUNT'].apply(lambda x: get_custom_shade(x, max_obs_value))
        # Add a formatted OBS_VALUE column for tooltip
        world_copy['formatted_OBS_VALUE'] = world_copy['AMOUNT'].apply(lambda x: f"{x:,.0f}")

        # Set up the Pydeck layer with precomputed colors
        layer = pdk.Layer(
            "GeoJsonLayer",
            world_copy.__geo_interface__,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            get_fill_color="properties.fill_color",  # Use the precomputed color
            get_line_color=[255, 255, 255],  # Border color in white
            auto_highlight=False,  # Disable auto-highlight to keep colors consistent
        )

        # View configuration
        view_state = pdk.ViewState(latitude=10, longitude=20, zoom=1)

        # Display map with light style background
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
            "html": "<b>{SOV_A3}</b>: {formatted_OBS_VALUE} tonnes/year",
            "style": {
                "backgroundColor": "aliceblue",
                "color": "white"
            }},
            map_style="light"  # Set map background to light style
        )
        with st.spinner("Generating export visualization..."):
            st.pydeck_chart(r, use_container_width=True)
            
        st.write(
            "Data Source:"
            "Eurostat. (2024). *Trade in waste by type of material and partner* [Online data set]. DOI: "
            "[10.2908/env_wastrdmp](https://doi.org/10.2908/env_wastrdmp)"
        )
        
        # Divider for visual separation
        st.markdown("---")

        # Add the content sections
        st.subheader("Global Plastic Production and Its Challenges")
        st.write(
            "Plastic production has skyrocketed since the mid-20th century, thanks to its affordability, durability, and versatility [1][2]. "
            "This rapid growth has created significant problems in waste management, with recycling often viewed as the go-to solution. "
            "However, in reality, recycling faces a series of structural and market-based challenges that highlight its limitations—and the negative externalities tied to global plastic production."
        )

        st.write(
            "One major issue is how households interact with recycling systems. Improper recycling and contamination of collected plastics often make the materials unusable [2]. "
            "Adding to the problem, many plastics labeled as recyclable aren't actually recyclable, further confusing and hurting the process [3]. "
            "Considerably though, the challenges don't stop with consumers; they extend into the economics of recycling itself."
        )

        st.write(
            "Recycled plastics are considered an inferior good compared to virgin plastics. Since the two are substitutes, market demand for recycled materials fluctuates with the price of virgin plastics, "
            "which is tightly linked to oil prices [2]. When oil prices are low, virgin plastics become cheaper, and demand for recycled materials drops. This volatility undermines the "
            "recycling industry's financial viability, leaving it at the mercy of global markets rather than environmental imperatives."
        )

        st.subheader("The EU's Plastic Waste Exports and Their Consequences")
        st.write(
            "The European Union presents itself as a global leader in sustainability, but its heavy reliance on exporting plastic waste tells a different story. "
            "Turkey is currently the largest recipient of EU plastic waste exports [4]. While plastic isn't the most frequently exported material overall, "
            "it's the one that sparks the most debate due to its environmental impact and visibility in public discourse. An estimated 6 billion tonnes of plastic waste now sit "
            "in landfills or the environment globally [1], making plastic a focal point of discussions around waste management. This context challenges Europe's self-image as a recycling role model, "
            "raising questions about who really pays for its waste."
        )

        st.write(
            "The export of plastic waste to countries like Turkey shifts the negative externalities associated with plastic consumption and disposal. These externalities—such as the environmental and health impacts of "
            "improper waste management—are transferred to recipient countries. In Turkey, much of the imported plastic waste ends up in illegal dumpsites or is openly burned, releasing toxic chemicals linked to cancers, "
            "respiratory illnesses, and disruptions to endocrine and immune systems. Beyond health impacts, the environmental consequences are severe: contaminated soil, air, and water threaten agricultural safety and ecosystems. "
            "Even after partial cleanups, hazardous residues remain, posing long-term risks [5]."
        )

        st.subheader("Plastic Pollution's Economic Costs")
        st.write(
            "The impact of plastic waste isn't confined to landfills and dumpsites. Marine plastic pollution alone costs the global economy up to $2.5 trillion annually [1]. "
            "These costs reflect the cascading externalities of plastic mismanagement—economic burdens borne not by producers but by the global community. By exporting waste to regions with inadequate infrastructure, "
            "high-income countries like those in the EU shift these costs onto lower-income nations, perpetuating environmental and economic inequalities."
        )

        st.subheader("The Netherlands: A 'Green' Contradiction")
        st.write(
            "The Netherlands, often praised for its sustainability and eco-conscious policies, is a prime example of the contradictions in global plastic waste management. "
            "Despite its reputation as a 'green' country, it is among the largest exporters of plastic waste in the EU—and globally."
        )

        st.write(
            "Research estimates that 4,300 to 21,200 tonnes of Dutch plastic waste end up in the environment annually, primarily due to mismanagement in recipient countries [6]. "
            "This reflects systemic issues in low-income nations, where weak infrastructure exacerbates environmental degradation and public health risks [7]. "
            "The Netherlands' significant role in global plastic pollution raises uncomfortable questions about the true cost of its green reputation and the responsibility of high-income countries in addressing the consequences of their waste exports."
        )

        st.subheader("Conclusion")
        st.write(
            "The global plastic waste crisis exposes the flaws and inequalities in current waste management systems. High-income countries, including the EU, continue to externalize the environmental and social costs of their plastic waste by exporting it to regions ill-equipped to manage it. "
            "This practice undermines their sustainability narratives and furthers global environmental injustices. Addressing these challenges demands more than incremental changes to recycling systems—it requires a fundamental rethinking of global plastic production, consumption, and accountability."
        )
        with st.expander("Why is this an ethics concern?"):
            # Introduction
            st.write("""
            If we look at the full issue through the lens of **Iris Young's Social Connection Model (SCM)**, the negative consequences of waste export become an example of *structural injustice*: some people bear the consequences of an issue created by many intertwined choices and incentives. Since everyone creates waste, everyone in the EU shares responsibility for both the situation and its improvement—there is no single entity to blame, but rather a web of actors whose decisions collectively lead to harmful outcomes.
            """)

            # Highlighted Quote
            st.markdown("""
            > *"There is no one entity doing the harm but rather a series of choices of various actors that lead to the outcome."*
            """)

            # Incentives and Responsibility Section
            st.markdown("### Incentives and Responsibility")

            st.write("""
            Young argues that injustice persists because the system provides incentives at every step. For the EU’s waste export, the **main incentive is cost**: it’s cheaper to dispose of waste abroad than domestically. Companies often operate in legal gray zones, exporting waste to countries with fewer regulations and paying local firms to dispose of it. These companies claim they are simply following market incentives. As a result, consumers are shielded from the consequences of their consumption, and products remain cheaper due to lower disposal costs.

            This perspective shifts the focus from *blame* to *shared responsibility*. However, a common criticism of SCM is that it leaves unclear exactly how responsibility should be distributed or what concrete actions individuals or companies should take. In practice, meaningful change requires **incentives for all actors**—companies and individuals alike—to choose actions that combat, rather than perpetuate, systemic problems.
            """)

            # Collective Action and Incentives Section
            st.markdown("### The Role of Collective Action and Incentives")

            st.write("""
            Young emphasizes the need for **collective action**—such as campaigning and lobbying for better regulations—to create more effective incentives (like laws or tax breaks). Yet, even well-intentioned incentives can be misused, and corruption remains a risk in the sector.
            """)

            # Highlighted Quote
            st.markdown("""
            > *"Sometimes incentives can be misused and do not guarantee a roadblock to the easier path."*
            """)

            # Economic Externalities and Inequality Section
            st.markdown("### Economic Externalities and Inequality")

            st.write("""
            Research shows that **housing values can drop by 5.5–12.9%** depending on proximity to a landfill. When landfills are sited in lower-income regions or countries, this perpetuates economic inequality by devaluing local property. The “not-in-my-backyard” logic that protects wealthier communities simply shifts the burden elsewhere, making property devaluation and other negative externalities someone else’s problem.
            """)

            # Highlighted Quote
            st.markdown("""
            > *"The property devaluation happens elsewhere. It is yet another negative externality of the waste market that will happen somewhere."*
            """)

            st.write("""
            Communities with more socio-economic power can direct waste disposal costs away from themselves, deepening disparities both locally and globally. These **power imbalances** reinforce the SCM framework’s relevance: they show how structural injustice is perpetuated by the ability of some to avoid costs at the expense of others.
            """)

            # What Can Be Done Section
            st.markdown("### What Can Be Done?")

            st.write(
                "The key question is: What can we do about it? As with any structural injustice, the answer is far from straightforward. For one, regulations already exist and are set to be strengthened. However, as discussed, they often fail to fully address the problem, especially when waste trade has largely shifted into legal gray zones or outright illegal practices. Stronger enforcement is necessary, but just as important is a cultural shift in how waste trade is perceived."
            )

            st.markdown(
                "> **This is precisely what the Social Connection Model argues:** the entire system bears responsibility because everyone treats it as if it’s not their problem. The goal is to change this mindset—not to simply push for waste disposal elsewhere but to advocate for disposal methods that do no harm."
            )

            st.write(
                "A key step is improving **corporate accountability**, ensuring that recyclables are correctly labeled and that producers take financial responsibility for their products’ end-of-life disposal. The broader aim is to establish a system of incentives that prevents every actor, at every stage, from defaulting to the easiest, most harmful option. **Individuals** play a crucial role in pushing for these changes—both in regulations and in the incentive structures that shape decision-making."
            )

            # Final Highlighted Quote
            st.markdown("""
            > *"The entire system bears responsibility because everyone treats it as if it's not their problem. The goal is to change this mindset—not to simply push for waste disposal elsewhere but to advocate for disposal methods that do no harm."*
            """)

        # Divider for references
        st.markdown("---")

        # Add references
        st.markdown(
            """
            <h4 style="font-size: 16px;">References</h4>
            <p style="font-size: 12px;">
            1. Environmental Investigation Agency. (2021). <em>The truth behind trash: The scale and impact of the international trade in plastic waste</em>. 
            <a href="https://eia-international.org/wp-content/uploads/The-Truth-Behind-Trash-FINAL.pdf">https://eia-international.org/wp-content/uploads/The-Truth-Behind-Trash-FINAL.pdf</a>
            </p>
            <p style="font-size: 12px;">
            2. Walt, V., & Meyer, S. (2020, March 16). Plastic that travels 8,000 miles: The global crisis in recycling. <em>Pulitzer Center</em>. 
            <a href="https://pulitzercenter.org/stories/plastic-travels-8000-miles-global-crisis-recycling">https://pulitzercenter.org/stories/plastic-travels-8000-miles-global-crisis-recycling</a>
            </p>
            <p style="font-size: 12px;">
            3. DW Planet A. (2021, December 24). Your plastic waste might be traded by criminals [Video]. YouTube. 
            <a href="https://www.youtube.com/watch?v=tID-AChSg7o">https://www.youtube.com/watch?v=tID-AChSg7o</a>
            </p>
            <p style="font-size: 12px;">
            4. Ritchie, H. (2022). <em>Ocean plastics: How much do rich countries contribute by shipping their waste overseas?</em> Our World in Data. 
            <a href="https://ourworldindata.org/plastic-waste-trade">https://ourworldindata.org/plastic-waste-trade</a>
            </p>
            <p style="font-size: 12px;">
            5. Greenpeace Mediterranean. (2022). <em>Game of Waste: Irreversible Impact</em>. 
            <a href="https://act.gp/game-of-waste-report">https://act.gp/game-of-waste-report</a>
            </p>
            <p style="font-size: 12px;">
            6. Lobelle, D., Shen, L., van Huet, B., van Emmerik, T., Kaandorp, M., Iattoni, G., Baldé, C. P., Lavender Law, K., & van Sebille, E. (2024). Knowns and unknowns of plastic waste flows in the Netherlands. <em>Waste Management & Research, 42</em>(1), 27–40. 
            <a href="https://doi.org/10.1177/0734242X231180863">https://doi.org/10.1177/0734242X231180863</a>
            </p>
            <p style="font-size: 12px;">
            7. Ferronato, N., & Torretta, V. (2019). Waste mismanagement in developing countries: A review of global issues. <em>International Journal of Environmental Research and Public Health, 16</em>(6), 1060. 
            <a href="https://doi.org/10.3390/ijerph16061060">https://doi.org/10.3390/ijerph16061060</a>
            </p>
            <p style="font-size: 12px;">
            8. Young, I. M. (2006). Responsibility and Global Justice: A Social Connection Model. Social Philosophy and Policy, 23(1), 102–130. 
            <a href="https://doi.org/10.1017/S0265052506060043">https://doi.org/10.1017/S0265052506060043</a>
            </p>
            <p style="font-size: 12px;">
            9. Danthurebandara, M., Van Passel, S., Nelen, D., Tielemans, Y., & Van Acker, K. (2013). Environmental and socio-economic impacts of landfills. Linnaeus ECO-TECH 2012, Kalmar, Sweden. 
            <a href="https://www.researchgate.net/publication/278738702">https://www.researchgate.net/publication/278738702</a>
            </p>
            """,
            unsafe_allow_html=True
        )

    elif page == "Metal":
        st.title("Metal")
        st.write("Explore the definition and nuances of metal waste")
        st.info(
            "This interactive map shows the amounts of metal waste exported from the EU to specific countries. "
            "\n\n*Feel free to adjust the selections on the side to explore different years, material types, and export reasons.*"
        )
            # Load datasets
        metal_data = pd.read_csv("metal01.csv")
        country_codes = pd.read_csv("countries_codes_and_coordinates.csv", encoding="latin1")

        # Merge the Alpha-3 codes directly into the plastic dataset
        metal_data = metal_data.merge(
            country_codes[['Country', 'Alpha-3 code']],
            left_on='partner',
            right_on='Country',
            how='left'
        )

        # Drop the redundant 'Country' column from the merge
        metal_data.drop(columns=['Country'], inplace=True)

        # Save or display the updated dataset
        #metal_data.to_csv("metal01_with_alpha3.csv", index=False)
        #print("Updated file saved as 'metal01_with_alpha3.csv'")

        # Sidebar to choose the year
        st.sidebar.title("Select Year")
        year = st.sidebar.slider(
            "Year",
            min_value=int(metal_data['TIME_PERIOD'].min()),
            max_value=int(metal_data['TIME_PERIOD'].max()),
            value=int(metal_data['TIME_PERIOD'].max()),  # Default to max year
        )

        # Sidebar checklist to filter raw material
        rawmat_options = ["Metal - ferrous", "Metal - non ferrous"]
        selected_rawmat = st.sidebar.multiselect(
        "Select Material Type",
        options=rawmat_options,
        default=rawmat_options  # Default to show both
        )
        
        # Filter data for the selected year and raw material
        filtered_data = metal_data[
        (metal_data['TIME_PERIOD'] == year) & 
        (metal_data['rawmat'].isin(selected_rawmat))
        ]


           # Merge the filtered data with the world shapefile using SOV_A3 (shapefile) and Alpha-3 code (filtered_data)
        world_copy01 = gpd.read_file(shapefile_path)
        world_copy01['SOV_A3'] = world_copy01['SOV_A3'].replace('CH1', 'CHN')
        world_copy01['SOV_A3'] = world_copy01['SOV_A3'].replace('KA1', 'KAZ')
        world_copy01['SOV_A3'] = world_copy01['SOV_A3'].replace('US1', 'USA')
        world_copy01['SOV_A3'] = world_copy01['SOV_A3'].replace('AU1', 'AUS')
        world_copy01 = world_copy01.merge(
            filtered_data, how='left', left_on='SOV_A3', right_on='Alpha-3 code'
        )

        # Fill missing values in OBS_VALUE
        if 'OBS_VALUE' in world_copy01.columns:
            world_copy01['OBS_VALUE'].fillna(0, inplace=True)
        else:
            st.error("'OBS_VALUE' column is missing after the merge")
            st.write(filtered_data.head())
            st.stop()
        


        # Define the color gradient
        max_obs_value = world_copy01['OBS_VALUE'].max()

        def get_custom_shade(obs_value, max_value):
            if obs_value == 0:
                return [150, 150, 150]  # Gray for zero
            elif obs_value / max_value < 0.1:
                return [173, 216, 230]  # Light blue
            elif obs_value / max_value < 0.2:
                return [135, 206, 235]  # Sky blue
            elif obs_value / max_value < 0.3:
                return [100, 149, 237]  # Cornflower blue
            elif obs_value / max_value < 0.4:
                return [65, 105, 225]  # Royal blue
            elif obs_value / max_value < 0.5:
                return [30, 144, 255]  # Dodger blue
            elif obs_value / max_value < 0.6:
                return [0, 191, 255]  # Deep sky blue
            elif obs_value / max_value < 0.7:
                return [0, 0, 255]  # Blue
            elif obs_value / max_value < 0.8:
                return [0, 0, 205]  # Medium blue
            elif obs_value / max_value < 0.9:
                return [0, 0, 139]  # Dark blue
            else:
                return [0, 0, 100]  # Navy

        # Apply the function to create the `fill_color` column
        world_copy01['fill_color'] = world_copy01['OBS_VALUE'].apply(lambda x: get_custom_shade(x, max_obs_value))
        # Add a formatted OBS_VALUE column for tooltip
        world_copy01['formatted_OBS_VALUE'] = world_copy01['OBS_VALUE'].apply(lambda x: f"{x:,.0f}")

        # Set up the Pydeck layer with precomputed colors
        layer = pdk.Layer(
            "GeoJsonLayer",
            world_copy01.__geo_interface__,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            get_fill_color="properties.fill_color",  # Use the precomputed color
            get_line_color=[255, 255, 255],  # Border color in white
            auto_highlight=False,  # Disable auto-highlight to keep colors consistent
        )

        # View configuration
        view_state = pdk.ViewState(latitude=10, longitude=20, zoom=1)

        # Display map with light style background
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
            "html": "<b>{SOV_A3}</b>: {formatted_OBS_VALUE} tonnes/year",
            "style": {
                "backgroundColor": "aliceblue",
                "color": "white"
            }},
            map_style="light"  # Set map background to light style
        )
        with st.spinner("Generating export visualization..."):
            st.pydeck_chart(r, use_container_width=True)
            
        st.write(
            "Data Source:"
            "Eurostat. (2024). *Trade in waste by type of material and partner* [Online data set]. DOI: "
            "[10.2908/env_wastrdmp](https://doi.org/10.2908/env_wastrdmp)"
        )
        
        # Divider for visual separation
        st.markdown("---")

        # Add the content sections
        st.subheader("Overview of Metal Recycling")
        st.write(
            """
        The global trade in recycled plastic is widely discussed and often viewed critically. In contrast, the trade in recycled metal receives far less attention, making it harder to draw direct parallels between the two. While plastic and metal are fundamentally different materials with distinct properties and markets, the market for recycled metal is presently seen as having more potential. However, this optimism echoes the early enthusiasm surrounding recycled plastic as a solution to reduce reliance on virgin plastic [1]. One might wonder whether the recycled metal market will follow a similar trajectory, initially perceived as a cost-effective and sustainable alternative, only to reveal inefficiencies and unforeseen challenges, such as the influence of substitutes and negative externalities.
            """
        )

        st.subheader("Ferrous vs. Non-Ferrous Metals")
        st.info(
            """
        *Did you know?*
        Metals are generally divided into two groups: ferrous and non-ferrous metals.
        1. Ferrous metals are usually magnetic, stronger, more durable, and more susceptible to corrosion. Some examples include: steel, cast iron, wrought iron.
        2. Non-ferrous materials are non-magnetic, highly conductive, resistant to corrosion, and more lightweight. Examples include aluminum, copper, zinc, bronze, and lead.""")

        st.write("""Ferrous metals, while cheaper and easier to recycle, are less durable and more prone to corrosion compared to non-ferrous metals. They are also considered less harmful to the environment. Understanding the balance between these two types of metals is crucial in the context of the global metal waste trade. Including data on the occurrence and trade patterns of ferrous versus non-ferrous metals would help shed light on their respective roles in this market.
            """
        )

        st.subheader("The Promise and Challenges of Recycled Metal")
        st.write(
            """
        Recycled metal holds promise for addressing environmental concerns and material shortages, but a more balanced and integrated market is necessary for its success. The current market is not yet very international[2]. However, proposals for easier international metal recycling raise questions about whether lower-income countries can handle the volumes of metal waste exported by developed countries.

        Countries like China and Japan have implemented mandates requiring recycled content in products, which encourage higher domestic recycling rates.[3] While the assumption that stronger policies directly boost recycling rates is debatable (due to all the issues with the recycling market and the constraints of its impact), such initiatives undeniably create momentum for recycling.
            """
        )

        st.subheader("The Growing Role of Steel Scrap")
        st.write(
            """
        Steel scrap is an increasingly significant material in global steel production, with the European Union (EU) maintaining an important role as both an importer and exporter. In 2021, the trade in steel scrap—including exchanges within the EU—reached 109.6 million tonnes, reflecting a 9.7% increase from the previous year. This growth highlights the expanding use of recycled steel in the EU and its integration into global markets [4].
            """
        )

        st.subheader("EU's Role in Steel Scrap Trade")
        st.write(
            """
        The EU's trade patterns demonstrate a dual involvement in steel scrap markets. On the import side, the EU sources steel scrap predominantly from the United Kingdom, Switzerland, and the United States. In 2021, EU imports rose significantly, totaling 5.36 million tonnes—a 31.1% increase compared to 2020. The UK increased its exports to the EU by 26.8%, while exports from the United States more than doubled, rising by 107.1%. These figures illustrate the trade relationships that supply steel scrap to the EU [4].

        On the export side, the EU continues to send large volumes of steel scrap to other countries, with Turkey being the largest recipient. In 2021, Turkey imported nearly 25 million tonnes of steel scrap, much of it from EU [4]. Other significant EU export destinations include Egypt and Switzerland, reflecting that the EU has strong waste export ties.
            """
        )

        st.subheader("Trade Complexity and Interdependence")
        st.write(
            """
        This dual role as both importer and exporter underscores the EU’s interconnected position in the global steel scrap market. However, the difference between who are EU’s importers and who are its exporters yet again shows that the flow of material is more significant in one direction. That direction is from higher-income countries to middle-income countries to lower-income countries. The trade happens also vice versa but not in comparable numbers.
            """
        )

        st.subheader("Need for Regulatory Frameworks")
        st.write(
            """
        The idea of a potential sustainable metal re-creation from recycling done in an international setting—and hence traded so it is done as efficiently as possible (that is why trade exists)—is nice but rather utopic. The impacts of mismanaged metal waste will be huge. The odds for proper regulation are quite low. Given that we know the consequences of current and past waste trade, we might want to pause and think whether this is the best course forward.
            """
        )
        with st.expander("Want to know more about past, current, and future policies and their effectiveness?"):
            # Info box for context or TLDR
            st.success("**TLDR:** The EU is banning all waste exports from 2026 and 2027. However, exports for disposal to non-EFTA and non-EU countries have technically been banned since 2006. That means, in theory, any exports to places like Turkey or India should have been strictly for recovery or treatment.")

            # Main narrative as regular text
            st.write("""
            Back in 2006, the EU introduced Regulation (EC) No 1013/2006 [5], which prohibited hazardous waste exports to non-EU and non-EFTA countries. This same regulation also banned exports to these countries for disposal (i.e., landfilling or incineration). In theory, only waste meant for material recovery or treatment was allowed. But as we know from available data, that has not been the reality—plenty of exported waste still ended up in landfills. That is especially concerning given that waste exports for recovery or recycling were supposed to be heavily documented and require permits, a process that was further tightened in 2014. India followed suit in 2016, banning all imports of waste for disposal and introducing stricter documentation and permit requirements for recycling and recovery.
            """)

            # Highlight key quotes or skeptical points (Medium-style)
            st.markdown("""
            But as we know from available data, that has not been the reality—plenty of exported waste still ended up in landfills.

            On paper, this sounds promising, especially since it forces EU member states to actively track and monitor waste trade to curb illegal exports. But let us stay skeptical.
            """)
            # Use st.success or st.warning for regulatory milestones or caveats
            st.success("**Key Milestones:**\n\n- **May 2026:** All waste trade within the EU must be documented digitally to improve transparency.\n- **November 2026:** Non-hazardous plastic waste exports to non-OECD countries banned for 2.5 years.\n- **May 2027:** Even non-hazardous waste exports to non-OECD countries face new restrictions—recipient countries must explicitly approve and prove proper management.")

            st.warning("**Caveat:** The biggest issue with this new regulation is that waste exports are still allowed under certain conditions. Given the history of weak enforcement, does this just leave the door open for waste to keep flowing under a different label?")

            # More narrative
            st.write("""
            One major shift, however, is the increased power given to OLAF (European Anti-Fraud Office). Until now, OLAF could only track and assist national authorities—like those in the Netherlands or Germany—in their investigations into illegal waste trade. However, it did not have the authority to launch its own investigations.
            """)

            st.markdown("""
                        With Regulation (EU) 2024/1157, that changes. OLAF now has the power to independently investigate waste shipments not just entering, exiting, or transiting through the EU, but also those occurring entirely within EU member states.
            """)

            # Use st.error for alarming statistics or negative outcomes
            st.warning("**Illegal trade is rampant:** According to the EU’s own estimates, between 15% and 30% of waste shipments might be illegal. These shipments are far more likely to end up in landfills or open dumps [9].")

            st.write("""
            The problem of high-income countries exporting waste to lower-income ones—where it is often dumped improperly—has been a known issue for decades. That is why the Basel Convention came into force in 1992, banning all hazardous waste exports from OECD to non-OECD countries as of 2019 [10]. The goal was to stop wealthier nations from offloading toxic waste onto lower-income countries, where it creates disproportionate environmental and public health consequences.
            """)

            st.markdown("""
            The issue is not the lack of rules—it is the lack of enforcement. Maybe if all waste trade was banned, hazardous waste exports would stop altogether, and illegal trade would be easier to detect and prevent.
            """)

            st.write("""
            Given everything we know about the costs and consequences, the real question is: If we cannot regulate waste trade in a way that does not disproportionately harm lower-income countries, should we allow it at all?
            """)
 

        # Divider for footnotes
        st.markdown("---")

        # Add footnotes
        st.markdown(
            """
            <h4 style="font-size: 16px;">References</h4>
            <p style="font-size: 12px;">
            1. DW Planet A. (2021, December 24). Your plastic waste might be traded by criminals [Video]. YouTube. 
            <a href="https://www.youtube.com/watch?v=tID-AChSg7o">https://www.youtube.com/watch?v=tID-AChSg7o</a>
            </p>
            <p style="font-size: 12px;">
            2. Pickens N., Kettle J., Why recycling metal is an opportunity too good to waste. (2024, April 22). 
            <a href="https://www.weforum.org/stories/2024/04/why-recycling-metal-is-an-opportunity-too-good-to-waste/">World Economic Forum</a>.
            </p>
            <p style="font-size: 12px;">
            3. Ltd, C. M. I. P. (2024, November 26). Scrap Metal Recycling Market Trends, Size, Share & Analysis 2031. 
            <a href="https://www.coherentmarketinsights.com/industry-reports/scrap-metal-recycling-market">Coherent Market Insights</a>.
            </p>
            <p style="font-size: 12px;">
            4. Bureau of International Recycling (BIR). (2022). World steel recycling in figures 2017–2021: Steel scrap – 
            A raw material for green steelmaking (13th edition). Brussels, Belgium: BIR.
            </p>
            <p style="font-size: 12px;">
            5. European Parliament and Council. (2006, July 12). Regulation (EC) No 1013/2006 of the European Parliament and of the Council of 14 June 2006 on shipments of waste. Official Journal of the European Union, L 190, 1–98. 
            <a href="http://data.europa.eu/eli/reg/2006/1013/oj">http://data.europa.eu/eli/reg/2006/1013/oj</a>
            </p>
            <p style="font-size: 12px;">
            6. European Parliament and Council. (2024, April 30). Regulation (EU) 2024/1157 of the European Parliament and of the Council of 11 April 2024 on shipments of waste, amending Regulations (EU) No 1257/2013 and (EU) 2020/1056 and repealing Regulation (EC) No 1013/2006 (Text with EEA relevance). Official Journal of the European Union, L 1157. 
            <a href="http://data.europa.eu/eli/reg/2024/1157/oj">http://data.europa.eu/eli/reg/2024/1157/oj</a>
            </p>
            <p style="font-size: 12px;">
            7. EUROPEN. (2024, June). Info note on WSR June 2024 PDF. 
            <a href="https://www.europen-packaging.eu/wp-content/uploads/2024/10/EUROPEN-Info-note-on-WSR-June-2024.pdf">https://www.europen-packaging.eu/wp-content/uploads/2024/10/EUROPEN-Info-note-on-WSR-June-2024.pdf</a>
            </p>
            <p style="font-size: 12px;">
            8. Garruto, L. I., & Grassin, S. (2024). Fighting Waste Trafficking in the EU: A Stronger Role for the European Anti-Fraud Office. Eucrim. 
            <a href="https://doi.org/10.30709/eucrim-2024-009">https://doi.org/10.30709/eucrim-2024-009</a>
            </p>
            <p style="font-size: 12px;">
            9. Council of the European Union. (2024, January 11). Waste trade. 
            <a href="https://www.consilium.europa.eu/en/policies/waste-trade/#why">https://www.consilium.europa.eu/en/policies/waste-trade/#why</a>
            </p>
            <p style="font-size: 12px;">
            10. United Nations Environment Programme. (2023). Basel Convention on the Control of Transboundary Movements of Hazardous Wastes and Their Disposal: Protocol on Liability and Compensation for Damage Resulting from Transboundary Movements of Hazardous Wastes and Their Disposal (Revised 2023). UNEP. Retrieved from 
            <a href="https://www.basel.int/TheConvention/Overview/TextoftheConvention/tabid/1275/Default.aspx">https://www.basel.int/TheConvention/Overview/TextoftheConvention/tabid/1275/Default.aspx</a>
            </p>
            <p style="font-size: 12px;">
            11. United Nations Environment Programme & Food and Agriculture Organization. (2023). Rotterdam Convention on the Prior Informed Consent Procedure for Certain Hazardous Chemicals and Pesticides in International Trade: Text and Annexes (Revised 2023). UNEP & FAO. Retrieved from 
            <a href="https://www.pic.int/TheConvention/Overview/TextoftheConvention/tabid/1048/language/en-US/Default.aspx">https://www.pic.int/TheConvention/Overview/TextoftheConvention/tabid/1048/language/en-US/Default.aspx</a>
            </p>
            <p style="font-size: 12px;">
            12. Greenpeace Mediterranean. (2022). <em>Game of Waste: Irreversible Impact</em>. 
            <a href="https://act.gp/game-of-waste-report">https://act.gp/game-of-waste-report</a>
            </p>
            <p style="font-size: 12px;">
            13. Ministry of Environment and Urbanization. (2021, May 18). [Regulation on Waste that Cannot Be Imported]. Official Gazette (No. 31485). 
            <a href="https://www.resmigazete.gov.tr/eskiler/2021/05/20210518-10.htm">https://www.resmigazete.gov.tr/eskiler/2021/05/20210518-10.htm</a>
            </p>
            """,
            unsafe_allow_html=True
        )

    elif page == "Hazardous Waste":
        st.title("Hazardous Waste")
        st.write("Explore the definition and nuances of hazardous waste")
        # Similar to Plastic page with relevant data and visuals
        st.info(
            "This interactive map shows the amounts of hazardous waste exported from the EU to specific countries. "
            "\n\n*Feel free to adjust the selections on the side to explore different years, material types, and export reasons.*"
        )
            # Load datasets
        haz_data = pd.read_csv("hazardous01.csv")
        country_codes = pd.read_csv("countries_codes_and_coordinates.csv", encoding="latin1")

        # Merge the Alpha-3 codes directly into the plastic dataset
        haz_data = haz_data.merge(
            country_codes[['Country', 'Alpha-3 code']],
            left_on='partner',
            right_on='Country',
            how='left'
        )

        # Drop the redundant 'Country' column from the merge
        haz_data.drop(columns=['Country'], inplace=True)

        # Save or display the updated dataset
        #haz_data.to_csv("haz01_with_alpha3.csv", index=False)
        #print("Updated file saved as 'haz01_with_alpha3.csv'")

        # Sidebar to choose the year
        st.sidebar.title("Select Year")
        year = st.sidebar.slider(
            "Year",
            min_value=int(haz_data['TIME_PERIOD'].min()),
            max_value=int(haz_data['TIME_PERIOD'].max()),
            value=int(haz_data['TIME_PERIOD'].max()),  # Default to max year
        )
        # For Hazardous Waste Material Type
        selected_rawmat = st.sidebar.multiselect(
            "Select Material Type",
            options=["Hazardous and non-hazardous - total",
                     "Hazardous", "Other"],
            default="Hazardous"
        )
        # For Hazardous Waste Treatment Reasons
        selected_treat = st.sidebar.multiselect(
            "Select Reason For Export",
            options=["Recovery", "Disposal", "Waste treatment not allocated"],
            default=["Recovery", "Disposal", "Waste treatment not allocated"]
        )
        
        # Filter data for the selected year and raw material
        filtered_data = haz_data[
        (haz_data['TIME_PERIOD'] == year) & 
        (haz_data['hazard'].isin(selected_rawmat)) & (haz_data['wst_oper'].isin(selected_treat))
        ]

           # Merge the filtered data with the world shapefile using SOV_A3 (shapefile) and Alpha-3 code (filtered_data)
        world_copy02 = gpd.read_file(shapefile_path)
        world_copy02['SOV_A3'] = world_copy02['SOV_A3'].replace('CH1', 'CHN')
        world_copy02['SOV_A3'] = world_copy02['SOV_A3'].replace('KA1', 'KAZ')
        world_copy02['SOV_A3'] = world_copy02['SOV_A3'].replace('US1', 'USA')
        world_copy02['SOV_A3'] = world_copy02['SOV_A3'].replace('AU1', 'AUS')
        world_copy02 = world_copy02.merge(
            filtered_data, how='left', left_on='SOV_A3', right_on='Alpha-3 code'
        )

        # Fill missing values in OBS_VALUE
        if 'OBS_VALUE' in world_copy02.columns:
            world_copy02['OBS_VALUE'].fillna(0, inplace=True)
        else:
            st.error("'OBS_VALUE' column is missing after the merge")
            st.write(filtered_data.head())
            st.stop()
        


        # Define the color gradient
        max_obs_value = world_copy02['OBS_VALUE'].max()

        def get_custom_shade(obs_value, max_value):
            if obs_value == 0:
                return [150, 150, 150]  # Gray for zero
            elif obs_value / max_value < 0.1:
                return [173, 216, 230]  # Light blue
            elif obs_value / max_value < 0.2:
                return [135, 206, 235]  # Sky blue
            elif obs_value / max_value < 0.3:
                return [100, 149, 237]  # Cornflower blue
            elif obs_value / max_value < 0.4:
                return [65, 105, 225]  # Royal blue
            elif obs_value / max_value < 0.5:
                return [30, 144, 255]  # Dodger blue
            elif obs_value / max_value < 0.6:
                return [0, 191, 255]  # Deep sky blue
            elif obs_value / max_value < 0.7:
                return [0, 0, 255]  # Blue
            elif obs_value / max_value < 0.8:
                return [0, 0, 205]  # Medium blue
            elif obs_value / max_value < 0.9:
                return [0, 0, 139]  # Dark blue
            else:
                return [0, 0, 100]  # Navy

        # Apply the function to create the `fill_color` column
        world_copy02['fill_color'] = world_copy02['OBS_VALUE'].apply(lambda x: get_custom_shade(x, max_obs_value))
        # Add a formatted OBS_VALUE column for tooltip
        world_copy02['formatted_OBS_VALUE'] = world_copy02['OBS_VALUE'].apply(lambda x: f"{x:,.0f}")

        # Set up the Pydeck layer with precomputed colors
        layer = pdk.Layer(
            "GeoJsonLayer",
            world_copy02.__geo_interface__,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            get_fill_color="properties.fill_color",  # Use the precomputed color
            get_line_color=[255, 255, 255],  # Border color in white
            auto_highlight=False,  # Disable auto-highlight to keep colors consistent
        )

        # View configuration
        view_state = pdk.ViewState(latitude=10, longitude=20, zoom=1)

        # Display map with light style background
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
            "html": "<b>{SOV_A3}</b>: {formatted_OBS_VALUE} tonnes/year",
            "style": {
                "backgroundColor": "aliceblue",
                "color": "white"
            }},
            map_style="light"  # Set map background to light style
        )
        with st.spinner("Generating export visualization..."):
            st.pydeck_chart(r, use_container_width=True)
            
        st.write(
            "Data Source:"
            "Eurostat. (2024). *Transboundary shipments of notified waste by partner, hazardousness and waste management operations* [Online data set]. DOI: "
            "[10.2908/env_wasship](https://doi.org/10.2908/env_wasship)"
        )
        
        # Divider for visual separation
        st.markdown("---")

        # Add the content sections
        st.subheader("The Complexities of Hazardous Waste Management")
        st.write(
            "Hazardous waste is a broad category encompassing materials that pose risks to people, ecosystems, or infrastructure. "
            "These substances vary widely, ranging from physical threats, such as explosives and flammable materials, to severe health hazards, "
            "including carcinogens and toxins that damage organs. Some hazardous materials are particularly harmful to the environment, disrupting "
            "aquatic ecosystems or depleting the ozone layer. [1] In regulatory terms, such materials are often identified by specific 'H-codes,' short for their hazardous properties."
        )

        st.write(
            "Managing hazardous waste is inherently challenging due to the variety of risks involved. Disposal measures include options such as land-based methods "
            "(e.g., landfills and deep injection), chemical and thermal treatments (e.g., incineration and physicochemical processing), and long-term containment in "
            "engineered landfills or permanent storage sites. Recovery measures, by contrast, aim to reclaim value from waste, whether through energy generation, "
            "recycling materials like metals and solvents, or land treatment applications like composting. [2]"
        )

        st.write(
            "However, hazardous waste management often faces social resistance. The Not-In-My-Backyard (NIMBY) phenomenon, where communities with greater political "
            "influence or lobbying power resist the siting of hazardous waste facilities, typically shifts the burden onto marginalized communities. This dynamic creates "
            "significant inequalities in waste management, concentrating risks in areas with limited resources to advocate for safer alternatives. [3]"
        )

        st.subheader("Hazardous Waste in Global Contexts")
        st.write(
            "The issue of hazardous waste mismanagement extends beyond domestic boundaries. Historically, stringent environmental regulations in industrialized nations "
            "have incentivized the export of hazardous waste to less-regulated countries. This phenomenon, often referred to as the 'pollution haven' hypothesis, suggests "
            "that industries seek out countries with lax environmental protections to dispose of hazardous materials. Although the concept has been widely debated, "
            "with limited empirical evidence to firmly establish its prevalence [4][5], case studies like the Colbert brothers’ waste exports provide anecdotal examples of this dynamic. [5]"
        )

        st.write(
            "Recent reports on plastic waste dumpsites in Turkey raise further concerns about hazardous waste mismanagement. These sites, known for receiving waste exports "
            "from the EU, have been contaminated with hazardous chemicals. [6] Whether this contamination stemmed from intentional hazardous waste shipments (H-coded) or "
            "mismanagement after arrival remains unclear, leaving both sides—exporters and recipients—implicated in the problem."
        )

        st.subheader("The Case of Hazardous Waste in Turkey")
        st.write(
            "Turkey itself provides a striking example of hazardous waste challenges. In 2010 alone, the country produced 786,418 tons of hazardous waste. "
            "Of this, only 81.4% were managed through formal disposal methods, such as controlled landfills, while 18% ended up in municipal garbage dumps, and 0.6% was incinerated. [7] "
            "The reliance on questionable disposal methods highlights systemic weaknesses in hazardous waste infrastructure, which mirror global trends in regions grappling with similar issues."
        )

        st.write(
            "Considering how Turkey struggles with the safe disposal of its own waste, it is not ready to safely dispose of the EU’s hazardous waste, which in 2022 amounted to around 200,000 tonnes, as illustrated in the maps."
        )

        st.subheader("Broader Implications")
        st.write(
            "The management of hazardous waste, whether domestically or through international trade, reveals persistent inequities and inefficiencies. "
            "While recovery and disposal measures exist, their implementation is often uneven, shaped by power dynamics and resource availability. "
            "As global waste trade continues to intersect with local waste production, the risks of mismanagement, contamination, and disproportionate harm to vulnerable communities remain pressing challenges for policymakers and industry alike."
        )
        with st.expander("Want to know how does hazardous waste become harmful to the environment?"):
            st.write(
                "**Leachate** — specifically, landfill leachate (as the term can also refer to other substances breaking down) — is a toxic liquid that escapes from landfills into the environment. "
                "It is **high-strength wastewater**, meaning it contains extreme pH levels, high chemical oxygen demand (COD) and biochemical oxygen demand (BOD), inorganic salts, "
                "and toxins [8]."
            )

            st.write(
                "Preventing leachate formation is impossible, as it is a natural byproduct of waste decomposition, especially in warmer climates. You may have even seen leachate yourself "
                "around landfills. While many countries have regulations for leachate treatment to minimize its impact, issues with leachate contamination continue to emerge. For example, "
                "research from the U.S. Geological Survey (USGS) has identified landfill leachate as a host to numerous **contaminants of emerging concern**, which enter environmental pathways "
                "through wastewater treatment systems [9]."
            )

            st.markdown("## Soil Contamination from Leachate")

            st.write(
                "Soil contamination is a significant concern near landfills and waste disposal sites. **Leachate forms when water goes through waste, dissolving various contaminants.** "
                "If not properly managed, it migrates into the soil, carrying pollutants such as **heavy metals, organic chemicals, and pathogens**. These pollutants can react with soil "
                "minerals, altering both the soil's physical and chemical properties [10]."
            )

            st.write(
                "This contamination has several environmental and public health consequences. It can **degrade soil structure and nutrient content**, making the land unsuitable for agriculture "
                "and disrupting local ecosystems. If contaminated soil is used for farming, toxins can enter the food chain, posing health risks to humans and animals. Additionally, "
                "pollutants can reach further into the ground, contaminating **groundwater supplies**, which are more difficult to remediate [10]."
            )

            st.warning(
                "Soil and, by extension, every natural environment, has a stable state—a point to which it returns even after some disturbance (for example, a forest regrowing after "
                "low-intensity tree cutting). However, if the disturbance is significant enough, the soil might not be able to revert to its original stable state. This can happen when "
                "chemicals released through leachate are too toxic and do not break down."
            )

            st.write(
                "When contamination reaches this level, it can push the environment into what is known as an **alternative stable state (ASS)**—a condition where the soil undergoes fundamental "
                "changes and cannot return to its original state (see a picture below for demonstration). The shift to ASS can happen when landfills remain in one place for extended periods, "
                "polluting the surrounding soil to the point where it becomes unsuitable for typical use, such as planting vegetation. In these cases, the soil does not recover from the "
                "disturbance, marking a transition into **degradation** [11]."
            )

            col1, col2, col3 = st.columns([1, 4, 1])  # Adjust column widths as needed
            with col2:
                st.image(
                    "basin.png",
                    caption="A picture demonstrating soil degradation, modeled after a forest degradation example from Ghazoul et al. (2015)[11]",
                    use_container_width=True
                )

            st.write(
                "**Soil degradation** is the result of human-induced changes that strip the soil of its ability to recover naturally [11]. This means a shift not just "
                "in its chemical and mineral composition but also in its properties and usability—whether for pasture, agriculture, or other purposes. When this resilience is lost, "
                "the damage becomes long-term or even permanent."
            )

            st.write(
                "The severity of these changes varies, but a concerning example is the presence of **persistent toxic chemicals** in landfill sites in Adana, Turkey[12]. These substances break "
                "down extremely slowly, continuing to affect the environment long after waste disposal has ceased. Even when pollution is no longer actively occurring, hazardous particles "
                "can remain in the soil."
            )

            st.write(
                "Scientists in Iran [13] observed similar patterns when studying landfill sites, finding that landfills significantly degrade soil quality over time, leading "
                "to various environmental consequences. Among these effects, soil near landfills tends to be less fertile due to leachate contamination. Additionally, **biomass and microbial "
                "respiration are disrupted**, and **heavy metal accumulation** poses further risks. Comparable findings emerged from research in Lithuania [14], where scientists "
                "studied post-closure landfill sites. While individual heavy metal concentrations often remained within acceptable limits, their combined presence led to pollution levels "
                "classified as hazardous. This suggests that it is not any single metal that poses the greatest danger, but rather the **cumulative effect of multiple contaminants**."
            )

            st.write(
                "However, the extent of soil contamination around a landfill varies significantly based on the level of contamination within the landfill itself. Research in Germany [15] "
                "found that landfills with lower contamination levels also had surrounding areas with significantly less pollution—sometimes even safe enough for livestock grazing. This highlights the "
                "importance of proper landfill management. The existence of a landfill does not automatically mean severe soil contamination; rather, the impact depends on what is disposed of and "
                "how leachate is treated."
            )

            st.write(
                "**Leachate contamination of drinking water, particularly with heavy metals, has severe health implications.** Exposure to these contaminants increases the risk of both carcinogenic "
                "and non-carcinogenic diseases in both children and adults [16]. However, these risks can be mitigated with proper leachate management and soil protection measures."
            )

            st.markdown("## Liner Systems and Solutions")

            st.success(
                "**Liner systems** are a critical component in preventing leachate from contaminating the surrounding soil. These barriers are designed to contain leachate within the landfill, reducing "
                "the risk of environmental harm. There are two main types of liner systems: **natural and synthetic**. Natural liners include Compacted Clay Liners (CCL) and Soil Liners, while synthetic "
                "options encompass Geomembranes, Geosynthetic Clay Liners, and Composite Liners [16]. Each type has variations, and ongoing research is determining which liners perform best "
                "under different conditions. While Soil Liners tend to have higher leakage rates, Geosynthetic Clay Liners currently appear to be the most effective option. However, continued innovation and "
                "site-specific evaluations remain essential in selecting the most suitable liner for each landfill."
            )

            st.write(
                "On the positive side, ongoing research is focused on improving leachate treatment and developing solutions that effectively prevent contamination. However, much of this research is still "
                "in its early stages, and effective leachate treatment is either insufficient or nonexistent in many landfills due to a lack of funding and regulation. After all, if the waste being dumped into a "
                "landfill goes unregulated, why would the landfill itself be any different?"
            )

        # Divider for references
        st.markdown("---")

        # Add references
        st.markdown(
            """
            <h4 style="font-size: 16px;">References</h4>
            <p style="font-size: 12px;">
            1. United Nations Economic Commission for Europe. (2011). <em>Globally Harmonized System of Classification and Labelling of Chemicals (GHS): Fourth revised edition</em>. United Nations. ISBN: 978-92-1-117042-9. 
            <a href="https://unece.org">https://unece.org</a>
            </p>
            <p style="font-size: 12px;">
            2. Environmental Protection Agency. (n.d.). <em>Explanation of recovery and disposal codes</em>. 
            <a href="https://www.epa.ie/publications/monitoring--assessment/waste/national-waste-statistics/Explanation_of_Recovery_and_Disposal_Codes_TB.pdf">https://www.epa.ie/publications/monitoring--assessment/waste/national-waste-statistics/Explanation_of_Recovery_and_Disposal_Codes_TB.pdf</a>
            </p>
            <p style="font-size: 12px;">
            3. Hamilton, J. T. (1993). Politics and Social Costs: Estimating the Impact of Collective Action on Hazardous Waste Facilities. <em>The RAND Journal of Economics, 24</em>(1), 101–125. 
            <a href="https://doi.org/10.2307/2555955">https://doi.org/10.2307/2555955</a>
            </p>
            <p style="font-size: 12px;">
            4. Pearson, C. S., & World Resources Institute. (1987). <em>Multinational corporations, environment, and the Third World: Business matters</em>. Duke University Press. 
            <a href="http://books.google.com/books?id=GwRDAAAAYAAJ">http://books.google.com/books?id=GwRDAAAAYAAJ</a>
            </p>
            <p style="font-size: 12px;">
            5. Müller, S. M. (2019). Hidden Externalities: The Globalization of Hazardous Waste. <em>Business History Review, 93</em>(1), 51–74. 
            <a href="https://doi.org/10.1017/S0007680519000357">https://doi.org/10.1017/S0007680519000357</a>
            </p>
            <p style="font-size: 12px;">
            6. Greenpeace Mediterranean. (2022). <em>Game of Waste: Irreversible Impact</em>. 
            <a href="https://act.gp/game-of-waste-report">https://act.gp/game-of-waste-report</a>
            </p>
            <p style="font-size: 12px;">
            7. Akkoyunlu, A., Avşar, Y., & Ergüven, G. Ö. (2017). Hazardous waste management in Turkey. <em>Journal of Hazardous, Toxic, and Radioactive Waste, 21</em>(4), 04017018. 
            <a href="https://doi.org/10.1061/(ASCE)HZ.2153-5515.0000373">https://doi.org/10.1061/(ASCE)HZ.2153-5515.0000373</a>
            </p>
            <p style="font-size: 12px;">
            8. Kamaruddin, M. A., Yusoff, M. S., Rui, L. M., Isa, A. M., Zawawi, M. H., & Alrozi, R. (2017). An overview of municipal solid waste management and landfill leachate treatment: Malaysia and Asian perspectives. <em>Environmental Science and Pollution Research International</em>, 24(35), 26988-27020. 
            <a href="https://doi.org/10.1007/s11356-017-0303-9">https://doi.org/10.1007/s11356-017-0303-9</a>
            </p>
            <p style="font-size: 12px;">
            9. U.S. Geological Survey. (2015, November 13). Landfill leachate released to wastewater treatment plants and other environmental pathways contains a mixture of contaminants including pharmaceuticals. Retrieved from 
            <a href="https://www.usgs.gov/programs/environmental-health-program/science/landfill-leachate-released-wastewater-treatment">https://www.usgs.gov/programs/environmental-health-program/science/landfill-leachate-released-wastewater-treatment</a>
            </p>
            <p style="font-size: 12px;">
            10. Recycling View. (2023). Leachate: Definition, environmental impact & treatment solutions. Retrieved from 
            <a href="https://www.recyclingview.com/leachate-definition-environmental-impact-treatment-solutions/">https://www.recyclingview.com/leachate-definition-environmental-impact-treatment-solutions/</a>
            </p>
            <p style="font-size: 12px;">
            11. Ghazoul, J., Burivalova, Z., Garcia-Ulloa, J., & King, L. A. (2015). Conceptualizing forest degradation. <em>Trends in Ecology & Evolution, 30</em>(10), 622-632. 
            <a href="https://doi.org/10.1016/j.tree.2015.08.001">https://doi.org/10.1016/j.tree.2015.08.001</a>
            </p>
            <p style="font-size: 12px;">
            12. Greenpeace Mediterranean. (2022). <em>Game of Waste: Irreversible Impact</em>. 
            <a href="https://act.gp/game-of-waste-report">https://act.gp/game-of-waste-report</a>
            </p>
            <p style="font-size: 12px;">
            13. Kooch, Y., Nouraei, A., Wang, L., Wang, X., Wu, D., Francaviglia, R., Frouz, J., & Parsapour, M. K. (2024). Long-term landfill leachate pollution suppresses soil health indicators in natural ecosystems of a semi-arid environment. <em>Chemosphere</em>, 367, 143647. 
            <a href="https://doi.org/10.1016/j.chemosphere.2024.143647">https://doi.org/10.1016/j.chemosphere.2024.143647</a>
            </p>
            <p style="font-size: 12px;">
            14. Baziene, K., Tetsman, I., & Albrektiene, R. (2020). Level of pollution on the surrounding environment from landfill aftercare. <em>International Journal of Environmental Research and Public Health, 17</em>(6), 2007. 
            <a href="https://doi.org/10.3390/ijerph17062007">https://doi.org/10.3390/ijerph17062007</a>
            </p>
            <p style="font-size: 12px;">
            15. Hard, H. R., Brusseau, M., & Ramirez-Andreotta, M. (2019). Assessing the feasibility of using a closed landfill for agricultural graze land. <em>Environmental Monitoring and Assessment</em>, 191(7), 458. 
            <a href="https://doi.org/10.1007/s10661-019-7579-9">https://doi.org/10.1007/s10661-019-7579-9</a>
            </p>
            <p style="font-size: 12px;">
            16. Mishra, H., Karmakar, S., Kumar, R., & Kadambala, P. (2018). A long-term comparative assessment of human health risk to leachate-contaminated groundwater from heavy metal with different liner systems. <em>Environmental Science and Pollution Research International</em>, 25(3), 2911-2923. 
            <a href="https://doi.org/10.1007/s11356-017-0717-4">https://doi.org/10.1007/s11356-017-0717-4</a>
            </p>
            """,
            unsafe_allow_html=True
        )

elif horizontal_menu == "The Project's Purpose":
    st.title("The Project's Purpose")

    st.subheader("The Purpose of This Project")
    st.write(
        "There are actually two objectives of this project:"
    )

    st.write(
        "1. **Educate**: Provide an understandable narrative about the EU’s waste export practices, creating a resource that is engaging and accessible."
    )

    st.write(
        "2. **Challenge Narratives**: Encourage critical thinking about the EU's environmental role by presenting data-driven insights that reveal inconsistencies and inequities in its waste management systems."
    )
    
    st.write(
        "This project began as a social media initiative to raise awareness about local and global waste management practices. "
        "Over time, it evolved into a more academically and policy-focused effort aimed at presenting a comprehensive narrative about the EU’s waste export practices. "
        "While many academic and popular resources exist on this topic, they are often inaccessible or underutilized by the general public. "
        "This project seeks to bridge that gap, providing an analytical resource that is accessible to advocacy groups, non-profits, policymakers, and the broader public."
    )

    st.write(
        "The goal is to mitigate the bias that frames the EU as a “magical green space” that is fully environmentally friendly and equitable. "
        "While the EU has many strong regulations and initiatives, this project critically examines their limitations, showing that these systems are not perfect and do not always function as intended. "
        "By challenging this dominant narrative, the project aims to offer a more balanced perspective on the EU’s environmental practices."
    )
elif horizontal_menu == "About Me":
    st.title("About Me")
    st.write(
        "Hi all! Thank you for visiting this project’s website—it means a lot to me. 😊"
    )

    st.write(
        "My name is Hana Pasková, and I am a senior at Minerva University, majoring in Economics and Sustainability. "
        "This project is my Capstone (bachelor’s thesis) and reflects my journey into waste management and waste trade. "
        "The idea for this project began during my internship with the Undersecretary of Human Resources in Buenos Aires, where I analyzed policies on integrating waste pickers into the formal economy. "
        "As someone originally from the Czech Republic, I chose to focus on the EU to explore these issues in a region I know well."
    )

    st.write(
        "I studied at Pearson College UWC in Canada and, through Minerva University, traveled across seven countries during my bachelor’s degree. "
        "These experiences have shaped my critical perspective on global sustainability issues. "
        "I don’t believe the EU should be placed on a pedestal, and I aim to approach its practices with as much scrutiny as possible. "
        "To me, sustainability cannot exist without environmental justice, and I ground my analysis in a data-focused approach."
    )
elif horizontal_menu == "More Resources":
    st.title("More Resources")
    # Data for annotated bibliography
    bibliography = [
        {"citation": "Akkoyunlu, A., Avşar, Y., & Ergüven, G. Ö. (2017). Hazardous waste management in Turkey. *Journal of Hazardous, Toxic, and Radioactive Waste, 21*(4), 04017018.",
         "annotation": "This article examines Turkey's hazardous waste management systems and challenges, providing insights into regulatory frameworks and their implementation."},
        {"citation": "Baziene, K., Tetsman, I., & Albrektiene, R. (2020). Level of pollution on the surrounding environment from landfill aftercare. *International Journal of Environmental Research and Public Health, 17*(6), 2007.",
         "annotation": "This study assesses the pollution levels in environments surrounding landfills during aftercare, highlighting the long-term impacts of waste disposal sites."},
        {"citation": "Bishop, A. (2017, October 30). Examining waste as an economic externality. *Discard Studies: Social Studies of Waste, Pollution & Externalities*.",
         "annotation": "This piece discusses how waste serves as an economic externality, exploring its societal and environmental costs."},
        {"citation": "Council of the European Union. (2024, January 11). Waste trade.",
         "annotation": "This resource outlines the EU's approach to waste trade, explaining the rationale behind the new regulations and their expected impact on waste management practices."},
        {"citation": "Danthurebandara, M., Van Passel, S., Nelen, D., Tielemans, Y., & Van Acker, K. (2013). Environmental and socio-economic impacts of landfills. *Linnaeus ECO-TECH 2012, Kalmar, Sweden*.",
         "annotation": "This study examines the environmental and socio-economic impacts of landfills, providing insights into the consequences of waste disposal practices."},
        {"citation": "DW Planet A. (2021, December 24). Your plastic waste might be traded by criminals [Video]. YouTube.",
         "annotation": "This video highlights the role of illegal trade in plastic waste, showcasing how criminal networks exploit weak regulations to manage global waste streams."},
        {"citation": "Environmental Investigation Agency. (2021). *The truth behind trash: The scale and impact of the international trade in plastic waste*.",
         "annotation": "This report analyzes the international plastic waste trade, detailing its environmental and social impacts."},
        {"citation": "Environmental Protection Agency. (n.d.). *Explanation of recovery and disposal codes*.",
         "annotation": "This document explains the recovery and disposal codes used in waste management, offering a foundational guide for understanding classification standards in the waste sector."},
        {"citation": "EUROPEN. (2024). Extended producer responsibility. *The European Organization for Packaging and the Environment*.",
         "annotation": "This resource discusses extended producer responsibility (EPR) policies and their role in achieving recycling and recovery targets in the EU."},
        {"citation": "EUROPEN. (2024, June). Info note on WSR June 2024 PDF.",
         "annotation": "This information note provides an overview of the new Waste Shipment Regulation, highlighting key changes and implications for stakeholders in the packaging industry."},
        {"citation": "European Parliament and Council. (2006, July 12). Regulation (EC) No 1013/2006 of the European Parliament and of the Council of 14 June 2006 on shipments of waste. *Official Journal of the European Union, L 190*, 1–98.",
         "annotation": "This regulation established the framework for controlling waste shipments within, into, and out of the European Union."},
        {"citation": "European Parliament and Council. (2024, April 30). Regulation (EU) 2024/1157 of the European Parliament and of the Council of 11 April 2024 on shipments of waste, amending Regulations (EU) No 1257/2013 and (EU) 2020/1056 and repealing Regulation (EC) No 1013/2006 (Text with EEA relevance). *Official Journal of the European Union, L 1157*.",
         "annotation": "This new regulation updates and replaces the 2006 waste shipment rules, introducing stricter controls and enhanced transparency for waste shipments."},
        {"citation": "Ferronato, N., & Torretta, V. (2019). Waste mismanagement in developing countries: A review of global issues. *International Journal of Environmental Research and Public Health, 16*(6), 1060.",
         "annotation": "This review outlines global issues related to waste mismanagement in developing countries, focusing on environmental and public health impacts."},
        {"citation": "Garruto, L. I., & Grassin, S. (2024). Fighting Waste Trafficking in the EU: A Stronger Role for the European Anti-Fraud Office. *Eucrim*.",
         "annotation": "This article discusses the enhanced role of the European Anti-Fraud Office (OLAF) in combating waste trafficking under the new Waste Shipment Regulation."},
        {"citation": "Ghazoul, J., Burivalova, Z., Garcia-Ulloa, J., & King, L. A. (2015). Conceptualizing forest degradation. *Trends in Ecology & Evolution, 30*(10), 622–632.",
         "annotation": "This article provides a theoretical framework for discussing degradation in general, focusing on ecological processes and resilience."},
        {"citation": "Greenpeace Mediterranean. (2022). *Game of Waste: Irreversible Impact*.",
         "annotation": "This report investigates the environmental and social costs of waste mismanagement, using case studies to emphasize the irreversible impacts of poorly regulated waste systems."},
        {"citation": "Hamilton, J. T. (1993). Politics and Social Costs: Estimating the Impact of Collective Action on Hazardous Waste Facilities. *The RAND Journal of Economics, 24*(1), 101–125.",
         "annotation": "This study estimates the societal costs associated with hazardous waste facilities, highlighting the political dynamics that influence their siting and regulation."},
        {"citation": "Hard, H. R., Brusseau, M., & Ramirez-Andreotta, M. (2019). Assessing the feasibility of using a closed landfill for agricultural graze land. *Environmental Monitoring and Assessment, 191*(7), 458.",
         "annotation": "This research evaluates the potential for repurposing closed landfills as agricultural grazing land."},
        {"citation": "Kamaruddin, M. A., et al. (2017). An overview of municipal solid waste management and landfill leachate treatment: Malaysia and Asian perspectives. *Environmental Science and Pollution Research International, 24*(35), 26988–27020.",
         "annotation": "This article offers an Asian perspective on municipal solid waste management and landfill leachate treatment, highlighting regional challenges and solutions."},
        {"citation": "Kaza, S., et al. (2018). What a Waste 2.0: A Global Snapshot of Solid Waste Management to 2050. *World Bank Group*.",
         "annotation": "This comprehensive report provides a global overview of solid waste management trends, focusing on challenges and projections."},
        {"citation": "Kooch, Y., et al. (2024). Long-term landfill leachate pollution suppresses soil health indicators in natural ecosystems of a semi-arid environment. *Chemosphere, 367*, 143647.",
         "annotation": "This research examines the long-term effects of landfill leachate on soil health in semi-arid ecosystems."},
        {"citation": "Latiff, R. (2024, August 9). Malaysia opens anti-dumping duty probe on plastic imports from China, Indonesia. *Reuters*.",
         "annotation": "This news piece covers Malaysia's investigation into anti-dumping duties on plastic imports, shedding light on trade practices and their environmental implications."},
        {"citation": "Lobelle, D., et al. (2024). Knowns and unknowns of plastic waste flows in the Netherlands. *Waste Management & Research, 42*(1), 27–40.",
         "annotation": "This article analyzes plastic waste flows in the Netherlands, identifying gaps in data and policy challenges."},
        {"citation": "Ministry of Environment and Urbanization. (2021, May 18). [Regulation on Waste that Cannot Be Imported]. *Official Gazette* (No. 31485).",
         "annotation": "This Turkish regulation specifies types of waste that cannot be imported into the country."},
        {"citation": "Mishra, H., Karmakar, S., Kumar, R., & Kadambala, P. (2018). A long-term comparative assessment of human health risk to leachate-contaminated groundwater from heavy metal with different liner systems. *Environmental Science and Pollution Research International, 25*(3), 2911–2923.",
         "annotation": "This study compares the long-term human health risks associated with leachate-contaminated groundwater from landfills using different liner systems."},
        {"citation": "Müller, S. M. (2019). Hidden Externalities: The Globalization of Hazardous Waste. *Business History Review, 93*(1), 51–74.",
         "annotation": "This article investigates the globalization of hazardous waste, emphasizing hidden costs and externalities."},
        {"citation": "Pearson, C. S., & World Resources Institute. (1987). *Multinational corporations, environment, and the Third World: Business matters*.",
         "annotation": "This book explores the environmental impact of multinational corporations in non-European countries."},
        {"citation": "Pickens, N., & Kettle, J. (2024, April 22). Why recycling metal is an opportunity too good to waste. *World Economic Forum*.",
         "annotation": "This article discusses the economic and environmental benefits of metal recycling."},
        {"citation": "Recycling View. (2023). Leachate: Definition, environmental impact & treatment solutions.",
         "annotation": "This article provides an overview of leachate, its environmental impacts, and various treatment solutions."},
        {"citation": "Ritchie, H. (2022). *Ocean plastics: How much do rich countries contribute by shipping their waste overseas?* Our World in Data.",
         "annotation": "This analysis examines how wealthy nations contribute to ocean plastic pollution through waste exports."},
        {"citation": "Rosenthal, E. (2009). What Makes Europe Greener than the U.S.? *Yale E360*.",
         "annotation": "This article compares waste management practices in Europe and the U.S., emphasizing policies that have made Europe a leader in sustainability."},
        {"citation": "Schandl, H., et al. (2024). Global material flows and resource productivity: The 2024 update. *Journal of Industrial Ecology*.",
         "annotation": "This report provides an updated overview of global material flows, focusing on resource productivity."},
        {"citation": "U.S. Geological Survey. (2015, November 13). Landfill leachate released to wastewater treatment plants and other environmental pathways contains a mixture of contaminants including pharmaceuticals.",
         "annotation": "This resource discusses the environmental impact of landfill leachate, focusing on its contaminant content."},
        {"citation": "United Nations Economic Commission for Europe. (2011). *Globally Harmonized System of Classification and Labelling of Chemicals (GHS): Fourth revised edition*.",
         "annotation": "This publication outlines the standardized system for classifying and labeling chemicals."},
        {"citation": "United Nations Environment Programme. (2023). Basel Convention on the Control of Transboundary Movements of Hazardous Wastes and Their Disposal: Protocol on Liability and Compensation for Damage Resulting from Transboundary Movements of Hazardous Wastes and Their Disposal (Revised 2023).",
         "annotation": "This document provides the updated text of the Basel Convention, which serves as a foundation for international regulations on hazardous waste shipments."},
        {"citation": "United Nations Environment Programme & Food and Agriculture Organization. (2023). Rotterdam Convention on the Prior Informed Consent Procedure for Certain Hazardous Chemicals and Pesticides in International Trade: Text and Annexes (Revised 2023).",
         "annotation": "This resource outlines the Rotterdam Convention, which establishes procedures for the international trade of certain hazardous chemicals and pesticides."},
        {"citation": "Walt, V., & Meyer, S. (2020, March 16). Plastic that travels 8,000 miles: The global crisis in recycling. *Pulitzer Center*.",
         "annotation": "This article explores the global recycling crisis, following the journey of plastic waste across continents to highlight systemic failures and potential solutions."},
        {"citation": "Young, I. M. (2006). Responsibility and Global Justice: A Social Connection Model. *Social Philosophy and Policy, 23*(1), 102–130.",
         "annotation": "This philosophical article proposes a model for understanding global responsibility."}
    ]

    st.write("## Annotated Bibliography")

    st.write("Below is an ordered annotated bibliography for your further research:")

    for i, entry in enumerate(bibliography, start=1):
        st.markdown(f"**{i}. {entry['citation']}**")
        st.write(f"- {entry['annotation']}\n")

        

