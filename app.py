import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

FEED_URL = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"
CACHE_DURATION = 300  # 5 minutes in seconds

# Simple in-memory cache
feed_cache = {
    "data": None,
    "last_fetched": 0
}

def parse_release_notes():
    """Fetches and parses the BigQuery release notes XML feed."""
    try:
        # Standard urllib request with a user-agent to avoid potential bot blockers
        req = urllib.request.Request(
            FEED_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        entries = []
        
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            date_str = title.text if title is not None else "Unknown Date"
            
            updated = entry.find('atom:updated', ns)
            updated_str = updated.text if updated is not None else ""
            
            link_elem = entry.find('atom:link', ns)
            link_href = link_elem.attrib.get('href', '') if link_elem is not None else ""
            
            content_elem = entry.find('atom:content', ns)
            content_html = content_elem.text if content_elem is not None else ""
            
            # Parse content_html to split by H3 tags
            parts = re.split(r'(<h3>.*?</h3>)', content_html)
            
            items = []
            if len(parts) <= 1:
                # No H3 tags found, treat as general
                items.append({
                    "category": "General",
                    "html": content_html.strip()
                })
            else:
                i = 1
                while i < len(parts):
                    h3_tag = parts[i]
                    cat_match = re.search(r'<h3>(.*?)</h3>', h3_tag)
                    category = cat_match.group(1) if cat_match else "General"
                    
                    content = parts[i+1] if i+1 < len(parts) else ""
                    
                    items.append({
                        "category": category,
                        "html": content.strip()
                    })
                    i += 2
                    
            entries.append({
                "date": date_str,
                "updated": updated_str,
                "link": link_href,
                "items": items
            })
            
        return entries, None
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/releases')
def get_releases():
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    now = time.time()
    
    if force_refresh or not feed_cache["data"] or (now - feed_cache["last_fetched"] > CACHE_DURATION):
        data, error = parse_release_notes()
        if error:
            # If we fail but have cached data, return that with a warning
            if feed_cache["data"]:
                return jsonify({
                    "releases": feed_cache["data"],
                    "source": "cache_fallback",
                    "error": f"Failed to refresh feed: {error}",
                    "last_updated": feed_cache["last_fetched"]
                })
            return jsonify({"error": error}), 500
        
        feed_cache["data"] = data
        feed_cache["last_fetched"] = now
        source = "network"
    else:
        source = "cache"
        
    return jsonify({
        "releases": feed_cache["data"],
        "source": source,
        "last_updated": feed_cache["last_fetched"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
