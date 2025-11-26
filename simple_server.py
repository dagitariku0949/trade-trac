#!/usr/bin/env python3
"""
Simple HTTP Server for Trading Dashboard
Serves frontend files without backend functionality
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent / 'frontend'), **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_simple_server():
    """Start a simple HTTP server for frontend files"""
    PORT = 8000
    
    print("🚀 Starting Simple Trading Dashboard Server")
    print("=" * 50)
    print(f"📁 Serving files from: {Path(__file__).parent / 'frontend'}")
    print(f"🌐 Server running at: http://localhost:{PORT}")
    print()
    print("📋 Available URLs:")
    print(f"   Main Dashboard: http://localhost:{PORT}/index.html")
    print(f"   Admin Panel:    http://localhost:{PORT}/admin-standalone.html")
    print()
    print("ℹ️  Note: This is frontend-only mode. For full functionality,")
    print("   install Python dependencies and run the Flask backend.")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            # Open browser automatically
            webbrowser.open(f'http://localhost:{PORT}/index.html')
            
            print(f"✅ Server started successfully!")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use.")
            print("   Try closing other applications or use a different port.")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_simple_server()