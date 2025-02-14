import arxiv
from datetime import datetime, timedelta, timezone
from config import Config

class ArxivClient:
    def __init__(self):
        self.search_query = Config.ARXIV_SEARCH_QUERY
        self.days = Config.ARXIV_SEARCH_DAYS
        self.num = Config.ARXIV_SEARCH_NUM

    def get_recent_papers(self):
        search = arxiv.Search(
            query=self.search_query,
            max_results=self.num,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        tz_east8 = timezone(timedelta(hours=8))
        threshold_date = datetime.now(tz=tz_east8) - timedelta(days=self.days)

        papers = []
        try:
            for result in search.results():
                published_east8 = result.published.astimezone(tz_east8)
                if published_east8 >= threshold_date:
                    papers.append({
                        'title': result.title,
                        'summary': result.summary,
                        'download_url': result.pdf_url,
                        'published': published_east8  
                    })
        except arxiv.UnexpectedEmptyPageError as e:
            print(f"警告：遇到空页面，错误信息：{e}")
        return papers
