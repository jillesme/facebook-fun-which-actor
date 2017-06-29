from random import randint
import gender_guesser.detector as gender_detector

from django.views.generic import TemplateView

from .models import Actor, Person


class ActorView(TemplateView):

    template_name = 'actor_view.html'

    def create_new_actor(self):
        first_name = self.get_first_name()

        # First check if name is any of the actors
        # e.g. John would get ['John Wayne', 'Johnny Depp', 'John Goodman']
        name_matches = Actor.objects.filter(name__istartswith=first_name)
        count = len(name_matches)
        if count == 1:
            actor = name_matches.first()
        elif count > 1:
            actor = name_matches[randint(0, count - 1)]
        else:
            guesser = gender_detector.Detector()
            guessed_gender = guesser.get_gender(first_name)
            if guessed_gender == 'unknown':
                actor = self.get_random_actor()
            else:
                gender = 'M' if guessed_gender == 'male' else 'F'
                actor = self.get_random_actor(gender)
        return Person.objects.create(name=self.name, actor=actor)

    def get_first_name(self):
        # Gender guesses returns unknown if name doesn't start with a capital letter
        return (self.name.split('-')[0] if '-' in self.name else self.name).title()

    @staticmethod
    def get_random_actor(gender=None):
        qs = Actor.objects.filter(gender=gender) if gender else Actor.objects.all()
        total_count = qs.count()
        random_actor = qs[randint(0, total_count - 1)]
        return random_actor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.name = kwargs['name'] or 'unknown'
        visitor = Person.objects.filter(name=self.name).first()
        if not visitor:
            visitor = self.create_new_actor()

        context['actor'] = visitor.actor
        context['first_name'] = self.get_first_name()
        return context
