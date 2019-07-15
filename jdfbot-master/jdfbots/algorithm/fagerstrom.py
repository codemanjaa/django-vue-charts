# -*- coding: utf-8 -*-
"""Algorithm for computing Fagerström score."""


def compute_category(data):
    """Compute the category from the user data."""
    score = compute_score(data)
    return _score_to_category(score)


def compute_score(data):
    """Compute the score from the user data."""
    score = 0
    # Delay
    score += {"FS_DELAY_5-": 3,
              "FS_DELAY_6_30": 2,
              "FS_DELAY_31_60": 1,
              "FS_DELAY_60+": 0, }.get(data['fs_delay'], 1.5)
    # Forbidden
    score += {"FS_FORBIDDEN_YES": 1,
              "FS_FORBIDDEN_NO": 0, }.get(data['fs_forbidden'], 0.5)
    # Difficult
    score += {"FS_DIFFICULT_FIRST": 1,
              "FS_DIFFICULT_OTHER": 0}.get(data['fs_difficult'], 0.5)
    # Count
    score += {"FS_COUNT_1_10": 0,
              "FS_COUNT_11_20": 1,
              "FS_COUNT_21_30": 2,
              "FS_COUNT_30+": 3, }.get(data['fs_count'], 1.5)
    # Rhythm
    score += {"FS_RHYTHM_YES": 1,
              "FS_RHYTHM_NO": 0, }.get(data['fs_rhythm'], 0.5)
    # Ill
    score += {"FS_ILL_YES": 1,
              "FS_ILL_NO": 0, }.get(data['fs_ill'], 0.5)
    return score


def _score_to_category(score):
    """Transform the score value to the category name."""
    if score < 3:
        return "Très faible dépendance à la nicotine"
    elif 3 <= score < 5:
        return "Faible dépendance à la nicotine"
    elif 5 <= score < 7:
        return "Dépendance moyenne à la nicotine"
    elif 7 <= score < 9:
        return "Forte dépendance à la nicotine"
    elif 9 <= score:
        return "Très forte dépendance à la nicotine"
    return "Erreur, la catégorie n'a pas pu être définie"
