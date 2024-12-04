import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(layout="wide")

# Path to the SQLite database file
database_path = 'Dashboard_healthcare_database_v2.db'

# Connect to the SQLite database
connection = sqlite3.connect(database_path)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

########## QUESTION ONE ##########
st.header("Income and Chronic Conditions")
########## QUESTION TWO ##########



########## QUESTION THREE ##########
# Write your SQL query, use triple quotes for multi-line string values
question_three = """
SELECT
   hci.State AS Region,
   AVG(cds."Cervical Cancer Screening") AS Avg_Cervical_Cancer_Screening,
   AVG(cds."Breast Cancer Screening") AS Avg_Breast_Cancer_Screening,
   AVG(cds."Childhood Immunization") AS Avg_Childhood_Immunization,
   AVG(cds."Blood Pressure Control (Hypertensive Patients with Blood Pressure < 140/90)") AS Avg_Blood_Pressure_Control,
   AVG(cds."Uncontrolled Diabetes > 9%") AS Avg_Uncontrolled_Diabetes,
   AVG(cds."Depression Remission") AS Avg_Depression_Remission
FROM
   "Health Center Information" hci
JOIN
   "Clinical Data & Services" cds
   ON hci."Center ID" = cds."Center ID"
JOIN
   "Age, Race, Ethnicity" are
   ON hci."Center ID" = are."Center ID"
JOIN
   "Cost" c
   ON hci."Center ID" = c."Center ID"
GROUP BY
   hci.State
ORDER BY
   hci.State;
"""

# Execute the query
cursor.execute(question_three)

# Fetch all results_question_three from the executed query
results_question_three = cursor.fetchall()

results_question_three = pd.DataFrame(results_question_three)

st.subheader("SQL Query results_question_three")
st.dataframe(results_question_three, use_container_width=True)

########## QUESTION 4 ##########
# Write your SQL query, use triple quotes for multi-line string values
question_four = """
SELECT
   hci."State" AS Region,
   COUNT(cds."Prenatal Patients who Delivered") AS Total_Prenatal_Deliveries,
   SUM(cds."Access to Prenatal Care (First Prenatal Visit in 1st Trimester)") AS Total_First_Trimester_Visits,
   SUM(cds."Low Birth Weight") AS Total_Low_Birth_Weight,
   AVG(CAST(cds."Low Birth Weight" AS FLOAT) / NULLIF(cds."Prenatal Patients who Delivered", 0)) AS Low_Birth_Weight_Ratio
FROM
   "Health Center Information" hci
JOIN
   "Clinical Data & Services" cds ON hci."Center ID" = cds."Center ID"
GROUP BY
   hci."State"
ORDER BY
   hci."State";
"""

# Execute the query
cursor.execute(question_four)

# Fetch all results_question_six from the executed query
results_question_six = cursor.fetchall()

results_question_six = pd.DataFrame(results_question_six)


st.subheader("SQL Query results_question_six")
st.dataframe(results_question_six, use_container_width=True)

########## QUESTION 5 ##########

st.title("Demographic Utilization of Services")
st.write("What is the relationship between the racial/ethnic composition of clinic patients and the percentage of medical, dental, mental health, substance abuse, and vision services offered?")

# Write your SQL query, use triple quotes for multi-line string values
question_five_a = """
SELECT 
    'Medical' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S.Medical < 0.25
UNION ALL
SELECT 
    'Dental' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S.Dental < 0.25
UNION ALL
SELECT 
    'Mental Health' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S."Mental Health" < 0.25
UNION ALL
SELECT 
    'Substance Abuse' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S."Substance Abuse" < 0.25
UNION ALL
SELECT 
    'Vision' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S.Vision < 0.25
ORDER BY ServiceType;
"""

# Execute the query
cursor.execute(question_five_a)

# Fetch all results_question_five_b from the executed query
results_question_five_a = cursor.fetchall()

