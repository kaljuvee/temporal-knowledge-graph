# Examples and Use Cases

This document provides comprehensive examples of using the Temporal Knowledge Graph system across different domains and scenarios.

## 🏢 Corporate Intelligence

### Executive Tracking

Track leadership changes over time:

```python
from utils import KnowledgeGraphManager
from datetime import datetime

manager = KnowledgeGraphManager(api_key="your-api-key")

# Add executive information
statements = [
    "John Smith was appointed CEO of TechCorp on January 15, 2020.",
    "John Smith resigned as CEO of TechCorp on December 31, 2023.",
    "Sarah Johnson became the new CEO of TechCorp on January 1, 2024.",
    "Sarah Johnson previously worked as CTO at InnovateTech for 5 years.",
    "Mike Wilson was CFO of TechCorp from 2018 to 2023.",
    "Lisa Chen joined as CFO of TechCorp in January 2024."
]

for stmt in statements:
    manager.add_statement_text(stmt, source="executive_tracking")

# Query leadership at different times
print("CEO in 2022:")
result = manager.query_entity("TechCorp", timestamp=datetime(2022, 6, 1))
for stmt in result.statements:
    if "CEO" in stmt.text:
        print(f"  {stmt.text}")

print("\nCEO in 2024:")
result = manager.query_entity("TechCorp", timestamp=datetime(2024, 6, 1))
for stmt in result.statements:
    if "CEO" in stmt.text:
        print(f"  {stmt.text}")

# Get complete timeline
timeline = manager.get_entity_timeline("TechCorp")
print(f"\nTechCorp Timeline ({len(timeline)} events):")
for event in timeline:
    print(f"  {event['text']}")
```

### Acquisition Analysis

Track mergers and acquisitions:

```bash
# CLI commands for acquisition tracking
python cli_demo.py --add "Microsoft acquired GitHub for $7.5 billion in June 2018"
python cli_demo.py --add "Microsoft acquired Activision Blizzard for $68.7 billion in October 2023"
python cli_demo.py --add "Microsoft acquired LinkedIn for $26.2 billion in June 2016"

# Query acquisitions
python cli_demo.py --ask "What companies did Microsoft acquire?"
python cli_demo.py --ask "How much did Microsoft spend on acquisitions?"
python cli_demo.py --timeline "Microsoft"
```

### Financial Performance

Track financial metrics over time:

```python
# Financial data processing
financial_data = [
    "TechCorp reported revenue of $100 million in Q1 2023.",
    "TechCorp reported revenue of $120 million in Q2 2023.",
    "TechCorp reported revenue of $110 million in Q3 2023.",
    "TechCorp reported revenue of $130 million in Q4 2023.",
    "TechCorp's annual revenue for 2023 was $460 million.",
    "TechCorp reported revenue of $140 million in Q1 2024."
]

for data in financial_data:
    manager.add_statement_text(data, source="financial_reports")

# Analyze revenue trends
result = manager.query_natural_language("What was TechCorp's revenue trend in 2023?")
print(f"Revenue Analysis: {result.answer}")

# Get quarterly performance
timeline = manager.get_entity_timeline("TechCorp")
revenue_events = [e for e in timeline if "revenue" in e['text'].lower()]
for event in revenue_events:
    print(f"  {event['text']}")
```

## 🔬 Research and Academia

### Scientific Discovery Tracking

Track scientific breakthroughs and discoveries:

```python
# Scientific discoveries
discoveries = [
    "The structure of DNA was discovered by Watson and Crick in 1953.",
    "The Higgs boson was discovered at CERN in 2012.",
    "CRISPR gene editing was developed by Jennifer Doudna and Emmanuelle Charpentier in 2012.",
    "The first exoplanet around a sun-like star was discovered in 1995.",
    "Gravitational waves were first detected by LIGO in 2015.",
    "The COVID-19 vaccine was developed by Pfizer-BioNTech in 2020."
]

for discovery in discoveries:
    manager.add_statement_text(discovery, source="science_timeline")

# Query scientific progress
result = manager.query_natural_language("What major scientific discoveries happened in the 2010s?")
print(f"2010s Discoveries: {result.answer}")

# Timeline of genetics research
timeline = manager.get_entity_timeline("gene editing")
for event in timeline:
    print(f"Genetics: {event['text']}")
```

### Academic Career Tracking

Track academic positions and achievements:

```python
academic_info = [
    "Dr. Jane Smith was appointed Professor of Computer Science at MIT in 2015.",
    "Dr. Jane Smith published 'Machine Learning Fundamentals' in 2018.",
    "Dr. Jane Smith received the Turing Award in 2020.",
    "Dr. Jane Smith became Department Head at MIT in 2021.",
    "Dr. Jane Smith was elected to the National Academy of Sciences in 2022."
]

for info in academic_info:
    manager.add_statement_text(info, source="academic_records")

# Query academic achievements
result = manager.query_entity("Dr. Jane Smith")
print("Academic Timeline:")
for stmt in result.statements:
    print(f"  {stmt.text}")
```

## 🏛️ Government and Policy

### Legislative Tracking

Track policy changes and legislation:

```bash
# Policy tracking via CLI
python cli_demo.py --add "The GDPR was enacted in the European Union on May 25, 2018"
python cli_demo.py --add "The California Consumer Privacy Act (CCPA) went into effect on January 1, 2020"
python cli_demo.py --add "The EU AI Act was approved by the European Parliament in 2024"

# Query policy landscape
python cli_demo.py --ask "What privacy laws were enacted in the 2010s and 2020s?"
python cli_demo.py --timeline "European Union"
```

### Political Leadership

Track political appointments and terms:

```python
political_data = [
    "Joe Biden was inaugurated as the 46th President of the United States on January 20, 2021.",
    "Kamala Harris became Vice President of the United States on January 20, 2021.",
    "Donald Trump served as the 45th President from January 20, 2017 to January 20, 2021.",
    "Barack Obama served as the 44th President from January 20, 2009 to January 20, 2017."
]

for data in political_data:
    manager.add_statement_text(data, source="political_records")

# Query by time period
result = manager.query_natural_language("Who was President of the United States in 2019?")
print(f"2019 President: {result.answer}")
```

## 🏥 Healthcare and Medicine

### Drug Development Timeline

Track pharmaceutical development:

```python
drug_development = [
    "Pfizer began Phase I trials for BNT162b2 COVID-19 vaccine in April 2020.",
    "Pfizer completed Phase III trials for BNT162b2 in November 2020.",
    "FDA granted emergency use authorization for Pfizer COVID-19 vaccine on December 11, 2020.",
    "Pfizer COVID-19 vaccine received full FDA approval on August 23, 2021.",
    "Pfizer developed an updated bivalent vaccine in September 2022."
]

for development in drug_development:
    manager.add_statement_text(development, source="fda_records")

# Track development phases
timeline = manager.get_entity_timeline("BNT162b2")
print("Vaccine Development Timeline:")
for event in timeline:
    print(f"  {event['text']}")
```

### Medical Research

Track clinical studies and outcomes:

```bash
# Medical research tracking
python cli_demo.py --add "The Framingham Heart Study began in 1948 and is still ongoing"
python cli_demo.py --add "The Women's Health Initiative study ran from 1991 to 2005"
python cli_demo.py --add "The Human Genome Project was completed in 2003"

python cli_demo.py --ask "What major medical studies were conducted in the 20th century?"
```

## 🌍 Environmental and Climate

### Climate Policy Tracking

Track environmental policies and agreements:

```python
climate_data = [
    "The Paris Climate Agreement was signed on April 22, 2016.",
    "The United States withdrew from the Paris Agreement on November 4, 2020.",
    "The United States rejoined the Paris Agreement on February 19, 2021.",
    "The Kyoto Protocol was adopted on December 11, 1997.",
    "The Montreal Protocol was signed on September 16, 1987."
]

for data in climate_data:
    manager.add_statement_text(data, source="climate_policy")

# Track policy changes
result = manager.query_natural_language("How did US participation in climate agreements change over time?")
print(f"Climate Policy Evolution: {result.answer}")
```

### Environmental Events

Track environmental incidents and responses:

```bash
# Environmental event tracking
python cli_demo.py --add "The Exxon Valdez oil spill occurred in Alaska on March 24, 1989"
python cli_demo.py --add "The Deepwater Horizon oil spill began on April 20, 2010"
python cli_demo.py --add "The Fukushima nuclear disaster occurred on March 11, 2011"

python cli_demo.py --ask "What major environmental disasters occurred in the 21st century?"
python cli_demo.py --timeline "oil spill"
```

## 💼 Technology Industry

### Tech Company Evolution

Track technology company milestones:

