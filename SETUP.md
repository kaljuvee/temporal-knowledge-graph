# Setup and Usage Guide

This guide provides detailed instructions for setting up and using the Temporal Knowledge Graph demo.

## 🔧 Installation

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 4GB RAM recommended
- **Storage**: 1GB free space for dependencies

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kaljuvee/temporal-knowledge-graph.git
   cd temporal-knowledge-graph
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   # Using venv
   python -m venv temporal-kg-env
   
   # Activate on Windows
   temporal-kg-env\Scripts\activate
   
   # Activate on macOS/Linux
   source temporal-kg-env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set OpenAI API Key**
   
   **Option A: Environment Variable**
   ```bash
   # Windows
   set OPENAI_API_KEY=your-api-key-here
   
   # macOS/Linux
   export OPENAI_API_KEY=your-api-key-here
   ```
   
   **Option B: .env File**
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

5. **Verify Installation**
   ```bash
   python test_demo.py
   ```

## 🖥️ Command Line Interface

### Basic Commands

#### Demo Mode
Load sample data and explore the system:
```bash
python cli_demo.py --demo
```

#### Adding Content
Add individual statements:
```bash
python cli_demo.py --add "Microsoft acquired GitHub in 2018"
```

Add content from a file:
```bash
python cli_demo.py --add-file document.txt --source "company_report"
```

#### Querying
Query specific entities:
```bash
python cli_demo.py --query-entity "Microsoft"
```

Query at specific times:
```bash
python cli_demo.py --query-entity "Microsoft" --at-time "2019-01-01T00:00:00"
```

Ask natural language questions:
```bash
python cli_demo.py --ask "What companies did Microsoft acquire?"
```

#### Timeline Analysis
Get entity timelines:
```bash
python cli_demo.py --timeline "Microsoft"
```

#### Data Management
Save knowledge graph:
```bash
python cli_demo.py --save my_graph.json
```

Load existing graph:
```bash
python cli_demo.py --load my_graph.json --stats
```

### Interactive Mode

Start interactive mode by running without arguments:
```bash
python cli_demo.py
```

Available commands in interactive mode:
- `add <text>` - Add a statement
- `query <entity>` - Query an entity
- `ask <question>` - Ask a natural language question
- `timeline <entity>` - Get entity timeline
- `entities` - List all entities
- `stats` - Show statistics
- `save <file>` - Save knowledge graph
- `load <file>` - Load knowledge graph
- `demo` - Load demo data
- `help` - Show help
- `quit` - Exit

### Advanced CLI Usage

#### Batch Processing
Process multiple files:
```bash
for file in documents/*.txt; do
    python cli_demo.py --add-file "$file" --source "$(basename "$file")"
done
```

#### Temporal Queries
Query what was true at specific times:
```bash
python cli_demo.py --query-entity "Apple" --at-time "2010-01-01T00:00:00"
python cli_demo.py --query-entity "Apple" --at-time "2020-01-01T00:00:00"
```

#### Verbose Output
Get detailed information:
```bash
python cli_demo.py --add "New statement" --verbose
python cli_demo.py --query-entity "Company" --verbose
```

## 🌐 Web Interface

### Starting the Web App

1. **Launch Streamlit**
   ```bash
   streamlit run Home.py
   ```

2. **Open Browser**
   Navigate to the displayed URL (typically `http://localhost:8501`)

3. **Enter API Key**
   Enter your OpenAI API key in the sidebar

### Web Interface Features

#### Configuration Panel (Sidebar)
- **API Key Input**: Enter your OpenAI API key
- **Load Demo Data**: Populate with sample data
- **Clear Graph**: Reset the knowledge graph
- **File Upload**: Upload previously saved knowledge graphs
- **Download**: Save current graph as JSON

#### Main Tabs

**1. Add Content**
- Add individual statements with source tracking
- Process entire documents with automatic chunking
- View extracted triplets and temporal information

