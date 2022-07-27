from .models import Cart
def context_processor(request):
    current_user=request.user
    context = {}
    context['cart_record'] = Cart.objects.filter(userid= current_user.id).count()
    return context    