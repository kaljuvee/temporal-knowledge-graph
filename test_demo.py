#!/usr/bin/env python3
"""
Test Demo for Temporal Knowledge Graph (without OpenAI API dependency)
This version uses mock data to demonstrate functionality
"""

import json
from datetime import datetime, timedelta
from models import (
    Statement, Triplet, TemporalEvent, TemporalClass, FactType, 
    KnowledgeGraph, TemporalQuery, QueryResult
)


def create_mock_statement(text: str, statement_id: str, temporal_class: TemporalClass = TemporalClass.STATIC) -> Statement:
    """Create a mock statement with predefined triplets and temporal events"""
    
    # Mock triplet extraction based on common patterns
    triplets = []
    temporal_event = None
    
    if "CEO" in text and "became" in text:
        # Extract CEO appointment
        if "John Smith" in text:
            triplets.append(Triplet(subject="John Smith", predicate="hasRole", object="CEO"))
            triplets.append(Triplet(subject="John Smith", predicate="worksFor", object="TechCorp"))
        elif "Sarah Johnson" in text:
            triplets.append(Triplet(subject="Sarah Johnson", predicate="hasRole", object="CEO"))
            triplets.append(Triplet(subject="Sarah Johnson", predicate="worksFor", object="TechCorp"))
        
        # Mock temporal event
        if "January 1, 2024" in text:
            temporal_event = TemporalEvent(
                t_valid=datetime(2024, 1, 1),
                t_created=datetime.now()
            )
        elif "January 15, 2020" in text:
            temporal_event = TemporalEvent(
                t_valid=datetime(2020, 1, 15),
                t_created=datetime.now()
            )
    
    elif "resigned" in text:
        if "John Smith" in text:
            triplets.append(Triplet(subject="John Smith", predicate="resignedFrom", object="CEO"))
            triplets.append(Triplet(subject="John Smith", predicate="endDate", object="December 31, 2023"))
        
        if "December 31, 2023" in text:
            temporal_event = TemporalEvent(
                t_invalid=datetime(2023, 12, 31),
                t_created=datetime.now()
            )
    
    elif "acquired" in text:
        if "TechCorp" in text and "DataSystems" in text:
            triplets.append(Triplet(subject="TechCorp", predicate="acquired", object="DataSystems Inc"))
            triplets.append(Triplet(subject="TechCorp", predicate="acquisitionPrice", object="$50 million"))
        
        if "March 2021" in text:
            temporal_event = TemporalEvent(
                t_valid=datetime(2021, 3, 1),
                t_created=datetime.now()
            )
    
    elif "headquarters" in text:
        if "TechCorp" in text and "San Francisco" in text:
            triplets.append(Triplet(subject="TechCorp", predicate="hasHeadquarters", object="San Francisco"))
            triplets.append(Triplet(subject="TechCorp", predicate="locatedIn", object="California"))
        temporal_class = TemporalClass.ATEMPORAL
    
    elif "speed of light" in text:
        triplets.append(Triplet(subject="speed of light", predicate="hasValue", object="299,792,458 meters per second"))
        triplets.append(Triplet(subject="speed of light", predicate="measuredIn", object="vacuum"))
        temporal_class = TemporalClass.ATEMPORAL
    
    elif "revenue" in text:
        if "TechCorp" in text and "2023" in text:
            triplets.append(Triplet(subject="TechCorp", predicate="hasRevenue", object="$100 million"))
            triplets.append(Triplet(subject="TechCorp", predicate="revenueYear", object="2023"))
        
        temporal_event = TemporalEvent(
            t_valid=datetime(2023, 1, 1),
            t_invalid=datetime(2024, 1, 1),
            t_created=datetime.now()
        )
    
    elif "founded" in text:
        if "DataSystems" in text and "2015" in text:
            triplets.append(Triplet(subject="DataSystems Inc", predicate="foundedBy", object="Mike Wilson"))
            triplets.append(Triplet(subject="DataSystems Inc", predicate="foundedIn", object="2015"))
        
        temporal_event = TemporalEvent(
            t_valid=datetime(2015, 1, 1),
            t_created=datetime.now()
        )
    
    elif "plans to expand" in text:
        if "TechCorp" in text and "European" in text:
            triplets.append(Triplet(subject="TechCorp", predicate="plansToExpandTo", object="European markets"))
            triplets.append(Triplet(subject="TechCorp", predicate="expansionTarget", object="2025"))
        
        temporal_event = TemporalEvent(
            t_valid=datetime(2025, 1, 1),
            t_created=datetime.now()
        )
        temporal_class = TemporalClass.DYNAMIC
    
    elif "previously worked" in text:
        if "Sarah Johnson" in text and "InnovateTech" in text:
            triplets.append(Triplet(subject="Sarah Johnson", predicate="previouslyWorkedAt", object="InnovateTech"))
            triplets.append(Triplet(subject="Sarah Johnson", predicate="previousRole", object="CTO"))
            triplets.append(Triplet(subject="Sarah Johnson", predicate="workDuration", object="5 years"))
        
        temporal_event = TemporalEvent(
            t_invalid=datetime(2024, 1, 1),  # Ended when she became CEO
            t_created=datetime.now()
        )
    
    return Statement(
        id=statement_id,
        text=text,
        temporal_class=temporal_class,
        fact_type=FactType.FACT,
        triplets=triplets,
        temporal_event=temporal_event,
        source="test_demo",
        confidence=0.9
    )