# Create a DataFrame and assign column names
results_question_five_a = pd.DataFrame(
    results_question_five_a,
    columns=["ServiceType", "Hispanic/Latino", "Black/African American", "Asian", 
             "American Indian/Alaska Native", "Native Hawaiian / Other Pacific Islander"]
)

# Display the DataFrame with Streamlit
# st.subheader("Average Client Percent by Race and Ethnicity for Facilities with Limited Services")
# st.write("Less than 25%")
# st.dataframe(results_question_five_a, use_container_width=True)

# Write your SQL query, use triple quotes for multi-line string values
question_five_b = """
SELECT 
    'Medical' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S.Medical >0.75
UNION ALL
SELECT 
    'Dental' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S.Dental >0.75
UNION ALL
SELECT 
    'Mental Health' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S."Mental Health" >0.75
UNION ALL
SELECT 
    'Substance Abuse' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S."Substance Abuse" >0.75
UNION ALL
SELECT 
    'Vision' AS ServiceType,
    round(avg(A."Hispanic/Latino Ethnicity"),2) As [Hispanic/Latino],
    round(avg(A."Black/African American"),2) AS [Black/African American],
    round(avg(A.Asian),2) as [Asian],
    round(avg(A."American Indian/Alaska Native"),2) as [American Indian/Alaska Native], 
    round(avg(A."Native Hawaiian / Other Pacific Islander"),2) as [Native Hawaiian / Other Pacific Islander]
FROM "Clinical Data & Services" as S
INNER JOIN "Age, Race, Ethnicity" as A
ON S."Center ID" = A."Center ID" 
WHERE S.Vision >0.75
ORDER BY ServiceType;
"""

# Execute the query
cursor.execute(question_five_b)

# Fetch all results_question_five_b from the executed query
results_question_five_b = cursor.fetchall()

# Create a DataFrame and assign column names
results_question_five_b = pd.DataFrame(
    results_question_five_b,
    columns=["ServiceType", "Hispanic/Latino", "Black/African American", "Asian", 
             "American Indian/Alaska Native", "Native Hawaiian / Other Pacific Islander"]
)

# Display the DataFrame with Streamlit
# st.subheader("Average Client Percent by Race and Ethnicity for Facilities with Robust Services")
# st.write("More than 75%")
# st.dataframe(results_question_five_b, use_container_width=True)

st.write("The data shows some clear disparities in service accessibility across racial groups when comparing facilities that offer less than 25% of a service versus those offering more than 75%. For example, Hispanic/Latino individuals are much more likely to visit facilities with limited (<25%) Dental services (32%) but are less represented in facilities with greater access (>75%) at only 14%. On the other hand, Vision services stand out with Native Hawaiian/Other Pacific Islanders making up 86% of those accessing facilities with the highest level of service, while other racial groups are more evenly distributed. Another interesting trend is that Asian individuals are much more represented in facilities offering extensive Substance Abuse services (>75%) at 43%, compared to 22% in facilities with limited access. Overall, this highlights potential inequalities in service availability that might need further attention, especially for groups who are less represented in higher-quality facilities.")

# Heatmap comparing Q Five A and Five B
import pandas as pd
import plotly.express as px
import streamlit as st

# Your data for less than 25% (question_five_a)
data_a = {
    "ServiceType": ["Dental", "Medical", "Mental Health", "Substance Abuse", "Vision"],
    "Hispanic/Latino": [0.32, 0.27, 0.31, 0.31, 0.31],
    "Black/African American": [0.25, 0.17, 0.22, 0.22, 0.22],
    "Asian": [0.04, 0.03, 0.04, 0.04, 0.04],
    "American Indian/Alaska Native": [0.02, 0.01, 0.04, 0.03, 0.03],
    "Native Hawaiian / Other Pacific Islander": [0.01, 0.01, 0.01, 0.01, 0.01],
}
df_a = pd.DataFrame(data_a)

