# Anime Recommendation System: Project Overview
## Background
Anime holds a special place in my heart, providing support and inspiration in moments of solitude and failure. For many, anime is not just entertainment; it's a loyal companion in loneliness, a source of inspiration in failure, and an art form that captures the essence of human emotions. Anime not only presents stories but also has the ability to depict the strength of determination, spirit, and courage that can motivate viewers. In its uniqueness, anime can touch emotions that are difficult to explain through other forms of entertainment.

A common question that arises after watching an anime is, "If I liked this anime, what other anime is suitable for me?" or "What anime can provide a similar experience?". After watching numerous anime, I wondered, if I had to recommend one anime to someone, which anime should it be, and even for myself?. Therefore, with this motivation, I embarked on creating this anime recommendation project.
## Project Goal
Build a content-based anime recommendation system that provides recommendations based on the similarity of features among anime and integrate visualizations within the Streamlit application to illustrate the underlying data. 
In this project, my main focus is to provide recommendations based on the plot synopsis of anime. Users who enjoy anime based on specific genres may be interested in other anime with similar plot synopsis.
<ul>
      <li>Used CountVectorizer to convert words in the plot synopsis into vectors.</li>
      <li>Calculated linear kernel to create a function that recommends anime with similar plot synopsis</li>
</ul>

## Code and Resources Used:
<ul>
      <li>Python Version: 3.10.0</li>
      <li>Packages: numpy, pandas, matplotlib, seaborn, wordcloud, sklearn, streamlit</li>
      <li>Dataset: https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset</li>
</ul>

## Content-Based Recommendeation System
Content-based recommendation system is an algorithm that provides recommendations to users based on the characteristics and features of an item, as well as the user's historical preferences. This algorithm analyzes the content or attributes of an item and understands user preferences by comparing these attributes with the user's previous interactions or explicit preferences. For example, in a movie recommendation system, a content-based algorithm might consider factors such as genre, director, actors, and user ratings. This system is particularly useful for recommending items that have similar content to items the user has liked in the past. Its main advantage is that it doesn't rely on collaborative filtering or user behavior patterns, making it suitable for situations where user data is limited or privacy is a priority.
