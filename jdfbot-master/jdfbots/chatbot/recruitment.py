# -*- coding: utf-8 -*-
"""Recruitment chatbot."""

import os
import time

from fbmq import attachment as Attachment

from jdfbots import i18n
from jdfbots.algorithm import fagerstrom
from jdfbots.chatbot import State, Transition
from jdfbots.chatbot.helper import MultipleChoice


class Start(State):
    """Start state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        return cls.on_event(page, user, None)

    @classmethod
    def on_event(cls, page, user, event):
        t = i18n.translator(user)
        page.send(
            user.facebook_id,
            (t("Bienvenue {name}, je suis HELP. 👋", {"name": user.first_name})),
        )
        return Transition.MOVE("recruitment.Welcome")


class Welcome(MultipleChoice):
    """Welcome message."""

    name = "welcome"
    question = "Durant l’arrêt, quand tu auras une crise de manque, une envie forte de reprendre une cigarette, je t’apporterai une solution immédiate. Pour cela, j’ai besoin de te connaître un peu. Merci de répondre à ces questions."
    buttons = [{"title": "C'est parti!", "payload": "LETS_GO"}]
    next = "recruitment.ButtonsUsage"


class ButtonsUsage(State):
    """Explaining the usage of the buttons."""

    buttons = [
        {"title": "a", "payload": "BUTTONS_A"},
        {"title": "b", "payload": "BUTTONS_B"},
        {"title": "c", "payload": "BUTTONS_C"},
        {"title": "d", "payload": "BUTTONS_D"},
        {"title": "e", "payload": "BUTTONS_E"},
        {"title": "f", "payload": "BUTTONS_F"},
        {"title": "g", "payload": "BUTTONS_G"},
        {"title": "h", "payload": "BUTTONS_H"},
        {"title": "i", "payload": "BUTTONS_I"},
        {"title": "j", "payload": "BUTTONS_J"},
        {"title": "Ok", "payload": "BUTTONS_OK"},
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        page.send(
            user.facebook_id,
            t(
                "Avant d'aller plus loin, voilà une brève explication sur l'utilisation des boutons pour répondre. Il se peut que tous les boutons ne soient pas affichés en même temps sur ton écran. Pour cela tu peux les faire défiler comme illustré sur l'image ci-dessous."
            ),
        )
        page.send(
            user.facebook_id,
            Attachment.Image(os.environ["SERVER_URL"] + "/static/buttons.gif"),
        )
        page.send(
            user.facebook_id,
            t(
                "Pour montrer que tu as bien compris, appuie maintenant sur le bouton «Ok» qui se situe à la fin de la liste des boutons."
            ),
            quick_replies=cls.buttons,
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        t = i18n.translator(user)
        # Get the response
        response = event.quick_reply_payload
        # If the answer is not valid
        if not response:
            page.send(
                user.facebook_id,
                t("Il faut que tu répondes en utilisant les boutons!"),
                quick_replies=cls.buttons,
            )
            return Transition.STAY
        if response != "BUTTONS_OK":
            page.send(
                user.facebook_id,
                t("Tu dois cliquer sur le bouton «Ok»"),
                quick_replies=cls.buttons,
            )
            return Transition.STAY
        page.send(
            user.facebook_id,
            t(
                "Voilà, tu sais maintenant répondre en utilisant les boutons, on peut donc y aller avec les questions."
            ),
        )
        return Transition.MOVE("recruitment.Age")


class Age(MultipleChoice):
    """Age question."""

    name = "age"
    question = "Quel âge as-tu?"
    buttons = [
        {"title": "18–24", "payload": "AGE_18_24"},
        {"title": "25–34", "payload": "AGE_25_34"},
        {"title": "35–44", "payload": "AGE_35_44"},
        {"title": "45–54", "payload": "AGE_45_54"},
        {"title": "55–64", "payload": "AGE_55_64"},
        {"title": "65+", "payload": "AGE_65_+"},
    ]
    next = "recruitment.Sex"


class Sex(MultipleChoice):
    """Sex question."""

    name = "sex"
    question = "Tu es:"
    buttons = [
        {"title": "Un homme", "payload": "SEX_M"},
        {"title": "Une femme", "payload": "SEX_W"},
    ]
    next = "recruitment.Job"


class Job(MultipleChoice):
    """Job question."""

    name = "job"
    question = "Si tu exerces actuellement une activité professionnelle, est-ce plutôt:"
    buttons = [
        {"title": "À l'intérieur", "payload": "JOB_INT"},
        {"title": "À l'extérieur", "payload": "JOB_EXT"},
        {"title": "Pas d'activité prof.", "payload": "JOB_NO"},
    ]
    next = "recruitment.Dependency"


class Dependency(MultipleChoice):
    """Dependency question."""

    name = "dependency"
    question = "Comment estimes-tu ta dépendance à la cigarette?"
    buttons = [
        {"title": "Faible", "payload": "DEPENDENCY_LOW"},
        {"title": "Modérée", "payload": "DEPENDENCY_MEDIUM"},
        {"title": "Forte", "payload": "DEPENDENCY_HIGH"},
        {"title": "Très forte", "payload": "DEPENDENCY_VERY_HIGH"},
    ]
    next = "recruitment.Try"


class Try(MultipleChoice):
    """Try question."""

    name = "try"
    question = "As-tu déjà tenté d'arrêter de fumer?"
    buttons = [
        {"title": "Non", "payload": "TRY_FIRST"},
        {"title": "Oui, une fois", "payload": "TRY_SECOND"},
        {"title": "Oui, 2 ou 3 fois", "payload": "TRY_THIRD_FOURTH"},
        {"title": "Oui, 4 à 9 fois", "payload": "TRY_FIFTH_TENTH"},
        {"title": "Oui, plus de 10 fois", "payload": "TRY_ELEVENTH_MORE"},
    ]
    next = "recruitment.FSDelay"


###################
# FAGERSTROM TEST #
###################


class FSDelay(MultipleChoice):
    """Fagerström Delay question."""

    name = "fs_delay"
    question = "Le matin, quel est le délai entre ton réveil et ta première cigarette?"
    buttons = [
        {"title": "Moins de 5 minutes", "payload": "FS_DELAY_5-"},
        {"title": "6 à 30 minutes", "payload": "FS_DELAY_6_30"},
        {"title": "31 à 60 minutes", "payload": "FS_DELAY_31_60"},
        {"title": "Plus de 60 minutes", "payload": "FS_DELAY_60+"},
    ]
    next = "recruitment.FSForbidden"


class FSForbidden(MultipleChoice):
    """Fagerström Forbidden question."""

    name = "fs_forbidden"
    question = (
        "T'es-t'il difficile de t'abstenir de fumer dans les endroits "
        "où c'est interdit?"
    )
    buttons = [
        {"title": "Oui", "payload": "FS_FORBIDDEN_YES"},
        {"title": "Non", "payload": "FS_FORBIDDEN_NO"},
    ]
    next = "recruitment.FSDifficult"


class FSDifficult(MultipleChoice):
    """Fagerström Difficult question."""

    name = "fs_difficult"
    question = "À quelle cigarette de la journée as-tu le plus de peine à renoncer?"
    buttons = [
        {"title": "La première", "payload": "FS_DIFFICULT_FIRST"},
        {"title": "Une autre", "payload": "FS_DIFFICULT_OTHER"},
    ]
    next = "recruitment.FSCount"


class FSCount(MultipleChoice):
    """Fagerström Count question."""

    name = "fs_count"
    question = "Combien de cigarettes fumes-tu par jour, en moyenne?"
    buttons = [
        {"title": "1 à 10", "payload": "FS_COUNT_1_10"},
        {"title": "11 à 20", "payload": "FS_COUNT_11_20"},
        {"title": "21 à 30", "payload": "FS_COUNT_21_30"},
        {"title": "Plus de 30", "payload": "FS_COUNT_30+"},
    ]
    next = "recruitment.FSRhythm"


class FSRhythm(MultipleChoice):
    """Fagerström Rhythm question."""

    name = "fs_rhythm"
    question = "Fumes-tu à un rythme plus soutenu le matin que l'après-midi?"
    buttons = [
        {"title": "Oui", "payload": "FS_RHYTHM_YES"},
        {"title": "Non", "payload": "FS_RHYTHM_NO"},
    ]
    next = "recruitment.FSIll"


class FSIll(MultipleChoice):
    """Fagerström Ill question."""

    name = "fs_ill"
    question = "Fumes-tu aussi quand tu es malade au lit toute la journée?"
    buttons = [
        {"title": "Oui", "payload": "FS_ILL_YES"},
        {"title": "Non", "payload": "FS_ILL_NO"},
    ]
    next = "recruitment.Motivation"


##########################
# END OF FAGERSTROM TEST #
##########################


class Motivation(MultipleChoice):
    """Motivation question."""

    name = "motivation"
    question = (
        "Et la dernière question concerne ta volonté d'arrêter de fumer.\n"
        "Quel est, à ce moment, ton degré de motivation d'arrêter de fumer?"
    )
    buttons = [
        {"title": "Très faible", "payload": "MOTIVATION_VERY_LOW"},
        {"title": "Faible", "payload": "MOTIVATION_LOW"},
        {"title": "Moyen", "payload": "MOTIVATION_MEDIUM"},
        {"title": "Fort", "payload": "MOTIVATION_HIGH"},
        {"title": "Très fort", "payload": "MOTIVATION_VERY_HIGH"},
    ]
    next = "recruitment.Result"


class Result(State):
    """Result state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        with cls.storage(user) as s:
            score = fagerstrom.compute_score(s)
            category = fagerstrom.compute_category(s)
            s["fs_result_score"] = score
            s["fs_result_category"] = category
        page.send(
            user.facebook_id,
            t(
                "Certaines de ces questions font partie du test de Fagerström, qui mesure la dépendance à la nicotine. Selon tes réponses tu es dans la catégorie:\n\n\t→ {category}",
                {"category": t(category)},
            ),
        )
        return Transition.MOVE("recruitment.End")