**2. Query & Search**
- Query by entity with optional time filtering
- Natural language question answering
- View supporting evidence and temporal context

**3. Timeline View**
- Select entities to view their timelines
- Interactive timeline visualization
- Detailed event information with temporal bounds

**4. Analytics**
- Temporal class distribution (pie charts)
- Fact type distribution
- Entity activity analysis (bar charts)
- Detailed statistics tables

**5. Browse Data**
- Filter statements by temporal class, fact type, or entity
- Paginated view of all statements
- Detailed statement information including triplets and temporal events

### Web Interface Tips

1. **Start with Demo Data**: Click "Load Demo Data" to populate the system
2. **Use Filters**: In the Browse Data tab, use filters to find specific information
3. **Explore Timelines**: The Timeline View provides excellent visualization of temporal relationships
4. **Save Your Work**: Use the Download button to save your knowledge graph
5. **Monitor Statistics**: The Analytics tab shows the health and composition of your graph

## 🐍 Python API

### Basic Usage

```python
from utils import KnowledgeGraphManager

# Initialize
manager = KnowledgeGraphManager(api_key="your-api-key")

# Add content
statement = manager.add_statement_text("Apple was founded in 1976")
print(f"Added: {statement.text}")
print(f"Temporal class: {statement.temporal_class}")

# Query
result = manager.query_entity("Apple")
print(f"Found {len(result.statements)} statements about Apple")

# Timeline
timeline = manager.get_entity_timeline("Apple")
for event in timeline:
    print(f"Event: {event['text']}")
```

### Advanced API Usage

#### Working with Documents
```python
# Process a document
with open("company_report.txt", "r") as f:
    content = f.read()

statements = manager.add_document(content, source="annual_report_2024")
print(f"Extracted {len(statements)} statements")

# Analyze temporal classes
temporal_counts = {}
for stmt in statements:
    tc = stmt.temporal_class.value
    temporal_counts[tc] = temporal_counts.get(tc, 0) + 1

print("Temporal distribution:", temporal_counts)
```

#### Temporal Queries
```python
from datetime import datetime

# Query at specific time
past_date = datetime(2020, 1, 1)
result = manager.query_entity("Apple", timestamp=past_date)
print(f"Apple information as of {past_date}: {len(result.statements)} statements")

# Check what was valid at different times
for year in [2010, 2015, 2020, 2025]:
    test_date = datetime(year, 1, 1)
    valid_statements = manager.kg.get_valid_statements_at(test_date)
    print(f"{year}: {len(valid_statements)} valid statements")
```

#### Natural Language Processing
```python
# Ask complex questions
questions = [
    "Who was the CEO of Apple in 2010?",
    "What acquisitions did Microsoft make?",
    "When was Google founded?",
    "What is the current revenue of Tesla?"
]

for question in questions:
    result = manager.query_natural_language(question)
    print(f"Q: {question}")
    print(f"A: {result.answer}")
    print(f"Evidence: {len(result.statements)} supporting statements\n")
```

#### Data Management
```python
# Save and load
manager.save_to_file("my_knowledge_graph.json")

# Create new manager and load
new_manager = KnowledgeGraphManager(api_key="your-api-key")
new_manager.load_from_file("my_knowledge_graph.json")

# Get statistics
stats = new_manager.get_statistics()
print(f"Loaded graph with {stats['total_statements']} statements")
```

## 🔍 Troubleshooting

### Common Issues

#### API Key Problems
**Error**: `Error code: 401 - {'error': 'Invalid or expired sandbox token'}`

**Solutions**:
1. Verify your API key is correct
2. Check that the API key has sufficient credits
3. Ensure the key is properly set in environment variables

#### Import Errors
**Error**: `ModuleNotFoundError: No module named 'openai'`

**Solutions**:
1. Ensure you've activated your virtual environment
2. Run `pip install -r requirements.txt` again
3. Check Python version compatibility

