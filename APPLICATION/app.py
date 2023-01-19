# IMPORTING TOOLS
import streamlit as st
from rdflib import Graph, Literal
from rdflib.plugins.sparql import prepareQuery
import pandas as pd
import plotly.express as px
import numpy as np
import sparql_dataframe

# SET PAGE SETTINGS
st.set_page_config(page_title='Alto Adige Turism', layout="centered")

# CONFIGURE THE ENDPOINT
endpoint = "http://localhost:8080/sparql"

# METHOD TO CONVERT THE QUERY RESULT INTO A DATAFRAME
def sparql_results_to_df(results):
    return pd.DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in results),
        columns=[str(x) for x in results.vars],
    )

# METHOD TO EXECUTE A GENERIC QUERY 
def computeQuery(query, executor):
    result = executor.query(query)
    res_df = sparql_results_to_df(result)
    return res_df

def computeQuery(query, endpoint):
    res_df = sparql_dataframe.get(endpoint, query)
    return res_df

# METHOD TO EXECUTE A PARAMETRIC QUERY
def rideAccidentDescription(ride_name, executor):
        ride_name = Literal(ride_name)
        query = """
            PREFIX ride_type: <http://example.org/ride_type#>
            PREFIX acc: <http://example.org/accident#>
            PREFIX ride: <http://example.org/ride#>
            SELECT (?manuf AS ?Manufacturer) (?description AS ?Accident_Description)
            WHERE {
                ?instance acc:description ?description ;
                          acc:ref-ride_id ?ride_id .
                ?ride_id ride:name ?name ;
                         ride:manufacturer ?manuf .
                FILTER (?name = ?ride_name)
            }
        """
        prep_query = prepareQuery(query)
        r = executor.query(prep_query, initBindings={'ride_name': ride_name})
        return sparql_results_to_df(r), query

# PROCESSING & DISPLAY
def display():
    with st.container():
        st.write("#### What are the 10 cities with the highest number of accomodations?")
        res = computeQuery(query_1, endpoint=endpoint)
        fig = px.bar(res, x="city", y="count", color="count", labels={"ciry":"City", "count":"Num. of Accomodations"}, text_auto="True")
        fig.update_xaxes(type="category")
        fig.update_yaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Show query"):
            st.code(query_1, language="sparql")
        st.markdown("---")

    with st.container():
        st.write("#### What are the 10 cities with the highest number of events?")
        res = computeQuery(query_2, endpoint=endpoint)
        fig = px.bar(res, x="city", y="count", color="count", labels={"ciry":"City", "count":"Num. of Events"}, text_auto="True")
        fig.update_xaxes(type="category")
        fig.update_yaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Show query"):
            st.code(query_2, language="sparql")
        st.markdown("---")

    with st.container():
        st.write("#### What are names, phone numbers, and adrresses of accomodations in Merano?")
        res = computeQuery(query_3, endpoint=endpoint)
        res_count = res.count()[0]
        if (res_count < 3):
            st.table(res)
        else:
            limit = st.slider("Num. of Accomodations to Visualize", 1, int(res_count), 2, 1)
            st.table(res[:limit])
        with st.expander("Show query"):
            st.code(query_3, language="sparql")
        st.markdown("---")

    return None

# ANALYTICAL QUERIES DEFINITION
# get the names of all the rides
query_0 = """
    PREFIX ride:<http://example.org/ride#>        

    SELECT DISTINCT ?name
    WHERE {
        ?ride ride:name ?name .
    }
"""
# 10 cities with highest number of accomodations
query_1 = """
    PREFIX accomodation: <http://example.org/accomodation#>
    PREFIX location: <http://example.org/location#>

    SELECT ?city (COUNT(?accomodation) AS ?count)
    WHERE {
        ?accomodation accomodation:ref-location_id ?location .
        ?location location:city ?city .
    }
    GROUP BY ?city
    ORDER BY DESC(?count)
    LIMIT 10
"""

# 10 cities with highest number of events
query_2 = """
    PREFIX event: <http://example.org/event#>
    PREFIX location: <http://example.org/location#>
    SELECT ?city (COUNT(?event) as ?count) 
    WHERE {
        ?event event:ref-location_id ?location .
        ?location location:city ?city .
    } GROUP BY ?city
    ORDER BY DESC(?count)
    LIMIT 10
"""

# accomodations in Merano
query_3 = """
    PREFIX accomodation: <http://example.org/accomodation#>
    PREFIX location: <http://example.org/location#>
    SELECT ?name ?acco_type ?street ?phone
    WHERE {
        ?loc_id location:city "Merano" ;
                location:street ?street .
        ?id accomodation:ref-location_id ?loc_id ;
            accomodation:name ?name ;
            accomodation:acco_type_id ?acco_type ;
            accomodation:phone ?phone .
    }
"""



# TITLE
st.header("Turism and Events in South Tyrol")
st.markdown("""
Welcome to the South Tyrol Event and Accommodation Explorer! With this simple app you can discover events and accommodations in the region. 
Browse data and visualizations, filter by location and date, and plan your perfect trip. Start exploring now!
""")
st.markdown("---")

display()

# WRITE & RUN YOUR OWN QUERY
st.write("#### Write & Run your Custom Query")
pers_query = st.text_area('', """
    PREFIX acco: <http://example.org/accomodation#>
    SELECT *
    WHERE {
        ?acco acco:has_room True .
        ?acco acco:name ?name ;
            acco:phone ?phone .
    }
    LIMIT 5
""", height=200)
with st.container():
    try:
        res = computeQuery(pers_query, endpoint=endpoint)
        st.table(res)
    except:
        st.error("Ooops! Check you query syntax...")
    st.markdown("---")

# SIDEBAR
with st.sidebar:
    st.write("""
    This App proposes some visualizations about events and accommodations in South Tyrol. 
    The data, which comes from the Open Data Hub South Tyrol, was collected using the public API and is in JSON format. 
    The data was then converted to CSV, profiled, preprocessed and uploaded to a relational database. 
    Using the Ontop tool and an ontology, a Virtual Knowledge Graph was created and queried with SPARQL.
    """)
    st.markdown("---")
    st.markdown("## Dataset Resources:")
    st.markdown("""
        Accomodations: https://opendatahub.com/datasets/tourism/accommodation_one/

        Events: https://opendatahub.com/datasets/tourism/events/

        Parking: https://opendatahub.com/datasets/traffic/parking/
        """)
