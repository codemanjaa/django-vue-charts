# -*- coding: utf-8 -*-
"""Cigarettes tracker chatbot."""

import os
import time
from datetime import datetime

from fbmq import attachment as Attachment

from jdfbots import i18n
from jdfbots.chatbot import State, Transition
from jdfbots.chatbot.helper import MultipleChoice, MultipleChoiceAccumulate


class Start(State):
    """Start state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        return cls.on_event(page, user, None)

    @classmethod
    def on_event(cls, page, user, event):
        # t = i18n.translator(user)
        # page.send(
        #     user.facebook_id,
        #     t(
        #         "Nous allons maintenant suivre ensemble ta consommation de cigarettes pour établir ton profil de fumeur! Pour cela il va falloir que tu viennes m'indiquer durant ces prochaines semaines chacune des cigarettes que tu fumes, au moment même où tu la fumes. Tu sors ton téléphone au moment pile où tu sors ton paquet. ☺️"
        #     ),
        # )
        # time.sleep(2)
        # return Transition.MOVE("tracker.Introduction")
        return Transition.MOVE("tracker.End")


class Introduction(MultipleChoice):
    """Introduction message."""

    name = "introduction"
    question = "On va faire une fois l'essai avant de suivre pour de vrai ta consommation... let's go!"
    buttons = [{"title": "Essayons", "payload": "LETS_TRY"}]
    # next = "tracker.Announce"
    next = "tracker.End"


class Announce(State):
    """Announce state."""

    buttons = [{"title": "Je fume", "payload": "SMOKE"}]

    @classmethod
    def on_enter(cls, page, user, prev):
        return Transition.MOVE("tracker.End")
        t = i18n.translator(user)
        group = "cigarettes"
        with cls.storage(user) as s:
            if group not in s:
                page.send(
                    user.facebook_id,
                    t(
                        "Pour faire un essai, clique sur le bouton «Je fume» ci-dessous. Réponds ensuite aux questions qui suivront, au hasard pour cette fois."
                    ),
                    quick_replies=i18n.translate_buttons(
                        cls.buttons, lang=user.language
                    ),
                )
            else:
                page.send(
                    user.facebook_id,
                    t(
                        "Pour enregistrer une cigarette clique sur le bouton «Je fume» ci-dessous."
                    ),
                    quick_replies=i18n.translate_buttons(
                        cls.buttons, lang=user.language
                    ),
                )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        # t = i18n.translator(user)
        # # Get the response
        # response = event.quick_reply_payload
        # # If the answer is not valid
        # if not response or response != "SMOKE":
        #     page.send(
        #         user.facebook_id,
        #         t(
        #             "Pour éviter que ça ne soit du à une mauvaise manipulation, il faut que tu appuies le bouton!"
        #         ),
        #         quick_replies=i18n.translate_buttons(cls.buttons, lang=user.language),
        #     )
        #     return Transition.STAY
        # return Transition.MOVE("tracker.NewRecord")
        return Transition.MOVE("tracker.End")


class NewRecord(State):
    """New record state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        # group = "cigarettes"
        # with cls.storage(user) as s:
        #     if group not in s:
        #         s[group] = list()
        #     s[group].append({"datetime": datetime.now().isoformat()})
        # return Transition.MOVE("tracker.Context")
        return Transition.MOVE("tracker.End")


class Context(MultipleChoiceAccumulate):
    """Context question."""

    group = "cigarettes"
    name = "context"
    question = "Dans quel cadre te trouves-tu?"
    buttons = [
        {"title": "Privé", "payload": "CONTEXT_PRIVE"},
        {"title": "Professionnel", "payload": "CONTEXT_PROF"},
    ]
    # next = "tracker.Alone"
    next = "tracker.End"


class Alone(MultipleChoiceAccumulate):
    """Alone question."""

    group = "cigarettes"
    name = "alone"
    question = "Fumes-tu?"
    buttons = [
        {"title": "Seul", "payload": "ALONE_YES"},
        {"title": "En groupe", "payload": "ALONE_NO"},
    ]
    # next = "tracker.Driving"
    next = "tracker.End"


class Driving(MultipleChoiceAccumulate):
    """Driving question."""

    group = "cigarettes"
    name = "driving"
    question = "Es-tu en voiture?"
    buttons = [
        {"title": "Oui", "payload": "DRIVING_YES"},
        {"title": "Non", "payload": "DRIVING_NO"},
    ]
    # next = "tracker.Mood"
    next = "tracker.End"


class Mood(MultipleChoiceAccumulate):
    """Mood question."""

    group = "cigarettes"
    name = "mood"
    question = (
        "Quelle était ton humeur au moment d'allumer ta cigarette?"
        "\n\n"
        "a. Stressé\n"
        "b. Fatigué\n"
        "c. Neutre\n"
        "d. Inquiet\n"
        "e. En colère\n"
        "f. Déprimé\n"
        "g. Content\n"
        "h. Détendu\n"
        "i. Ennui"
    )
    buttons = [
        {"title": "a", "payload": "MOOD_STRESSED"},
        {"title": "b", "payload": "MOOD_TIRED"},
        {"title": "c", "payload": "MOOD_NEUTRAL"},
        {"title": "d", "payload": "MOOD_WORRIED"},
        {"title": "e", "payload": "MOOD_ANGRY"},
        {"title": "f", "payload": "MOOD_SAD"},
        {"title": "g", "payload": "MOOD_HAPPY"},
        {"title": "h", "payload": "MOOD_RELAXED"},
        {"title": "i", "payload": "MOOD_BORED"},
    ]
    # next = "tracker.Desire"
    next = "tracker.End"


