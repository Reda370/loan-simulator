"""Backend Flask pour calculer les emprunts et générer le tableau d'amortissement."""

from __future__ import annotations

from flask import Flask, jsonify, request
from flask_cors import CORS

from loan import amortization_schedule, calculate_missing_value


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.route("/api/calculate", methods=["POST"])
    def calculate() -> tuple[dict, int]:
        payload = request.get_json(force=True)
        if not payload:
            return {"error": "Aucune donnée reçue"}, 400

        try:
            frequency = payload.get("frequency", "mensuelle")
            if frequency not in {"mensuelle", "trimestrielle", "annuelle"}:
                return {"error": "Périodicité invalide"}, 400

            data = {
                "principal": payload.get("principal"),
                "annual_rate": payload.get("annual_rate"),
                "periods": payload.get("periods"),
                "payment": payload.get("payment"),
            }

            filled = calculate_missing_value(data, frequency)

            periods = int(filled["periods"])
            payment = float(filled["payment"])
            principal = float(filled["principal"])
            annual_rate = float(filled["annual_rate"])

            computed_payment, schedule = amortization_schedule(
                principal=principal,
                annual_rate=annual_rate,
                periods=periods,
                frequency=frequency,
                payment=payment,
            )

            response = {
                "input": {
                    "principal": principal,
                    "annual_rate": annual_rate,
                    "periods": periods,
                    "payment": computed_payment,
                    "frequency": frequency,
                },
                "result": {
                    "duration_periods": periods,
                    "payment": computed_payment,
                },
                "schedule": schedule,
            }
            return jsonify(response), 200

        except Exception as exc:
            return {"error": str(exc)}, 400

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
