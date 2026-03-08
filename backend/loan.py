"""Calcul du remboursement et génération du tableau d'amortissement."""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple


def periodic_rate(annual_rate: float, frequency: str) -> float:
    """Convertit un taux annuel (%) en taux périodique (décimal)."""
    freq = frequency.lower()
    if freq == "mensuelle" or freq == "mensuel" or freq == "monthly":
        periods = 12
    elif freq == "trimestrielle" or freq == "trimestriel" or freq == "quarterly":
        periods = 4
    elif freq == "annuelle" or freq == "annuel" or freq == "yearly":
        periods = 1
    else:
        raise ValueError(f"Périodicité inconnue : {frequency}")
    return annual_rate / 100 / periods


def calculate_payment(principal: float, annual_rate: float, periods: int, frequency: str) -> float:
    """Calcule le montant du remboursement périodique (annuité)."""
    r = periodic_rate(annual_rate, frequency)
    if r == 0:
        return principal / periods
    return principal * r / (1 - (1 + r) ** -periods)


def calculate_periods(principal: float, annual_rate: float, payment: float, frequency: str) -> int:
    """Calcule le nombre de périodes nécessaires pour rembourser le prêt."""
    r = periodic_rate(annual_rate, frequency)
    if r == 0:
        return math.ceil(principal / payment)

    # n = -ln(1 - PV*r/P) / ln(1+r)
    numerator = math.log(1 - principal * r / payment)
    denominator = math.log(1 + r)
    n = -numerator / denominator
    return math.ceil(n)


def amortization_schedule(
    principal: float,
    annual_rate: float,
    periods: int,
    frequency: str,
    payment: Optional[float] = None,
) -> Tuple[float, List[Dict[str, float]]]:
    """Génère le tableau d'amortissement et retourne le montant du paiement utilisé.

    Retourne:
        (payment, schedule)

    La variable `schedule` est une liste de lignes contenant :
        - period (int)
        - balance_before
        - interest
        - principal
        - payment
        - balance_after
    """

    if payment is None:
        payment = calculate_payment(principal, annual_rate, periods, frequency)

    r = periodic_rate(annual_rate, frequency)
    balance = principal
    schedule: List[Dict[str, float]] = []

    for period in range(1, periods + 1):
        interest = balance * r
        principal_paid = payment - interest
        # Ajuster pour la période finale afin d'éviter un solde négatif à cause des arrondis.
        if period == periods and abs(balance - principal_paid) > 1e-6:
            principal_paid = balance
            payment = principal_paid + interest

        balance_after = balance - principal_paid
        schedule.append(
            {
                "period": period,
                "balance_before": round(balance, 2),
                "interest": round(interest, 2),
                "principal": round(principal_paid, 2),
                "payment": round(payment, 2),
                "balance_after": round(balance_after, 2),
            }
        )
        balance = balance_after

    return round(payment, 2), schedule


def calculate_missing_value(data: Dict[str, Optional[float]], frequency: str) -> Dict[str, float]:
    """Calcule la valeur manquante parmi : principal, annual_rate, periods, payment."""
    principal = data.get("principal")
    annual_rate = data.get("annual_rate")
    periods = data.get("periods")
    payment = data.get("payment")

    filled: Dict[str, float] = {}

    if principal is None:
        raise ValueError("Le capital (principal) est requis")
    if annual_rate is None:
        raise ValueError("Le taux annuel est requis")

    filled["principal"] = principal
    filled["annual_rate"] = annual_rate

    if periods is None and payment is None:
        raise ValueError("Au moins une des valeurs 'periods' ou 'payment' doit être fournie")

    if periods is None:
        if payment is None:
            raise ValueError("Le montant de la période est requis pour calculer la durée")
        periods = calculate_periods(principal, annual_rate, payment, frequency)

    if payment is None:
        payment = calculate_payment(principal, annual_rate, periods, frequency)

    filled["periods"] = int(periods)
    filled["payment"] = round(payment, 2)

    return filled
