import json
import os
from datetime import datetime
from typing import List, Dict, Any

from src.utils.performance_monitor import monitor_performance
from src.core.analysis.entity_extractor import EntityExtractor

# Global list to collect all entities across sources
all_entities: List[Dict[str, str]] = []

entity_extractor = EntityExtractor()

def process_intelligence(target_urls: List[str], analyzer, preprocessor, pinecone, ingestor, console) -> List[Dict[str, Any]]:
    """Process each URL: fetch, clean, summarize, extract entities, store.
    Returns a list of report entries for each source.
    """
    report_entries = []
    for url in target_urls:
        console.print(f"\nProcessing: [dim]{url}[/dim]")
        raw = ingestor.fetch_osint([url])
        if not raw or raw[0].get('status') != 'success':
            continue
        content = raw[0]['content']
        cleaned_text = preprocessor.clean_text(content)
        summary = analyzer.generate_summary(cleaned_text)
        console.print(f"[bold]Summary:[/bold] {summary[:200]}...")
        # Entity extraction
        entities = entity_extractor.extract(cleaned_text)
        all_entities.extend(entities)
        # Store in Pinecone (optional)
        try:
            vector_id = f"doc_{hash(url)}"
            metadata = {"url": url, "summary": summary[:1000]}
            pinecone.upsert_vectors([(vector_id, cleaned_text[:8000], metadata)])
        except Exception as e:
            console.print(f"[yellow]⚠ Pinecone storage skipped: {str(e)[:100]}[/yellow]")

        report_entries.append({
            "url": url,
            "summary": summary,
            "entities": entities,
        })
    return report_entries

def compute_trends(entities: List[Dict[str, str]], top_n: int = 5) -> List[Dict[str, Any]]:
    """Simple frequency count of extracted entities."""
    freq: Dict[str, int] = {}
    for e in entities:
        key = f"{e['type']}:{e['value']}"
        freq[key] = freq.get(key, 0) + 1
    sorted_items = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    trends = []
    for key, count in sorted_items[:top_n]:
        typ, val = key.split(":", 1)
        trends.append({"entity_type": typ, "entity": val, "occurrences": count})
    return trends

def build_report(metadata: Dict[str, Any], executive_summary: Dict[str, Any], entries: List[Dict[str, Any]], trends: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Assemble the final JSON report using the universal schema (minimal fields)."""
    report = {
        "report_metadata": metadata,
        "executive_summary": executive_summary,
        "detailed_findings": {
            "categories": [
                {
                    "category_name": "Aggregated Entities",
                    "items_identified": len(entries),
                    "significance": "HIGH",
                    "key_observations": [f"Found {len(trends)} top entities across sources"],
                    "data_points": trends,
                }
            ]
        },
        "entities_identified": {"primary_entities": []},
        "recommendations": {"immediate_actions": []},
        "data_sources": {"source_breakdown": {"total_urls": len(metadata.get('target_urls', []))}},
    }
    return report

@monitor_performance(step_name="intelligence_cycle")
def run_intelligence_cycle(user_prompt: str, analyzer, ingestor, preprocessor, pinecone, console) -> str:
    """High‑level wrapper that runs the full cycle and writes a JSON report.
    Returns the path to the generated report file.
    """
    target_urls = analyzer.generate_plan(user_prompt)
    if not target_urls:
        console.print("[red]No URLs generated for the prompt.[/red]")
        return ""
    entries = process_intelligence(target_urls, analyzer, preprocessor, pinecone, ingestor, console)
    trends = compute_trends(all_entities)
    executive_summary = {
        "research_objective": user_prompt,
        "overview": f"Processed {len(entries)} sources and extracted {len(all_entities)} entities.",
        "key_findings": [f"Top entity: {t['entity']} ({t['entity_type']}) with {t['occurrences']} mentions" for t in trends],
    }
    metadata = {
        "report_id": f"INTEL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "classification": "INTERNAL",
        "report_type": "Intelligence Analysis Report",
        "title": f"Research on {user_prompt}",
        "generated_by": "Transcendence T1",
        "date_generated": datetime.utcnow().isoformat() + "Z",
        "research_period": {"start_date": datetime.utcnow().date().isoformat(), "end_date": datetime.utcnow().date().isoformat()},
        "sources_analyzed": len(target_urls),
        "target_urls": target_urls,
        "confidence_level": "HIGH",
    }
    final_report = build_report(metadata, executive_summary, entries, trends)
    report_path = os.path.join("docs", f"report_{metadata['report_id']}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2)
    console.print(f"[bold green]✅ Report written to {report_path}[/bold green]")
    return report_path
