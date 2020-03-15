from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes((AllowAny,))
def handle(request):
    print("132313")