#### Memory Issues
**Error**: System runs slowly or crashes

**Solutions**:
1. Process smaller documents
2. Use batch processing for large datasets
3. Increase system memory if possible

#### Streamlit Issues
**Error**: Streamlit won't start or shows errors

**Solutions**:
1. Check that port 8501 is available
2. Try a different port: `streamlit run Home.py --server.port 8502`
3. Clear Streamlit cache: `streamlit cache clear`

### Performance Optimization

#### For Large Datasets
1. **Batch Processing**: Process documents in smaller chunks
2. **Selective Loading**: Load only necessary data
3. **Caching**: Use the built-in caching mechanisms

#### For Better Accuracy
1. **Quality Input**: Provide clean, well-formatted text
2. **Source Attribution**: Always specify sources for better tracking
3. **Manual Review**: Review extracted triplets for accuracy

### Debugging

#### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Check Extracted Data
```python
# Examine a statement in detail
statement = manager.kg.statements["stmt_1"]
print(f"Text: {statement.text}")
print(f"Triplets: {[str(t) for t in statement.triplets]}")
print(f"Temporal event: {statement.temporal_event}")
```

#### Validate Temporal Logic
```python
from datetime import datetime

# Check temporal validity
test_date = datetime(2023, 6, 1)
for stmt in manager.kg.statements.values():
    is_valid = stmt.is_valid_at(test_date)
    print(f"Statement valid at {test_date}: {is_valid}")
    print(f"  Text: {stmt.text}")
    if stmt.temporal_event:
        print(f"  Valid from: {stmt.temporal_event.t_valid}")
        print(f"  Valid until: {stmt.temporal_event.t_invalid}")
```

## 📊 Best Practices

### Data Input
1. **Clear Statements**: Use clear, unambiguous statements
2. **Date Formats**: Use standard date formats (ISO 8601 preferred)
3. **Source Tracking**: Always specify sources for traceability
4. **Consistent Entities**: Use consistent entity names

### Query Optimization
1. **Specific Entities**: Query specific entities rather than broad terms
2. **Time Bounds**: Use temporal constraints to narrow results
3. **Iterative Refinement**: Start broad, then narrow down queries

### System Maintenance
1. **Regular Backups**: Save knowledge graphs regularly
2. **Data Validation**: Periodically review extracted information
3. **Performance Monitoring**: Monitor system performance with large datasets
4. **Update Management**: Keep dependencies updated

## 🎯 Example Workflows

### Corporate Intelligence Workflow
```bash
# 1. Set up environment
export OPENAI_API_KEY="your-key"

# 2. Process annual reports
python cli_demo.py --add-file "annual_report_2023.txt" --source "AR2023"
python cli_demo.py --add-file "annual_report_2024.txt" --source "AR2024"

# 3. Analyze changes
python cli_demo.py --ask "What changed between 2023 and 2024?"
python cli_demo.py --timeline "Company Name"

# 4. Save results
python cli_demo.py --save "corporate_intelligence.json"
```

### Research Analysis Workflow
```python
# Python script for research analysis
from utils import KnowledgeGraphManager
from datetime import datetime

manager = KnowledgeGraphManager(api_key="your-key")

# Process research papers
papers = ["paper1.txt", "paper2.txt", "paper3.txt"]
for paper in papers:
    with open(paper, "r") as f:
        content = f.read()
    manager.add_document(content, source=paper)

# Analyze temporal trends
entities = manager.get_all_entities()
for entity in entities[:10]:  # Top 10 entities
    timeline = manager.get_entity_timeline(entity)
    if len(timeline) > 1:
        print(f"Entity {entity} has {len(timeline)} temporal events")

# Generate research summary
result = manager.query_natural_language("What are the key findings?")
print(f"Research Summary: {result.answer}")
```

This setup guide should help you get started with the Temporal Knowledge Graph demo. For additional support, refer to the main README or create an issue in the repository.

