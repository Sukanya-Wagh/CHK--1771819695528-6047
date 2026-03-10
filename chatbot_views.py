from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid

from .models import ChatMessage
from .chatbot_ai import AgricultureChatbot


# Initialize chatbot
chatbot = AgricultureChatbot()


@login_required
def chatbot_page(request):
    """Main chatbot interface page"""
    # Get user's recent chat history
    recent_chats = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:20]
    
    context = {
        'recent_chats': recent_chats,
    }
    return render(request, 'core/chatbot.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def chatbot_api(request):
    """API endpoint for chatbot responses"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        crop_type = data.get('crop_type', '')
        season = data.get('season', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Get AI response
        response_data = chatbot.get_response(user_message, crop_type, season)
        
        # Save to database
        chat_message = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=session_id,
            user_message=user_message,
            bot_response=response_data['response'],
            crop_type=crop_type,
            season=season,
            query_category=response_data['category'],
            confidence_score=response_data['confidence'],
            response_time=response_data['response_time']
        )
        
        return JsonResponse({
            'success': True,
            'response': response_data['response'],
            'category': response_data['category'],
            'confidence': response_data['confidence'],
            'message_id': chat_message.id,
            'session_id': session_id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def chatbot_feedback(request):
    """Record user feedback on chatbot response"""
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        is_helpful = data.get('is_helpful')
        
        chat_message = ChatMessage.objects.get(id=message_id, user=request.user)
        chat_message.is_helpful = is_helpful
        chat_message.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def chatbot_history(request):
    """Get user's chat history"""
    chats = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    history = []
    for chat in chats:
        history.append({
            'id': chat.id,
            'user_message': chat.user_message,
            'bot_response': chat.bot_response,
            'category': chat.query_category,
            'crop_type': chat.crop_type,
            'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_helpful': chat.is_helpful
        })
    
    return JsonResponse({'history': history})


@login_required
def clear_chat_history(request):
    """Clear user's chat history"""
    if request.method == 'POST':
        ChatMessage.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=400)
