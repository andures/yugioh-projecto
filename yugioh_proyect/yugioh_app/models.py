from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Carta(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    nivel = models.IntegerField()
    ataque = models.IntegerField()
    defensa = models.IntegerField()
    descripcion = models.TextField()
    imagen_url = models.URLField()
    
    def __str__(self):
        return self.nombre

# modelo para los decks
class Deck(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - {self.usuario.username}'

# modelo realacion muchos a muchos entre deck y carta
class CartaDeck(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.cantidad}x {self.carta.nombre} en {self.deck.nombre}'

#model para las partidas
class Partida(models.Model):
    jugador1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jugador1')
    jugador2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jugador2')
    ganador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ganador')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.jugador1.username} vs {self.jugador2.username}'