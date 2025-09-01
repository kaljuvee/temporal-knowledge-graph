"""
User Guide for Temporal Knowledge Graph Demo
Comprehensive guide explaining concepts, usage, and examples
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="User Guide - Temporal Knowledge Graph",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .guide-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .concept-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .example-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="guide-header">📚 Temporal Knowledge Graph User Guide</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    ## 🎯 Introduction
    
    Welcome to the comprehensive guide for the **Temporal Knowledge Graph Demo**! This application is based on the 
    [OpenAI Cookbook: Temporal Agents with Knowledge Graphs](https://cookbook.openai.com/examples/partners/temporal_agents_with_knowledge_graphs/temporal_agents_with_knowledge_graphs) 
    and demonstrates how to build, manage, and query knowledge graphs that understand time.
    
    ### 🎥 Demo Video
    
    Watch a quick walkthrough of the application:
    """)
    
    # Check if demo video exists
    import os
    video_path = "../demo_walkthrough.mp4"
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.info("📹 Demo video available in the GitHub repository: [demo_walkthrough.mp4](https://github.com/kaljuvee/temporal-knowledge-graph/blob/main/demo_walkthrough.mp4)")
    
    st.markdown("""
    ### What is a Temporal Knowledge Graph?
    
    A temporal knowledge graph is a data structure that stores information along with its temporal context - 
    when facts become true, when they change, and when they become invalid. Unlike traditional knowledge graphs 
    that represent static relationships, temporal knowledge graphs can answer questions like:
    
    - "Who was the CEO of Apple in 2010?"
    - "When did Microsoft acquire GitHub?"
    - "What was Tesla's revenue in Q3 2023?"
    """)
    
    # Core Concepts
    st.markdown("## 🧠 Core Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="concept-box">
        <h4>🏷️ Temporal Classification</h4>
        <p><strong>Atemporal:</strong> Facts that never change<br>
        <em>Example: "The speed of light is 299,792,458 m/s"</em></p>
        
        <p><strong>Static:</strong> Facts valid from a specific point in time<br>
        <em>Example: "John became CEO on Jan 1, 2020"</em></p>
        
        <p><strong>Dynamic:</strong> Facts that evolve over time<br>
        <em>Example: "Company revenue grows quarterly"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-box">
        <h4>🔗 Triplets</h4>
        <p>Knowledge is stored as Subject-Predicate-Object relationships:</p>
        <ul>
        <li><strong>Subject:</strong> "John Smith"</li>
        <li><strong>Predicate:</strong> "hasRole"</li>
        <li><strong>Object:</strong> "CEO"</li>
        </ul>
        <p>This creates the relationship: <em>"John Smith hasRole CEO"</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-box">
        <h4>⏰ Temporal Events</h4>
        <p>Each statement can have multiple timestamps:</p>
        <ul>
        <li><strong>t_created:</strong> When the statement was added</li>
        <li><strong>t_valid:</strong> When the fact becomes true</li>
        <li><strong>t_invalid:</strong> When the fact becomes false</li>
        <li><strong>t_expired:</strong> When the information expires</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-box">
        <h4>🔄 Invalidation</h4>
        <p>The system automatically handles conflicting information:</p>
        <ul>
        <li>New facts can invalidate old ones</li>
        <li>Temporal precedence determines validity</li>
        <li>Maintains historical accuracy</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Getting Started
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    ### Step 1: Setup Your API Key
    
    You need an OpenAI API key to use the temporal processing features:
    
    1. **Option A:** Enter it directly in the sidebar
    2. **Option B:** Set the `OPENAI_API_KEY` environment variable
    3. **Option C:** Create a `.env` file with `OPENAI_API_KEY=your-key-here`
    """)
    
    st.markdown("""
    <div class="warning-box">
    <strong>⚠️ Important:</strong> Your API key is used to process text and extract temporal information. 
    The system makes API calls to classify statements, extract relationships, and identify temporal events.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Step 2: Load Demo Data
    
    Click "🎯 Load Demo Data" in the sidebar to populate the system with sample data including:
    - Executive appointments and resignations
    - Company acquisitions
    - Financial reports
    - Product launches
    - Scientific facts
    """)
    
    # Using the Interface
    st.markdown("## 🖥️ Using the Interface")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add Content", 
        "🔍 Query & Search", 
        "📅 Timeline View", 
        "📊 Analytics", 
        "🗂️ Browse Data"
    ])
    
    with tab1:
        st.markdown("""
        ### Adding Content to Your Knowledge Graph
        
        #### Single Statements
        Add individual facts or statements:
        
        **Examples:**
        - "Apple was founded by Steve Jobs in 1976"
        - "Microsoft acquired GitHub for $7.5 billion in 2018"
        - "Elon Musk became CEO of Tesla in 2008"
        
        #### Document Processing
        Upload or paste entire documents for automatic processing:
        - Annual reports
        - News articles
        - Research papers
        - Meeting minutes
        
        The system will automatically:
        1. **Chunk** the document into individual statements
        2. **Classify** each statement temporally
        3. **Extract** relationships and entities
        4. **Identify** temporal events and dates
        """)
        
        st.markdown("""
        <div class="example-box">
        <h4>💡 Best Practices for Adding Content</h4>
        <ul>
        <li><strong>Be specific with dates:</strong> "January 1, 2024" vs "early 2024"</li>
        <li><strong>Include context:</strong> "John Smith of TechCorp" vs just "John Smith"</li>
        <li><strong>Use clear language:</strong> Avoid ambiguous pronouns</li>
        <li><strong>Specify sources:</strong> Always include source information for traceability</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        ### Querying Your Knowledge Graph
        
        #### Entity Queries
        Search for all information about specific entities:
        - Companies: "Apple", "Microsoft", "Tesla"
        - People: "Steve Jobs", "Bill Gates", "Elon Musk"
        - Products: "iPhone", "Windows", "Model S"
        
        #### Temporal Queries
        Query information at specific points in time:
        - "Who was CEO of Apple in 2010?"
        - "What was Microsoft's revenue in 2020?"
        - "Which companies did Google acquire before 2015?"
        
        #### Natural Language Questions
        Ask complex questions in plain English:
        - "What major acquisitions happened in the tech industry?"
        - "How did Apple's leadership change over time?"
        - "When did Tesla become profitable?"
        """)
        
        st.markdown("""
        <div class="example-box">
        <h4>🎯 Query Examples</h4>
        <p><strong>Simple Entity Query:</strong><br>
        Input: "Apple"<br>
        Returns: All statements mentioning Apple with temporal context</p>
        
        <p><strong>Temporal Query:</strong><br>
        Input: Entity="Apple", Time="2011-01-01"<br>
        Returns: What was true about Apple on January 1, 2011</p>
        
        <p><strong>Natural Language:</strong><br>
        Input: "Who founded Google and when?"<br>
        Returns: Founding information with dates and founders</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        ### Timeline Visualization
        
        The Timeline View shows how entities evolve over time:
        
        #### Features:
        - **Chronological ordering** of events
        - **Interactive timeline** with hover details
        - **Event categorization** by type
        - **Temporal relationships** between events
        
        #### Use Cases:
        - **Corporate history:** Track leadership changes, acquisitions, product launches
        - **Personal careers:** Follow someone's professional journey
        - **Product evolution:** See how products develop over time
        - **Market analysis:** Understand industry trends and changes
        """)
        
        # Create a sample timeline visualization
        st.markdown("#### Sample Timeline: TechCorp Evolution")
        
        sample_timeline = pd.DataFrame({
            'Date': [
                datetime(2020, 1, 15),
                datetime(2021, 3, 1),
                datetime(2023, 12, 31),
                datetime(2024, 1, 1)
            ],
            'Event': [
                'John Smith appointed CEO',
                'Acquired DataSystems Inc',
                'John Smith resigned',
                'Sarah Johnson became CEO'
            ],
            'Type': ['Leadership', 'Acquisition', 'Leadership', 'Leadership']
        })
        
        st.line_chart(sample_timeline.set_index('Date')['Event'].map(lambda x: hash(x) % 100))
        st.dataframe(sample_timeline, use_container_width=True)
    
    with tab4:
        st.markdown("""
        ### Analytics and Insights
        
        The Analytics tab provides comprehensive insights into your knowledge graph:
        
        #### Composition Analysis:
        - **Temporal class distribution:** How many statements are atemporal vs temporal
        - **Fact type breakdown:** Distribution of different types of facts
        - **Entity activity:** Which entities have the most associated information
        
        #### Health Metrics:
        - **Total statements:** Overall size of your knowledge graph
        - **Entity coverage:** Number of unique entities tracked
        - **Temporal events:** How much temporal information is captured
        - **Invalidation rate:** How often information gets updated or corrected
        
        #### Visualization Types:
        - **Pie charts** for categorical distributions
        - **Bar charts** for entity activity rankings
        - **Time series** for temporal trends
        - **Network graphs** for relationship visualization
        """)
    
    with tab5:
        st.markdown("""
        ### Browsing and Filtering Data
        
        The Browse Data tab lets you explore your entire knowledge graph:
        
        #### Filtering Options:
        - **By temporal class:** Show only atemporal, static, or dynamic statements
        - **By fact type:** Filter by different categories of facts
        - **By entity:** Show statements related to specific entities
        - **By source:** Filter by document or data source
        
        #### Pagination:
        - Navigate through large datasets efficiently
        - Configurable items per page
        - Jump to specific pages
        
        #### Detailed View:
        Each statement shows:
        - Full text content
        - Temporal classification and fact type
        - Extracted triplets (relationships)
        - Temporal event information
        - Source attribution
        - Invalidation status
        """)
    
    # Advanced Features
    st.markdown("## 🔬 Advanced Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Conflict Resolution
        
        The system automatically handles conflicting information:
        
        **Example Scenario:**
        1. Statement A: "John is CEO since 2020"
        2. Statement B: "Sarah became CEO in 2024"
        
        **System Response:**
        - Automatically invalidates John's CEO status in 2024
        - Maintains historical accuracy
        - Preserves both statements with proper temporal bounds
        """)
        
        st.markdown("""
        ### Multi-Source Integration
        
        Combine information from multiple sources:
        - Corporate reports
        - News articles
        - Press releases
        - Social media
        - Government filings
        
        Each source is tracked for provenance and reliability.
        """)
    
    with col2:
        st.markdown("""
        ### Temporal Reasoning
        
        The system can infer temporal relationships:
        
        **Implicit Relationships:**
        - If A happened before B, and B before C, then A before C
        - Duration calculations between events
        - Overlap detection for concurrent events
        
        **Temporal Constraints:**
        - Validity periods for facts
        - Expiration dates for time-sensitive information
        - Automatic invalidation based on temporal logic
        """)
        
        st.markdown("""
        ### Export and Integration
        
        Your knowledge graph can be:
        - **Exported** as JSON for backup or sharing
        - **Imported** from previous sessions
        - **Integrated** with other systems via API
        - **Visualized** in external tools
        """)
    
    # Best Practices
    st.markdown("## 💡 Best Practices")
    
    st.markdown("""
    ### Data Quality
    
    1. **Consistent Entity Names:** Use the same name format for entities across statements
    2. **Clear Temporal References:** Be specific about dates and time periods
    3. **Source Attribution:** Always specify where information comes from
    4. **Regular Updates:** Keep information current and mark outdated facts
    
    ### Query Optimization
    
    1. **Start Broad, Then Narrow:** Begin with general queries, then add filters
    2. **Use Temporal Constraints:** Specify time periods to get more relevant results
    3. **Leverage Natural Language:** The system understands complex questions
    4. **Check Multiple Entities:** Cross-reference information across related entities
    
    ### System Performance
    
    1. **Batch Processing:** Add multiple statements at once when possible
    2. **Regular Cleanup:** Remove or archive outdated information
    3. **Monitor Statistics:** Keep track of graph size and composition
    4. **Backup Regularly:** Export your knowledge graph periodically
    """)
    
    # Troubleshooting
    st.markdown("## 🔧 Troubleshooting")
    
    with st.expander("Common Issues and Solutions"):
        st.markdown("""
        ### API Key Issues
        **Problem:** "Please enter your OpenAI API key"
        **Solution:** 
        - Verify your API key is correct
        - Check that you have sufficient credits
        - Ensure the key has the necessary permissions
        
        ### Processing Errors
        **Problem:** Statements not being processed correctly
        **Solution:**
        - Check for clear, unambiguous language
        - Ensure dates are in recognizable formats
        - Verify entity names are consistent
        
        ### Performance Issues
        **Problem:** Slow response times
        **Solution:**
        - Process smaller batches of text
        - Use more specific queries
        - Clear browser cache and reload
        
        ### Data Quality Issues
        **Problem:** Incorrect relationships or temporal information
        **Solution:**
        - Review and edit extracted triplets
        - Verify temporal event dates
        - Add more context to ambiguous statements
        """)
    
    # Resources
    st.markdown("## 📖 Additional Resources")
    
    st.markdown("""
    ### Learn More
    
    - **[OpenAI Cookbook](https://cookbook.openai.com/examples/partners/temporal_agents_with_knowledge_graphs/temporal_agents_with_knowledge_graphs):** 
      Original tutorial and concepts
    - **[Knowledge Graphs](https://en.wikipedia.org/wiki/Knowledge_graph):** 
      General background on knowledge graphs
    - **[Temporal Databases](https://en.wikipedia.org/wiki/Temporal_database):** 
      Understanding temporal data concepts
    
    ### Technical Documentation
    
    - **API Reference:** Available in the repository documentation
    - **Data Models:** Detailed schema information
    - **Integration Guide:** How to connect with other systems
    
    ### Community and Support
    
    - **GitHub Repository:** Source code and issue tracking
    - **Examples Collection:** Real-world use cases and implementations
    - **Best Practices Guide:** Advanced usage patterns
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
    <p>Built with ❤️ using OpenAI's temporal knowledge graph concepts</p>
    <p>Based on <a href="https://cookbook.openai.com/examples/partners/temporal_agents_with_knowledge_graphs/temporal_agents_with_knowledge_graphs">OpenAI Cookbook: Temporal Agents with Knowledge Graphs</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

