import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title('Schools in New York based on your Preferences:')

st.sidebar.title("Filters:")

def loadata():
    data = pd.read_excel('data/data.xlsx', index_col=None)
    return data

data = loadata()

print(data)

Borough = st.sidebar.multiselect('What Boroughs do you want the school to be located in?',
                 options=data["Borough"].unique())

Grades = st.sidebar.multiselect('Grades available in the school:',
                 options=data["grades2018"].unique())

TotalStudents = st.sidebar.slider('Numbers of Students in the School:',
                            min_value=int(data["total_students"].min()), max_value=int(data["total_students"].max()))


mask=data["Borough"].isin(Borough)
data=data[mask]

mask=data["total_students"]<=TotalStudents
data=data[mask]

mask=data["grades2018"].isin(Grades)
data=data[mask]

for index, row in data.iterrows():

     with st.expander(row["school_name"]):

        st.header(row['school_name'])

        col1, col2 = st.columns(2)

        with col1:

            mask = data["school_name"] == row["school_name"]
            datamap = data[mask]
            fig = px.scatter_mapbox(lat= datamap["Latitude"],
                                    lon=datamap["Longitude"],
                                    hover_name=datamap["school_name"],
                                    color_discrete_sequence=["blue"],
                                    zoom=11,
                                    height=200, width = 100
                                    )
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig)

        with col2:
            st.subheader('Overview: ')
            st.write(""
                     "{}".format(row["overview_paragraph"]))

        st.header('More Details:')

        st.write("Neighborhood: {}".format(row["neighborhood"]))
        st.write("Address: {}".format(row["location"]))

        col3, col4 = st.columns(2)
        with col3:
            st.write("Phone Number: {}".format(row["phone_number"]))
        with col4:
            st.write("Email: {}".format(row["school_email"]))
        st.markdown('[Website](https://{})'.format(row['website']))

        st.subheader('Classes Offered:')
        col5, col6 = st.columns(2)
        with col5:
            st.write('Language Classes: {}'.format(row['language_classes']))
        with col6:
            st.write('AP classes: {}'.format(row['advancedplacement_courses']))

        st.subheader('School Rates:')
        col5, col6 = st.columns(2)
        with col5:
            st.write('Graduation Rate: {}%'.format(row['graduation_rate']*100))
        with col6:
            st.write('Attendance Rate: {}%'.format(row['attendance_rate']*100))
