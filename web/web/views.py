# Random number generator to select a random entry
from random import randint
# Our awesome gender guesser
import gender_guesser.detector as gender_detector

# Django supplied Class Based View to show a template
from django.views.generic import TemplateView

from .models import Actor, Person


class ActorView(TemplateView):

    template_name = 'actor_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # The name from the URL
        self.name = kwargs['name'] or 'unknown'
        # Check if we already have this person.
        # We don't want a new result for the same name!
        visitor = Person.objects.filter(name=self.name).first()

        if not visitor:
            visitor = self.create_new_actor()

        context['actor'] = visitor.actor
        return context

    def create_new_actor(self):
        # We need just the first name to match against our actors
        first_name = self.get_first_name()

        # Filters our objects that start with the name
        # e.g. John would get ['John Wayne', 'Johnny Depp', 'John Goodman']
        # istartswith is case insensitive startswith
        name_matches = Actor.objects.filter(name__istartswith=first_name)

        count = len(name_matches)
        if count == 1:
            # If we have 1 Actor, use that one
            actor = name_matches.first()
        elif count > 1:
            # If there's more than one, use a random one *from those*
            actor = name_matches[randint(0, count - 1)]
        else:
            # Otherwise, most likely create a new actor
            guesser = gender_detector.Detector()
            guessed_gender = guesser.get_gender(first_name)
            if guessed_gender == 'unknown':
                # We didn't find the gender, just use any actor
                actor = self.get_random_actor()
            else:
                gender = 'M' if guessed_gender == 'male' else 'F'
                # Woohoo we can get a gender accurate actor!
                actor = self.get_random_actor(gender)

        return Person.objects.create(name=self.name, actor=actor)

    def get_first_name(self):
        # Returns 'Jilles' for 'jilles-soeters'
        # Gender guesses returns unknown if name doesn't start with a capital letter
        return (self.name.split('-')[0] if '-' in self.name else self.name).title()

    @staticmethod
    def get_random_actor(gender=None):
        # Get all our Actor objects, perhaps filtered by gender
        qs = Actor.objects.filter(gender=gender) if gender else Actor.objects.all()
        total_count = qs.count()
        random_actor = qs[randint(0, total_count - 1)]
        # Return a random one
        return random_actor
