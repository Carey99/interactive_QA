"""
Simplest possible Vercel function
"""

def handler(request):
    """HTTP handler function"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': '*',
        },
        'body': '{"status":"healthy","message":"Backend working"}'
    }
