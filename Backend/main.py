from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

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