```python
tech_milestones = [
    "Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne on April 1, 1976.",
    "Apple went public on December 12, 1980.",
    "Steve Jobs left Apple in 1985 to found NeXT.",
    "Steve Jobs returned to Apple as interim CEO in 1997.",
    "Apple launched the iPhone on June 29, 2007.",
    "Tim Cook became CEO of Apple on August 24, 2011.",
    "Apple became the first company to reach a $1 trillion market cap on August 2, 2018."
]

for milestone in tech_milestones:
    manager.add_statement_text(milestone, source="tech_history")

# Query company evolution
timeline = manager.get_entity_timeline("Apple")
print("Apple Timeline:")
for event in timeline:
    print(f"  {event['text']}")

# Query leadership changes
result = manager.query_natural_language("Who were the CEOs of Apple and when did they serve?")
print(f"Apple Leadership: {result.answer}")
```

### Product Launch Tracking

Track product releases and updates:

```bash
# Product launch tracking
python cli_demo.py --add "iPhone 15 was released by Apple on September 22, 2023"
python cli_demo.py --add "ChatGPT was launched by OpenAI on November 30, 2022"
python cli_demo.py --add "GPT-4 was released by OpenAI on March 14, 2023"
python cli_demo.py --add "Tesla Model S was first delivered in June 2012"

python cli_demo.py --ask "What major tech products were launched in 2023?"
python cli_demo.py --timeline "OpenAI"
```

## 📚 Media and Entertainment

### Movie Industry Tracking

Track film releases and industry events:

```python
movie_data = [
    "Avatar was released by James Cameron on December 18, 2009.",
    "Avatar became the highest-grossing film of all time in 2010.",
    "Avengers: Endgame surpassed Avatar as the highest-grossing film in July 2019.",
    "Avatar: The Way of Water was released on December 16, 2022.",
    "The Marvel Cinematic Universe began with Iron Man in 2008."
]

for data in movie_data:
    manager.add_statement_text(data, source="box_office")

# Query box office records
result = manager.query_natural_language("Which movies held the box office record and when?")
print(f"Box Office History: {result.answer}")
```

### Sports Records

Track sports achievements and records:

```bash
# Sports records tracking
python cli_demo.py --add "Usain Bolt set the 100m world record of 9.58 seconds on August 16, 2009"
python cli_demo.py --add "Michael Phelps won 8 gold medals at the 2008 Beijing Olympics"
python cli_demo.py --add "Serena Williams won her 23rd Grand Slam title at the 2017 Australian Open"

python cli_demo.py --ask "What world records were set in the 2000s?"
python cli_demo.py --timeline "Olympics"
```

## 🏗️ Advanced Use Cases

### Multi-Source Information Reconciliation

Handle conflicting information from different sources:

```python
# Add conflicting information
manager.add_statement_text(
    "Company X reported revenue of $100 million in 2023", 
    source="company_report"
)
manager.add_statement_text(
    "Company X reported revenue of $95 million in 2023", 
    source="sec_filing"
)
manager.add_statement_text(
    "Company X's actual revenue was $98 million in 2023", 
    source="audit_report"
)

# Query to see how conflicts are handled
result = manager.query_entity("Company X")
print("Revenue Information:")
for stmt in result.statements:
    if "revenue" in stmt.text:
        print(f"  {stmt.text} (Source: {stmt.source})")
```

### Temporal Reasoning

Complex temporal queries and reasoning:

```python
# Add temporal relationships
temporal_statements = [
    "Project Alpha was announced in January 2023.",
    "Project Alpha entered development phase in March 2023.",
    "Project Alpha completed beta testing in September 2023.",
    "Project Alpha was launched to the public in December 2023.",
    "Project Alpha was discontinued in June 2024."
]

for stmt in temporal_statements:
    manager.add_statement_text(stmt, source="project_tracking")

# Query project lifecycle
result = manager.query_natural_language("What was the lifecycle of Project Alpha?")
print(f"Project Lifecycle: {result.answer}")

# Check status at different times
for month in ["2023-02", "2023-08", "2024-01", "2024-07"]:
    test_date = datetime.strptime(month, "%Y-%m")
    valid_statements = [s for s in manager.kg.statements.values() 
                       if "Project Alpha" in s.text and s.is_valid_at(test_date)]
    print(f"\nProject Alpha status in {month}:")
    for stmt in valid_statements:
        print(f"  {stmt.text}")
```

### Batch Processing

Process large volumes of documents:

