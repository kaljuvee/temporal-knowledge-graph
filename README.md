# Temporal Knowledge Graph Demo

A comprehensive implementation of temporal knowledge graphs based on the [OpenAI Cookbook: Temporal Agents with Knowledge Graphs](https://cookbook.openai.com/examples/partners/temporal_agents_with_knowledge_graphs/temporal_agents_with_knowledge_graphs).

## 🧠 Overview

This project demonstrates how to build and use temporal knowledge graphs that can:

- **Track information over time** - Know what was true at any given moment
- **Handle evolving facts** - Manage statements that change or become invalid
- **Extract temporal relationships** - Automatically identify when events occurred
- **Query across time** - Ask questions like "Who was CEO in 2023?"
- **Visualize timelines** - See how entities and relationships evolve

## 🏗️ Architecture

The system implements a complete temporal knowledge graph pipeline:

### Core Components

1. **Temporal Agent** - Processes text and extracts temporal information
2. **Knowledge Graph** - Stores statements with temporal validity
3. **Query Engine** - Handles temporal and natural language queries
4. **Invalidation System** - Manages conflicting or outdated information

### Pipeline Flow

```
Text Input
    ↓
Semantic Chunking
    ↓
Statement Extraction
    ↓
Temporal Classification (Atemporal/Static/Dynamic)
    ↓
Triplet Extraction (Subject-Predicate-Object)
    ↓
Temporal Event Extraction (t_valid, t_invalid, etc.)
    ↓
Entity Resolution
    ↓
Invalidation Checking
    ↓
Knowledge Graph Storage
```

### Temporal Classifications

- **Atemporal**: Facts that never change (e.g., "Speed of light is 299,792,458 m/s")
- **Static**: Facts valid from a point in time (e.g., "Company A acquired Company B on Jan 1, 2020")
- **Dynamic**: Facts that evolve over time (e.g., "John was CEO from 2019 to 2022")

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kaljuvee/temporal-knowledge-graph.git
cd temporal-knowledge-graph
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Demo Usage

#### Command Line Interface

1. **Load demo data and explore:**
```bash
python cli_demo.py --demo
```

2. **Add a statement:**
```bash
python cli_demo.py --add "John Smith became CEO of TechCorp on January 1, 2024"
```

3. **Query an entity:**
```bash
python cli_demo.py --query-entity "TechCorp"
```

4. **Ask natural language questions:**
```bash
python cli_demo.py --ask "Who was CEO of TechCorp in 2023?"
```

5. **Get entity timeline:**
```bash
python cli_demo.py --timeline "TechCorp"
```

6. **Interactive mode:**
```bash
python cli_demo.py
```

#### Streamlit Web Interface

1. **Launch the web app:**
```bash
streamlit run Home.py
```

2. **Open your browser** to the displayed URL (typically http://localhost:8501)

3. **Explore the interface:**
   - Add content via the "Add Content" tab
   - Query and search in the "Query & Search" tab
   - View timelines in the "Timeline View" tab
   - Analyze data in the "Analytics" tab
   - Browse all data in the "Browse Data" tab

## 📚 Detailed Usage

### Core Data Models

The system uses several key data models:

#### Statement
Represents a piece of information with temporal context:
```python
statement = Statement(
    id="stmt_1",
    text="John Smith became CEO on January 1, 2024",
    temporal_class=TemporalClass.STATIC,
    fact_type=FactType.FACT,
    triplets=[...],
    temporal_event=TemporalEvent(t_valid=datetime(2024, 1, 1)),
    source="annual_report"
)
```

#### Triplet
Knowledge graph relationships in Subject-Predicate-Object format:
```python
triplet = Triplet(
    subject="John Smith",
    predicate="hasRole", 
    object="CEO"
)
```

#### TemporalEvent
Temporal validity information:
```python
temporal_event = TemporalEvent(
    t_created=datetime(2024, 1, 1),    # When statement was created
    t_valid=datetime(2024, 1, 1),      # When it becomes valid
    t_invalid=datetime(2025, 1, 1),    # When it becomes invalid
    t_expired=datetime(2025, 12, 31)   # When it expires
)
```

### Programming Interface

#### Basic Usage

```python
from utils import KnowledgeGraphManager

# Initialize
manager = KnowledgeGraphManager(api_key="your-api-key")

# Add content
statement = manager.add_statement_text(
    "Sarah Johnson became CEO of TechCorp on January 1, 2024"
)

# Query entity
result = manager.query_entity("TechCorp")

# Ask questions
result = manager.query_natural_language("Who is the current CEO?")

# Get timeline
timeline = manager.get_entity_timeline("TechCorp")
```

#### Advanced Usage

```python
from datetime import datetime
from models import TemporalQuery

# Query at specific time
result = manager.query_entity("TechCorp", timestamp=datetime(2023, 6, 1))

# Process documents
statements = manager.add_document(document_text, source="annual_report_2024")

# Save/load knowledge graph
manager.save_to_file("my_knowledge_graph.json")
manager.load_from_file("my_knowledge_graph.json")

# Get statistics
stats = manager.get_statistics()
print(f"Total statements: {stats['total_statements']}")
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Model Configuration

The system uses `gpt-4o-mini` by default. You can modify the model in `temporal_agent.py`:

```python
self.model = "gpt-4o-mini"  # Change to your preferred model
```

## 📊 Features

### Temporal Capabilities

- **Time-aware queries**: Query what was true at any specific time
- **Temporal validity tracking**: Know when facts become valid/invalid
- **Statement invalidation**: Automatically handle conflicting information
- **Timeline visualization**: See how entities evolve over time

### Query Capabilities

- **Entity queries**: Find all information about specific entities
- **Natural language queries**: Ask questions in plain English
- **Temporal range queries**: Find events within time periods
- **Multi-hop reasoning**: Follow relationships across the graph

### Interface Options

- **Command Line Interface**: Full-featured CLI with interactive mode
- **Web Interface**: Rich Streamlit app with visualizations
- **Python API**: Direct programmatic access to all functionality

## 🧪 Testing

Run the test suite to validate functionality:

```bash
python test_demo.py
```

This will test all core functionality with mock data, demonstrating:
- Statement processing and classification
- Triplet extraction
- Temporal event handling
- Entity queries
- Timeline generation
- Natural language query simulation

## 📁 Project Structure

```
temporal-knowledge-graph/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── models.py                # Core data models
├── temporal_agent.py        # Temporal processing agent
├── utils.py                 # Utility functions and manager
├── cli_demo.py             # Command line interface
├── Home.py       # Web interface
├── test_demo.py            # Test suite
└── research_notes.md       # Research findings from OpenAI cookbook
```

## 🎯 Use Cases

### Business Intelligence
- Track executive changes over time
- Monitor company acquisitions and mergers
- Analyze revenue and performance trends
- Understand organizational evolution

### Knowledge Management
- Maintain up-to-date corporate knowledge bases
- Track policy and procedure changes
- Monitor regulatory compliance over time
- Manage product lifecycle information

### Research and Analysis
- Study historical trends and patterns
- Analyze cause-and-effect relationships
- Track scientific discoveries and updates
- Monitor market and industry changes

## 🔮 Future Enhancements

### Planned Features
- **Enhanced entity resolution**: Better handling of entity aliases and variations
- **Confidence scoring**: Probabilistic confidence in extracted information
- **Multi-source reconciliation**: Handling conflicting information from different sources
- **Graph visualization**: Interactive network visualization of the knowledge graph
- **Batch processing**: Efficient processing of large document collections

### Integration Opportunities
- **Database backends**: Support for PostgreSQL, Neo4j, and other graph databases
- **Document processing**: Integration with PDF, Word, and other document formats
- **Real-time updates**: Streaming updates from news feeds and data sources
- **API endpoints**: REST API for integration with other systems

## 🤝 Contributing

This project is based on the OpenAI Cookbook example and serves as a demonstration of temporal knowledge graph concepts. Contributions are welcome!

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Guidelines

- Follow the existing code style
- Add documentation for new features
- Include tests for new functionality
- Update the README for significant changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Cookbook**: This implementation is based on the excellent [Temporal Agents with Knowledge Graphs](https://cookbook.openai.com/examples/partners/temporal_agents_with_knowledge_graphs/temporal_agents_with_knowledge_graphs) cookbook
- **OpenAI**: For providing the language models that power the temporal extraction
- **Streamlit**: For the excellent web framework used in the demo interface

## 📞 Support

For questions, issues, or contributions:

1. Check the [Issues](https://github.com/kaljuvee/temporal-knowledge-graph/issues) page
2. Create a new issue if needed
3. Refer to the OpenAI Cookbook for additional context

---

*Built with ❤️ using OpenAI's temporal knowledge graph concepts*

