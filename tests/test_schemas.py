from app.schemas import RequestAnalysisInput


def test_input_trims_whitespace():
    payload = RequestAnalysisInput(
        subject="  Unterlagen  ",
        message="  Ich habe meine Unterlagen nicht erhalten.  ",
    )
    assert payload.subject == "Unterlagen"
    assert payload.message == "Ich habe meine Unterlagen nicht erhalten."
