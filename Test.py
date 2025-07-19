import asyncio
import asyncpraw
from datetime import datetime

async def search_reddit(query):
    # ✅ 初始化放在协程内
    reddit = asyncpraw.Reddit(
        client_id="jBLXT3Y1tzJYJg0jwIR1Zw",
        client_secret="WjWJKu4QDTNANmTAhMYNHyRLTSEWlg",
        user_agent="sentiment-analyzer-async"
    )

    subreddit = await reddit.subreddit("all")
    submissions = subreddit.search(query, sort="relevance", limit=20)

    tasks = []
    async for submission in submissions:
        if submission.score < 3:
            continue
        if submission.is_self and len(submission.selftext) < 50:
            continue
        if "[removed]" in submission.selftext.lower():
            continue
        tasks.append(fetch_post_details(submission))

    await asyncio.gather(*tasks)
    await reddit.close()  # ✅ 记得关闭 reddit 会话，避免 Unclosed client session

async def fetch_post_details(submission):
    await submission.load()
    created_time = datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
    content = submission.selftext.strip() if submission.selftext else f"[🔗 外部链接] {submission.url}"

    print("🧵" + "═" * 78)
    print(f"📝 标题     : {submission.title}")
    print(f"👤 作者     : {submission.author}")
    print(f"🕒 时间     : {created_time}")
    print(f"👍 分数     : {submission.score}")
    print(f"💬 评论数   : {submission.num_comments}")
    print(f"🔗 链接     : https://reddit.com{submission.permalink}")
    print(f"📄 内容     :\n{content[:500]}")

    try:
        await submission.comments.replace_more(limit=0)
        top_comments = submission.comments[:3]
        print(f"\n🗨️ 精选评论:")
        for idx, comment in enumerate(top_comments, 1):
            print(f"   💬 评论 {idx}: {comment.body[:200].replace('\n', ' ')}")
    except Exception as e:
        print(f"⚠️ 获取评论失败: {e}")

    print("🧵" + "═" * 78 + "\n")

if __name__ == "__main__":
    asyncio.run(search_reddit("AI"))
