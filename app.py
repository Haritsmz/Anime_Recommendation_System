import streamlit as st
from PIL import Image
import pickle
import warnings
warnings.filterwarnings(action='ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import time

df1_anime_cleaned=pickle.load(open("anime_recommendation.pkl","rb"))
similarity=pickle.load(open("similarity.pkl", "rb"))

# Sidebar
st.sidebar.title("Anime Dashboard")
selected_visualization = st.sidebar.selectbox("Select Visualization", ["Anime Type Counts", "Score vs Members",
                                                                      "Top 10 Animes by Members", "Anime Genres Counts",
                                                                      "Top 10 Genres", "Word Cloud - Genres", "Distribution of Anime Scores by Type", 
                                                                      "Relationship between Popularity, Number of Scores, and Score", 
                                                                      "Correlation Matrix", "Top Studios", "Animes by Source", "Top 20 Most Favorited Anime"])

# Main content
st.title("Visualization")

# Visualizations
if selected_visualization == "Anime Type Counts":
    # Bar chart for anime type counts
    st.subheader("Anime Type Counts")
    type_counts = df1_anime_cleaned[df1_anime_cleaned['Type'] != 'Unknown']['Type'].value_counts()
    st.bar_chart(type_counts)
    
elif selected_visualization == "Score vs Members":
    # Scatterplot for Score vs Members
    st.subheader("Score vs Members")
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df1_anime_cleaned, x='Score', y='Members', color='blue', alpha=0.5)
    plt.xlabel('Overall Score')
    plt.ylabel('Number of Scores')
    plt.title('Anime Score vs Number of Scores')
    st.pyplot(plt.gcf())

elif selected_visualization == "Top 10 Animes by Members":
    # Bar chart for top 10 animes by members
    st.subheader("Top 10 Animes by Members")
    top_10_scored = df1_anime_cleaned.sort_values(by='Members', ascending=False).head(10)
    st.bar_chart(top_10_scored.set_index('Name')['Members'])
    
