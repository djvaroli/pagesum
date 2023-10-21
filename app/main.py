import os

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rich.console import Console
from rich.markdown import Markdown
from notion_client import Client
from dotenv import load_dotenv


load_dotenv(".env")


app = FastAPI()

# Allow CORS for all origins:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PageSummary(BaseModel):
    url: str
    title: str


@app.post("/save")
async def save_page_info(page_summary: PageSummary):
    console = Console()
    content = Markdown(f"# {page_summary}")
    console.print(content)
    
    notion = Client(auth=os.environ["NOTION_TOKEN"])

    db_id = "455cd96609664d30bb450d61c615096e"
    
    notion.pages.create(
        parent={"database_id": db_id},
        properties={
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": page_summary.title
                        }
                    }
                ]
            },
            "URL": {
                "rich_text": [
                    {
                        "text": {
                            "content": page_summary.url,
                            "link": {
                                "url": page_summary.url
                            }
                        },
                    }
                ]
            }
        }
    )
    
    return {"message": "Data received!"}
    


