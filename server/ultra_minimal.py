"""
Ultra-minimal API for Vercel - no dependencies
"""

def app(scope, receive, send):
    """
    Minimal ASGI app without FastAPI
    """
    if scope["type"] == "http":
        if scope["path"] == "/health" or scope["path"] == "/":
            response_body = b'{"status":"healthy","message":"Backend working"}'
        else:
            response_body = b'{"error":"Not found"}'
        
        async def asgi_app():
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', b'application/json'],
                    [b'access-control-allow-origin', b'*'],
                    [b'access-control-allow-methods', b'GET, POST, OPTIONS'],
                    [b'access-control-allow-headers', b'*'],
                ]
            })
            await send({
                'type': 'http.response.body',
                'body': response_body,
            })
        
        return asgi_app()

# Export for Vercel
handler = app
