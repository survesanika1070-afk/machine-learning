import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="News Clustering App",
    page_icon="📰",
    layout="centered"
)

st.title("📰 News Clustering App")
st.write("Group news articles into topics using Unsupervised Learning")

# ===============================
# Sample Dataset (Replace with CSV if needed)
# ===============================
data = pd.DataFrame({
    "text": [
        "Government passes new law in parliament",
        "Election results spark political debate",
        "Stock markets rise as economy improves",
        "New AI technology is transforming industries",
        "New smartphone released with advanced features",
        "Scientists discover new species in ocean",
        "Football team wins championship",
        "Basketball tournament draws huge crowd"
    ]
})

# ===============================
# Train Model
# ===============================
@st.cache_resource
def train_model():
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data['text'])

    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)

    return vectorizer, kmeans

vectorizer, kmeans = train_model()

# ===============================
# User Input
# ===============================
st.subheader("✍️ Enter News Text")
user_input = st.text_area("Type or paste your news article here:")

# ===============================
# Predict Button
# ===============================
if st.button("🔍 Predict Cluster"):
    if user_input.strip() == "":
        st.warning("Please enter some text!")
    else:
        input_vector = vectorizer.transform([user_input])
        cluster = kmeans.predict(input_vector)[0]

        # Optional Labels
        labels = {
            0: "🟣 Politics",
            1: "🟢 Business/Sports",
            2: "🔵 Technology/Science"
        }

        st.success(f"Predicted Category: {labels.get(cluster, cluster)}")

# ===============================
# Show Sample Data
# ===============================
if st.checkbox("📊 Show Sample Dataset"):
    st.write(data)

# ===============================
# Footer
# ===============================
st.markdown("---")
st.caption("Built using Streamlit & Machine Learning")