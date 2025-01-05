from django.shortcuts import render, get_object_or_404
from .models import Carta, Deck, CartaDeck

# Vista para la página de inicio
def home(request):
    return render(request, 'yugioh_app/home.html')

# Vista para listar todas las cartas
def cartas_list(request):
    cartas = Carta.objects.all()  # Obtener todas las cartas
    return render(request, 'yugioh_app/cartas_list.html', {'cartas': cartas})

# Vista para listar todos los decks
def decks_list(request):
    decks = Deck.objects.all()  # Obtener todos los decks
    return render(request, 'yugioh_app/decks_list.html', {'decks': decks})

# Vista para mostrar los detalles de un deck específico
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)  # Obtener el deck por su ID
    # Obtener todas las cartas asociadas a este deck
    cartas_en_deck = CartaDeck.objects.filter(deck=deck)
    return render(request, 'yugioh_app/deck_detail.html', {'deck': deck, 'cartas_en_deck': cartas_en_deck})

# vista para crear un nuevo deck
def deck_create(request, deck_id=None):
    if deck_id:
        #si el deck ya existe, se edita
        deck = get_object_or_404(Deck, pk=deck_id, usuario=request.user)
    else:
        # si no existe, se crea uno nuevo 
        deck = Deck.objects.create(nombre='Nuevo Deck', usuario=request.user)
    
    return render(request, 'yugioh_app/deck_create.html', {'deck': deck})
