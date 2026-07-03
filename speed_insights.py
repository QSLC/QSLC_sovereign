"""
Vercel Speed Insights integration for Streamlit applications.

This module provides integration with Vercel Speed Insights for tracking
web vitals and performance metrics in Streamlit applications.
"""

import streamlit as st
import streamlit.components.v1 as components


def inject_speed_insights(
    debug: bool = False,
    sample_rate: float = 1.0,
    route: str = None,
    dsn: str = None
):
    """
    Inject Vercel Speed Insights tracking into the Streamlit app.
    
    This function injects the Speed Insights script using Streamlit's HTML
    component functionality. The script automatically tracks web vitals and
    performance metrics when the app is deployed on Vercel.
    
    Parameters
    ----------
    debug : bool, optional
        Enable debug logging in development mode (default: False)
    sample_rate : float, optional
        Sampling rate for events (0.0 to 1.0). Use lower values to reduce
        data collection and costs. Default is 1.0 (100% of events)
    route : str, optional
        Dynamic page route for aggregating metrics across similar paths
    dsn : str, optional
        Project DSN for self-hosting scenarios
        
    Notes
    -----
    - Speed Insights does not track data in development mode
    - The tracking script is injected once per session to avoid duplicates
    - Requires the app to be deployed on Vercel for data collection
    
    Examples
    --------
    Basic usage (recommended for most cases):
    >>> inject_speed_insights()
    
    With custom sampling (50% of events):
    >>> inject_speed_insights(sample_rate=0.5)
    
    With debug mode enabled:
    >>> inject_speed_insights(debug=True)
    """
    # Only inject once per session to avoid duplicates
    if 'speed_insights_injected' not in st.session_state:
        st.session_state.speed_insights_injected = True
        
        # Build configuration object
        config_parts = []
        if debug:
            config_parts.append(f'debug: {str(debug).lower()}')
        if sample_rate != 1.0:
            config_parts.append(f'sampleRate: {sample_rate}')
        if route:
            config_parts.append(f'route: "{route}"')
        if dsn:
            config_parts.append(f'dsn: "{dsn}"')
        
        config_str = f"{{ {', '.join(config_parts)} }}" if config_parts else "{}"
        
        # Create the injection script
        # This uses the generic inject method from @vercel/speed-insights
        script = f"""
        <script type="module">
            // Import the Speed Insights injection function
            import {{ injectSpeedInsights }} from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@1/dist/index.mjs';
            
            // Inject Speed Insights with configuration
            injectSpeedInsights({config_str});
        </script>
        """
        
        # Inject the script using Streamlit's HTML component
        components.html(script, height=0)


def set_route(route: str):
    """
    Update the current route for Speed Insights tracking.
    
    This is useful for single-page applications where the route changes
    without a full page reload.
    
    Parameters
    ----------
    route : str
        The new route path to track
        
    Examples
    --------
    >>> set_route("/dashboard")
    """
    # Note: In Streamlit, pages reload on interaction, so this is less
    # commonly needed than in SPAs. However, it's provided for completeness.
    script = f"""
    <script type="module">
        if (window.speedInsights && window.speedInsights.setRoute) {{
            window.speedInsights.setRoute("{route}");
        }}
    </script>
    """
    components.html(script, height=0)
