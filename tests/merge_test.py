from core.models.result import ScrapeResult, Source, SourceType, WrappedFloat
from core.merge import merge_scrape_results

def test_merge_scrape_results_1():
    wf_1 = WrappedFloat(value=1.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.WEBSITE))
    wf_2 = WrappedFloat(value=2.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.WEBSITE))
    result_1 = ScrapeResult(scope_1=wf_1, scope_2=wf_2, scope_3=WrappedFloat(value=3.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.WEBSITE)))
    result_2 = ScrapeResult(scope_1=wf_1, scope_2=wf_2)
    result = merge_scrape_results(result_1, result_2)
    assert result.scope_1.value == 1.0
    assert result.scope_2.value == 2.0
    assert result.scope_3.value == 3.0

def test_merge_scrape_results_2():
    wf_1 = WrappedFloat(value=1.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.PDF))
    wf_2 = WrappedFloat(value=2.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.WEBSITE))
    result_1 = ScrapeResult(scope_1=wf_1, scope_2=wf_2)
    result_2 = ScrapeResult(scope_1=wf_1, scope_2=wf_2)
    result = merge_scrape_results(result_1, result_2)
    assert result.scope_1.value == 1.0
    assert result.scope_2.value == 2.0
    assert result.scope_3 is None

def test_merge_scrape_results_3():
    wf_1 = WrappedFloat(value=1.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.PDF))
    wf_2 = WrappedFloat(value=2.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.WEBSITE))
    wf_3 = WrappedFloat(value=3.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.PDF))
    result_1 = ScrapeResult(scope_1=wf_1, scope_2=wf_2)
    result_2 = ScrapeResult(scope_1=wf_1, scope_3=wf_3)
    result = merge_scrape_results(result_1, result_2)
    assert result.scope_1.value == 1.0
    assert result.scope_2.value == 2.0
    assert result.scope_3.value == 3.0
    assert result.scope_2.source == wf_2.source
    assert result.scope_3.source == wf_3.source

def test_merge_scrape_results_4():
    result_1 = ScrapeResult()
    wf_2 = WrappedFloat(value=2.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.WEBSITE))
    wf_3 = WrappedFloat(value=3.0, source=Source(url="https://www.example.com", page=1, src_type=SourceType.PDF))
    result_2 = ScrapeResult(scope_2=wf_2, scope_3=wf_3)
    result = merge_scrape_results(result_1, result_2)
    assert result.scope_1 is None
    assert result.scope_2.value == 2.0
    assert result.scope_3.value == 3.0