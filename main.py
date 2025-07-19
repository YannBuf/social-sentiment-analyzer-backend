from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v2 import sentence_sentiment_analysis
from api.auth import auth
from api.auth import me
from api.v2 import smart_search
from api.v2 import smart_search_analyze

from api.v2.analysis_report import sentiment_analysis, overall, platform_analysis, keywords_analysis
from api.v2 import dashboard,dashboard_modify
from api.v2 import search_history
from api.v2 import get_search_analysis_records
# Initial App
app = FastAPI()

# Allow all front end access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4.Router
'''
app.include_router(chat_with_chatgpt.router)
app.include_router(reddit_search.router)
app.include_router(auth.router)
app.include_router(register.router)
app.include_router(posts.router)
app.include_router(reddit_analysis_router.router)
app.include_router(reddit_analysis_each_router.router)
'''
app.include_router(sentence_sentiment_analysis.router, prefix="/api")
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(me.router, prefix="/api", tags=["auth"])
app.include_router(smart_search.router, prefix="/api")
app.include_router(smart_search_analyze.router, prefix="/api")

app.include_router(sentiment_analysis.router, prefix="/api", tags=["analysis reports"])
app.include_router(overall.router, prefix="/api", tags=["analysis reports"])
app.include_router(platform_analysis.router, prefix="/api", tags=["analysis reports"])
app.include_router(keywords_analysis.router, prefix="/api", tags=["analysis reports"])

app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
app.include_router(dashboard_modify.router, prefix="/api", tags=["dashboard"])

app.include_router(search_history.router, prefix="/api", tags=["search history"])

app.include_router(get_search_analysis_records.router, prefix="/api", tags=["search history"])