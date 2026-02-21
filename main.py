def filter_colors(image):

    # Split BGR channels
    b, g, r = cv2.split(image)

    # --- ORANGE (HSV) ---
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([8, 120, 120])
    upper_orange = np.array([25, 255, 255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # --- MAGENTA (BGR logic) ---
    # Magenta ≈ high R + high B + low G
    mask_magenta = (
        (r > 150) &
        (b > 150) &
        (g < 120)
    )

    # White canvas
    result = np.ones_like(image) * 255

    # Orange → Black
    result[mask_orange > 0] = [0, 0, 0]

    # Magenta → Gray
    result[mask_magenta] = [140, 140, 140]

    return result
