def filter_colors(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # -------- ORANGE (ELEMENTS) ----------
    lower_orange = np.array([8, 120, 120])
    upper_orange = np.array([25, 255, 255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # -------- MAGENTA (GRID) -------------
    lower_magenta = np.array([135, 80, 80])
    upper_magenta = np.array([170, 255, 255])
    mask_magenta = cv2.inRange(hsv, lower_magenta, upper_magenta)

    # White canvas
    result = np.ones_like(image) * 255

    # Orange → Black
    result[mask_orange > 0] = [0, 0, 0]

    # Magenta → Gray
    result[mask_magenta > 0] = [140, 140, 140]

    return result
