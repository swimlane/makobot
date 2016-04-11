def reaction(score):
    if score < 2:
        return 'sunny'
    elif 2 >= score < 3:
        return 'mostly_sunny'
    elif 3 >= score < 4:
        return 'partly_sunny'
    elif 4 >= score < 5:
        return 'barely_sunny'
    elif 5 >= score < 6:
        return 'cloud'
    elif 6 >= score < 7:
        return 'rain_cloud'
    elif 7 >= score < 8:
        return 'thunder_cloud_and_rain'
    elif 8 >= score < 9:
        return 'lightning'
    elif score >= 9:
        return 'tornado'


def risk_level(score):
    if score < 2:
        return 'VERY LOW'
    elif 2 <= score < 3:
        return 'LOW'
    elif 3 <= score < 5:
        return 'MODERATE'
    elif 5 <= score < 8:
        return 'HIGH'
    elif score >= 8:
        return 'VERY HIGH'
    return 'UNKNOWN'
