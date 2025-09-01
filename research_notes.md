# Temporal Knowledge Graph Research Notes

## Source: OpenAI Cookbook - Temporal Agents with Knowledge Graphs
URL: https://cookbook.openai.com/examples/partners/temporal_agents_with_knowledge_graphs/temporal_agents_with_knowledge_graphs

## Key Concepts

### 1. Temporal Knowledge Graphs
- Traditional knowledge graphs treat facts as static
- Real-world information evolves constantly
- Temporal KGs allow precise time-based querying: "What was true on a given date?"
- Enable timeline construction and trend analysis

### 2. Temporal Agent
- Pipeline component that ingests raw data and produces time-stamped triplets
- Enables precise time-based querying, timeline construction, trend analysis

### 3. Pipeline Architecture
1. Semantic chunking of raw documents
2. Decomposition into statements
3. Temporal Agent creates time-aware triplets
4. Invalidation Agent performs temporal validity checks

### 4. Multi-Step Retrieval
- Direct single-hop queries miss facts distributed across graph topology
- Multi-hop retrieval enables iterative traversal following relationships
- Surfaces complex dependencies and latent connections

### 5. Two Main Workflows
1. **Temporally-aware knowledge graph (KG) construction**
   - Systematically updating and validating knowledge base as new data arrives
   - Routinely validate and update KG entries

2. **Multi-hop retrieval using knowledge graphs**
   - Combine OpenAI models with structured graph queries via tool calls
   - Answer complex, multi-faceted questions requiring reasoning over linked facts

## Implementation Components
- Planners: Task-oriented vs Hypothesis-oriented
- Tool Design: Fixed tools vs Free-form tools vs Semi-structured tools
- Evaluation: Expert-curated "golden" answers vs Automated judgments

## Production Best Practices
1. Keep the graph lean with archival policies
2. Parallelize the ingestion pipeline
3. Integrate robust production safeguards



## Detailed Implementation Findings

### Temporal Agent Key Enhancements
1. **Temporal validity extraction** - Builds on Graphiti's prompt design to identify temporal spans and episodic context
2. **Fact invalidation logic** - Bidirectional checks and constraints comparisons by episodic type
3. **Temporal & episodic typing** - Differentiates between:
   - Fact types: `Fact`, `Opinion`, `Prediction`
   - Temporal classes: `Static`, `Dynamic`, `Atemporal`
4. **Multi-event extraction** - Handles compound sentences and nested date references

### Triplet Structure
- **Subject** - the entity you are talking about
- **Predicate** - the type of relationship or property  
- **Object** - the value or other entity that the subject is connected to

Example triplet: `"London" - "isCapitalOf" - "United Kingdom"`

### Statement Invalidation Example
- Existing statement: "Person YY is CEO of Company XX" (valid_from: 2014-10-23, valid_to: current date)
- Updated statement: "Person YY is CEO of Company XX" (valid_from: 2014-10-23, valid_to: 2023-12-31)
- This shows how temporal validity is updated when new information arrives

### Technologies Referenced
- **Zep** - Memory management for AI applications
- **Graphiti** - Knowledge graph framework that this implementation builds upon


## Complete Pipeline Architecture

### 11-Step Implementation Process
1. Load transcripts
2. Creating a Semantic Chunker
3. Laying the Foundations for our Temporal Agent
4. Statement Extraction
5. Temporal Range Extraction
6. Creating our Triplets
7. Temporal Events
8. Defining our Temporal Agent
9. Entity Resolution
10. Invalidation Agent
11. Building our pipeline

### Pipeline Flow Diagram
```
Transcript 
    ↓
Semantic Chunking
    ↓
Chunks
    ↓
Statement Extraction
    ↓
Labelled Statements
    ↓
Triplet extraction → Temporal agent
    ↓                      ↓
Triplets & entities    Temporal range
    ↓                      ↓
Entity resolution      Temporal events
    ↓                      ↓
Triplets & resolved entities
    ↓
Invalidation agent
    ↓
Validated events
```

### Temporal Agent Pipeline (3 stages)
1. **Temporal Classification**: Atemporal, Static, Dynamic
2. **Temporal Event Extraction**: Extract temporal information
3. **Temporal Validity Check**: t_created, t_expired, t_valid, t_invalid

### Key Timestamps
- `t_created`: When statement was created
- `t_expired`: When statement expires
- `t_valid`: When statement becomes valid
- `t_invalid`: When statement becomes invalid
- `invalidated_by`: Links to statements that invalidate this one

