from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import json
import os

def application(environ, start_response):
    """The main WSGI application that handles all requests"""
    
    # Get the request method and path
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    
    # Route the request based on the path
    if path == '/' or path == '/home':
        response = handle_home(environ)
    elif path == '/about':
        response = handle_about(environ)
    elif path == '/contact':
        response = handle_contact(environ)
    elif path.startswith('/static/'):
        response = handle_static(environ)
    elif path.startswith('/api/'):
        response = handle_api(environ)
    else:
        response = handle_not_found(environ)
    
    # Start the response with the appropriate status and headers
    start_response(response['status'], response['headers'])
    
    # Return the response body as a list of bytes (WSGI requirement)
    return [response['body'].encode('utf-8')]

def handle_home(environ):
    """Handle requests to the home page"""
    return {
        'status': '200 OK',
        'headers': [('Content-type', 'text/html; charset=utf-8')],
        'body': """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Python WSGI Home</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <nav>
                    <a href="/home">Home</a>
                    <a href="/about">About</a>
                    <a href="/contact">Contact</a>
                    <a href="/static/sample.pdf">Sample PDF</a>
                </nav>
                <h1>Welcome to our Static WSGI Website</h1>
                <p>This website is running on a pure Python WSGI server with static content.</p>
                <img src="/static/logo.png" alt="Logo" width="200">
                <footer>
                    <p>Powered by Python WSGI | Static IP: 203.0.113.45</p>
                </footer>
            </body>
            </html>
        """
    }

def handle_about(environ):
    """Handle requests to the about page"""
    return {
        'status': '200 OK',
        'headers': [('Content-type', 'text/html; charset=utf-8')],
        'body': """
            <!DOCTYPE html>
            <html>
            <head>
                <title>About Us</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <nav>
                    <a href="/home">Home</a>
                    <a href="/about">About</a>
                    <a href="/contact">Contact</a>
                </nav>
                <h1>About This Website</h1>
                <p>This is a static website built with Python's WSGI interface.</p>
                <p>Our server has a static IP address: 203.0.113.45</p>
                <footer>
                    <p>Powered by Python WSGI | Static IP: 203.0.113.45</p>
                </footer>
            </body>
            </html>
        """
    }

def handle_contact(environ):
    """Handle requests to the contact page"""
    return {
        'status': '200 OK',
        'headers': [('Content-type', 'text/html; charset=utf-8')],
        'body': """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Contact Us</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <nav>
                    <a href="/home">Home</a>
                    <a href="/about">About</a>
                    <a href="/contact">Contact</a>
                </nav>
                <h1>Contact Information</h1>
                <p>Email: contact@static-wsgi-example.com</p>
                <p>Server IP: 203.0.113.45</p>
                <p>Port: 8000</p>
                <footer>
                    <p>Powered by Python WSGI | Static IP: 203.0.113.45</p>
                </footer>
            </body>
            </html>
        """
    }

def handle_static(environ):
    """Handle static file requests"""
    path = environ['PATH_INFO']
    file_path = path[1:]  # Remove the leading slash
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Sample static files (in a real app, these would be actual files)
    static_files = {
        'style.css': """
            body { 
                font-family: Arial, sans-serif; 
                line-height: 1.6; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
            }
            nav { 
                background: #f4f4f4; 
                padding: 10px; 
                margin-bottom: 20px; 
            }
            nav a { 
                margin-right: 15px; 
                text-decoration: none; 
            }
            footer { 
                margin-top: 20px; 
                border-top: 1px solid #ccc; 
                padding-top: 10px; 
                font-size: 0.9em;
            }
            img {
                max-width: 100%;
                height: auto;
            }
        """,
        'logo.png': """
            [This would be binary PNG data in a real implementation]
            For demo purposes, we're just returning a placeholder
        """,
        'sample.pdf': """
            [This would be binary PDF data in a real implementation]
            For demo purposes, we're just returning a placeholder
        """
    }
    
    # Check if file exists in our static files
    filename = os.path.basename(file_path)
    if filename in static_files:
        content = static_files[filename]
        
        # Determine content type based on file extension
        if filename.endswith('.css'):
            content_type = 'text/css'
        elif filename.endswith('.png'):
            content_type = 'image/png'
        elif filename.endswith('.pdf'):
            content_type = 'application/pdf'
        else:
            content_type = 'text/plain'
            
        return {
            'status': '200 OK',
            'headers': [('Content-type', content_type)],
            'body': content
        }
    else:
        return handle_not_found(environ)

def handle_api(environ):
    """Handle API requests"""
    path = environ['PATH_INFO']
    
    if path == '/api/info':
        return {
            'status': '200 OK',
            'headers': [('Content-type', 'application/json')],
            'body': json.dumps({
                'server': 'Static WSGI Server',
                'ip': '13.41.128.226',
                'port': 8000,
                'status': 'online'
            })
        }
    else:
        return handle_not_found(environ)

def handle_not_found(environ):
    """Handle 404 Not Found errors"""
    return {
        'status': '404 Not Found',
        'headers': [('Content-type', 'text/html; charset=utf-8')],
        'body': """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Page Not Found</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <nav>
                    <a href="/home">Home</a>
                    <a href="/about">About</a>
                    <a href="/contact">Contact</a>
                </nav>
                <h1>404 - Page Not Found</h1>
                <p>The requested URL was not found on this server.</p>
                <p><a href="/home">Return to the home page</a></p>
                <footer>
                    <p>Powered by Python WSGI | Static IP: 203.0.113.45</p>
                </footer>
            </body>
            </html>
        """
    }

if __name__ == '__main__':
    # Create the WSGI server
    port = 8000
    static_ip = '13.41.128.226'  # Replace with your actual static IP
    
    print(f"Serving static website at http://{static_ip}:{port}")
    print("Available routes:")
    print(f"  http://{static_ip}:{port}/home")
    print(f"  http://{static_ip}:{port}/about")
    print(f"  http://{static_ip}:{port}/contact")
    print(f"  http://{static_ip}:{port}/static/style.css")
    print(f"  http://{static_ip}:{port}/api/info")
    
    with make_server('', port, application) as httpd:
        # Serve until process is killed
        httpd.serve_forever()
