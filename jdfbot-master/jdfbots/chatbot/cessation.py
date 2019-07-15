# -*- coding: utf-8 -*-
"""Cessation chatbot."""

import os
import random
import time
from datetime import datetime

from fbmq import attachment as Attachment

from jdfbots import i18n
from jdfbots.chatbot import State, Transition


class Wait(State):
    """Waiting state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        # return Transition.STAY
        return Transition.MOVE('cessation.Start')

    @classmethod
    def on_event(cls, page, user, event):
        # t = i18n.translator(user)
        # page.send(
        #     user.facebook_id,
        #     t(
        #         "Encore un peu de patience! La phase suivante n'a pas encore "
        #         "commencé 😉"
        #     ),
        # )
        # return Transition.STAY
        return Transition.MOVE('cessation.Start')


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
            t("Salut {name} 🤗 Lorsque tu auras des envies fortes de fumer je serai là pour te donner une aide d'urgence. Tu peux venir vers moi tous les jours de la semaine à n'importe quelle heure du jour ou de la nuit!", {"name": user.first_name}) + "\n\n" + t("Mais n'oublie pas que je suis un robot conversationnel, ce qui veut dire que bien que je puisse t'apporter une aide d'urgence en quelques secondes, je reste limité dans la compréhension du language. Si tu as des questions à poser, ou si tu vois que je ne peux pas t'aider, il faut te tourner vers le groupe Facebook! 🙂"),
        )
        return Transition.MOVE("cessation.Initialize")


class Initialize(State):
    """Initialization state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        group = "helped"
        with cls.storage(user) as s:
            if group not in s:
                s[group] = list()
        return Transition.MOVE("cessation.RequireHelp")