class Desire(MultipleChoiceAccumulate):
    """Desire question."""

    group = "cigarettes"
    name = "desire"
    question = "Concernant cette cigarette, est-ce une envie:"
    buttons = [
        {"title": "Nulle", "payload": "DESIRE_NONE"},
        {"title": "Faible", "payload": "DESIRE_LOW"},
        {"title": "Modérée", "payload": "DESIRE_MEDIUM"},
        {"title": "Forte", "payload": "DESIRE_HIGH"},
        {"title": "Extrême", "payload": "DESIRE_EXTREME"},
    ]
    # next = "tracker.Necessary"
    next = "tracker.End"


class Necessary(MultipleChoiceAccumulate):
    """Necessary question."""

    group = "cigarettes"
    name = "necessary"
    question = "Est-ce que cette cigarette est nécessaire?"
    buttons = [
        {"title": "Oui", "payload": "NECESSARY_YES"},
        {"title": "Non", "payload": "NECESSARY_NO"},
    ]
    # next = "tracker.Resisting"
    next = "tracker.End"


class Resisting(MultipleChoiceAccumulate):
    """Resisting question."""

    group = "cigarettes"
    name = "resisting"
    question = (
        "Comment aurais-tu pu y résister?"
        "\n\n"
        "a. En allant marcher\n"
        "b. En buvant un verre d'eau\n"
        "c. En me lavant les dents/mains\n"
        "d. En mâchant un chewing-gum\n"
        "e. En écoutant de la musique\n"
        "f. En surfant sur internet\n"
        "g. En parlant avec d'autres personnes\n"
        "h. En téléphonant à un ami/famille\n"
        "i. En prenant une douche ou un bain\n"
        "j. En faisant un exercice de relaxation\n"
        "k. En jouant avec un objet (stylo/balle anti-stress)"
    )
    buttons = [
        {"title": "a", "payload": "RESISTING_WALKING"},
        {"title": "b", "payload": "RESISTING_WATER"},
        {"title": "c", "payload": "RESISTING_TEETH"},
        {"title": "d", "payload": "RESISTING_CHEWING"},
        {"title": "e", "payload": "RESISTING_MUSIC"},
        {"title": "f", "payload": "RESISTING_WEB"},
        {"title": "g", "payload": "RESISTING_TALKING"},
        {"title": "h", "payload": "RESISTING_PHONE"},
        {"title": "i", "payload": "RESISTING_SHOWER"},
        {"title": "j", "payload": "RESISTING_RELAXING"},
        {"title": "k", "payload": "RESISTING_PLAYING"},
    ]
    # next = "tracker.Thanks"
    next = "tracker.End"


class Thanks(State):
    """Thanks state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        # t = i18n.translator(user)
        # page.send(user.facebook_id, t("Merci pour tes réponses!"))
        # group = "cigarettes"
        # with cls.storage(user) as s:
        #     if len(s[group]) == 1:
        #         page.send(
        #             user.facebook_id,
        #             t(
        #                 "Voilà, tu sais maintenant comment enregistrer une cigarette. Dès à présent, nous mémoriserons chacune d'entre-elles pour établir ton profil de fumeur. Le bouton «Je fume» reviendra automatiquement après avoir enregistré une cigarette afin que tu puisses enregistrer la suivante."
        #             ),
        #         )
        # return Transition.MOVE("tracker.Announce")
        return Transition.MOVE("tracker.End")


class End(State):
    """End state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        # t = i18n.translator(user)
        # if os.path.exists(f"media/profiles/{user.id}.png"):
        #     page.send(
        #         user.facebook_id,
        #         t(
        #             "Voici ton profil de fumeur que j'ai pu établir grâce "
        #             "aux cigarettes que tu m'as indiquées:"
        #         ),
        #     )
        #     page.send(
        #         user.facebook_id,
        #         Attachment.Image(
        #             os.environ["SERVER_URL"] + f"/media/profiles/{user.id}.png"
        #         ),
        #     )
        #     page.send(
        #         user.facebook_id,
        #         t(
        #             "Voilà, dans quelques jours tu vas arrêter de fumer et je "
        #             "serai là quand tu auras besoin d'un coup de pouce. D'ici là "
        #             "reste informé en suivant le groupe privé Facebook. "
        #             "À bientôt! 🤗"
        #         ),
        #     )
        # else:
        #     page.send(
        #         user.facebook_id,
        #         t(
        #             "Tu n'as pas enregistré de cigarettes et je ne peux donc "
        #             "malheureusement pas te donner ton profil. Mais cela ne "
        #             "m'empêchera pas de te donner un coup de main dans les "
        #             "moments difficiles de l'arrêt! D'ici là reste informé en "
        #             "suivant le groupe privé Facebook. À bientôt! 🤗"
        #         ),
        #     )
        return Transition.MOVE("cessation.Wait")
