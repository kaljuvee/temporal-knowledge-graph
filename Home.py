"""
Streamlit Web Interface Demo for Temporal Knowledge Graph
Based on OpenAI Cookbook: Temporal Agents with Knowledge Graphs
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Any

# Optional dotenv import - gracefully handle if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, skip loading .env file
    pass

from utils import KnowledgeGraphManager, format_query_result, demo_knowledge_graph
from models import TemporalClass, FactType


# Page configuration
st.set_page_config(
    page_title="Temporal Knowledge Graph Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .timeline-event {
        background-color: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border-left: 3px solid #28a745;
    }
    .statement-card {
        background-color: #ffffff;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_knowledge_graph(api_key: str):
    """Initialize knowledge graph manager with caching"""
    return KnowledgeGraphManager(api_key=api_key)


def load_demo_data(api_key: str):
    """Load demo data without caching to avoid serialization issues"""
    return demo_knowledge_graph(api_key=api_key)


def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Temporal Knowledge Graph Demo</h1>', unsafe_allow_html=True)
    st.markdown("*Based on [OpenAI Cookbook: Temporal Agents with Knowledge Graphs](https://cookbook.openai.com/examples/partners/temporal_agents_with_knowledge_graphs/temporal_agents_with_knowledge_graphs)*")
    
    # Instructions and overview
    with st.expander("📖 How to Use This Demo", expanded=False):
        st.markdown("""
        ### Welcome to the Temporal Knowledge Graph Demo! 🎯
        
        This application demonstrates how to build and query temporal knowledge graphs that track information changes over time.
        
        #### 🎥 Demo Video
        
        Watch a quick walkthrough of the key features:
        """)
        
        # Check if demo video exists
        import os
        video_path = "demo_walkthrough.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.info("📹 Demo video available in the GitHub repository: [demo_walkthrough.mp4](https://github.com/kaljuvee/temporal-knowledge-graph/blob/main/demo_walkthrough.mp4)")
        
        st.markdown("""
        #### 🚀 Quick Start:
        1. **Enter your OpenAI API key** in the sidebar (or set it in environment variables)
        2. **Load demo data** by clicking "🎯 Load Demo Data" to see the system in action
        3. **Explore the tabs** to add content, query information, and analyze timelines
        
        #### 📊 What You Can Do:
        - **Add Content**: Process individual statements or entire documents
        - **Query & Search**: Ask questions about entities or use natural language queries
        - **Timeline View**: See how entities and relationships evolve over time
        - **Analytics**: Analyze the composition and health of your knowledge graph
        - **Browse Data**: Filter and explore all statements in your graph
        
        #### 🧠 Key Concepts:
        - **Temporal Classification**: Statements are classified as Atemporal (never change), Static (valid from a point), or Dynamic (evolve over time)
        - **Triplets**: Knowledge is stored as Subject-Predicate-Object relationships
        - **Temporal Events**: Track when information becomes valid, invalid, or expires
        - **Entity Resolution**: Automatically link related information across statements
        
        #### 💡 Example Queries:
        - "Who was CEO of TechCorp in 2023?"
        - "What acquisitions did Microsoft make?"
        - "When did John Smith become CEO?"
        
        **👈 Start by entering your API key in the sidebar and loading the demo data!**
        """)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        default_api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Show status of environment variable loading
        if default_api_key:
            st.success("✅ API key loaded from environment variables")
        else:
            st.info("💡 No API key found in environment. Please enter manually or create a .env file.")
        
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=default_api_key,
            help="Enter your OpenAI API key (loaded from environment/.env by default)"
        )
        
        if not api_key:
            st.error("Please enter your OpenAI API key to continue")
            st.info("💡 Tip: Create a .env file with OPENAI_API_KEY=your-key-here")
            st.stop()
        
        st.divider()
        
        # Knowledge Graph Management
        st.header("📊 Knowledge Graph")
        
        # Initialize or load demo
        if "kg_manager" not in st.session_state:
            st.session_state.kg_manager = initialize_knowledge_graph(api_key)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Load Demo Data", use_container_width=True):
                with st.spinner("Loading demo data..."):
                    st.session_state.kg_manager = load_demo_data(api_key)
                st.success("Demo data loaded!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Graph", use_container_width=True):
                st.session_state.kg_manager = initialize_knowledge_graph(api_key)
                st.success("Knowledge graph cleared!")
                st.rerun()
        
        # File operations
        st.subheader("💾 File Operations")
        
        uploaded_file = st.file_uploader(
            "Upload Knowledge Graph",
            type=['json'],
            help="Upload a previously saved knowledge graph"
        )
        
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                with open("temp_kg.json", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.session_state.kg_manager.load_from_file("temp_kg.json")
                st.success("Knowledge graph loaded!")
                os.remove("temp_kg.json")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")
        
        if st.button("💾 Download Graph", use_container_width=True):
            try:
                st.session_state.kg_manager.save_to_file("current_kg.json")
                with open("current_kg.json", "r") as f:
                    st.download_button(
                        label="📥 Download JSON",
                        data=f.read(),
                        file_name=f"knowledge_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            except Exception as e:
                st.error(f"Error preparing download: {e}")
    
    # Main content area
    manager = st.session_state.kg_manager
    
    # Statistics overview
    stats = manager.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Total Statements", stats["total_statements"])
    
    with col2:
        st.metric("🏢 Total Entities", stats["total_entities"])
    
    with col3:
        st.metric("⏰ Temporal Events", stats["statements_with_temporal_events"])
    
    with col4:
        st.metric("❌ Invalidated", stats["invalidated_statements"])
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add Content", 
        "🔍 Query & Search", 
        "📅 Timeline View", 
        "📊 Analytics", 
        "🗂️ Browse Data"
    ])
    
    with tab1:
        st.header("➕ Add Content to Knowledge Graph")
        
        # Add single statement
        st.subheader("Add Single Statement")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            statement_text = st.text_area(
                "Statement Text",
                placeholder="Enter a statement like 'John Smith became CEO of TechCorp on January 1, 2024'",
                height=100
            )
        
        with col2:
            source = st.text_input("Source (optional)", placeholder="document_1")
            
            if st.button("🔄 Add Statement", use_container_width=True):
                if statement_text.strip():
                    with st.spinner("Processing statement..."):
                        try:
                            statement = manager.add_statement_text(statement_text, source=source)
                            
                            st.success("✅ Statement added successfully!")
                            
                            # Display processed statement details
                            with st.expander("📋 Statement Details", expanded=True):
                                st.write(f"**ID:** {statement.id}")
                                st.write(f"**Temporal Class:** {statement.temporal_class.value}")
                                st.write(f"**Fact Type:** {statement.fact_type.value}")
                                
                                if statement.triplets:
                                    st.write("**Extracted Triplets:**")
                                    for triplet in statement.triplets:
                                        st.write(f"• {triplet}")
                                
                                if statement.temporal_event:
                                    st.write("**Temporal Information:**")
                                    te = statement.temporal_event
                                    if te.t_created:
                                        st.write(f"• Created: {te.t_created}")
                                    if te.t_valid:
                                        st.write(f"• Valid from: {te.t_valid}")
                                    if te.t_invalid:
                                        st.write(f"• Valid until: {te.t_invalid}")
                            
                        except Exception as e:
                            st.error(f"Error processing statement: {e}")
                else:
                    st.warning("Please enter a statement")
        
        st.divider()
        
        # Add document
        st.subheader("Add Document")
        
        document_text = st.text_area(
            "Document Text",
            placeholder="Paste a longer document here. It will be automatically chunked into statements.",
            height=200
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            doc_source = st.text_input("Document Source", placeholder="annual_report_2024")
        
        with col2:
            if st.button("📄 Process Document", use_container_width=True):
                if document_text.strip():
                    with st.spinner("Processing document..."):
                        try:
                            statements = manager.add_document(document_text, source=doc_source)
                            
                            st.success(f"✅ Processed {len(statements)} statements from document!")
                            
                            # Show summary
                            with st.expander("📊 Processing Summary", expanded=True):
                                temporal_counts = {}
                                for stmt in statements:
                                    tc = stmt.temporal_class.value
                                    temporal_counts[tc] = temporal_counts.get(tc, 0) + 1
                                
                                for tc, count in temporal_counts.items():
                                    st.write(f"• {tc.title()}: {count} statements")
                            
                        except Exception as e:
                            st.error(f"Error processing document: {e}")
                else:
                    st.warning("Please enter document text")
    
    with tab2:
        st.header("🔍 Query & Search")
        
        # Entity query
        st.subheader("Query by Entity")
        
        entities = manager.get_all_entities()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if entities:
                selected_entity = st.selectbox(
                    "Select Entity",
                    options=[""] + sorted(entities),
                    help="Choose an entity to query"
                )
            else:
                selected_entity = st.text_input("Entity Name", placeholder="Enter entity name")
        
        with col2:
            query_time = st.date_input(
                "Query at specific time (optional)",
                value=None,
                help="Leave empty for current time"
            )
        
        if st.button("🔍 Query Entity", use_container_width=True):
            if selected_entity:
                with st.spinner("Querying knowledge graph..."):
                    try:
                        query_datetime = datetime.combine(query_time, datetime.min.time()) if query_time else None
                        result = manager.query_entity(selected_entity, timestamp=query_datetime)
                        
                        if result.statements:
                            st.success(f"Found {len(result.statements)} statements for '{selected_entity}'")
                            
                            for i, stmt in enumerate(result.statements, 1):
                                with st.expander(f"Statement {i}: {stmt.text[:80]}...", expanded=i<=3):
                                    st.write(f"**Full Text:** {stmt.text}")
                                    st.write(f"**Type:** {stmt.temporal_class.value} ({stmt.fact_type.value})")
                                    st.write(f"**Source:** {stmt.source or 'Unknown'}")
                                    
                                    if stmt.triplets:
                                        st.write("**Triplets:**")
                                        for triplet in stmt.triplets:
                                            st.write(f"• {triplet}")
                                    
                                    if stmt.temporal_event:
                                        st.write("**Temporal Info:**")
                                        te = stmt.temporal_event
                                        if te.t_valid:
                                            st.write(f"• Valid from: {te.t_valid}")
                                        if te.t_invalid:
                                            st.write(f"• Valid until: {te.t_invalid}")
                        else:
                            st.info(f"No statements found for entity '{selected_entity}'")
                    
                    except Exception as e:
                        st.error(f"Error querying entity: {e}")
            else:
                st.warning("Please select or enter an entity name")
        
        st.divider()
        
        # Natural language query
        st.subheader("Natural Language Query")
        
        question = st.text_input(
            "Ask a Question",
            placeholder="Who was CEO of TechCorp in 2023?",
            help="Ask questions about the knowledge graph in natural language"
        )
        
        if st.button("❓ Ask Question", use_container_width=True):
            if question:
                with st.spinner("Processing question..."):
                    try:
                        result = manager.query_natural_language(question)
                        
                        if result.answer:
                            st.success("Answer found!")
                            st.markdown(f"**Answer:** {result.answer}")
                        
                        if result.statements:
                            st.write(f"**Supporting Evidence ({len(result.statements)} statements):**")
                            
                            for i, stmt in enumerate(result.statements[:5], 1):  # Show top 5
                                with st.expander(f"Evidence {i}: {stmt.text[:60]}..."):
                                    st.write(stmt.text)
                                    if stmt.temporal_event:
                                        te = stmt.temporal_event
                                        if te.t_valid:
                                            st.write(f"Valid from: {te.t_valid}")
                                        if te.t_invalid:
                                            st.write(f"Valid until: {te.t_invalid}")
                        
                        if not result.answer and not result.statements:
                            st.info("No relevant information found for your question.")
                    
                    except Exception as e:
                        st.error(f"Error processing question: {e}")
            else:
                st.warning("Please enter a question")
    
    with tab3:
        st.header("📅 Timeline View")
        
        # Entity timeline
        if entities:
            timeline_entity = st.selectbox(
                "Select Entity for Timeline",
                options=[""] + sorted(entities),
                key="timeline_entity"
            )
            
            if timeline_entity:
                timeline = manager.get_entity_timeline(timeline_entity)
                
                if timeline:
                    st.success(f"Timeline for '{timeline_entity}' ({len(timeline)} events)")
                    
                    # Create timeline visualization
                    timeline_data = []
                    for event in timeline:
                        te = event.get('temporal_event', {})
                        
                        # Use creation time or valid time as the main timestamp
                        timestamp = te.get('t_created') or te.get('t_valid')
                        
                        if timestamp:
                            timeline_data.append({
                                'Date': timestamp,
                                'Event': event['text'][:100] + ('...' if len(event['text']) > 100 else ''),
                                'Type': event['temporal_class'],
                                'Full_Text': event['text']
                            })
                    
                    if timeline_data:
                        # Sort by date
                        timeline_data.sort(key=lambda x: x['Date'])
                        
                        # Create timeline chart
                        fig = px.scatter(
                            timeline_data,
                            x='Date',
                            y=[1] * len(timeline_data),
                            color='Type',
                            hover_data=['Full_Text'],
                            title=f"Timeline for {timeline_entity}"
                        )
                        
                        fig.update_layout(
                            yaxis=dict(showticklabels=False, title=""),
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Display timeline events
                    st.subheader("Timeline Events")
                    
                    for i, event in enumerate(timeline, 1):
                        with st.expander(f"Event {i}: {event['text'][:80]}...", expanded=i<=3):
                            st.write(f"**Text:** {event['text']}")
                            st.write(f"**Type:** {event['temporal_class']} ({event['fact_type']})")
                            
                            te = event.get('temporal_event', {})
                            if te:
                                if te.get('t_created'):
                                    st.write(f"**Created:** {te['t_created']}")
                                if te.get('t_valid'):
                                    st.write(f"**Valid from:** {te['t_valid']}")
                                if te.get('t_invalid'):
                                    st.write(f"**Valid until:** {te['t_invalid']}")
                            
                            if event.get('triplets'):
                                st.write("**Triplets:**")
                                for triplet in event['triplets']:
                                    st.write(f"• {triplet}")
                
                else:
                    st.info(f"No timeline events found for '{timeline_entity}'")
        else:
            st.info("No entities available. Add some content first.")
    
    with tab4:
        st.header("📊 Analytics")
        
        if stats["total_statements"] > 0:
            # Temporal class distribution
            col1, col2 = st.columns(2)
            
            with col1:
                if stats["temporal_classes"]:
                    fig_temporal = px.pie(
                        values=list(stats["temporal_classes"].values()),
                        names=list(stats["temporal_classes"].keys()),
                        title="Temporal Class Distribution"
                    )
                    st.plotly_chart(fig_temporal, use_container_width=True)
            
            with col2:
                if stats["fact_types"]:
                    fig_facts = px.pie(
                        values=list(stats["fact_types"].values()),
                        names=list(stats["fact_types"].keys()),
                        title="Fact Type Distribution"
                    )
                    st.plotly_chart(fig_facts, use_container_width=True)
            
            # Entity activity
            st.subheader("Entity Activity")
            
            entity_counts = []
            for entity in entities[:20]:  # Top 20 entities
                statements = manager.kg.get_statements_for_entity(entity)
                entity_counts.append({
                    'Entity': entity,
                    'Statement Count': len(statements)
                })
            
            if entity_counts:
                entity_df = pd.DataFrame(entity_counts)
                entity_df = entity_df.sort_values('Statement Count', ascending=False)
                
                fig_entities = px.bar(
                    entity_df,
                    x='Statement Count',
                    y='Entity',
                    orientation='h',
                    title="Top Entities by Statement Count"
                )
                
                st.plotly_chart(fig_entities, use_container_width=True)
            
            # Detailed statistics
            st.subheader("Detailed Statistics")
            
            stats_df = pd.DataFrame([
                {"Metric": "Total Statements", "Value": stats["total_statements"]},
                {"Metric": "Total Entities", "Value": stats["total_entities"]},
                {"Metric": "Statements with Temporal Events", "Value": stats["statements_with_temporal_events"]},
                {"Metric": "Invalidated Statements", "Value": stats["invalidated_statements"]},
            ])
            
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        else:
            st.info("No data available for analytics. Add some content first.")
    
    with tab5:
        st.header("🗂️ Browse Data")
        
        if stats["total_statements"] > 0:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_temporal = st.selectbox(
                    "Filter by Temporal Class",
                    options=["All"] + [tc.value for tc in TemporalClass]
                )
            
            with col2:
                filter_fact = st.selectbox(
                    "Filter by Fact Type",
                    options=["All"] + [ft.value for ft in FactType]
                )
            
            with col3:
                filter_entity = st.selectbox(
                    "Filter by Entity",
                    options=["All"] + sorted(entities)[:50]  # Limit to 50 for performance
                )
            
            # Get filtered statements
            filtered_statements = []
            
            for stmt in manager.kg.statements.values():
                # Apply filters
                if filter_temporal != "All" and stmt.temporal_class.value != filter_temporal:
                    continue
                
                if filter_fact != "All" and stmt.fact_type.value != filter_fact:
                    continue
                
                if filter_entity != "All":
                    # Check if entity appears in any triplet
                    entity_found = False
                    for triplet in stmt.triplets:
                        if filter_entity in [triplet.subject, triplet.object]:
                            entity_found = True
                            break
                    if not entity_found:
                        continue
                
                filtered_statements.append(stmt)
            
            st.write(f"**Showing {len(filtered_statements)} statements**")
            
            # Pagination
            items_per_page = 10
            total_pages = (len(filtered_statements) + items_per_page - 1) // items_per_page
            
            if total_pages > 1:
                page = st.selectbox(
                    "Page",
                    options=list(range(1, total_pages + 1)),
                    format_func=lambda x: f"Page {x} of {total_pages}"
                )
            else:
                page = 1
            
            # Display statements for current page
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_statements = filtered_statements[start_idx:end_idx]
            
            for i, stmt in enumerate(page_statements, start_idx + 1):
                with st.expander(f"{i}. {stmt.text[:100]}...", expanded=False):
                    st.write(f"**ID:** {stmt.id}")
                    st.write(f"**Full Text:** {stmt.text}")
                    st.write(f"**Type:** {stmt.temporal_class.value} ({stmt.fact_type.value})")
                    st.write(f"**Source:** {stmt.source or 'Unknown'}")
                    
                    if stmt.triplets:
                        st.write("**Triplets:**")
                        for triplet in stmt.triplets:
                            st.write(f"• {triplet}")
                    
                    if stmt.temporal_event:
                        st.write("**Temporal Information:**")
                        te = stmt.temporal_event
                        if te.t_created:
                            st.write(f"• Created: {te.t_created}")
                        if te.t_valid:
                            st.write(f"• Valid from: {te.t_valid}")
                        if te.t_invalid:
                            st.write(f"• Valid until: {te.t_invalid}")
                        if te.t_expired:
                            st.write(f"• Expires: {te.t_expired}")
                    
                    if stmt.invalidated_by:
                        st.write(f"**Invalidated by:** {', '.join(stmt.invalidated_by)}")
        
        else:
            st.info("No statements available. Add some content first.")


if __name__ == "__main__":
    main()