# Your data for more than 75% (question_five_b)
data_b = {
    "ServiceType": ["Dental", "Medical", "Mental Health", "Substance Abuse", "Vision"],
    "Hispanic/Latino": [0.14, 0.33, 0.19, 0.11, 0.86],
    "Black/African American": [0.12, 0.23, 0.31, 0.43, 0.02],
    "Asian": [0.02, 0.04, 0.01, 0.04, 0.02],
    "American Indian/Alaska Native": [0.01, 0.03, 0.01, 0.04, 0.02],
    "Native Hawaiian / Other Pacific Islander": [0.00, 0.01, 0.01, 0.01, 0.00],
}
df_b = pd.DataFrame(data_b)

# Streamlit app with a filter
st.subheader("Service Accessibility Heatmap")

# Dropdown for filtering
filter_option = st.selectbox("Choose service accessibility level:", ["<25%", ">75%"])

# Select dataset based on filter
if filter_option == "<25%":
    selected_df = df_a
else:
    selected_df = df_b

# Melt the DataFrame for Plotly Express (long format)
selected_df_melted = selected_df.melt(id_vars="ServiceType", var_name="Racial Group", value_name="Percentage")

# Create the heatmap
st.write(f"Heatmap for facilities offering {filter_option} of services.")
fig = px.density_heatmap(
    selected_df_melted,
    x="Racial Group",
    y="ServiceType",
    z="Percentage",
    color_continuous_scale="viridis",  # Use a valid Plotly colorscale
    title=f"Racial Distribution for {filter_option} Service Accessibility",
    labels={"Percentage": "Percentage (%)"},
    text_auto=True,
)

# Adjust layout for better readability
fig.update_layout(
    xaxis_title="Racial Group",
    yaxis_title="Service Type",
    coloraxis_colorbar=dict(title="Percentage (%)"),
    font=dict(size=12),
)

# Display the heatmap in Streamlit
st.plotly_chart(fig, use_container_width=True)

########## QUESTION 6 ########## 
st.header("Question 6")
st.write("insert question")

question_six = """
SELECT 
    c."Cervical Cancer Screening", 
    c."Adolescent Weight Screening and Follow Up" , 
    c."Adult Weight Screening and Follow Up", 
    c."Colorectal Cancer Screening",
    c."HIV Screening", 
    c."Adults Screened for Tobacco Use and Receiving Cessation Intervention", 
    c."Depression Screening",
    c."Breast Cancer Screening",
    a."Hispanic/Latino Ethnicity", 
    a."Black/African American", 
    a.Asian, 
    a."American Indian/Alaska Native", 
    a."Native Hawaiian / Other Pacific Islander" 
FROM 
    "Age, Race, Ethnicity" as a
INNER JOIN 
    "Clinical Data & Services" as c
ON 
    a."Center ID" = c."Center ID" 
"""

# Execute the query
cursor.execute(question_six)

# Fetch all results from the executed query
results_question_six = cursor.fetchall()

# Define column names explicitly
columns = [
    "Cervical Cancer Screening",
    "Adolescent Weight Screening and Follow Up",
    "Adult Weight Screening and Follow Up",
    "Colorectal Cancer Screening",
    "HIV Screening",
    "Tobacco Use and Cessation Intervention",
    "Depression Screening",
    "Breast Cancer Screening",
    "Hispanic/Latino Ethnicity",
    "Black/African American",
    "Asian",
    "American Indian/Alaska Native",
    "Native Hawaiian / Other Pacific Islander"
]

# Create a DataFrame with the column names
results_question_six_df = pd.DataFrame(results_question_six, columns=columns)

# Display the DataFrame in Streamlit
st.subheader("SQL Query Results - Question Six")
st.dataframe(results_question_six_df, use_container_width=True)

