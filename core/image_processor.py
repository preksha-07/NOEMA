import cv2
import matplotlib.pyplot as plt


# =====================================================
# LOAD IMAGE + EDGE DETECTION
# =====================================================

def load_and_detect_edges(image_path):

    # -----------------------------
    # 1. Load image
    # -----------------------------
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found!")

    # -----------------------------
    # 2. Convert to grayscale
    # -----------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # 3. Edge detection
    # -----------------------------
    edges = cv2.Canny(gray, 100, 200)

    return image, gray, edges


# =====================================================
# SHOW RESULTS
# =====================================================

def show_results(image, gray, edges):

    plt.figure(figsize=(12, 4))

    # Original image
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original")

    # Grayscale
    plt.subplot(1, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title("Grayscale")

    # Edges
    plt.subplot(1, 3, 3)
    plt.imshow(edges, cmap='gray')
    plt.title("Edges")

    plt.show()


# =====================================================
# EXTRACT POINTS FROM EDGES
# =====================================================

def extract_points_from_edges(edges, max_points=300):

    # -----------------------------------
    # Find contours
    # -----------------------------------
    result = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    contours = result[0] if len(result) == 2 else result[1]

    all_points = []

    # -----------------------------------
    # Process each contour separately
    # -----------------------------------
    for contour in contours:

        contour_points = []

        for p in contour:

            x, y = p[0]

            contour_points.append((int(x), int(y)))

        # -----------------------------------
        # Reduce points INSIDE contour
        # -----------------------------------
        if len(contour_points) > 0:

            step = max(1, len(contour_points) // 100)

            contour_points = contour_points[::step]

        # -----------------------------------
        # Add contour in ORDER
        # -----------------------------------
        all_points.extend(contour_points)

    # -----------------------------------
    # Final reduction
    # -----------------------------------
    if len(all_points) > max_points:

        step = max(1, len(all_points) // max_points)

        all_points = all_points[::step]

    # =====================================================
    # REMOVE DUPLICATE POINTS
    # =====================================================

    filtered_points = []

    for p in all_points:

        if p not in filtered_points:

            filtered_points.append(p)

    all_points = filtered_points

    return all_points
