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
  
    year = st.number_input("Year",min_value=1932, max_value=2100, step=1)
    imdb = st.slider("Minimum IMDB rating", 0.0, 10.0, 5.0)
    sort_by = st.selectbox("Sort by", ["Title", "Rating"])
    sort_ascending = st.checkbox("Sort ascending", value=True)
    
    if st.button("Search"):
        
        res = searchMovie(imdb,year)
        
        if res:
            ratings = [m["rating"] for m in res if m.get("rating") is not None]
            hist_values, bins = np.histogram(ratings, bins=10, range=(0.0, 10.0))
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            hist_df = pd.DataFrame({
                "Rating": bin_centers,
                "Number of Movies": hist_values
            })
            st.bar_chart(hist_df.set_index("Rating"))
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