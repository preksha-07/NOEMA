from core.pipeline import run_pipeline


# =====================================================
# SIMPLE BACKEND API
# =====================================================

def process_image(
    image_path,
    mode="balanced",
    risk_weight=1.0
):

    result = run_pipeline(
        image_path,
        mode,
        risk_weight
    )

    return result