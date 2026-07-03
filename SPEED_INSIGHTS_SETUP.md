# Vercel Speed Insights Setup Documentation

## Overview

This document describes the Vercel Speed Insights integration for the QSLC Sovereign Streamlit application. Speed Insights automatically tracks web vitals and performance metrics when the application is deployed on Vercel.

## Implementation

### Files Added

1. **`package.json`** - Node.js package configuration for installing `@vercel/speed-insights`
2. **`speed_insights.py`** - Python module providing Speed Insights integration for Streamlit
3. **`node_modules/@vercel/speed-insights/`** - The Speed Insights npm package (installed)
4. **`package-lock.json`** - Lock file for npm dependencies

### Files Modified

1. **`streamlit_app.py`** - Main Streamlit application
   - Added import for `inject_speed_insights` 
   - Added Speed Insights initialization after page configuration
   - Updated section numbering to accommodate new Speed Insights section

## How It Works

### Architecture

Since Streamlit is a Python framework and Vercel Speed Insights is a JavaScript library, this integration uses a hybrid approach:

1. **npm Package Installation**: The `@vercel/speed-insights` npm package is installed to provide the tracking library
2. **Python Integration Module**: `speed_insights.py` provides a Python API that wraps the JavaScript library
3. **HTML Injection**: Uses Streamlit's `components.html()` to inject the Speed Insights script via CDN
4. **Session Management**: Ensures the script is only injected once per session to avoid duplicates

### Technical Details

The integration uses the `injectSpeedInsights()` function from the `@vercel/speed-insights` package, loaded via CDN:

```javascript
import { injectSpeedInsights } from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@1/dist/index.mjs';
```

This approach:
- ✅ Works with Python/Streamlit applications
- ✅ Loads the library from CDN (no build step required)
- ✅ Automatically tracks Core Web Vitals (LCP, FID, CLS, FCP, TTFB, INP)
- ✅ Only collects data in production (on Vercel)
- ✅ Does not affect local development

## Usage

### Basic Usage (Current Implementation)

The application currently uses the default configuration:

```python
from speed_insights import inject_speed_insights

inject_speed_insights()
```

This is called once at the top of `streamlit_app.py` after `st.set_page_config()`.

### Advanced Configuration Options

The `inject_speed_insights()` function supports several optional parameters:

#### Debug Mode
Enable console logging for debugging:
```python
inject_speed_insights(debug=True)
```

#### Sample Rate
Reduce data collection to a percentage of page views (e.g., 50%):
```python
inject_speed_insights(sample_rate=0.5)
```

This is useful for:
- Reducing costs for high-traffic applications
- Testing the integration before full rollout

#### Custom Route Tracking
Specify a custom route for grouping metrics:
```python
inject_speed_insights(route="/dashboard")
```

#### Custom DSN (Self-Hosting)
For self-hosted Vercel projects:
```python
inject_speed_insights(dsn="your-custom-dsn")
```

### Dynamic Route Updates

For single-page applications, you can update the route dynamically:

```python
from speed_insights import set_route

set_route("/new-page")
```

**Note**: In Streamlit, pages reload on interaction, so this is less commonly needed than in traditional SPAs.

## Viewing Metrics

Once deployed to Vercel:

1. Navigate to your project in the [Vercel Dashboard](https://vercel.com/dashboard)
2. Click on "Speed Insights" in the sidebar
3. Enable Speed Insights if not already enabled
4. View collected metrics after users visit your site

### Metrics Tracked

- **LCP (Largest Contentful Paint)**: Loading performance
- **FID (First Input Delay)**: Interactivity
- **CLS (Cumulative Layout Shift)**: Visual stability
- **FCP (First Contentful Paint)**: Initial rendering
- **TTFB (Time to First Byte)**: Server response time
- **INP (Interaction to Next Paint)**: Responsiveness

## Development vs Production

- **Development Mode**: Speed Insights does NOT collect data locally
- **Production Mode**: Data collection is automatic when deployed to Vercel

This ensures:
- No performance impact during development
- No polluted metrics from local testing
- Accurate production performance data

## Requirements

### Prerequisites

1. **Vercel Account**: Active Vercel account with deployment access
2. **Vercel Deployment**: Application must be deployed to Vercel
3. **Enable Speed Insights**: Enable Speed Insights in the Vercel Dashboard

### Dependencies

**Python:**
- `streamlit>=1.35.0` (already in requirements.txt)

**Node.js:**
- `@vercel/speed-insights@^1.0.0` (installed via package.json)

## Cost Considerations

Speed Insights usage is tracked per data point:
- **Free Tier**: Typically includes a generous amount of data points
- **Sample Rate**: Use `sample_rate` parameter to reduce costs for high-traffic sites
- **Monitoring**: Check usage in Vercel Dashboard under Speed Insights

## Troubleshooting

### Metrics Not Appearing

1. **Check Deployment**: Ensure the app is deployed to Vercel (not running locally)
2. **Enable Speed Insights**: Verify Speed Insights is enabled in the Vercel Dashboard
3. **Wait for Data**: Initial metrics may take a few minutes to appear
4. **Check Sample Rate**: Ensure `sample_rate` is not set too low

### Debug Mode

Enable debug mode to see events in the browser console:

```python
inject_speed_insights(debug=True)
```

### Browser Console Errors

If you see errors about CSP (Content Security Policy):
- Ensure your Vercel project allows CDN scripts
- Check `vercel.json` for CSP configurations

## Additional Resources

- [Vercel Speed Insights Documentation](https://vercel.com/docs/speed-insights)
- [Speed Insights Quickstart Guide](https://vercel.com/docs/speed-insights/quickstart)
- [Speed Insights Package Documentation](https://vercel.com/docs/speed-insights/package)
- [Web Vitals Guide](https://web.dev/vitals/)

## Support

For issues specific to:
- **Speed Insights**: Contact Vercel Support or check [Vercel Community](https://vercel.com/community)
- **Integration Issues**: Check the implementation in `speed_insights.py`
- **Streamlit Issues**: Refer to [Streamlit Documentation](https://docs.streamlit.io/)