class RequireHelp(State):
    """RequireHelp state."""

    texts = [
        "Rappelle-toi, je suis accessible à n'importe quelle heure du jour ou de la nuit! 😊",
        "En cas d'envie urgente de fumer, appuie sur le bouton! 😊",
    ]
    buttons = [{"title": "HELP 🆘", "payload": "I_NEED_HELP"}]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        sep = "-" * 50 + "\n"
        page.send(
            user.facebook_id, sep + t(random.choice(cls.texts)), quick_replies=i18n.translate_buttons(cls.buttons, lang=user.language)
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        with cls.storage(user) as s:
            s["helped"].append({"start_datetime": datetime.now().isoformat()})
        return Transition.MOVE("cessation.Motivate")


class Motivate(State):
    """Motivate state."""

    texts = [
        "Il est normal d'avoir des envies urgentes de fumer, mais tu peux tenir bon, je suis là pour t'aider!",
        "Dis toi qu'une envie urgente de fumer ne dure que quelques minutes, tu seras encore plus fort après y avoir résisté!",
    ]
    say_it = [
        "Clique sur ce bouton en croyant à ce qu'il dit! 😊",
        "Lis à haute voix le texte du bouton, plusieurs fois si il le faut, et clique dessus! 😊",
    ]
    buttons = [
        {"title": "Je vais résister! 💪", "payload": "I_CAN_DO_IT"},
        {"title": "Je vais tenir! 💪", "payload": "I_CAN_DO_IT"},
        {"title": "Je suis fort(e)! 💪", "payload": "I_CAN_DO_IT"},
        {"title": "Je peux le faire! 💪", "payload": "I_CAN_DO_IT"},
        {"title": "J'y arriverai! 💪", "payload": "I_CAN_DO_IT"},
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        page.send(
            user.facebook_id,
            t(random.choice(cls.texts)) + " " + t(random.choice(cls.say_it)),
            quick_replies=i18n.translate_buttons([random.choice(cls.buttons)], lang=user.language),
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        next_state = random.choice(
            [
                "cessation.ImageMotivator",
                "cessation.ImageMotivator",
                "cessation.QuoteMotivator",
                "cessation.QuoteMotivator",
                "cessation.QuoteMotivator",
                "cessation.AdviceMotivator",
                "cessation.AdviceMotivator",
            ]
        )
        with cls.storage(user) as s:
            s["helped"][-1]["motivate_pressed"] = datetime.now().isoformat()
            s["helped"][-1]["motivator"] = next_state
        return Transition.MOVE(next_state)


class ImageMotivator(State):
    @classmethod
    def on_enter(cls, page, user, prev):
        pictures = os.listdir("static/motivators/" + user.language)
        picture = random.choice(pictures)
        page.send(
            user.facebook_id,
            Attachment.Image(
                os.environ["SERVER_URL"] + "/static/motivators/" + user.language + "/" + picture
            ),
        )
        with cls.storage(user) as s:
            s["helped"][-1]["motivator_content"] = picture
        time.sleep(2)
        return Transition.MOVE("cessation.Distract")


class QuoteMotivator(State):

    quotes = [
        (
            "Il faut la quitter comme un esclave qui se libère. Au début, on est un peu perdu. C’est petit à petit qu'on apprécie de goûter à la délivrance.",
            "",
        ),
        (
            "Un jour, vous pourrez vous dire, ça n’a pas été facile, mais j’ai réussi !",
            "",
        ),
        ("Le succès est la somme des petits efforts, répétés jour après jour.", ""),
        ("Il n’y a pas de réussite facile, ni d’échec définitifs.", "Marcel Proust"),
        ("La volonté peut faire bien des merveilles.", ""),
        (
            "Les buts que vous vous fixez doivent être suffisamment audacieux pour que, dans le processus qui mène à leur réalisation, vous deveniez une personne de grande valeur.",
            "Jim Rohn",
        ),
        (
            "Tout ce que votre esprit peut concevoir et désirer, votre esprit peut le réaliser",
            "Napoleon Hill",
        ),
        ("Jamais jamais jamais. N’abandonnez jamais.", "Winston Churchill"),
        (
            "Le succès n’est pas final, l’échec n’est pas fatal : c’est le courage de continuer qui compte.",
            "Winston Churchill",
        ),
        ("Agissez comme s’il était impossible d’échouer.", "Winston Churchill"),
        (
            "Un pessimiste voit la difficulté dans chaque opportunité, un optimiste voit l’opportunité dans chaque difficulté.",
            "Winston Churchill",
        ),
        (
            "Il est dur d’échouer ; mais il est pire de n’avoir jamais tenté de réussir.",
            "F. D. Roosevelt",
        ),
        (
            "La seule limite à notre épanouissement de demain sera nos doutes d’aujourd’hui.",
            "F. D. Roosevelt",
        ),
        ("La plus grande victoire, c’est la victoire sur soi.", "Platon"),
        (
            "Il ne peut y avoir d’échec pour celui qui continue la lutte.",
            "Napoleon Hill",
        ),
        (
            "La détermination est le facteur le plus important de la réussite.",
            "Lord Chesterfield",
        ),
        (
            "On ne se débarrasse pas d’une habitude en la flanquant par la fenêtre ; il faut lui faire descendre l’escalier marche par marche.",
            "Mark Twain",
        ),
        (
            "La cigarette est l'invention la plus dangereuse de l'histoire de la civilisation.",
            "",
        ),
        (
            "La dépendance à la nicotine est aussi forte que celle à l'héroïne ou à la cocaïne. Cette drogue puissante 'détourne' le cerveau, obligeant les individus à lutter contre leur propre corps",
            "",
        ),
        (
            "L'industrie a réussi à nous faire croire que fumer était une forme de liberté, alors qu'il s'agit en réalité d'une forme d'esclavage.",
            "",
        ),
        (
            "Les bonnes choses de la vie sont la récompense de ceux qui agissent.",
            "Aristote",
        ),
        (
            "Tout ce que vous désirez se trouve juste à l’extérieur de votre zone de confort.",
            "Robert Allen",
        ),
        (
            "Ce qui sauve, c’est de faire un pas et encore un pas.",
            "Antoine de Saint-Exupéry",
        ),
        (
            "Le plus grand secret pour le bonheur, c'est d'être bien avec soi.",
            "Bernard Fontenelle",
        ),
        (
            "La véritable force est celle que nous exerçons à chaque instant  sur nos pensées, nos sentiments, nos actes.",
            "Morikei Ueshiba",
        ),
        ("La joie est en tout, il faut savoir l’extraire.", "Confucius"),
        (
            "Nul ne peut atteindre l’aube sans passer par le chemin de la nuit.",
            "Khalil Gibran",
        ),
        (
            "On ne s’aperçoit pas toujours que l’on parcourt chaque jour un nouveau chemin.",
            "Paulo Coelho",
        ),
        ("Rien de grand n’a été accompli sans enthousiasme.", "Ralph Wando Emerson"),
        (
            "Tous les jours et à tous point de vue, je vais de mieux en mieux.",
            "Emile Coué",
        ),
        ("La vraie grandeur consiste à être maître de soi-même.", "Daniel Defoe"),
        (
            "Quand tu arrives en haut de la montagne, continue de grimper.",
            "proverbe tibétain",
        ),
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        sep = "ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ"
        selected = random.choice(cls.quotes)
        quote = t(selected[0])
        author = selected[1]
        if author:
            text = "{sep}\n\n«{0}»\n\n[{1}]\n\n{sep}".format(quote, author, sep=sep)
        else:
            text = "{sep}\n\n«{0}»\n\n{sep}".format(quote, sep=sep)
        page.send(user.facebook_id, text)
        with cls.storage(user) as s:
            s["helped"][-1]["motivator_content"] = quote
        time.sleep(2)
        return Transition.MOVE("cessation.Distract")


class AdviceMotivator(State):

    advices = [
        "« Je vais en reprendre juste une seule… », dis-toi : « NON, ça risque fortement de me faire rechuter, ça ne me servirait à rien et j’ai déjà tenu bon quelques temps, ce serait dommage de tout remettre en question. »",
        "« C’est trop dur, je ne tiendrai jamais le coup... », dis-toi : « Le plus dur est bientôt passé. J’ai décidé, j’ai décidé, et je ne reviens plus en arrière, à la toux, aux bronchites… ! »",
        "« Je suis devenue insupportable à cause de l’arrêt... », dis-toi : « C’est juste un symptôme normal, ça va passer, je vais redevenir cool, même encore plus qu’avant! »",
        "« Je n’arrive pas à faire face à mes soucis … », dis-toi « La cigarette ne m’aidait pas à résoudre mes soucis. Je suis tout à fait capable de résoudre mes problèmes sans fumer. »",
        "« Ce n’était pas le bon moment pour moi, j’arrêterai plus tard… », dis-toi « Il n’y a jamais de moment idéal. A quoi bon attendre encore? Il y a tout un groupe avec moi là, alors j’en profite et je me motive»",
        "Parle-toi à toi-même: «Si je tiens le coup encore 2 minutes, l'envie aura passé», envoie-toi des messages positifs.",
        "Rappelle-toi pourquoi tu as voulu arrêter de fumer, relis ta liste des raisons et des avantages d’une vie sans tabac.",
        "Rappelle-toi les désagréments de la cigarette (odeur, haleine, fatigue, toux.)",
        "Dites-vous: Je suis plus fort que la cigarette!",
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        sep = "(¯`·._.·(¯`·._.·(¯`·._.··._.·´¯)·._.·´¯)·._.·´¯)"
        advice = t(random.choice(cls.advices))
        keyword = t('Conseil')
        text = "{sep}\n\n{0}:\n\n{1}\n\n{sep}".format(keyword, advice, sep=sep)
        page.send(user.facebook_id, text)
        with cls.storage(user) as s:
            s["helped"][-1]["motivator_content"] = advice
        time.sleep(2)
        return Transition.MOVE("cessation.Distract")


class Distract(State):
    """Distract state."""

    texts = [
        "Pour être sûr que tu ne craques pas, je veux que tu *t'engages* à faire une de ces activités:",
        "Voilà une liste d'activités que tu peux faire pour te distraire de fumer. Je veux que tu en choisisses une et que tu *t'engages* à la réaliser.",
    ]

    choices = [
        ("DISTRACT_WALKING", "Aller faire un petit tour"),
        ("DISTRACT_WATER", "Boire un verre d'eau"),
        ("DISTRACT_TEETH", "Se laver les dents"),
        ("DISTRACT_CHEWING", "Macher un chewing-gum/bâton de réglisse/bonbon"),
        ("DISTRACT_MUSIC", "Écouter un morceau de musique"),
        ("DISTRACT_WEB", "Aller surfer sur internet"),
        ("DISTRACT_TALKING", "Discuter avec un proche/ami/collègue"),
        ("DISTRACT_PHONE", "Appeler un ami/un proche"),
        ("DISTRACT_SHOWER", "Prendre une douche ou un bain"),
        ("DISTRACT_RELAXING", "Faire des exercices de relaxation"),
        ("DISTRACT_PLAYING", "Jouer avec un objet (stylo, bague, …)"),
        ("DISTRACT_GAME", "Jouer à un jeu vidéo/puzzle/énigmes"),
        ("DISTRACT_APPLE", "Manger une pomme"),
        ("DISTRACT_VEGETABLES", "Manger des légumes pré-coupés"),
        ("DISTRACT_MOVE", "Se déplacer dans une pièce où tu ne fumes pas d'habitude"),
        ("DISTRACT_JUICE", "Boire un jus de fruit"),
        ("DISTRACT_EXERCISING", "Faire des exercices d'étirement"),
    ]

    @classmethod
    def to_question(cls, proposed, user, num=5):
        t = i18n.translator(user)
        question = "\n".join(
            ["{}) {}".format(chr(97 + i), t(proposed[i][1])) for i in range(num)]
        )
        question += '\n'
        question += t("Autre) Je m'engage à m'occuper autrement durant 4 minutes")
        return question

    @classmethod
    def to_buttons(cls, proposed, user, num=5):
        buttons = [
            {"title": chr(97 + i), "payload": proposed[i][0]} for i in range(num)
        ]
        other = i18n.translate_buttons([{"title": "Autre", "payload": "DISTRACT_OTHER"}], lang=user.language)
        return buttons + other

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        proposed = random.sample(cls.choices, len(cls.choices))
        with cls.storage(user) as s:
            s["last_proposed"] = proposed
        page.send(
            user.facebook_id,
            t(random.choice(cls.texts)) + "\n\n" + cls.to_question(proposed, user),
            quick_replies=cls.to_buttons(proposed, user),
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        t = i18n.translator(user)
        # Get the response
        response = event.quick_reply_payload
        # If the answer is not valid
        if not response or not response.startswith("DISTRACT_"):
            with cls.storage(user) as s:
                proposed = s["last_proposed"]
            page.send(
                user.facebook_id,
                t("Merci de répondre en utilisant les boutons"),
                quick_replies=cls.to_buttons(proposed, user),
            )
            return Transition.STAY
        # Save it
        with cls.storage(user) as s:
            s["helped"][-1]["distraction"] = response
        if response == "DISTRACT_OTHER":
            return Transition.MOVE("cessation.Other")
        return Transition.MOVE("cessation.Choice")


class Other(State):
    """Other distraction selected state."""

    questions = [
        "Que t'engages-tu donc à faire en quelques mots? Connaître cela me permettra de mieux aider les prochains participants au programme!"
    ]

    thanks = [
        "C'est enregistré, merci. Maintenant occupes tes 4 prochaines minutes pour éviter de craquer. 💪😀"
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        page.send(
            user.facebook_id, t(random.choice(cls.questions)) + t(" (1 message maximum)")
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        t = i18n.translator(user)
        # Get the response
        response = event.message.get("text")
        with cls.storage(user) as s:
            s["helped"][-1]["distraction_other"] = response
        page.send(user.facebook_id, t(random.choice(cls.thanks)))
        time.sleep(2)
        return Transition.MOVE("cessation.Closing")


class Choice(State):
    """Choice state."""

    texts = [
        "Bon choix. Tous les participants du programme sont avec toi, tu peux le faire! 👏",
        "Bravo pour ton engagement! Le temps d'avoir fait cette activité, ton envie de fumer sera passée! 👏",
        "Bonne décision! Chaque cigarette à laquelle tu arrives à renoncer est un pas de plus vers la liberté! 👏",
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        page.send(user.facebook_id, t(random.choice(cls.texts)))
        time.sleep(2)
        return Transition.MOVE("cessation.Closing")


class Closing(State):
    """Closing state."""

    texts = [
        "N'hésites pas à revenir vers moi si tu as besoin d'un autre coup de pouce!\n\nEt si tu sens que mon aide ne te suffit pas, va chercher du soutien sur le groupe, mais surtout ne craques pas!"
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        t = i18n.translator(user)
        page.send(user.facebook_id, t(random.choice(cls.texts)))
        with cls.storage(user) as s:
            s["helped"][-1]["stop_datetime"] = datetime.now().isoformat()
        time.sleep(2)
        return Transition.MOVE("cessation.RequireHelp")


def test_translations():
    """Test translations."""
    from functools import partial
    t = partial(i18n.translate, lang='de')
    tb = partial(i18n.translate_buttons, lang='de')
    # RequireHelp
    for text in RequireHelp.texts:
        print(t(text))
    print(tb(RequireHelp.buttons))
    # Motivate
    for text in Motivate.texts:
        print(t(text))
    for text in Motivate.say_it:
        print(t(text))
    print(tb(Motivate.buttons))
    # QuoteMotivator
    for entry in QuoteMotivator.quotes:
        text, _ = entry
        print(t(text))
    # AdviceMotivator
    for text in AdviceMotivator.advices:
        print(t(text))
    # Distract
    for text in Distract.texts:
        print(t(text))
    for entry in Distract.choices:
        _, text = entry
        print(t(text))
    # Other
    for text in Other.questions:
        print(t(text))
    for text in Other.thanks:
        print(t(text))
    # Choice
    for text in Choice.texts:
        print(t(text))
    # Closing
    for text in Closing.texts:
        print(t(text))


if __name__ == '__main__':
    test_translations()
