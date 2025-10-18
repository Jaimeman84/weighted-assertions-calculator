import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_weighted_score(assertions, threshold=0.6):
    """
    Calculate weighted aggregate score based on promptfoo logic
    
    Args:
        assertions: List of dicts with 'name', 'score', 'weight', 'pass' keys
        threshold: Test threshold for pass/fail
    
    Returns:
        dict with aggregate score, total weights, and pass status
    """
    total_weighted_score = 0
    total_weights = 0
    passed_assertions = 0
    failed_assertions = 0
    
    for assertion in assertions:
        score = assertion['score']
        weight = assertion['weight']
        
        total_weighted_score += score * weight
        total_weights += weight
        
        if assertion['pass']:
            passed_assertions += 1
        else:
            failed_assertions += 1
    
    aggregate_score = total_weighted_score / total_weights if total_weights > 0 else 0
    overall_pass = aggregate_score >= threshold
    
    return {
        'aggregate_score': aggregate_score,
        'total_weighted_score': total_weighted_score,
        'total_weights': total_weights,
        'passed_assertions': passed_assertions,
        'failed_assertions': failed_assertions,
        'overall_pass': overall_pass,
        'threshold': threshold
    }

def create_score_visualization(assertions, result):
    """Create visualizations for the weighted scoring"""
    
    # Prepare data for visualization
    df = pd.DataFrame(assertions)
    df['weighted_contribution'] = df['score'] * df['weight']
    df['status'] = df['pass'].map({True: 'PASS', False: 'FAIL'})
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Individual Scores', 'Weighted Contributions', 'Pass/Fail Status', 'Aggregate Score'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "indicator"}]]
    )
    
    # Individual scores
    fig.add_trace(
        go.Bar(x=df['name'], y=df['score'], name='Scores', 
               marker_color=['green' if p else 'red' for p in df['pass']]),
        row=1, col=1
    )
    
    # Weighted contributions
    fig.add_trace(
        go.Bar(x=df['name'], y=df['weighted_contribution'], name='Weighted Contribution',
               marker_color=['green' if p else 'red' for p in df['pass']]),
        row=1, col=2
    )
    
    # Pass/Fail status
    status_counts = df['status'].value_counts()
    fig.add_trace(
        go.Bar(x=status_counts.index, y=status_counts.values, name='Status Count',
               marker_color=['green', 'red']),
        row=2, col=1
    )
    
    # Aggregate score gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=result['aggregate_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Aggregate Score"},
            delta={'reference': result['threshold']},
            gauge={
                'axis': {'range': [None, 1]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, result['threshold']], 'color': "lightgray"},
                    {'range': [result['threshold'], 1], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': result['threshold']
                }
            }
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=500, showlegend=False, title_text="Weighted Assertions Analysis")
    return fig

