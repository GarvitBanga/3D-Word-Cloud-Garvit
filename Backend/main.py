from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

app = FastAPI()

def get_stopwords():
    try:
        return set(stopwords.words('english')).union({
            'said', 'says', 'would', 'could', 'also', 'mr', 'ms', 'mrs', 'one', 'two', 'new', 'year', 'years', 'time', 'people'
        })
    except LookupError:
        nltk.download('stopwords')
        return set(stopwords.words('english'))

STOPWORDS = get_stopwords()

def extract_text(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            script.decompose()
            
        # Get text
        text = " ".join([p.get_text() for p in soup.find_all('p')])
        
        # Simple cleanup
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch document: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

def perform_topic_modeling(text: str, n_topics=5, n_words=10):
    try:
        sentences = sent_tokenize(text)
    except Exception:
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 3]
    
    if len(sentences) < 5:
        try:
             words = word_tokenize(text.lower())
        except:
             words = re.findall(r'\w+', text.lower())
        c = Counter([w for w in words if w.isalpha() and w not in STOPWORDS and len(w) > 2])
        return [{"word": w, "weight": count} for w, count in c.most_common(n_topics * n_words)]

    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words=list(STOPWORDS))
    try:
        tf = tf_vectorizer.fit_transform(sentences)
    except ValueError:
        try:
             words = word_tokenize(text.lower())
        except:
             words = re.findall(r'\w+', text.lower())
        c = Counter([w for w in words if w.isalpha() and w not in STOPWORDS and len(w) > 2])
        return [{"word": w, "weight": count} for w, count in c.most_common(n_topics * n_words)]
        
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
    lda.fit(tf)
    tf_feature_names = tf_vectorizer.get_feature_names_out()
    results = {}
    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[:-n_words - 1:-1]
        for i in top_indices:
            word = tf_feature_names[i]
            weight = topic[i]
            if word not in results:
                results[word] = weight
            else:
                results[word] = max(results[word], weight)
    max_weight = max(results.values()) if results else 1
    structured_data = [{"word": w, "weight": (wt / max_weight) * 10} for w, wt in results.items()]
    return sorted(structured_data, key=lambda x: x['weight'], reverse=True)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "3D Word Cloud Backend"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    if not request.url:
         raise HTTPException(status_code=400, detail="URL is required")
    text = extract_text(request.url)
    if not text or len(text) < 50:
        raise HTTPException(status_code=400, detail="Could not extract enough text from the URL.")
    topics = perform_topic_modeling(text)
    return {"topics": topics}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
