from core.models.result import ScrapeResult

def merge_scrape_results(result_1: ScrapeResult, result_2: ScrapeResult) -> ScrapeResult:
    result = ScrapeResult()
    result.scope_1 = result_1.scope_1 or result_2.scope_1
    result.scope_2 = result_1.scope_2 or result_2.scope_2
    result.scope_3 = result_1.scope_3 or result_2.scope_3
    return result
