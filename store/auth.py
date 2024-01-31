from django.shortcuts import redirect
def authMiddleware(get_response):
    
    def middleware(request):
        
        if not request.session.get('customer'):
            return redirect('login')    
        
        response = get_response(request)
        
        
        
        return response
    
    return middleware