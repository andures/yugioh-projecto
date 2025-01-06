from django.shortcuts import render, get_object_or_404, redirect
from .models import Carta, Deck, CartaDeck
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    deck = get_object_or_404(Deck, pk=deck_id)
    cartas_en_deck = CartaDeck.objects.filter(deck=deck)
    return render(request, 'yugioh_app/deck_detail.html', {'deck': deck, 'cartas_en_deck': cartas_en_deck})

# vista para eliminar un deck
def deck_delete(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)

    # validacion para asegurar que solo el creador pueda eliminar su deck
    if deck.usuario != request.user:
        messages.error(request, "No tienes permiso para eliminar este deck.")
    
    # Eliminar el deck
    deck.delete()
    messages.success(request, "Deck eliminado con éxito.")
    return redirect('decks_list')

# Vista para crear un nuevo deck
# Tipos de cartas válidas para el Extra Deck
VALID_EXTRA_DECK_TYPES = [
    "fusion",
    "link",
    "pendulum_fusion",
    "synchro",
    "synchro_pendulum",
    "synchro_tuner",
    "xyz",
    "XYZ_Pendulum",
]

def deck_create(request):
    if request.method == "POST":
        nombre_deck = request.POST.get('nombre_deck')
        deck = Deck.objects.create(nombre=nombre_deck, usuario=request.user)

        cartas_seleccionadas = request.POST.getlist('cartas')
        cantidades = request.POST.getlist('cantidad_cartas')
        extra_cartas_seleccionadas = request.POST.getlist('extra_cartas')
        extra_cantidades = request.POST.getlist('extra_cantidad_cartas')

        main_deck_count = sum(int(cantidad) for cantidad in cantidades)
        extra_deck_count = sum(int(cantidad) for cantidad in extra_cantidades)

        # Validaciones
        if not (40 <= main_deck_count <= 60):
            messages.error(request, "El deck principal debe tener entre 40 y 60 cartas.")
            return redirect('deck_create')
        if extra_deck_count > 15:
            messages.error(request, "El Extra Deck no puede tener más de 15 cartas.")
            return redirect('deck_create')

        # Validación para las cartas del Extra Deck
        for carta_id in extra_cartas_seleccionadas:
            carta = Carta.objects.get(id=carta_id)
            if carta.frame_type not in VALID_EXTRA_DECK_TYPES:
                messages.error(request, f"La carta {carta.nombre} no puede ser agregada al Extra Deck porque no es de tipo válido.")
                return redirect('deck_create')

        # Guardar cartas del Main Deck
        for carta_id, cantidad in zip(cartas_seleccionadas, cantidades):
            carta = Carta.objects.get(id=carta_id)
            CartaDeck.objects.create(deck=deck, carta=carta, cantidad=int(cantidad))

        # Guardar cartas del Extra Deck
        for carta_id, cantidad in zip(extra_cartas_seleccionadas, extra_cantidades):
            carta = Carta.objects.get(id=carta_id)
            CartaDeck.objects.create(deck=deck, carta=carta, cantidad=int(cantidad))

        messages.success(request, "Deck creado con éxito.")
        return redirect('deck_detail', deck_id=deck.id)

    # Cargar cartas desde la base de datos
    cartas = Carta.objects.all()
    return render(request, 'yugioh_app/deck_create.html', {'cartas': cartas})