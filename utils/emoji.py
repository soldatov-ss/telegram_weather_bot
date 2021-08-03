def translate(descr):
    emoji = {
        'Thunderstorm': ['Гроза', '⛈'], 'Drizzle': ['Моросящий дождь', '🌧'], 'Rain': ['Дождь', '🌧'],
        'Snow': ['Снег', '🌨'], 'Atmosphere': ['Туман', '🌫'], 'Clear': ['Солнечно', '☀'], 'Clouds': ['Облачно', '☁']
    }
    return emoji[descr]
