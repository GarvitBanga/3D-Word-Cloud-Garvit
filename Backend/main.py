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

@app.get("/")
def read_root():
    return {"status": "ok", "service": "3D Word Cloud Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
