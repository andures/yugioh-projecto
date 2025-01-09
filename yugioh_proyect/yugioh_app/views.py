from django.shortcuts import render, get_object_or_404, redirect
from .models import Carta, Deck, CartaDeck
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.db import transaction
from collections import Counter
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout , login



MAX_DECKS = 10 # Cantidad máxima de decks que un usuario puede tener

# Vista para la página de inicio
def home(request):
    return render(request, 'yugioh_app/home.html')

# vista para registar un usuario
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('home')
        else:
            form= UserCreationForm()
    return render(request, 'yugioh_app/register.html', { 'form': form })

# Vista para iniciar sesión
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'yugioh_app/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')

# vista para la pagina de comunity
def comunity(request):
    
    return render(request, 'yugioh_app/comunity.html')

# Vista para listar todas las cartas
def cartas_list(request):
    cartas = Carta.objects.all()  # Obtener todas las cartas
    return render(request, 'yugioh_app/cartas_list.html', {'cartas': cartas})

# Vista para listar todos los decks
def decks_list(request):
    #usando select_related para evitar hacer una consulta por cada deck
    decks = Deck.objects.all().order_by('-id')[:10]  # Obtener todos los decks
    deck_count = Deck.objects.count() # Contar la cantidad de decks
    return render(request, 'yugioh_app/decks_list.html', {'decks': decks, 
                                                          'deck_count': deck_count, 
                                                          'max_decks': MAX_DECKS})

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
@login_required
def deck_create(request):
    if request.method == "POST":
        nombre_deck = request.POST.get('nombre_deck')
        cartas_seleccionadas = request.POST.getlist('cartas')
        cantidades = list(map(int, request.POST.getlist('cantidad_cartas')))
        extra_cartas_seleccionadas = request.POST.getlist('extra_cartas')
        extra_cantidades = list(map(int, request.POST.getlist('extra_cantidad_cartas')))

        main_deck_count = sum(cantidades)
        extra_deck_count = sum(extra_cantidades)

        # Validaciones de catidad todal de cartas en Main Deck y Extra Deck
        if not (40 <= main_deck_count <= 60):
            messages.error(request, "El deck principal debe tener entre 40 y 60 cartas.")
            return redirect('deck_create')
        if extra_deck_count > 15:
            messages.error(request, "El Extra Deck no puede tener más de 15 cartas.")
            return redirect('deck_create')
        
        # contar todas las cartas seleccionadas, tanto del main deck como del extra deck
        all_cards = cartas_seleccionadas + extra_cartas_seleccionadas
        all_cantidades = cantidades + extra_cantidades

        # usar Counter para contar las cantidades de cartas
        cartas_counter = Counter(dict(zip(all_cards, all_cantidades)))

        # verificar que no haya mas de 3 copias de una carta
        for carta_id, total_cantidad in cartas_counter.items():
            if total_cantidad > 3:
                carta = Carta.objects.get(id=carta_id)
                messages.error(request, f"La carta {carta.nombre} no puede tener más de 3 copias.")
                return redirect('deck_create')

        try:
            with transaction.atomic():  # Garantizar que todo se guarde correctamente
                # Crear el deck
                deck = Deck.objects.create(nombre=nombre_deck, usuario=request.user)

                # Recuperar todas las cartas en una sola consulta
                todas_cartas_ids = set(cartas_seleccionadas + extra_cartas_seleccionadas)
                cartas_dict = {carta.id: carta for carta in Carta.objects.filter(id__in=todas_cartas_ids)}

                # Guardar main deck
                for carta_id, cantidad in zip(cartas_seleccionadas, cantidades):
                    CartaDeck.objects.create(deck=deck, carta=cartas_dict[int(carta_id)], cantidad=cantidad)
                
                # Guardar extra deck con validación
                for carta_id, cantidad in zip(extra_cartas_seleccionadas, extra_cantidades):
                    carta = cartas_dict[int(carta_id)]
                    if carta.frame_type not in VALID_EXTRA_DECK_TYPES:
                        messages.error(request, f"La carta {carta.nombre} no puede ser agregada al Extra Deck porque no es de tipo válido.")
                        return redirect('deck_create')
                    CartaDeck.objects.create(deck=deck, carta=carta, cantidad=cantidad)

                messages.success(request, "Deck creado con éxito.")
                return redirect('deck_detail', deck_id=deck.id)
        
        except Exception as e:
            messages.error(request, f"Ocurrió un error al crear el deck: {str(e)}")
            return redirect('deck_create')

    # Si no es un POST, mostrar el formulario de creación de deck
    cartas = Carta.objects.all()
    return render(request, 'yugioh_app/deck_create.html', {'cartas': cartas})