def test_knowledge_graph():
    """Test the knowledge graph functionality with mock data"""
    
    print("🧠 Testing Temporal Knowledge Graph Functionality")
    print("=" * 60)
    
    # Create knowledge graph
    kg = KnowledgeGraph()
    
    # Sample statements
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
    
    # Add statements to knowledge graph
    print("📝 Adding statements to knowledge graph...")
    for i, text in enumerate(sample_texts):
        statement = create_mock_statement(text, f"stmt_{i+1}")
        kg.add_statement(statement)
        print(f"  ✅ Added: {text[:60]}...")
    
    print(f"\n📊 Knowledge Graph Statistics:")
    print(f"  Total statements: {len(kg.statements)}")
    print(f"  Total entities: {len(kg.entities)}")
    
    # Test entity queries
    print(f"\n🔍 Testing Entity Queries:")
    
    entities_to_test = ["TechCorp", "John Smith", "Sarah Johnson"]
    
    for entity in entities_to_test:
        statements = kg.get_statements_for_entity(entity)
        print(f"\n  Entity: {entity}")
        print(f"  Found {len(statements)} statements:")
        
        for stmt in statements:
            print(f"    • {stmt.text}")
            if stmt.temporal_event:
                if stmt.temporal_event.t_valid:
                    print(f"      Valid from: {stmt.temporal_event.t_valid}")
                if stmt.temporal_event.t_invalid:
                    print(f"      Valid until: {stmt.temporal_event.t_invalid}")
    
    # Test temporal queries
    print(f"\n📅 Testing Temporal Queries:")
    
    # Query at specific times
    test_dates = [
        datetime(2022, 6, 1),  # During John Smith's tenure
        datetime(2024, 6, 1),  # During Sarah Johnson's tenure
    ]
    
    for test_date in test_dates:
        print(f"\n  Querying at {test_date.strftime('%Y-%m-%d')}:")
        valid_statements = kg.get_valid_statements_at(test_date)
        
        for stmt in valid_statements:
            if any(entity in stmt.text for entity in ["CEO", "TechCorp"]):
                print(f"    • {stmt.text}")
    
    # Test timeline
    print(f"\n📈 Testing Timeline for TechCorp:")
    timeline = kg.get_timeline_for_entity("TechCorp")
    
    for event in timeline:
        print(f"  📅 {event['text']}")
        te = event.get('temporal_event', {})
        if te.get('t_valid'):
            print(f"     Valid from: {te['t_valid']}")
        if te.get('t_invalid'):
            print(f"     Valid until: {te['t_invalid']}")
    
    # Test temporal classes
    print(f"\n🏷️ Testing Temporal Classifications:")
    temporal_counts = {}
    for stmt in kg.statements.values():
        tc = stmt.temporal_class.value
        temporal_counts[tc] = temporal_counts.get(tc, 0) + 1
    
    for tc, count in temporal_counts.items():
        print(f"  {tc.title()}: {count} statements")
    
    # Test triplet extraction
    print(f"\n🔗 Sample Triplets:")
    triplet_count = 0
    for stmt in kg.statements.values():
        for triplet in stmt.triplets:
            if triplet_count < 10:  # Show first 10 triplets
                print(f"  • {triplet}")
                triplet_count += 1
    
    print(f"\n✅ Test completed successfully!")
    print(f"   Total triplets extracted: {sum(len(stmt.triplets) for stmt in kg.statements.values())}")
    
    return kg


def test_cli_functionality():
    """Test CLI-like functionality"""
    
    print("\n" + "=" * 60)
    print("🖥️ Testing CLI Functionality")
    print("=" * 60)
    
    kg = test_knowledge_graph()
    
    # Simulate CLI queries
    print(f"\n💬 Simulating Natural Language Queries:")
    
    queries = [
        "Who was CEO of TechCorp in 2022?",
        "When did Sarah Johnson become CEO?",
        "What acquisitions did TechCorp make?",
        "Where is TechCorp located?"
    ]
    
    for query in queries:
        print(f"\n  ❓ Query: {query}")
        
        # Simple keyword-based matching for demo
        relevant_statements = []
        
        if "CEO" in query and "2022" in query:
            # Find CEO statements valid in 2022
            test_date = datetime(2022, 6, 1)
            for stmt in kg.statements.values():
                if "CEO" in stmt.text and stmt.is_valid_at(test_date):
                    relevant_statements.append(stmt)
        
        elif "Sarah Johnson" in query and "CEO" in query:
            for stmt in kg.statements.values():
                if "Sarah Johnson" in stmt.text and "CEO" in stmt.text:
                    relevant_statements.append(stmt)
        
        elif "acquisitions" in query or "acquired" in query:
            for stmt in kg.statements.values():
                if "acquired" in stmt.text:
                    relevant_statements.append(stmt)
        
        elif "located" in query or "headquarters" in query:
            for stmt in kg.statements.values():
                if "headquarters" in stmt.text or "located" in stmt.text:
                    relevant_statements.append(stmt)
        
        if relevant_statements:
            print(f"     Found {len(relevant_statements)} relevant statements:")
            for stmt in relevant_statements:
                print(f"     • {stmt.text}")
        else:
            print(f"     No relevant statements found.")
    
    print(f"\n✅ CLI functionality test completed!")


if __name__ == "__main__":
    test_cli_functionality()

