from django.contrib import admin
from .models import Carta, Deck, CartaDeck, Partida
# Register your models here.

@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'nivel', 'ataque', 'defensa')

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'fecha_creacion')

@admin.register(CartaDeck)
class CartaDeckAdmin(admin.ModelAdmin):
    list_display = ('deck', 'carta', 'cantidad')

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('jugador1', 'jugador2', 'ganador', 'fecha_inicio', 'fecha_fin')