########## QUESTION 7 ##########
# Query for Question 7: Correlation Between Limited Access and Outcomes/Costs
question_seven = """
WITH Service_Access AS (
    SELECT 
        c."Center ID",
        h."City",
        h."State",
        -- Shows how many services are deemed "available" based on availability threshold
        CASE WHEN c.Medical > 0.5 THEN 1 ELSE 0 END +
        CASE WHEN c.Dental > 0.5 THEN 1 ELSE 0 END +
        CASE WHEN c."Mental Health" > 0.5 THEN 1 ELSE 0 END +
        CASE WHEN c."Substance Abuse" > 0.5 THEN 1 ELSE 0 END +
        CASE WHEN c.Vision > 0.5 THEN 1 ELSE 0 END +
        CASE WHEN c.Enabling > 0.5 THEN 1 ELSE 0 END AS "Service_Count"
    FROM 
        "Clinical Data & Services" AS c
    JOIN 
        "Health Center Information" AS h
    ON 
        c."Center ID" = h."Center ID"
)
SELECT 
    sa."City",
    sa."State",
    ROUND(pc."Patients at or below 200% of poverty", 2) AS Low_Income_Patients,
    ROUND(pc.Uninsured, 2) AS Uninsured_Patients,
    ROUND(age."Racial and/or Ethnic Minority", 2) AS Minority_Patients,
    ROUND(age."Older Adults (age 65 and over)", 2) AS Elderly_Patients,
    ROUND(cost."Total Cost Per Patient", 2) AS Total_Cost_Per_Patient,
    sa.Service_Count,
    
    CASE 
        WHEN sa."Service_Count" < 3 THEN 'Limited Access'
        ELSE 'Adequate Access'
    END AS "Access_Level"
FROM 
    Service_Access AS sa
JOIN 
    "Patient Characteristics" AS pc 
ON 
    sa."Center ID" = pc."Center ID"
JOIN 
    "Age, Race, Ethnicity" AS age 
ON 
    sa."Center ID" = age."Center ID"
JOIN 
    "Cost" AS cost 
ON 
    sa."Center ID" = cost."Center ID"
WHERE 
    pc."Patients at or below 200% of poverty" > 0.5 OR
    pc.Uninsured > 0.5 OR
    age."Racial and/or Ethnic Minority" > 0.5 OR
    age."Older Adults (age 65 and over)" > 0.5
ORDER BY 
    sa."City",
    sa."State",
    sa."Service_Count" ASC, 
    cost."Total Cost Per Patient" DESC;
"""

# Execute the query
cursor.execute(question_seven)

# Fetch results and create DataFrame
question_seven_results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]  # Extract column names from the query
results_df_q7 = pd.DataFrame(question_seven_results, columns=columns)

st.title("Question 7")
st.write("What top 5 cities/states have the highest costs, service count, or vulnerable patient proportions, and are they mainly in metro areas? Which bottom 5 have the lowest and are they in rural areas? How do states compare in average metrics based on selected criteria?")

st.dataframe(results_df_q7)

# Main layout: Select criteria using a selectbox
criteria = st.selectbox(
    "Select Criteria for Filtering Top/Bottom 5:",
    ["Total_Cost_Per_Patient", "Low_Income_Patients", "Uninsured_Patients", "Minority_Patients", "Elderly_Patients", "Service_Count"]
)

# Filter Top 5 and Bottom 5
top_5 = results_df_q7.nlargest(5, criteria)
bottom_5 = results_df_q7.nsmallest(5, criteria)

# Display the filtered data
st.title("Top 5 and Bottom 5 Health Centers")
st.subheader("Top 5 Health Centers")
st.dataframe(top_5)

st.subheader("Bottom 5 Health Centers")
st.dataframe(bottom_5)

# Combine Top 5 and Bottom 5 for visualization
combined_data = pd.concat([top_5, bottom_5])

# Create two columns for side-by-side charts
col1, col2 = st.columns(2)

# Top 5 Bar Chart
with col1:
    fig_top5 = px.bar(
        top_5.head(5),  
        x="City",  
        y=criteria,  
        #color="Service_Count", 
        hover_data=["State", "Service_Count", criteria],  
        title=f"Top 5 Centers by {criteria.replace('_', ' ')}"
    )
    st.plotly_chart(fig_top5)

