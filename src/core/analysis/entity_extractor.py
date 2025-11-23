import re
from typing import List, Dict

class EntityExtractor:
    """Very lightweight entity extractor.
    It looks for capitalized words and common patterns (e.g., "Apple Inc.", "CVE-2024-12345").
    In a production system you would replace this with spaCy or a custom NER model.
    """
    def extract(self, text: str) -> List[Dict[str, str]]:
        # Find potential entities: capitalized words, acronyms, CVE IDs, URLs
        entities = []
        # Simple regex for CVE IDs
        for cve in re.findall(r"CVE-\d{4}-\d{4,7}", text):
            entities.append({"type": "CVE", "value": cve})
        # Capitalized words (at least 2 characters) not at sentence start
        for word in re.findall(r"(?<!\.)\s([A-Z][a-zA-Z0-9&\-]+(?:\s[A-Z][a-zA-Z0-9&\-]+)*)", text):
            entities.append({"type": "Entity", "value": word.strip()})
        # URLs as entities
        for url in re.findall(r"https?://[\w./?=&%-]+", text):
            entities.append({"type": "URL", "value": url})
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for e in entities:
            key = (e["type"], e["value"]) 
            if key not in seen:
                seen.add(key)
                unique.append(e)
        return unique
