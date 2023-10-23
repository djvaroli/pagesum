import time
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .utils.notion import get_notion_client
from .utils.html import get_page_html, strip_html
from .utils.ai import Summarizer, TextSummary


app = FastAPI()

# Allow CORS for all origins:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PageInfo(BaseModel):
    url: str
    title: str
    type: Literal["paper", "blog"]  
    summary: str = ""


@app.get("/summary")
async def get_summary(url: str) -> TextSummary:
    summarizer = Summarizer(model="gpt-3.5-turbo-16k")

    try:
        page_html = get_page_html(url)
        page_text = strip_html(page_html)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Failed to get page text."})

    try:
        summary = summarizer.summarize(page_text)
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Failed to summarize text."})

    print(summary.summary, url, summary.usage)

    return summary


@app.post("/save")
async def save_page_info(page_info: PageInfo):
    client = get_notion_client()
    
    blog_db_id = "455cd96609664d30bb450d61c615096e"
    paper_db_id = "fb968a68483141de93570208b17b223c"

    if page_info.type == "paper":
        db_id = paper_db_id
    elif page_info.type == "blog":
        db_id = blog_db_id
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid page type."})

    client.pages.create(
        parent={"database_id": db_id},
        properties={
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": page_info.title
                        }
                    }
                ]
            },
            "URL": {
                "rich_text": [
                    {
                        "text": {
                            "content": page_info.url,
                            "link": {
                                "url": page_info.url
                            }
                        },
                    }
                ]
            },
            "Summary": {
                "rich_text": [
                    {
                        "text": {
                            "content": page_info.summary
                        }
                    }
                ]
            }
        }
    )
    
    return {"message": "Data received!"}
    


