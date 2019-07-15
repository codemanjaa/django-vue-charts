# -*- coding: utf-8 -*-
"""Survey chatbot."""

from jdfbots.chatbot import State, Transition
from jdfbots.chatbot.helper import MultipleChoice


class Start(State):
    """Start state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        return Transition.MOVE('survey.Welcome')

    @classmethod
    def on_event(cls, page, user, event):
        return Transition.MOVE('survey.Welcome')


class Welcome(MultipleChoice):
    """Welcome message."""

    name = 'welcome'
    question = ("Sondage intermédiaire\n" + "*" * 30 + "\n\nJe vais maintenant te poser quelques questions de mi-parcours. À la fin je te ramènerai au point où tu en étais avant qu'on commence.")
    buttons = [{'title': "C'est parti!", 'payload': 'LETS_GO'}]
    next = 'survey.Status'


class Status(MultipleChoice):
    """Status question."""

    name = 'status'
    question = ("Avez-vous recommencé à fumer depuis le début du programme?\n\n"
                "a) Non, je tiens bon\n"
                "b) J'essaie toujours d'arrêter\n"
                "c) J'ai renoncé à arrêter, mais je consomme moins de tabac qu'avant\n"
                "d) J'ai renoncé à arrêter, et j'ai repris ma consommation d'avant\n"
                "e) J'ai renoncé à arrêter, et je consomme plus de tabac qu'avant\n")
    buttons = [{'title': "a", 'payload': 'STATUS_HOLD'},
               {'title': "b", 'payload': 'STATUS_TRYING'},
               {'title': "c", 'payload': 'STATUS_DIMINISHED'},
               {'title': "d", 'payload': 'STATUS_SAME'},
               {'title': "e", 'payload': 'STATUS_INCREASED'}]
    next = lambda x: 'survey.Days' if x != 'STATUS_HOLD' else 'survey.Comments'


class Days(MultipleChoice):
    """Days question."""

    name = 'days'
    question = "Combien de jours d'affilée avez-vous tenu sans fumer au maximum durant ce programme?"
    buttons = [{'title': '0', 'payload': "DAYS_0"},
               {'title': "1–6", 'payload': "DAYS_1_6"},
               {'title': "7–13", 'payload': "DAYS_7_13"},
               {'title': "14–20", 'payload': "DAYS_14_20"},
               {'title': "21–27", 'payload': "DAYS_21_27"},
               {'title': "plus de 28", 'payload': "DAYS_28_MORE"}]
    next = 'survey.Comments'


class Comments(MultipleChoice):
    """Comments question."""

    name = 'comments'
    question = 'Pouvez-vous estimer approximativement le nombre de commentaires que vous avez postés sur la page Facebook “J’arrête de fumer” depuis le début du programme?'
    buttons = [{'title': '0', 'payload': 'COMMENTS_0'},
               {'title': '1–10', 'payload': 'COMMENTS_1_10'},
               {'title': '11–20', 'payload': 'COMMENTS_11_20'},
               {'title': '21–30', 'payload': 'COMMENTS_21_30'},
               {'title': 'plus de 30', 'payload': 'COMMENTS_31_MORE'}]
    next = 'survey.Visits'


class Visits(MultipleChoice):
    """Visits question."""

    name = 'visits'
    question = ("Depuis le début du programme, combien de fois approximativement avez-vous consulté la page Facebook “J’arrête de fumer” (conseils du jour, commentaires des participants, commentaires de l’équipe j’arrête de fumer), message privé )?\n\n"
                "a) Jamais\n"
                "b) Moins d’une fois par semaine\n"
                "c) Une à 3 fois par semaine\n"
                "d) 4 à 6 fois par semaine\n"
                "e) Une fois par jour\n"
                "f) Entre 2 et 10 fois par jour\n"
                "g) Plus de 10 fois par jour")
    buttons = [{'title': "a", 'payload': 'VISITS_NEVER'},
               {'title': "b", 'payload': 'VISITS_LESS_1_WEEK'},
               {'title': "c", 'payload': 'VISITS_1_3_WEEK'},
               {'title': "d", 'payload': 'VISITS_4_6_WEEK'},
               {'title': "e", 'payload': 'VISITS_1_DAY'},
               {'title': "f", 'payload': 'VISITS_2_10_DAY'},
               {'title': "g", 'payload': 'VISITS_10_MORE_DAY'}]
    next = 'survey.Useful'


class Useful(MultipleChoice):
    """Useful question."""

    name = 'useful'
    question = ("Depuis le début du programme, quelle a été pour vous l’aide la plus bénéfique ?\n\n"
                "a) La préparation qui vous a accompagné jusqu’à l’arrêt complet\n"
                "b) Le conseil quotidien sur la page\n"
                "c) Le soutien des autres candidats\n")
    buttons = [{'title': "a", 'payload': 'USEFUL_PREPA'},
               {'title': "b", 'payload': 'USEFUL_ADVICES'},
               {'title': "c", 'payload': 'USEFUL_COMMUNITY'}]
    next = 'survey.Weight'


class Weight(MultipleChoice):
    """Weight question."""

    name = 'weight'
    question = ("Durant l'arrêt, as-tu rencontré des problèmes de prise de poids?\n\n"
                "1 = Non, pas du tout // 7 = Oui, beaucoup")
    buttons = [
        {'title': "1", 'payload': "WEIGHT_1"},
        {'title': "2", 'payload': "WEIGHT_2"},
        {'title': "3", 'payload': "WEIGHT_3"},
        {'title': "4", 'payload': "WEIGHT_4"},
        {'title': "5", 'payload': "WEIGHT_5"},
        {'title': "6", 'payload': "WEIGHT_6"},
        {'title': "7", 'payload': "WEIGHT_7"},
    ]
    next = 'survey.Sleep'


class Sleep(MultipleChoice):
    """Sleep question."""

    name = 'sleep'
    question = ("Durant l'arrêt, as-tu rencontré des problèmes de sommeil?\n\n"
                "1 = Non, pas du tout // 7 = Oui, beaucoup")
    buttons = [
        {'title': "1", 'payload': "SLEEP_1"},
        {'title': "2", 'payload': "SLEEP_2"},
        {'title': "3", 'payload': "SLEEP_3"},
        {'title': "4", 'payload': "SLEEP_4"},
        {'title': "5", 'payload': "SLEEP_5"},
        {'title': "6", 'payload': "SLEEP_6"},
        {'title': "7", 'payload': "SLEEP_7"},
    ]
    next = 'survey.Stomach'


class Stomach(MultipleChoice):
    """Stomach question."""

    name = 'stomach'
    question = ("Durant l'arrêt, as-tu rencontré des problèmes intestinaux?\n\n"
                "1 = Non, pas du tout // 7 = Oui, beaucoup")
    buttons = [
        {'title': "1", 'payload': "STOMACH_1"},
        {'title': "2", 'payload': "STOMACH_2"},
        {'title': "3", 'payload': "STOMACH_3"},
        {'title': "4", 'payload': "STOMACH_4"},
        {'title': "5", 'payload': "STOMACH_5"},
        {'title': "6", 'payload': "STOMACH_6"},
        {'title': "7", 'payload': "STOMACH_7"},
    ]
    next = 'survey.Feelings'


class Feelings(MultipleChoice):
    """Feelings question."""

    name = 'feelings'
    question = ("Durant l'arrêt, as-tu rencontré des problèmes émotionnels (irritabilité, hypersensibilité, …)?\n\n"
                "1 = Non, pas du tout // 7 = Oui, beaucoup")
    buttons = [
        {'title': "1", 'payload': "FEELINGS_1"},
        {'title': "2", 'payload': "FEELINGS_2"},
        {'title': "3", 'payload': "FEELINGS_3"},
        {'title': "4", 'payload': "FEELINGS_4"},
        {'title': "5", 'payload': "FEELINGS_5"},
        {'title': "6", 'payload': "FEELINGS_6"},
        {'title': "7", 'payload': "FEELINGS_7"},
    ]
    next = 'survey.CommunityStrategy'


class CommunityStrategy(MultipleChoice):
    """CommunityStrategy question."""

    name = 'community_strategy'
    question = ("Je trouve que la stratégie d'aller chercher de l'aide sur le groupe Facebook dès qu'une envie de fumer se fait sentir est efficace:\n\n"
                "1 = Non, pas du tout // 7 = Oui, beaucoup")
    buttons = [
        {'title': "1", 'payload': "COMMUNITY_STRATEGY_1"},
        {'title': "2", 'payload': "COMMUNITY_STRATEGY_2"},
        {'title': "3", 'payload': "COMMUNITY_STRATEGY_3"},
        {'title': "4", 'payload': "COMMUNITY_STRATEGY_4"},
        {'title': "5", 'payload': "COMMUNITY_STRATEGY_5"},
        {'title': "6", 'payload': "COMMUNITY_STRATEGY_6"},
        {'title': "7", 'payload': "COMMUNITY_STRATEGY_7"},
    ]
    next = 'survey.HelpStrategy'


class HelpStrategy(MultipleChoice):
    """HelpStrategy question."""

    name = 'help_strategy'
    question = ("Je trouve que la stratégie d'aller chercher de l'aide sur HELP dès qu'une envie de fumer se fait sentir est efficace:\n\n"
                "1 = Non, pas du tout // 7 = Oui, beaucoup")
    buttons = [
        {'title': "1", 'payload': "HELP_STRATEGY_1"},
        {'title': "2", 'payload': "HELP_STRATEGY_2"},
        {'title': "3", 'payload': "HELP_STRATEGY_3"},
        {'title': "4", 'payload': "HELP_STRATEGY_4"},
        {'title': "5", 'payload': "HELP_STRATEGY_5"},
        {'title': "6", 'payload': "HELP_STRATEGY_6"},
        {'title': "7", 'payload': "HELP_STRATEGY_7"},
    ]
    next = 'survey.Help'


class Help(MultipleChoice):
    """Help question."""

    name = 'help'
    question = ("Je trouve que les interactions avec un chatbot (HELP) sont adéquates pour un programme de ce genre:\n\n"
                "1 = Non, pas du tout // 7 = Oui, beaucoup")
    buttons = [
        {'title': "1", 'payload': "HELP_1"},
        {'title': "2", 'payload': "HELP_2"},
        {'title': "3", 'payload': "HELP_3"},
        {'title': "4", 'payload': "HELP_4"},
        {'title': "5", 'payload': "HELP_5"},
        {'title': "6", 'payload': "HELP_6"},
        {'title': "7", 'payload': "HELP_7"},
    ]
    next = 'survey.End'


class End(State):
    """End state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        # Get the state to get back to
        with cls.storage(user) as s:
            next_state = s['previous_state']
        # Tell the user we are putting it back there
        page.send(
            user.facebook_id,
            "Merci d'avoir répondu à ce questionnaire. Tu vas maintenant retourner au status de notre interaction où tu en étais avant de commencer ce questionnaire!"
        )
        page.send(
            user.facebook_id,
            "*" * 30,
        )
        return Transition.MOVE(next_state)
