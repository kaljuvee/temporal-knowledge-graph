#!/usr/bin/env python3
"""
Command Line Interface Demo for Temporal Knowledge Graph
Based on OpenAI Cookbook: Temporal Agents with Knowledge Graphs
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Optional

from utils import KnowledgeGraphManager, format_query_result, format_timeline_for_display, demo_knowledge_graph
from models import TemporalQuery


def main():
    parser = argparse.ArgumentParser(
        description="Temporal Knowledge Graph CLI Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create demo knowledge graph
  python cli_demo.py --demo
  
  # Add a statement
  python cli_demo.py --add "John became CEO on Jan 1, 2024"
  
  # Query an entity
  python cli_demo.py --query-entity "John Smith"
  
  # Ask a natural language question
  python cli_demo.py --ask "Who was CEO of TechCorp in 2023?"
  
  # Get entity timeline
  python cli_demo.py --timeline "TechCorp"
  
  # Load from file and query
  python cli_demo.py --load kg.json --ask "What happened in 2023?"
        """
    )
    
    # API key
    parser.add_argument(
        "--api-key", 
        type=str, 
        default=os.getenv("OPENAI_API_KEY"),
        help="OpenAI API key (default: from OPENAI_API_KEY env var)"
    )
    
    # Knowledge graph file operations
    parser.add_argument(
        "--load", 
        type=str, 
        help="Load knowledge graph from JSON file"
    )
    
    parser.add_argument(
        "--save", 
        type=str, 
        help="Save knowledge graph to JSON file"
    )
    
    # Demo mode
    parser.add_argument(
        "--demo", 
        action="store_true",
        help="Create and explore demo knowledge graph"
    )
    
    # Add content
    parser.add_argument(
        "--add", 
        type=str, 
        help="Add a statement to the knowledge graph"
    )
    
    parser.add_argument(
        "--add-file", 
        type=str, 
        help="Add content from a text file"
    )
    
    parser.add_argument(
        "--source", 
        type=str, 
        help="Source identifier for added content"
    )
    
    # Query operations
    parser.add_argument(
        "--query-entity", 
        type=str, 
        help="Query information about a specific entity"
    )
    
    parser.add_argument(
        "--ask", 
        type=str, 
        help="Ask a natural language question"
    )
    
    parser.add_argument(
        "--timeline", 
        type=str, 
        help="Get timeline for an entity"
    )
    
    parser.add_argument(
        "--at-time", 
        type=str, 
        help="Query at specific time (ISO format: 2024-01-01T12:00:00)"
    )
    
    # Display options
    parser.add_argument(
        "--list-entities", 
        action="store_true",
        help="List all entities in the knowledge graph"
    )
    
    parser.add_argument(
        "--stats", 
        action="store_true",
        help="Show knowledge graph statistics"
    )
    
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Check API key
    if not args.api_key:
        print("Error: OpenAI API key required. Set OPENAI_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    # Initialize knowledge graph manager
    manager = KnowledgeGraphManager(api_key=args.api_key)
    
    # Load existing knowledge graph if specified
    if args.load:
        try:
            manager.load_from_file(args.load)
            if args.verbose:
                print(f"Loaded knowledge graph from {args.load}")
        except Exception as e:
            print(f"Error loading knowledge graph: {e}")
            sys.exit(1)
    
    # Demo mode
    if args.demo:
        print("🧠 Temporal Knowledge Graph Demo")
        print("=" * 50)
        
        manager = demo_knowledge_graph(api_key=args.api_key)
        
        print("\n📊 Knowledge Graph Statistics:")
        stats = manager.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n🏢 Available Entities:")
        entities = manager.get_all_entities()
        for entity in sorted(entities)[:10]:  # Show first 10
            print(f"  • {entity}")
        if len(entities) > 10:
            print(f"  ... and {len(entities) - 10} more")
        
        print("\n💡 Try these queries:")
        print("  python cli_demo.py --ask 'Who was CEO of TechCorp in 2023?'")
        print("  python cli_demo.py --timeline 'TechCorp'")
        print("  python cli_demo.py --query-entity 'John Smith'")
        
        if args.save:
            manager.save_to_file(args.save)
            print(f"\n💾 Saved demo knowledge graph to {args.save}")
        
        return
    
    # Add content
    if args.add:
        try:
            statement = manager.add_statement_text(args.add, source=args.source)
            print(f"✅ Added statement: {statement.text}")
            print(f"   ID: {statement.id}")
            print(f"   Temporal class: {statement.temporal_class.value}")
            print(f"   Triplets: {len(statement.triplets)}")
            
            if args.verbose and statement.triplets:
                for triplet in statement.triplets:
                    print(f"     • {triplet}")
                    
        except Exception as e:
            print(f"Error adding statement: {e}")
            sys.exit(1)
    
    if args.add_file:
        try:
            with open(args.add_file, 'r') as f:
                content = f.read()
            
            statements = manager.add_document(content, source=args.source or args.add_file)
            print(f"✅ Added {len(statements)} statements from {args.add_file}")
            
            if args.verbose:
                for stmt in statements:
                    print(f"  • {stmt.text[:80]}...")
                    
        except Exception as e:
            print(f"Error adding file: {e}")
            sys.exit(1)
    
    # Parse timestamp if provided
    query_time = None
    if args.at_time:
        try:
            query_time = datetime.fromisoformat(args.at_time)
        except ValueError:
            print(f"Error: Invalid timestamp format. Use ISO format like 2024-01-01T12:00:00")
            sys.exit(1)
    
    # Query operations
    if args.query_entity:
        try:
            result = manager.query_entity(args.query_entity, timestamp=query_time)
            
            print(f"🔍 Query results for entity: {args.query_entity}")
            if query_time:
                print(f"   At time: {query_time}")
            print("=" * 50)
            
            print(format_query_result(result))
            
        except Exception as e:
            print(f"Error querying entity: {e}")
            sys.exit(1)
    
    if args.ask:
        try:
            result = manager.query_natural_language(args.ask)
            
            print(f"❓ Question: {args.ask}")
            print("=" * 50)
            
            print(format_query_result(result))
            
        except Exception as e:
            print(f"Error processing question: {e}")
            sys.exit(1)
    
    if args.timeline:
        try:
            timeline = manager.get_entity_timeline(args.timeline)
            
            print(f"📅 Timeline for: {args.timeline}")
            print("=" * 50)
            
            print(format_timeline_for_display(timeline))
            
        except Exception as e:
            print(f"Error getting timeline: {e}")
            sys.exit(1)
    
    # Display operations
    if args.list_entities:
        entities = manager.get_all_entities()
        print(f"🏢 Entities in knowledge graph ({len(entities)} total):")
        print("=" * 50)
        
        for entity in sorted(entities):
            statements = manager.kg.get_statements_for_entity(entity)
            print(f"  • {entity} ({len(statements)} statements)")
    
    if args.stats:
        stats = manager.get_statistics()
        print("📊 Knowledge Graph Statistics:")
        print("=" * 50)
        
        for key, value in stats.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for subkey, subvalue in value.items():
                    print(f"  {subkey}: {subvalue}")
            else:
                print(f"{key}: {value}")
    
    # Save if requested
    if args.save:
        try:
            manager.save_to_file(args.save)
            print(f"💾 Saved knowledge graph to {args.save}")
        except Exception as e:
            print(f"Error saving knowledge graph: {e}")
            sys.exit(1)


def interactive_mode():
    """Interactive CLI mode"""
    
    print("🧠 Temporal Knowledge Graph - Interactive Mode")
    print("=" * 50)
    print("Commands:")
    print("  add <text>        - Add a statement")
    print("  query <entity>    - Query an entity")
    print("  ask <question>    - Ask a natural language question")
    print("  timeline <entity> - Get entity timeline")
    print("  entities          - List all entities")
    print("  stats             - Show statistics")
    print("  save <file>       - Save knowledge graph")
    print("  load <file>       - Load knowledge graph")
    print("  demo              - Load demo data")
    print("  help              - Show this help")
    print("  quit              - Exit")
    print()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    manager = KnowledgeGraphManager(api_key=api_key)
    
    while True:
        try:
            command = input("kg> ").strip()
            
            if not command:
                continue
            
            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""
            
            if cmd == "quit" or cmd == "exit":
                break
            
            elif cmd == "help":
                print("Commands: add, query, ask, timeline, entities, stats, save, load, demo, help, quit")
            
            elif cmd == "add":
                if not arg:
                    print("Usage: add <text>")
                    continue
                
                statement = manager.add_statement_text(arg)
                print(f"✅ Added: {statement.text}")
                print(f"   Type: {statement.temporal_class.value}")
            
            elif cmd == "query":
                if not arg:
                    print("Usage: query <entity>")
                    continue
                
                result = manager.query_entity(arg)
                print(format_query_result(result))
            
            elif cmd == "ask":
                if not arg:
                    print("Usage: ask <question>")
                    continue
                
                result = manager.query_natural_language(arg)
                print(format_query_result(result))
            
            elif cmd == "timeline":
                if not arg:
                    print("Usage: timeline <entity>")
                    continue
                
                timeline = manager.get_entity_timeline(arg)
                print(format_timeline_for_display(timeline))
            
            elif cmd == "entities":
                entities = manager.get_all_entities()
                print(f"Entities ({len(entities)}):")
                for entity in sorted(entities)[:20]:  # Show first 20
                    print(f"  • {entity}")
                if len(entities) > 20:
                    print(f"  ... and {len(entities) - 20} more")
            
            elif cmd == "stats":
                stats = manager.get_statistics()
                for key, value in stats.items():
                    print(f"{key}: {value}")
            
            elif cmd == "save":
                if not arg:
                    print("Usage: save <filename>")
                    continue
                
                manager.save_to_file(arg)
                print(f"💾 Saved to {arg}")
            
            elif cmd == "load":
                if not arg:
                    print("Usage: load <filename>")
                    continue
                
                manager.load_from_file(arg)
                print(f"📂 Loaded from {arg}")
            
            elif cmd == "demo":
                manager = demo_knowledge_graph(api_key=api_key)
                print("✅ Demo data loaded")
            
            else:
                print(f"Unknown command: {cmd}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments, start interactive mode
        interactive_mode()
    else:
        # Command line arguments provided
        main()

