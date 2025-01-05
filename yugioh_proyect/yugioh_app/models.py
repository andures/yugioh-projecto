from django.db import models
from django.contrib.auth.models import User

# Modelo para las cartas
class Carta(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    nivel = models.IntegerField(default=1)
    ataque = models.IntegerField(default=0)
    defensa = models.IntegerField(default=0)
    descripcion = models.TextField(default='')
    imagen_url = models.URLField(default='')
    # Atributos adicionales desde la API
    frame_type = models.CharField(max_length=50, null=True, blank=True)  # "xyz", etc.
    raza = models.CharField(max_length=50, null=True, blank=True)  # "Wyrm", "Dragon", etc.
    atributo = models.CharField(max_length=50, null=True, blank=True)  # "WIND", etc.
    
    def __str__(self):
        return self.nombre

# Modelo para los decks
class Deck(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - {self.usuario.username}'

# Modelo para la relación entre Deck y Carta (con cantidad)
class CartaDeck(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    en_extra_deck = models.BooleanField(default=False)# Si la carta está en el Extra Deck
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.cantidad}x {self.carta.nombre} en {self.deck.nombre}'

# Modelo para las partidas
class Partida(models.Model):
    jugador1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jugador1')
    jugador2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jugador2')
    ganador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ganador')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.jugador1.username} vs {self.jugador2.username}'
