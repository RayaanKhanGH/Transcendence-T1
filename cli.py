#!/usr/bin/env python3
"""
Transcendence T1 - Interactive CLI
The main entry point for the functional OSINT agent.
"""

import sys
import logging
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Import core modules
from src.config import config
from src.core.analysis.analyzer import Analyzer
from src.core.ingestion.ingestor import Ingestor
from src.core.preprocess.preprocessor import Preprocessor
from src.models.embeddings.pinecone_handler import PineconeHandler


# Configure logging
logging.basicConfig(level=logging.WARNING)
console = Console()

def print_header():
    """Print the CLI header."""
    console.clear()
    header = """
    ╔════════════════════════════════════════════════════════════╗
    ║                  TRANSCENDENCE T1                          ║
    ║          Cyber Intelligence OSINT Agent - CLI              ║
    ╚════════════════════════════════════════════════════════════╝
    """
    console.print(header, style="bold cyan")
    console.print("System Status: Online 🟢\n", style="bold green")

def check_config():
    """Check if API keys are configured."""
    status_table = Table(title="Configuration Status")
    status_table.add_column("Service", style="cyan")
    status_table.add_column("Status", style="green")

    gemini_status = "✅ Configured" if config.GEMINI_API_KEY else "❌ Missing"
    pinecone_status = "✅ Configured" if config.VECTOR_DB_API_KEY else "❌ Missing"
    postgres_status = "✅ Configured" if config.POSTGRES_URI else "❌ Missing"

    status_table.add_row("Gemini AI", gemini_status)
    status_table.add_row("Pinecone Vector DB (llama-embed-v2)", pinecone_status)
    status_table.add_row("PostgreSQL", postgres_status)
    
    console.print(status_table)
    console.print("\n")

def main():
    """Main CLI loop."""
    print_header()
    check_config()

    # Initialize modules
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Initializing modules...", total=None)
        
        analyzer = Analyzer()
        ingestor = Ingestor()
        preprocessor = Preprocessor()
        pinecone = PineconeHandler()
        
        progress.update(task, completed=True)

    console.print("[bold green]✓ Modules initialized successfully.[/bold green]\n")

    while True:
        try:
            # Step 1: User Input
            console.print("[bold yellow]Enter your research prompt (or 'exit' to quit):[/bold yellow]")
            user_prompt = Prompt.ask(">>")
            
            if user_prompt.lower() in ['exit', 'quit', 'q']:
                console.print("[bold cyan]Shutting down...[/bold cyan]")
                break

            if not user_prompt.strip():
                continue

            # Step 2: AI Planning
            console.print(f"\n[bold cyan]🤖 Analyzing prompt: '{user_prompt}'...[/bold cyan]")
            
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task("Generating research plan...", total=None)
                target_urls = analyzer.generate_plan(user_prompt)
                progress.update(task, completed=True)

            if not target_urls:
                console.print("[red]Could not generate a plan. Please try a different prompt.[/red]")
                continue

            console.print(f"\n[green]✓ Plan generated. Target URLs:[/green]")
            for url in target_urls:
                console.print(f"  - {url}")

            if not Prompt.ask("\nProceed with scraping?", choices=["y", "n"], default="y") == "y":
                console.print("[yellow]Operation cancelled.[/yellow]\n")
                continue

            # Step 3: Execution (Scraping)
            console.print("\n[bold cyan]🕷️  Starting scraping job...[/bold cyan]")
            
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task(f"Scraping {len(target_urls)} sources...", total=None)
                raw_data = ingestor.fetch_osint(target_urls)
                progress.update(task, completed=True)

            console.print(f"[green]✓ Successfully scraped {len([d for d in raw_data if d.get('status') == 'success'])}/{len(target_urls)} sources.[/green]")

            # Step 4: Processing
            console.print("\n[bold cyan]🧠 Processing intelligence...[/bold cyan]")
            
            findings = []
            
            for item in raw_data:
                if item.get('status') != 'success':
                    continue
                
                import time
                time.sleep(1) # Rate limit mitigation
                
                url = item['url']
                # Use the already-parsed content from ingestor
                content = item.get('content', '')
                title = item.get('title', '')
                
                console.print(f"\nProcessing: [dim]{url}[/dim]")
                if title:
                    console.print(f"Title: [bold]{title}[/bold]")
                
                # Analyze with Gemini (content is already clean from parser)
                # Analyze with Gemini (content is already clean from parser)
                summary = analyzer.generate_summary(content)
                if summary.startswith("Error"):
                     console.print(f"[bold red]{summary}[/bold red]")
                else:
                     console.print(f"[bold]Summary:[/bold] {summary[:200]}...")
                
                # Store in Pinecone (optional - will warn if fails)
                try:
                    vector_id = f"doc_{hash(url)}"
                    metadata = {"url": url, "summary": summary[:1000], "title": title}
                    pinecone.upsert_vectors([(vector_id, content[:8000], metadata)])
                except Exception as e:
                    console.print(f"[yellow]⚠ Pinecone storage skipped: {str(e)[:100]}[/yellow]")

                findings.append({
                    "url": url,
                    "title": title,
                    "summary": summary,
                    "content_snippet": content[:1000]
                })

            console.print("\n[bold green]✓ Intelligence cycle complete![/bold green]\n")
            
            # Step 5: Report Generation
            if findings:
                import json
                from datetime import datetime
                import os
                
                # Generate synthesized executive report
                console.print("\n[bold cyan]📝 Synthesizing executive report...[/bold cyan]")
                all_summaries = [f.get("summary", "") for f in findings]
                executive_narrative = analyzer.generate_executive_report(all_summaries, user_prompt)

                report_id = f"INTEL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                report_filename = f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                report_data = {
                    "report_metadata": {
                        "report_id": report_id,
                        "classification": "INTERNAL",
                        "report_type": "Intelligence Analysis Report",
                        "title": f"Research Analysis: {user_prompt[:50]}...",
                        "generated_by": "Transcendence T1 Intelligence System",
                        "date_generated": datetime.now().isoformat(),
                        "sources_analyzed": len(target_urls),
                        "successful_sources": len(findings)
                    },
                    "executive_summary": {
                        "research_objective": user_prompt,
                        "intelligence_extraction": executive_narrative
                    },
                    "detailed_findings": findings
                }
                
                # Ensure docs directory exists
                os.makedirs("docs", exist_ok=True)
                report_path = os.path.join("docs", report_filename)
                
                with open(report_path, "w", encoding="utf-8") as f:
                    json.dump(report_data, f, indent=2)
                
                console.print(Panel(f"Report generated: [bold]{report_path}[/bold]\nData stored in Vector DB.", border_style="green"))
            else:
                console.print(Panel("No data collected to generate report.", border_style="yellow"))

            console.print("-" * 50 + "\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted.[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]An error occurred: {e}[/red]")

if __name__ == "__main__":
    main()
