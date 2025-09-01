"""
Core data models for Temporal Knowledge Graph
Based on OpenAI Cookbook: Temporal Agents with Knowledge Graphs
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum


class TemporalClass(str, Enum):
    """Temporal classification of statements"""
    ATEMPORAL = "atemporal"  # Never change (e.g., "The speed of light is 3×10⁸ m s⁻¹")
    STATIC = "static"        # Valid from a point in time but do not change afterwards
    DYNAMIC = "dynamic"      # Evolve over time


class FactType(str, Enum):
    """Type of fact being represented"""
    FACT = "fact"           # Objective, verifiable information
    OPINION = "opinion"     # Subjective viewpoint
    PREDICTION = "prediction"  # Future-oriented statement


class TemporalEvent(BaseModel):
    """Represents a temporal event with validity periods"""
    t_created: Optional[datetime] = Field(None, description="When the statement was created")
    t_expired: Optional[datetime] = Field(None, description="When the statement expires")
    t_valid: Optional[datetime] = Field(None, description="When the statement becomes valid")
    t_invalid: Optional[datetime] = Field(None, description="When the statement becomes invalid")
    
    def is_valid_at(self, timestamp: datetime) -> bool:
        """Check if the event is valid at a given timestamp"""
        if self.t_valid and timestamp < self.t_valid:
            return False
        if self.t_invalid and timestamp >= self.t_invalid:
            return False
        if self.t_expired and timestamp >= self.t_expired:
            return False
        return True


class Triplet(BaseModel):
    """Knowledge graph triplet: Subject-Predicate-Object"""
    subject: str = Field(..., description="The entity being described")
    predicate: str = Field(..., description="The relationship or property")
    object: str = Field(..., description="The value or target entity")
    
    def __str__(self) -> str:
        return f'"{self.subject}" - "{self.predicate}" - "{self.object}"'


class Statement(BaseModel):
    """A statement extracted from text with temporal information"""
    id: str = Field(..., description="Unique identifier for the statement")
    text: str = Field(..., description="Original text of the statement")
    temporal_class: TemporalClass = Field(..., description="Temporal classification")
    fact_type: FactType = Field(FactType.FACT, description="Type of fact")
    triplets: List[Triplet] = Field(default_factory=list, description="Extracted triplets")
    temporal_event: Optional[TemporalEvent] = Field(None, description="Temporal validity information")
    source: Optional[str] = Field(None, description="Source of the statement")
    confidence: float = Field(1.0, description="Confidence score for the extraction")
    invalidated_by: List[str] = Field(default_factory=list, description="IDs of statements that invalidate this one")
    
    def is_valid_at(self, timestamp: datetime) -> bool:
        """Check if the statement is valid at a given timestamp"""
        if self.temporal_event:
            return self.temporal_event.is_valid_at(timestamp)
        return True


class KnowledgeGraph(BaseModel):
    """Temporal Knowledge Graph containing statements and their relationships"""
    statements: Dict[str, Statement] = Field(default_factory=dict, description="All statements in the graph")
    entities: Dict[str, List[str]] = Field(default_factory=dict, description="Entity to statement mappings")
    
    def add_statement(self, statement: Statement) -> None:
        """Add a statement to the knowledge graph"""
        self.statements[statement.id] = statement
        
        # Index entities
        for triplet in statement.triplets:
            if triplet.subject not in self.entities:
                self.entities[triplet.subject] = []
            if statement.id not in self.entities[triplet.subject]:
                self.entities[triplet.subject].append(statement.id)
                
            if triplet.object not in self.entities:
                self.entities[triplet.object] = []
            if statement.id not in self.entities[triplet.object]:
                self.entities[triplet.object].append(statement.id)
    
    def get_statements_for_entity(self, entity: str) -> List[Statement]:
        """Get all statements involving a specific entity"""
        statement_ids = self.entities.get(entity, [])
        return [self.statements[sid] for sid in statement_ids if sid in self.statements]
    
    def get_valid_statements_at(self, timestamp: datetime) -> List[Statement]:
        """Get all statements that are valid at a given timestamp"""
        return [stmt for stmt in self.statements.values() if stmt.is_valid_at(timestamp)]
    
    def invalidate_statement(self, statement_id: str, invalidated_by_id: str) -> None:
        """Mark a statement as invalidated by another statement"""
        if statement_id in self.statements:
            self.statements[statement_id].invalidated_by.append(invalidated_by_id)
    
    def get_timeline_for_entity(self, entity: str) -> List[Dict[str, Any]]:
        """Get a timeline of all events for a specific entity"""
        statements = self.get_statements_for_entity(entity)
        timeline = []
        
        for stmt in statements:
            if stmt.temporal_event:
                event_data = {
                    "statement_id": stmt.id,
                    "text": stmt.text,
                    "temporal_class": stmt.temporal_class,
                    "fact_type": stmt.fact_type,
                    "triplets": [str(t) for t in stmt.triplets],
                    "temporal_event": stmt.temporal_event.dict()
                }
                timeline.append(event_data)
        
        # Sort by creation time or valid time
        timeline.sort(key=lambda x: x["temporal_event"].get("t_created") or 
                                   x["temporal_event"].get("t_valid") or 
                                   datetime.min)
        
        return timeline


class TemporalQuery(BaseModel):
    """Query for temporal knowledge graph"""
    entity: Optional[str] = Field(None, description="Entity to query about")
    predicate: Optional[str] = Field(None, description="Relationship to query")
    timestamp: Optional[datetime] = Field(None, description="Timestamp for temporal query")
    temporal_range: Optional[tuple] = Field(None, description="Time range for query")
    question: Optional[str] = Field(None, description="Natural language question")


class QueryResult(BaseModel):
    """Result of a temporal knowledge graph query"""
    statements: List[Statement] = Field(default_factory=list, description="Matching statements")
    timeline: List[Dict[str, Any]] = Field(default_factory=list, description="Timeline of events")
    answer: Optional[str] = Field(None, description="Natural language answer")
    confidence: float = Field(0.0, description="Confidence in the result")