def main():
    st.set_page_config(
        page_title="Weighted Assertions Calculator",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Weighted Assertions Calculator")
    st.markdown("**Understanding how promptfoo calculates weighted aggregate scores**")
    
    # Initialize session state
    if 'assertions' not in st.session_state:
        st.session_state.assertions = []
    if 'last_example_choice' not in st.session_state:
        st.session_state.last_example_choice = "Custom"
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    threshold = st.sidebar.slider("Test Threshold", 0.0, 1.0, 0.6, 0.1)
    
    # Layout options
    st.sidebar.subheader("Layout")
    compact_mode = st.sidebar.checkbox("Compact Mode", value=True, help="Reduce spacing for better fit")
    
    # Example configurations
    st.sidebar.subheader("Quick Examples")
    example_choice = st.sidebar.selectbox(
        "Choose an example:",
        ["Custom", "French Greeting (from promptfoo docs)", "Performance vs Quality", "Balanced Scoring"]
    )
    
    # Load example data only when example choice changes
    if example_choice != st.session_state.last_example_choice:
        st.session_state.last_example_choice = example_choice
        
        if example_choice == "French Greeting (from promptfoo docs)":
            st.session_state.assertions = [
                {"name": "Correctness", "score": 1.00, "weight": 2.0, "pass": True, "reason": "Contains 'Bonjour'"},
                {"name": "Tone", "score": 1.00, "weight": 1.0, "pass": True, "reason": "Friendly and in French"},
                {"name": "Topicality", "score": 0.50, "weight": 1.0, "pass": False, "reason": "Relevance 0.50 < threshold 0.8"},
                {"name": "Greeting", "score": 1.00, "weight": 1.0, "pass": True, "reason": "Engaging and appropriate"},
                {"name": "Performance", "score": 0.00, "weight": 2.0, "pass": False, "reason": "Cost and latency too high"}
            ]
        elif example_choice == "Performance vs Quality":
            st.session_state.assertions = [
                {"name": "Accuracy", "score": 0.9, "weight": 3.0, "pass": True, "reason": "High accuracy"},
                {"name": "Speed", "score": 0.3, "weight": 2.0, "pass": False, "reason": "Too slow"},
                {"name": "Cost", "score": 0.2, "weight": 1.0, "pass": False, "reason": "Too expensive"},
                {"name": "Relevance", "score": 0.95, "weight": 4.0, "pass": True, "reason": "Highly relevant"}
            ]
        elif example_choice == "Balanced Scoring":
            st.session_state.assertions = [
                {"name": "Metric A", "score": 0.8, "weight": 1.0, "pass": True, "reason": "Good performance"},
                {"name": "Metric B", "score": 0.6, "weight": 1.0, "pass": True, "reason": "Acceptable"},
                {"name": "Metric C", "score": 0.4, "weight": 1.0, "pass": False, "reason": "Below threshold"},
                {"name": "Metric D", "score": 0.7, "weight": 1.0, "pass": True, "reason": "Above average"}
            ]
        else:
            # Custom - start with empty list
            st.session_state.assertions = []
    
    # Use session state assertions
    assertions = st.session_state.assertions
    
    # Main content area - ensure columns are always the same size
    col1, col2 = st.columns([1, 1])  # Equal columns for both modes
    
    with col1:
        st.header("📝 Configure Assertions")
        
        # Dynamic assertion editor
        col_add, col_clear = st.columns([1, 1])
        
        with col_add:
            if st.button("➕ Add Assertion", use_container_width=True):
                st.session_state.assertions.append({"name": f"Assertion {len(st.session_state.assertions)+1}", "score": 0.5, "weight": 1.0, "pass": True, "reason": ""})
                st.rerun()
        
        with col_clear:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.assertions = []
                st.rerun()
        
        # Show assertion count
        if assertions:
            st.info(f"📊 {len(assertions)} assertion(s) configured")
        
        # Display and edit assertions
        for i, assertion in enumerate(assertions):
            with st.expander(f"#{i+1} {assertion['name']}", expanded=not compact_mode):
                # Compact layout with smaller spacing
                col_a, col_b = st.columns([1, 1])
                
                with col_a:
                    new_name = st.text_input("Name", value=assertion['name'], key=f"name_{i}", help="Assertion name")
                    new_score = st.slider("Score", 0.0, 1.0, assertion['score'], 0.01, key=f"score_{i}", help="Score from 0.0 to 1.0")
                    new_weight = st.number_input("Weight", 0.1, 10.0, float(assertion['weight']), 0.1, key=f"weight_{i}", help="Weight multiplier")
                
                with col_b:
                    new_pass = st.checkbox("Pass", value=assertion['pass'], key=f"pass_{i}", help="Whether this assertion passes")
                    new_reason = st.text_area("Reason", value=assertion['reason'], key=f"reason_{i}", height=60, help="Optional reason for pass/fail")
                
                # Update session state if values changed
                if (new_name != assertion['name'] or 
                    new_score != assertion['score'] or 
                    new_weight != assertion['weight'] or 
                    new_pass != assertion['pass'] or 
                    new_reason != assertion['reason']):
                    st.session_state.assertions[i] = {
                        "name": new_name,
                        "score": new_score,
                        "weight": new_weight,
                        "pass": new_pass,
                        "reason": new_reason
                    }
                
                # Compact remove button
                col_remove, col_spacer = st.columns([1, 3])
                with col_remove:
                    if st.button(f"🗑️ Remove", key=f"remove_{i}", use_container_width=True):
                        st.session_state.assertions.pop(i)
                        st.rerun()
    
    with col2:
        st.header("📊 Results")
        
        if assertions:
            # Calculate results
            result = calculate_weighted_score(assertions, threshold)
            
            # Display summary
            st.subheader("Summary")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Aggregate Score", f"{result['aggregate_score']:.3f}")
            with col_b:
                st.metric("Pass/Fail", f"{result['passed_assertions']}/{len(assertions)}", 
                         f"{result['failed_assertions']} failed")
            with col_c:
                status = "✅ PASS" if result['overall_pass'] else "❌ FAIL"
                st.metric("Overall", status)
            
            # Quick explanation
            if result['overall_pass']:
                st.info(f"🎉 **Quick Summary:** Despite {result['failed_assertions']} failed assertion(s), your test passed because the weighted aggregate score ({result['aggregate_score']:.3f}) exceeded the threshold ({threshold}). High-performing assertions with significant weights compensated for the failures.")
            else:
                st.warning(f"⚠️ **Quick Summary:** Your test failed because the weighted aggregate score ({result['aggregate_score']:.3f}) fell below the threshold ({threshold}). Consider improving the {result['failed_assertions']} failing assertion(s) or increasing their weights if they're important.")
            
            # Detailed breakdown
            st.subheader("Detailed Breakdown")
            df = pd.DataFrame(assertions)
            df['weighted_contribution'] = df['score'] * df['weight']
            df['status'] = df['pass'].map({True: '✅ PASS', False: '❌ FAIL'})
            
            display_df = df[['name', 'score', 'weight', 'weighted_contribution', 'status', 'reason']].copy()
            display_df.columns = ['Assertion', 'Score', 'Weight', 'Weighted Contribution', 'Status', 'Reason']
            
            st.dataframe(display_df, use_container_width=True)
            
            # Results explanation
            st.subheader("📋 Results Explanation")
            
            # Overall result explanation
            if result['overall_pass']:
                st.success(f"✅ **TEST PASSED!** Your aggregate score of {result['aggregate_score']:.3f} meets the threshold of {threshold}")
            else:
                st.error(f"❌ **TEST FAILED!** Your aggregate score of {result['aggregate_score']:.3f} is below the threshold of {threshold}")
            
            # Detailed explanation
            st.markdown("**What this means:**")
            
            # Individual assertion analysis
            passed_assertions = [a for a in assertions if a['pass']]
            failed_assertions = [a for a in assertions if not a['pass']]
            
            if passed_assertions:
                st.markdown(f"**✅ {len(passed_assertions)} assertion(s) passed:**")
                for assertion in passed_assertions:
                    st.markdown(f"- **{assertion['name']}** (weight {assertion['weight']}): {assertion['reason'] or 'No reason provided'}")
            
            if failed_assertions:
                st.markdown(f"**❌ {len(failed_assertions)} assertion(s) failed:**")
                for assertion in failed_assertions:
                    st.markdown(f"- **{assertion['name']}** (weight {assertion['weight']}): {assertion['reason'] or 'No reason provided'}")
            
            # Weight analysis
            high_weight_passed = [a for a in passed_assertions if a['weight'] >= 2]
            high_weight_failed = [a for a in failed_assertions if a['weight'] >= 2]
            
            if high_weight_passed or high_weight_failed:
                st.markdown("**🎯 High-weight assertions impact:**")
                if high_weight_passed:
                    st.markdown(f"- High-weight passing assertions ({', '.join([a['name'] for a in high_weight_passed])}) significantly boosted your score")
                if high_weight_failed:
                    st.markdown(f"- High-weight failing assertions ({', '.join([a['name'] for a in high_weight_failed])}) significantly hurt your score")
            
            # Score distribution analysis
            avg_score = np.mean([a['score'] for a in assertions])
            if avg_score > 0.8:
                st.markdown("**📈 Overall performance:** High individual scores across most assertions")
            elif avg_score > 0.5:
                st.markdown("**📊 Overall performance:** Mixed results with some strong and some weak assertions")
            else:
                st.markdown("**📉 Overall performance:** Low individual scores across most assertions")
            
            # Threshold analysis
            margin = result['aggregate_score'] - threshold
            if abs(margin) < 0.05:
                st.warning(f"⚠️ **Close call!** You passed by only {margin:.3f} points. Consider improving weak assertions.")
            elif margin > 0.2:
                st.info(f"💪 **Strong performance!** You exceeded the threshold by {margin:.3f} points.")
            
            # Mathematical breakdown
            st.subheader("🧮 Mathematical Breakdown")
            st.code(f"""
Total Weighted Score = Σ(Score × Weight)
                    = {' + '.join([f"{a['score']}×{a['weight']}" for a in assertions])}
                    = {result['total_weighted_score']}

Total Weights = Σ(Weight)
              = {' + '.join([str(a['weight']) for a in assertions])}
              = {result['total_weights']}

Aggregate Score = Total Weighted Score ÷ Total Weights
                = {result['total_weighted_score']} ÷ {result['total_weights']}
                = {result['aggregate_score']:.3f}

Threshold = {threshold}
Result = {'PASS' if result['overall_pass'] else 'FAIL'} ({result['aggregate_score']:.3f} {'≥' if result['overall_pass'] else '<'} {threshold})
            """)
            
            # Visualization
            st.subheader("Visualization")
            fig = create_score_visualization(assertions, result)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("⚠️ No assertions configured. Add some assertions to see the calculation!")
            st.markdown("""
            **Getting Started:**
            1. Click "➕ Add Assertion" to create your first assertion
            2. Or select an example from the sidebar dropdown
            3. Configure the score (0.0 to 1.0), weight, and pass/fail status
            4. Watch the results update in real-time!
            """)
    
    # Educational content - collapsible to save space
    with st.expander("🎓 How Weighted Assertions Work", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Concepts")
            st.markdown("""
            **Weighted Assertions** allow you to:
            - Give different importance to different metrics
            - Pass tests even when some assertions fail
            - Balance multiple competing requirements
            
            **The Formula:**
            ```
            Aggregate Score = Σ(Score × Weight) ÷ Σ(Weight)
            ```
            
            **Test Passes When:**
            ```
            Aggregate Score ≥ Test Threshold
            ```
            """)
        
        with col2:
            st.subheader("Real Example from promptfoo")
            st.markdown("""
            **French Greeting Test:**
            - Correctness (weight 2): 1.00 × 2 = 2.00
            - Tone (weight 1): 1.00 × 1 = 1.00  
            - Topicality (weight 1): 0.50 × 1 = 0.50
            - Greeting (weight 1): 1.00 × 1 = 1.00
            - Performance (weight 2): 0.00 × 2 = 0.00
            
            **Total:** 4.50 ÷ 7 = 0.64
            
            **Result:** 0.64 ≥ 0.6 threshold = ✅ PASS
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by Jaime Mantilla, MSIT + AI | Built with Streamlit | Based on [promptfoo documentation](https://www.promptfoo.dev/docs/configuration/expected-outputs/#weighted-assertions)")

if __name__ == "__main__":
    main()
