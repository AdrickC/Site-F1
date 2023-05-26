from general.models import Game

def add_games(request):
    games = Game.objects.all()
    return {'games': games}
