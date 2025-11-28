import math


def sanitize_metrics(metrics: dict):
    """
    Cleans numeric fields safely:
    - Ensures floats
    - Replaces None / NaN / infinite values
    - Leaves text or structured values unchanged
    """

    cleaned = {}

    for k, v in metrics.items():

        # None -> 0
        if v is None:
            cleaned[k] = 0
            continue

        # Numeric handling
        if isinstance(v, (int, float)):
            if math.isnan(v) or math.isinf(v):
                cleaned[k] = 0
            else:
                cleaned[k] = round(float(v), 3)
            continue

        # String that might be numeric
        if isinstance(v, str):
            try:
                num = float(v)
                if math.isnan(num) or math.isinf(num):
                    cleaned[k] = 0
                else:
                    cleaned[k] = round(num, 3)
            except:
                cleaned[k] = v
            continue

        # Dict/List: leave intact
        if isinstance(v, (dict, list)):
            cleaned[k] = v
            continue

        # Fallback
        cleaned[k] = v

    return cleaned
