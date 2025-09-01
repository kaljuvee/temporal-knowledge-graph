"""
Temporal Agent for processing statements and extracting temporal information
Based on OpenAI Cookbook: Temporal Agents with Knowledge Graphs
"""

import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dateutil.parser import parse as parse_date
import openai
from openai import OpenAI

from models import (
    Statement, Triplet, TemporalEvent, TemporalClass, FactType, 
    KnowledgeGraph, TemporalQuery, QueryResult
)


class TemporalAgent:
    """Agent for processing temporal information in knowledge graphs"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Using the recommended model from cookbook
    
    def classify_temporal_type(self, text: str) -> TemporalClass:
        """Classify a statement as atemporal, static, or dynamic"""
        
        prompt = f"""
        Classify the following statement into one of these temporal categories:
        
        1. ATEMPORAL: Statements that never change (e.g., "The speed of light is 3×10⁸ m s⁻¹", "Water freezes at zero degrees")
        2. STATIC: Statements that are valid from a point in time but do not change afterwards (e.g., "Company A acquired Company B on January 1, 2020")
        3. DYNAMIC: Statements that evolve over time (e.g., "Boris was CEO from 2019 to 2022")
        
        Statement: "{text}"
        
        Respond with only one word: ATEMPORAL, STATIC, or DYNAMIC
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=10
            )
            
            classification = response.choices[0].message.content.strip().upper()
            
            if classification in ["ATEMPORAL", "STATIC", "DYNAMIC"]:
                return TemporalClass(classification.lower())
            else:
                return TemporalClass.STATIC  # Default fallback
                
        except Exception as e:
            print(f"Error in temporal classification: {e}")
            return TemporalClass.STATIC
    
    def extract_temporal_events(self, text: str, reference_date: Optional[datetime] = None) -> Optional[TemporalEvent]:
        """Extract temporal information from text"""
        
        if reference_date is None:
            reference_date = datetime.now()
        
        prompt = f"""
        Extract temporal information from the following statement. Look for:
        - Creation dates (when something was established/created)
        - Expiration dates (when something ends/expires)
        - Valid from dates (when something becomes valid)
        - Invalid from dates (when something becomes invalid)
        
        Statement: "{text}"
        Reference date: {reference_date.isoformat()}
        
        Return a JSON object with the following structure (use null for missing dates):
        {{
            "t_created": "ISO datetime or null",
            "t_expired": "ISO datetime or null", 
            "t_valid": "ISO datetime or null",
            "t_invalid": "ISO datetime or null"
        }}
        
        For relative dates like "yesterday", "last month", calculate based on the reference date.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            
            # Parse dates
            temporal_event = TemporalEvent()
            
            if result.get("t_created"):
                temporal_event.t_created = parse_date(result["t_created"])
            if result.get("t_expired"):
                temporal_event.t_expired = parse_date(result["t_expired"])
            if result.get("t_valid"):
                temporal_event.t_valid = parse_date(result["t_valid"])
            if result.get("t_invalid"):
                temporal_event.t_invalid = parse_date(result["t_invalid"])
            
            return temporal_event
            
        except Exception as e:
            print(f"Error in temporal event extraction: {e}")
            return None
    
    def extract_triplets(self, text: str) -> List[Triplet]:
        """Extract knowledge graph triplets from text"""
        
        prompt = f"""
        Extract knowledge graph triplets from the following statement.
        Each triplet should be in the format: Subject - Predicate - Object
        
        Statement: "{text}"
        
        Return a JSON array of triplets:
        [
            {{"subject": "entity1", "predicate": "relationship", "object": "entity2"}},
            {{"subject": "entity2", "predicate": "property", "object": "value"}}
        ]
        
        Focus on the most important relationships and facts in the statement.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            
            triplets = []
            for item in result:
                triplet = Triplet(
                    subject=item["subject"],
                    predicate=item["predicate"],
                    object=item["object"]
                )
                triplets.append(triplet)
            
            return triplets
            
        except Exception as e:
            print(f"Error in triplet extraction: {e}")
            return []
    
    def process_statement(self, text: str, statement_id: Optional[str] = None, 
                         source: Optional[str] = None, reference_date: Optional[datetime] = None) -> Statement:
        """Process a text statement through the complete temporal pipeline"""
        
        if statement_id is None:
            statement_id = f"stmt_{hash(text) % 1000000}"
        
        if reference_date is None:
            reference_date = datetime.now()
        
        # Step 1: Temporal Classification
        temporal_class = self.classify_temporal_type(text)
        
        # Step 2: Extract triplets
        triplets = self.extract_triplets(text)
        
        # Step 3: Extract temporal events
        temporal_event = self.extract_temporal_events(text, reference_date)
        
        # Create statement
        statement = Statement(
            id=statement_id,
            text=text,
            temporal_class=temporal_class,
            fact_type=FactType.FACT,  # Could be enhanced to detect opinion/prediction
            triplets=triplets,
            temporal_event=temporal_event,
            source=source,
            confidence=0.8  # Could be enhanced with confidence scoring
        )
        
        return statement
    
    def process_document(self, text: str, source: Optional[str] = None, 
                        reference_date: Optional[datetime] = None) -> List[Statement]:
        """Process a document by chunking it into statements"""
        
        # Simple sentence-based chunking (could be enhanced with semantic chunking)
        sentences = self._chunk_text(text)
        
        statements = []
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 10:  # Filter out very short sentences
                statement_id = f"{source or 'doc'}_{i}" if source else f"stmt_{i}"
                statement = self.process_statement(
                    sentence, 
                    statement_id=statement_id,
                    source=source,
                    reference_date=reference_date
                )
                statements.append(statement)
        
        return statements
    
    def _chunk_text(self, text: str) -> List[str]:
        """Simple text chunking by sentences"""
        # Split by sentence endings
        sentences = re.split(r'[.!?]+', text)
        
        # Clean up and filter
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Filter very short fragments
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def check_invalidation(self, new_statement: Statement, existing_statements: List[Statement]) -> List[str]:
        """Check if a new statement invalidates any existing statements"""
        
        invalidated_ids = []
        
        # Simple invalidation logic based on conflicting triplets
        for existing in existing_statements:
            if self._statements_conflict(new_statement, existing):
                invalidated_ids.append(existing.id)
        
        return invalidated_ids
    
    def _statements_conflict(self, stmt1: Statement, stmt2: Statement) -> bool:
        """Check if two statements conflict with each other"""
        
        # Check for conflicting triplets with same subject and predicate but different objects
        for t1 in stmt1.triplets:
            for t2 in stmt2.triplets:
                if (t1.subject == t2.subject and 
                    t1.predicate == t2.predicate and 
                    t1.object != t2.object):
                    
                    # Check temporal validity - newer statement might invalidate older one
                    if (stmt1.temporal_event and stmt2.temporal_event and
                        stmt1.temporal_event.t_created and stmt2.temporal_event.t_created):
                        
                        if stmt1.temporal_event.t_created > stmt2.temporal_event.t_created:
                            return True
        
        return False


