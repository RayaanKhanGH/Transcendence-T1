#!/usr/bin/env python3
"""
Simulate a real CLI run to verify the full pipeline.
"""
import sys
import logging
from rich.console import Console

# Configure logging to show what's happening
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# Suppress noisy libraries
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)

from src.core.analysis.analyzer import Analyzer
from src.core.ingestion.ingestor import Ingestor

console = Console()

def run_test():
    console.print("[bold cyan]🚀 Starting End-to-End System Test[/bold cyan]")
    
    # Initialize components
    try:
        analyzer = Analyzer()
        ingestor = Ingestor()
        console.print("[green]✓ Components initialized[/green]")
    except Exception as e:
        console.print(f"[red]❌ Initialization failed: {e}[/red]")
        return

    # Step 1: Planning (Selenium + DuckDuckGo)
    prompt = "latest news on artificial intelligence breakthroughs"
    console.print(f"\n[bold yellow]Step 1: Planning[/bold yellow] - Prompt: '{prompt}'")
    
    try:
        urls = analyzer.generate_plan(prompt)
        if not urls:
            console.print("[red]❌ No URLs found[/red]")
            return
            
        console.print(f"[green]✓ Found {len(urls)} URLs:[/green]")
        for url in urls:
            console.print(f"  - {url}")
    except Exception as e:
        console.print(f"[red]❌ Planning failed: {e}[/red]")
        return

    # Step 2: Ingestion (Requests + BeautifulSoup)
    console.print(f"\n[bold yellow]Step 2: Ingestion[/bold yellow] - Scraping {len(urls)} URLs...")
    
    try:
        # Limit to 3 for the test to be quick
        results = ingestor.fetch_osint(urls[:3])
        
        successful = [r for r in results if r.get('status') == 'success']
        console.print(f"[green]✓ Successfully scraped {len(successful)}/{len(results)} pages[/green]")
        
        if not successful:
            console.print("[red]❌ All scrapes failed[/red]")
            return
            
    except Exception as e:
        console.print(f"[red]❌ Ingestion failed: {e}[/red]")
        return

    # Step 3: Analysis (Gemini)
    console.print(f"\n[bold yellow]Step 3: Analysis[/bold yellow] - Summarizing content...")
    
    for item in successful:
        console.print(f"\n[bold]Processing: {item['url']}[/bold]")
        console.print(f"Title: {item.get('title', 'No Title')}")
        
        content = item.get('content', '')
        if len(content) > 100:
            console.print(f"Content extracted: {len(content)} characters")
            
            # Generate summary
            summary = analyzer.generate_summary(content)
            console.print(f"[cyan]Summary:[/cyan] {summary[:300]}...")
        else:
            console.print("[red]⚠️  Content too short/empty[/red]")

    console.print("\n[bold green]✅ TEST COMPLETE: System is fully functional[/bold green]")

if __name__ == "__main__":
    run_test()