```python
import os
from pathlib import Path

# Process multiple documents
document_folder = "documents/"
if os.path.exists(document_folder):
    for file_path in Path(document_folder).glob("*.txt"):
        with open(file_path, "r") as f:
            content = f.read()
        
        statements = manager.add_document(content, source=str(file_path))
        print(f"Processed {file_path}: {len(statements)} statements extracted")

# Analyze the complete dataset
stats = manager.get_statistics()
print(f"\nDataset Statistics:")
print(f"  Total statements: {stats['total_statements']}")
print(f"  Total entities: {stats['total_entities']}")
print(f"  Temporal events: {stats['statements_with_temporal_events']}")

# Find most active entities
entities = manager.get_all_entities()
entity_activity = []
for entity in entities:
    statements = manager.kg.get_statements_for_entity(entity)
    entity_activity.append((entity, len(statements)))

# Sort by activity
entity_activity.sort(key=lambda x: x[1], reverse=True)
print(f"\nTop 10 Most Active Entities:")
for entity, count in entity_activity[:10]:
    print(f"  {entity}: {count} statements")
```

## 🎯 Domain-Specific Examples

### Legal Case Tracking

```python
legal_cases = [
    "Brown v. Board of Education was decided by the Supreme Court on May 17, 1954.",
    "Roe v. Wade was decided by the Supreme Court on January 22, 1973.",
    "Roe v. Wade was overturned by Dobbs v. Jackson on June 24, 2022.",
    "Miranda v. Arizona was decided on June 13, 1966."
]

for case in legal_cases:
    manager.add_statement_text(case, source="legal_database")

# Query legal precedents
result = manager.query_natural_language("What Supreme Court cases were overturned?")
print(f"Overturned Cases: {result.answer}")
```

### Supply Chain Tracking

```bash
# Supply chain events
python cli_demo.py --add "Supplier A began providing components to Company B in January 2020"
python cli_demo.py --add "Supplier A's contract with Company B was terminated in March 2023"
python cli_demo.py --add "Supplier C replaced Supplier A for Company B in April 2023"

python cli_demo.py --ask "How did Company B's supply chain change over time?"
python cli_demo.py --timeline "Company B"
```

### Real Estate Development

```python
real_estate = [
    "Construction of Tower Plaza began in March 2020.",
    "Tower Plaza reached 50% completion in December 2020.",
    "Tower Plaza construction was delayed due to COVID-19 in January 2021.",
    "Tower Plaza construction resumed in June 2021.",
    "Tower Plaza was completed and opened in September 2022."
]

for event in real_estate:
    manager.add_statement_text(event, source="construction_log")

# Track project progress
timeline = manager.get_entity_timeline("Tower Plaza")
print("Construction Timeline:")
for event in timeline:
    print(f"  {event['text']}")
```

## 🔧 Integration Examples

### API Integration

Create a REST API wrapper:

```python
from flask import Flask, request, jsonify
from utils import KnowledgeGraphManager

app = Flask(__name__)
manager = KnowledgeGraphManager(api_key="your-api-key")

@app.route('/add_statement', methods=['POST'])
def add_statement():
    data = request.json
    statement = manager.add_statement_text(
        data['text'], 
        source=data.get('source')
    )
    return jsonify({
        'id': statement.id,
        'temporal_class': statement.temporal_class.value,
        'triplets': [str(t) for t in statement.triplets]
    })

@app.route('/query_entity/<entity>')
def query_entity(entity):
    result = manager.query_entity(entity)
    return jsonify({
        'statements': [stmt.text for stmt in result.statements],
        'timeline': result.timeline
    })

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json['question']
    result = manager.query_natural_language(question)
    return jsonify({
        'answer': result.answer,
        'confidence': result.confidence
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Database Integration

Store knowledge graph in a database:

```python
import sqlite3
import json

def save_to_database(manager, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statements (
            id TEXT PRIMARY KEY,
            text TEXT,
            temporal_class TEXT,
            fact_type TEXT,
            source TEXT,
            temporal_event TEXT,
            triplets TEXT
        )
    ''')
    
    # Insert statements
    for stmt in manager.kg.statements.values():
        cursor.execute('''
            INSERT OR REPLACE INTO statements 
            (id, text, temporal_class, fact_type, source, temporal_event, triplets)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            stmt.id,
            stmt.text,
            stmt.temporal_class.value,
            stmt.fact_type.value,
            stmt.source,
            json.dumps(stmt.temporal_event.dict() if stmt.temporal_event else None),
            json.dumps([t.dict() for t in stmt.triplets])
        ))
    
    conn.commit()
    conn.close()

# Usage
save_to_database(manager, "knowledge_graph.db")
```

These examples demonstrate the versatility and power of the Temporal Knowledge Graph system across various domains and use cases. The system can be adapted to track virtually any type of temporal information and relationships.