elif selected_visualization == "Anime Genres Counts":
    # Bar chart for anime genres counts
    st.subheader("Anime Genres Counts")
    df1_anime_cleaned['Genres'] = df1_anime_cleaned['Genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    genre_counts = df1_anime_cleaned[df1_anime_cleaned['Genres'] != "Unknown"]['Genres'].apply(lambda x: x.split(', ')).explode().value_counts()
    st.bar_chart(genre_counts)

elif selected_visualization == "Top 10 Genres":
    # Bar chart for top 10 genres
    st.subheader("Top 10 Genres")
    df1_anime_cleaned['Genres'] = df1_anime_cleaned['Genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    genre_counts = df1_anime_cleaned[df1_anime_cleaned['Genres'] != "Unknown"]['Genres'].apply(lambda x: x.split(', ')).explode().value_counts()
    top_10_genres = genre_counts.head(10)
    st.bar_chart(top_10_genres)

elif selected_visualization == "Word Cloud - Genres":
    # Word embedding plot - Genres
    st.subheader("Word Cloud - Genres")
    genre_text = ' '.join(df1_anime_cleaned[df1_anime_cleaned['Genres'] != "Unknown"]['Genres'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(genre_text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word Embedding Plot - Genre', fontsize=16)
    plt.axis('off')
    st.pyplot(plt.gcf())
    
elif selected_visualization == "Distribution of Anime Scores by Type":
    # Box plot for anime scores by type
    st.subheader("Distribution of Anime Scores by Type")
    df1_anime_cleaned_filtered = df1_anime_cleaned[df1_anime_cleaned['Type'] != 'Unknown']
    sns.boxplot(data=df1_anime_cleaned_filtered, x='Type', y='Score', palette=['skyblue', 'salmon', 'lightgreen', 'gold', 'lightcoral', 'darkblue'])
    plt.xlabel("Anime Type")
    plt.ylabel("Score")
    plt.title("Distribution of Anime Scores by Type")
    st.pyplot(plt.gcf())
    
elif selected_visualization == "Relationship between Popularity, Number of Scores, and Score":
    # Scatterplot Relationship between Popularity, Number of Scores, and Score
    st.subheader("Relationship between Popularity, Number of Scores, and Score")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df1_anime_cleaned, x="Popularity", y="Members", size="Score", hue="Type", palette="viridis", alpha=0.7)
    plt.xlabel("Popularity")
    plt.ylabel("Number of Scores")
    plt.title("Relationship between Popularity, Number of Scores, and Score")
    plt.legend()
    st.pyplot(fig)
    
elif selected_visualization == "Correlation Matrix":
    # Heatmap "Correlation Matrix"
    st.subheader("Correlation Matrix")
    correlation_matrix = df1_anime_cleaned[['Score', 'Popularity', 'Ranked']].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='viridis', fmt=".2f", linewidths=.5, ax=ax)
    plt.title('Correlation Matrix')
    st.pyplot(fig)

elif selected_visualization == "Top Studios":
    # Bar plot for top studios
    st.subheader("Top Studios")
    studio_counts = df1_anime_cleaned['Studios'].value_counts()
    studio_counts = studio_counts[studio_counts.index != 'Unknown']
    top_studios = studio_counts.head(15)
    st.bar_chart(top_studios)

elif selected_visualization == "Animes by Source":
    # Horizontal bar chart for animes by source
    st.subheader("Animes by Source")
    source_counts = df1_anime_cleaned['Source'].value_counts()
    source_counts = source_counts[source_counts.index != 'Unknown']
    st.bar_chart(source_counts)

else:
    # Horizontal bar chart for top 20 most favorited anime
    st.subheader("Top 20 Most Favorited Anime")
    sorted_df = df1_anime_cleaned.sort_values('Favorites', ascending=False)
    top_favorites = sorted_df.head(20)
    st.bar_chart(top_favorites.set_index('Name')['Favorites'])
    
st.title("Anime Recommendation App")
img = Image.open('anime_image1.jpg')
st.image(img, width=700)

list_anime=np.array(df1_anime_cleaned["Name"])
option = st.selectbox(
"Select Anime ",
(list_anime))

def anime_recommend(anime):
    if anime not in df1_anime_cleaned['Name'].values:
        st.warning(f"Anime '{anime}' not found in the DataFrame.")
        return None
    index = df1_anime_cleaned[df1_anime_cleaned['Name'] == anime].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    anime_recommendations = []
    filtered_genre = ['Hentai']
    for i in distances[1:11]:
        if 0 <= i[0] < len(df1_anime_cleaned):
            anime_row = df1_anime_cleaned.iloc[i[0]]
            if not any(genre in anime_row['Genres'] for genre in filtered_genre):
                anime_recommendations.append(df1_anime_cleaned.iloc[i[0]])
            elif len(anime_recommendations) == 0 and anime_row['Genres'] != filtered_genre:
                anime_recommendations.append(df1_anime_cleaned.iloc[i[0]])
 
    recommended_df = pd.DataFrame(anime_recommendations)[['Name', 'Score', 'Genres', 'Synopsis', 'Type', 'Ranked', 'Studios']]

    return recommended_df

if st.button('Recommend Me'):
    st.write('Anime Recommended for you are:')
    recommended_anime_df = anime_recommend(option)
    if recommended_anime_df is not None:
        with st.spinner(text='Wait a moment...'):
            recommended_anime_df = anime_recommend(option)
            time.sleep(2)
            st.success('Done')
            recommendations = len(recommended_anime_df)
            for i in range(10):
                if i < len(recommended_anime_df):
                    row = recommended_anime_df.iloc[i]
                    try:
                        Ranked = int(row['Ranked'])
                    except (ValueError, TypeError):
                        Ranked = None
                    st.write(f"{i + 1}) Title: {row['Name']}")
                    st.write(f"   Synopsis: {row['Synopsis']}")
                    st.write(f"   Score: {row['Score']}")
                    st.write(f"   Genre: {row['Genres']}")
                    st.write(f"   Type: {row['Type']}")
                    st.write(f"   Ranked: {Ranked}")
                    st.write(f"   Studio: {row['Studios']}")
                    st.write("\n")
