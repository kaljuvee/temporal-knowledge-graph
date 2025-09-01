"""
Utility functions for the Temporal Knowledge Graph system
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Optional dotenv import - gracefully handle if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, skip loading .env file
    pass

from models import (
    Statement, KnowledgeGraph, TemporalQuery, QueryResult, 
    TemporalClass, FactType, Triplet, TemporalEvent
)
from temporal_agent import TemporalAgent, TemporalQueryEngine


class KnowledgeGraphManager:
    """Manager for temporal knowledge graph operations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the knowledge graph manager
        
        Args:
            api_key: OpenAI API key. If None, will try to load from environment variables.
        """
        # Use provided API key or load from environment
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. "
                "Provide it as a parameter or set OPENAI_API_KEY environment variable "
                "or create a .env file with OPENAI_API_KEY=your-key-here"
            )
        
        self.kg = KnowledgeGraph()
        self.agent = TemporalAgent(api_key=api_key)
        self.query_engine = TemporalQueryEngine(self.kg, api_key=api_key)
    
    def add_document(self, text: str, source: Optional[str] = None, 
                    reference_date: Optional[datetime] = None) -> List[Statement]:
        """Add a document to the knowledge graph"""
        
        statements = self.agent.process_document(text, source, reference_date)
        
        for statement in statements:
            # Check for invalidations
            existing_statements = list(self.kg.statements.values())
            invalidated_ids = self.agent.check_invalidation(statement, existing_statements)
            
            # Mark invalidated statements
            for inv_id in invalidated_ids:
                self.kg.invalidate_statement(inv_id, statement.id)
            
            # Add the new statement
            self.kg.add_statement(statement)
        
        return statements
    
    def add_statement_text(self, text: str, source: Optional[str] = None,
                          reference_date: Optional[datetime] = None) -> Statement:
        """Add a single statement to the knowledge graph"""
        
        statement = self.agent.process_statement(text, source=source, reference_date=reference_date)
        
        # Check for invalidations
        existing_statements = list(self.kg.statements.values())
        invalidated_ids = self.agent.check_invalidation(statement, existing_statements)
        
        # Mark invalidated statements
        for inv_id in invalidated_ids:
            self.kg.invalidate_statement(inv_id, statement.id)
        
        # Add the new statement
        self.kg.add_statement(statement)
        
        return statement
    
    def query_entity(self, entity: str, timestamp: Optional[datetime] = None) -> QueryResult:
        """Query information about a specific entity"""
        
        query = TemporalQuery(entity=entity, timestamp=timestamp)
        return self.query_engine.query(query)
    
    def query_natural_language(self, question: str) -> QueryResult:
        """Query using natural language"""
        
        query = TemporalQuery(question=question)
        return self.query_engine.query(query)
    
    def get_entity_timeline(self, entity: str) -> List[Dict[str, Any]]:
        """Get timeline of events for an entity"""
        
        return self.kg.get_timeline_for_entity(entity)
    
    def get_all_entities(self) -> List[str]:
        """Get all entities in the knowledge graph"""
        
        return list(self.kg.entities.keys())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge graph"""
        
        stats = {
            "total_statements": len(self.kg.statements),
            "total_entities": len(self.kg.entities),
            "temporal_classes": {},
            "fact_types": {},
            "statements_with_temporal_events": 0,
            "invalidated_statements": 0
        }
        
        for statement in self.kg.statements.values():
            # Count temporal classes
            tc = statement.temporal_class.value
            stats["temporal_classes"][tc] = stats["temporal_classes"].get(tc, 0) + 1
            
            # Count fact types
            ft = statement.fact_type.value
            stats["fact_types"][ft] = stats["fact_types"].get(ft, 0) + 1
            
            # Count temporal events
            if statement.temporal_event:
                stats["statements_with_temporal_events"] += 1
            
            # Count invalidated statements
            if statement.invalidated_by:
                stats["invalidated_statements"] += 1
        
        return stats
    
    def save_to_file(self, filepath: str) -> None:
        """Save knowledge graph to file"""
        
        data = {
            "statements": {sid: stmt.dict() for sid, stmt in self.kg.statements.items()},
            "entities": self.kg.entities,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_from_file(self, filepath: str) -> None:
        """Load knowledge graph from file"""
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct knowledge graph
        self.kg = KnowledgeGraph()
        
        for sid, stmt_data in data["statements"].items():
            # Convert datetime strings back to datetime objects
            if stmt_data.get("temporal_event"):
                te = stmt_data["temporal_event"]
                for key in ["t_created", "t_expired", "t_valid", "t_invalid"]:
                    if te.get(key):
                        te[key] = datetime.fromisoformat(te[key])
            
            statement = Statement(**stmt_data)
            self.kg.add_statement(statement)
        
        # Update query engine
        self.query_engine = TemporalQueryEngine(self.kg, self.agent.client.api_key)


def format_timeline_for_display(timeline: List[Dict[str, Any]]) -> str:
    """Format timeline for human-readable display"""
    
    if not timeline:
        return "No timeline events found."
    
    formatted = []
    formatted.append("Timeline of Events:")
    formatted.append("=" * 50)
    
    for event in timeline:
        formatted.append(f"\n📅 Statement: {event['text']}")
        formatted.append(f"   Type: {event['temporal_class']} ({event['fact_type']})")
        
        if event.get('triplets'):
            formatted.append("   Triplets:")
            for triplet in event['triplets']:
                formatted.append(f"     • {triplet}")
        
        te = event.get('temporal_event', {})
        if te:
            if te.get('t_created'):
                formatted.append(f"   Created: {te['t_created']}")
            if te.get('t_valid'):
                formatted.append(f"   Valid from: {te['t_valid']}")
            if te.get('t_invalid'):
                formatted.append(f"   Valid until: {te['t_invalid']}")
            if te.get('t_expired'):
                formatted.append(f"   Expires: {te['t_expired']}")
        
        formatted.append("-" * 30)
    
    return "\n".join(formatted)


def format_query_result(result: QueryResult) -> str:
    """Format query result for human-readable display"""
    
    formatted = []
    
    if result.answer:
        formatted.append(f"Answer: {result.answer}")
        formatted.append("")
    
    if result.statements:
        formatted.append(f"Found {len(result.statements)} relevant statements:")
        formatted.append("=" * 50)
        
        for i, stmt in enumerate(result.statements, 1):
            formatted.append(f"\n{i}. {stmt.text}")
            formatted.append(f"   Type: {stmt.temporal_class.value} ({stmt.fact_type.value})")
            formatted.append(f"   Source: {stmt.source or 'Unknown'}")
            
            if stmt.triplets:
                formatted.append("   Triplets:")
                for triplet in stmt.triplets:
                    formatted.append(f"     • {triplet}")
            
            if stmt.temporal_event:
                te = stmt.temporal_event
                if te.t_valid:
                    formatted.append(f"   Valid from: {te.t_valid}")
                if te.t_invalid:
                    formatted.append(f"   Valid until: {te.t_invalid}")
            
            if stmt.invalidated_by:
                formatted.append(f"   Invalidated by: {', '.join(stmt.invalidated_by)}")
    
    if result.timeline:
        formatted.append("\n" + format_timeline_for_display(result.timeline))
    
    if not result.statements and not result.answer:
        formatted.append("No relevant information found.")
    
    return "\n".join(formatted)


def create_sample_data() -> List[str]:
    """Create sample data for demonstration"""
    
    sample_texts = [
        "John Smith was appointed CEO of TechCorp on January 15, 2020.",
        "TechCorp acquired DataSystems Inc. for $50 million in March 2021.",
        "John Smith resigned as CEO of TechCorp on December 31, 2023.",
        "Sarah Johnson became the new CEO of TechCorp on January 1, 2024.",
        "TechCorp's headquarters is located in San Francisco, California.",
        "The speed of light in vacuum is approximately 299,792,458 meters per second.",
        "TechCorp reported revenue of $100 million in 2023.",
        "DataSystems Inc. was founded in 2015 by Mike Wilson.",
        "TechCorp plans to expand to European markets by 2025.",
        "Sarah Johnson previously worked as CTO at InnovateTech for 5 years."
    ]
    
    return sample_texts


def demo_knowledge_graph(api_key: Optional[str] = None) -> KnowledgeGraphManager:
    """Create a demo knowledge graph with sample data"""
    
    manager = KnowledgeGraphManager(api_key=api_key)
    
    print("Creating demo knowledge graph...")
    
    sample_texts = create_sample_data()
    
    for i, text in enumerate(sample_texts):
        print(f"Processing statement {i+1}/{len(sample_texts)}: {text[:50]}...")
        manager.add_statement_text(text, source=f"demo_doc_{i//3}")
    
    print(f"\nDemo knowledge graph created!")
    print(f"Statistics: {manager.get_statistics()}")
    
    return manager