class End(State):
    """End state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        # page.send(
        #     user.facebook_id,
        #     t(
        #         "Merci d'avoir répondu à ces questions. Dans quelques jours on va suivre ensemble ta consommation de cigarette pour établir ton profil de fumeur! D'ici là reste informé en suivant le groupe privé Facebook, et si l'envie t'en prends, n'hésite pas à partage ton résultat du test de Fagerström sur le groupe pour en discuter avec les autres!"
        #     ),
        # )
        # page.send(user.facebook_id, t("À bientôt! 🤗"))
        # return Transition.STAY
        # page.send(
        #     user.facebook_id,
        #     t(
        #         "Merci d'avoir répondu à ces questions. Dans quelques jours tu "
        #         "vas arrêter de fumer et je serai là quand tu auras besoin d'un "
        #         "coup de pouce. D'ici là reste informé en suivant le groupe "
        #         "privé Facebook. À bientôt! 🤗"
        #     ),
        # )
        page.send(user.facebook_id, t("Merci d'avoir répondu à ces questions."))
        time.sleep(4)
        return Transition.MOVE("cessation.Wait")

    @classmethod
    def on_event(cls, page, user, event):
        return Transition.MOVE("cessation.Wait")
        # t = i18n.translator(user)
        # page.send(
        #     user.facebook_id,
        #     t("Encore un peu de patience! La phase suivante n'a pas encore commencé 😉"),
        # )
        # return Transition.STAY
        # page.send(
        #     user.facebook_id,
        #     t(
        #         "Comme tu n'as pas participé à la phase d'enregistrement des "
        #         "cigarettes, je n'ai pas pu établir ton profil de fumeur! Je "
        #         "serai néanmoins là pour te donner un coup de pouce quand tu "
        #         "en auras besoin lorsque tu arrêteras de fumer. À bientôt! 🤗"
        #     ),
        # )
        # return Transition.MOVE("cessation.Wait")