# Bottom 5 Bar Chart
with col2:
    fig_bottom5 = px.bar(
        bottom_5.head(5), 
        x="City",  
        y=criteria,  
        #color="Service_Count",  
        hover_data=["State", "Service_Count", criteria],  
        title=f"Bottom 5 Centers by {criteria.replace('_', ' ')}"
    )
    st.plotly_chart(fig_bottom5)

# Map to show aggregated data at state levels
# Aggregate data at state level
state_data = results_df_q7.groupby("State").agg({criteria: "mean"}).reset_index()

# Choropleth Map for State-Level Aggregation
st.subheader(f"Choropleth Map of {criteria.replace('_', ' ')} by State")
fig_choropleth = px.choropleth(
    state_data,
    locations="State",  
    locationmode="USA-states",  
    color=criteria,  
    color_continuous_scale="Blues",
    scope="usa", 
    labels={criteria: criteria.replace("_", " ")}, 
    title=f"Choropleth Map of {criteria.replace('_', ' ')} by State"
)

# Display the Choropleth Map
st.plotly_chart(fig_choropleth)

st.write("""This choropleth map visualizes the average values of the selected metric across states, allowing you to compare how different 
        regions perform in terms of the chosen criteria, such as healthcare costs, patient demographics, or service availability. Darker shades represent
         higher values, while lighter shades indicate lower values, providing a clear geographic overview""")

########## QUESTION 8 ##########

question_eight = """
SELECT 
    hci.City AS City, 
    hci.State AS State,
    ROUND(AVG(are."Children (< 18 years old)"), 2) AS "Children (< 18 years old)", 
    ROUND(AVG(are."Adult (18 - 64)"), 2) AS "Adult (18 - 64)", 
    ROUND(AVG(are."Older Adults (age 65 and over)"), 2) AS "Older Adults (age 65 and older)", 
    ROUND(AVG(are."Hispanic/Latino Ethnicity"), 2) AS "Hispanic/Latino Ethnicity",
    ROUND(AVG(are."Black/African American"), 2) AS "Black/African American",
    ROUND(AVG(are."Asian"), 2) AS "Asian",
    ROUND(AVG(are."American Indian/Alaska Native"), 2) AS "American Indian/Alaska Native",
    ROUND(AVG(are."Native Hawaiian / Other Pacific Islander"), 2) AS "Native Hawaiian / Other Pacific Islander",
    ROUND(AVG(are."More than one race"), 2) AS "More than one race",
    ROUND(AVG(cd.Hypertension), 2) AS "Hypertension",
    ROUND(AVG(cd.Diabetes), 2) AS "Diabetes",
    ROUND(AVG(cd.Asthma), 2) AS "Asthma",
    ROUND(AVG(cd.HIV), 2) AS "HIV",
    ROUND(AVG(cd."Prenatal Patients"), 2) AS "Prenatal Patients",
    ROUND(AVG(cd."Cervical Cancer Screening"), 2) AS "Cervical Cancer Screening",
    ROUND(AVG(cd."Colorectal Cancer Screening"), 2) AS "Colorectal Cancer Screening",
    ROUND(AVG(cd."Depression Screening"), 2) AS "Depression Screening",
    ROUND(AVG(cd."Breast Cancer Screening"), 2) AS "Breast Cancer Screening"
FROM 
    "Health Center Information" AS hci
JOIN 
    "Age, Race, Ethnicity" AS are ON hci."Center ID" = are."Center ID"
JOIN 
    "Clinical Data & Services" AS cd ON hci."Center ID" = cd."Center ID"
WHERE 
    are."Children (< 18 years old)" IS NOT NULL
    AND are."Adult (18 - 64)" IS NOT NULL
    AND are."Older Adults (age 65 and over)" IS NOT NULL
    AND are."Hispanic/Latino Ethnicity" IS NOT NULL
    AND are."Black/African American" IS NOT NULL
    AND are."Asian" IS NOT NULL
    AND are."American Indian/Alaska Native" IS NOT NULL
    AND are."Native Hawaiian / Other Pacific Islander" IS NOT NULL
    AND are."More than one race" IS NOT NULL
    AND cd.Hypertension IS NOT NULL
    AND cd.Diabetes IS NOT NULL
    AND cd.Asthma IS NOT NULL
    AND cd.HIV IS NOT NULL
    AND cd."Prenatal Patients" IS NOT NULL
    AND cd."Cervical Cancer Screening" IS NOT NULL
    AND cd."Colorectal Cancer Screening" IS NOT NULL
    AND cd."Depression Screening" IS NOT NULL
    AND cd."Breast Cancer Screening" IS NOT NULL
GROUP BY 
    hci.City, hci.State
ORDER BY 
    hci.City, hci.State;
    """ 