class TemporalQueryEngine:
    """Engine for querying temporal knowledge graphs"""
    
    def __init__(self, knowledge_graph: KnowledgeGraph, api_key: Optional[str] = None):
        self.kg = knowledge_graph
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def query(self, query: TemporalQuery) -> QueryResult:
        """Execute a temporal query against the knowledge graph"""
        
        result = QueryResult()
        
        # Entity-based query
        if query.entity:
            statements = self.kg.get_statements_for_entity(query.entity)
            
            # Filter by timestamp if provided
            if query.timestamp:
                statements = [s for s in statements if s.is_valid_at(query.timestamp)]
            
            result.statements = statements
            result.timeline = self.kg.get_timeline_for_entity(query.entity)
        
        # Temporal range query
        elif query.temporal_range:
            start_time, end_time = query.temporal_range
            statements = []
            
            for stmt in self.kg.statements.values():
                if stmt.temporal_event:
                    # Check if statement overlaps with query range
                    stmt_start = stmt.temporal_event.t_valid or stmt.temporal_event.t_created
                    stmt_end = stmt.temporal_event.t_invalid or stmt.temporal_event.t_expired
                    
                    if stmt_start and stmt_start <= end_time:
                        if not stmt_end or stmt_end >= start_time:
                            statements.append(stmt)
            
            result.statements = statements
        
        # Natural language query
        if query.question:
            result.answer = self._answer_question(query.question, result.statements)
        
        result.confidence = 0.8  # Could be enhanced with proper confidence scoring
        
        return result
    
    def _answer_question(self, question: str, relevant_statements: List[Statement]) -> str:
        """Generate a natural language answer based on relevant statements"""
        
        if not relevant_statements:
            return "No relevant information found in the knowledge graph."
        
        # Prepare context from statements
        context = []
        for stmt in relevant_statements[:10]:  # Limit to top 10 statements
            context.append(f"- {stmt.text}")
            if stmt.temporal_event:
                if stmt.temporal_event.t_valid:
                    context.append(f"  Valid from: {stmt.temporal_event.t_valid}")
                if stmt.temporal_event.t_invalid:
                    context.append(f"  Valid until: {stmt.temporal_event.t_invalid}")
        
        context_text = "\n".join(context)
        
        prompt = f"""
        Based on the following temporal knowledge graph information, answer the question.
        
        Question: {question}
        
        Relevant Information:
        {context_text}
        
        Provide a clear, concise answer based on the temporal information available.
        If the information is time-sensitive, mention the relevant time periods.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "Error generating answer from the knowledge graph."

