import streamlit as st
import pandas as pd
import numpy as np
import os
from supabase import create_client, Client


def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)

supabase = get_client()
    
def getMovies():
        res = supabase.table("IMDB").select("*").execute()
        return res.data

def searchMovie(imdb = None, year = None):
    query = supabase.table("IMDB").select("*")
    if year:
        query = query.like("year",f"%{year}%")
    if imdb:
        query = query.gte("rating",imdb)
    return query.execute().data



def main():
    st.title("Movie Finder")
    st.subheader('Minh Hoang Bui')
    
    all_movies = getMovies()
    ratings = [m["rating"] for m in all_movies if m.get("rating") is not None]
    rating_counts = pd.Series(ratings).value_counts().sort_index()
    st.subheader("Number of Movies by Rating")
    st.bar_chart(rating_counts)

   
    year = st.number_input("Year",min_value=2011, max_value=2100, step=1)
    imdb = st.slider("Minimum IMDB rating", 0.0, 10.0, 5.0)
    sort_by = st.selectbox("Sort by", ["Title", "Rating"])
    sort_ascending = st.checkbox("Sort ascending", value=True)
    
    if st.button("Search"):
        
        res = searchMovie(imdb,year)
        
        if res:
            
            st.header(f"Found {len(res)} movies!")
            if sort_by == "Title":
                sorted_res = sorted(res, key=lambda x: x.get('title', ''), reverse=not sort_ascending)
            else: 
                sorted_res = sorted(res, key=lambda x: x.get('rating', 0), reverse=not sort_ascending)
            for movie in sorted_res:
                with st.expander(f"{movie['title']} {movie['year']} - IMDB: {movie['rating']}"):
                    st.write(movie['description'])
                
        else:
            st.write("No movies found.")

    
if __name__ == "__main__":
    main()