# Execute the query
cursor.execute(question_eight)

# Fetch question_eight_results and create DataFrame
question_eight_results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]  # Extract column names from the query
results_df_q8 = pd.DataFrame(question_eight_results, columns=columns)

st.title("Question 8")
st.write("How do demographic factors such as average age and average race/ethnicity distributions correlate with key healthcare outcomes, including average rates of chronic conditions and preventive screenings, across different cities?")
st.dataframe(results_df_q8)

# Create a multiselect dropdown for states filter
states = results_df_q8['State'].unique()
selected_states = st.selectbox("Select State", options=["All States"] + list(states))

# Filter the data based on the selected state
if selected_states != "All States":
    filtered_df = results_df_q8[results_df_q8['State'] == selected_states]
else:
    filtered_df = results_df_q8

# Scatterplot for age demographics and healthcare outcomes
age_columns = ["Children (< 18 years old)", "Adult (18 - 64)", "Older Adults (age 65 and older)"]
healthcare_outcomes = ["Hypertension", "Diabetes", "Asthma", "HIV", "Prenatal Patients", "Cervical Cancer Screening", "Colorectal Cancer Screening", "Depression Screening", "Breast Cancer Screening"]

age_x_axis = st.selectbox("Select Age Demographic", options=age_columns, index=0)
healthcare_y_axis = st.selectbox("Select Healthcare Outcome", options=healthcare_outcomes, index=0)

st.subheader("Scatterplot: Age Demographics vs Healthcare Outcomes")
age_fig = px.scatter(
    filtered_df,
    x=age_x_axis,
    y=healthcare_y_axis,
    color="City",
    title=f"{age_x_axis} vs {healthcare_y_axis} by City",
    labels={"x": age_x_axis, "y": healthcare_y_axis},
    hover_data=["State", "City"]
)
st.plotly_chart(age_fig)

# Scatterplot for race/ethnicity and healthcare outcomes
race_columns = [
    "Hispanic/Latino Ethnicity",
    "Black/African American",
    "Asian",
    "American Indian/Alaska Native",
    "Native Hawaiian / Other Pacific Islander",
    "More than one race"
]

race_x_axis = st.selectbox("Select Race/Ethnicity Demographic", options=race_columns, index=0, key="race")

st.subheader("Scatterplot: Race/Ethnicity vs Healthcare Outcomes")
race_fig = px.scatter(
    filtered_df,
    x=race_x_axis,
    y=healthcare_y_axis,
    color="City",
    title=f"{race_x_axis} vs {healthcare_y_axis} by City",
    labels={"x": race_x_axis, "y": healthcare_y_axis},
    hover_data=["State", "City"]
)
st.plotly_chart(race_fig)

st.write("""After the user selects their criteria (age group or racial/ethnic demographic and 
    healthcare outcome), the scatterplots provide insights into the relationship between 
    demographic factors and healthcare outcomes across different cities within the selected state.""")

st.write("""The scatterplots highlight trends and disparities in healthcare outcomes across cities. For example, 
        cities with more older adults might have higher rates of chronic conditions, while those with larger racial or ethnic populations 
        could show disparities in outcomes like asthma or cancer screenings. Outliers may reveal unique local factors, offering insights 
        into healthcare needs and equity across regions.""")

# Close the connection
connection.close()