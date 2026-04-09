import math
from typing import List, Tuple, Dict, Any

# Demo location: Hoi An, Vietnam
USER_LOCATION = (15.8801, 108.3380)

def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) using Haversine formula.
    Returns distance in kilometers.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Radius of the Earth in kilometers
    R = 6371.0
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0)**2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

ATTRACTIONS = [
    # 🏛 Sightseeing
    {
        "id": "h1",
        "name": "Phố cổ Hội An",
        "type": "landmark",
        "coordinates": (15.8770, 108.3275),
        "description": "A well-preserved example of a Southeast Asian trading port dating from the 15th to the 19th century.",
        "estimatedVisitTime": 180,
        "image": "/images/hoi-an-old-town.jpg",
        "rating": 4.8
    },
    {
        "id": "h2",
        "name": "Chùa Cầu",
        "type": "landmark",
        "coordinates": (15.8771, 108.3259),
        "description": "Iconic 18th-century Japanese-style covered bridge with a small temple inside.",
        "estimatedVisitTime": 30,
        "image": "/images/japanese-bridge.jpg",
        "rating": 4.7
    },
    {
        "id": "h3",
        "name": "Nhà cổ Tấn Ký",
        "type": "museum",
        "coordinates": (15.8775, 108.3282),
        "description": "Traditional 18th-century merchant house showcasing a blend of Japanese, Chinese, and Vietnamese architecture.",
        "estimatedVisitTime": 45,
        "image": "/images/tan-ky-house.jpg",
        "rating": 4.6
    },
    {
        "id": "h4",
        "name": "Hội quán Phúc Kiến",
        "type": "temple",
        "coordinates": (15.8778, 108.3305),
        "description": "Stunning assembly hall built by Chinese merchants from Fujian in the 17th century.",
        "estimatedVisitTime": 60,
        "image": "/images/fujian-hall.jpg",
        "rating": 4.6
    },
    {
        "id": "h5",
        "name": "Chợ Hội An",
        "type": "market",
        "coordinates": (15.8780, 108.3320),
        "description": "Vibrant local market offering street food, fresh produce, and traditional souvenirs.",
        "estimatedVisitTime": 90,
        "image": "/images/hoi-an-market.jpg",
        "rating": 4.5
    },

    # 🍜 Food
    {
        "id": "f1",
        "name": "Bánh mì Phượng",
        "type": "restaurant",
        "coordinates": (15.8785, 108.3335),
        "description": "One of the most famous Banh Mi spots in Vietnam, immortalized by Anthony Bourdain.",
        "estimatedVisitTime": 45,
        "image": "/images/banh-mi-phuong.jpg",
        "rating": 4.7
    },
    {
        "id": "f2",
        "name": "Cao lầu Thanh",
        "type": "restaurant",
        "coordinates": (15.8800, 108.3350),
        "description": "Local favorite for the iconic Hoi An noodle dish, Cao Lau.",
        "estimatedVisitTime": 45,
        "image": "/images/cao-lau-thanh.jpg",
        "rating": 4.6
    },
    {
        "id": "f3",
        "name": "Morning Glory Restaurant",
        "type": "restaurant",
        "coordinates": (15.8772, 108.3315),
        "description": "Upscale restaurant serve classic central Vietnamese dishes in a refined setting.",
        "estimatedVisitTime": 90,
        "image": "/images/morning-glory.jpg",
        "rating": 4.7
    },
    {
        "id": "f4",
        "name": "Bale Well",
        "type": "restaurant",
        "coordinates": (15.8810, 108.3365),
        "description": "Famous for its set menu of grilled pork skewers (Nem Nurong) and crispy pancakes.",
        "estimatedVisitTime": 60,
        "image": "/images/bale-well.jpg",
        "rating": 4.5
    },
    {
        "id": "f5",
        "name": "Madam Khanh",
        "type": "restaurant",
        "coordinates": (15.8795, 108.3340),
        "description": "The Banh Mi Queen. A strong contender for the best sandwich in Hoi An.",
        "estimatedVisitTime": 30,
        "image": "/images/madam-khanh.jpg",
        "rating": 4.6
    },

    # ☕ Cafe
    {
        "id": "c1",
        "name": "Faifo Coffee",
        "type": "entertainment",
        "coordinates": (15.8774, 108.3298),
        "description": "Famous rooftop cafe with one of the best views over the yellow walls of Hoi An Old Town.",
        "estimatedVisitTime": 60,
        "image": "/images/faifo-coffee.jpg",
        "rating": 4.6
    },
    {
        "id": "c2",
        "name": "The Chef Cafe",
        "type": "entertainment",
        "coordinates": (15.8776, 108.3295),
        "description": "Rooftop coffee shop providing great street views and a peaceful atmosphere.",
        "estimatedVisitTime": 60,
        "image": "/images/the-chef.jpg",
        "rating": 4.5
    },

    # 🌿 Chill
    {
        "id": "ch1",
        "name": "Biển An Bàng",
        "type": "park",
        "coordinates": (15.9125, 108.3685),
        "description": "One of the best beaches in Asia, known for its soft sand and great local food.",
        "estimatedVisitTime": 150,
        "image": "/images/an-bang-beach.jpg",
        "rating": 4.7
    },
    {
        "id": "ch2",
        "name": "Roving Chillhouse",
        "type": "entertainment",
        "coordinates": (15.8950, 108.3550),
        "description": "Unique cafe located right in the middle of a rice field. Perfect for catching the sunset.",
        "estimatedVisitTime": 90,
        "image": "/images/roving-chillhouse.jpg",
        "rating": 4.8
    },

    # 🎯 Activity
    {
        "id": "a1",
        "name": "Rừng dừa Bảy Mẫu",
        "type": "entertainment",
        "coordinates": (15.8550, 108.3650),
        "description": "Cultural experience riding in traditional bamboo basket boats through water coconut forests.",
        "estimatedVisitTime": 120,
        "image": "/images/coconut-forest.jpg",
        "rating": 4.6
    },
    {
        "id": "a2",
        "name": "Làng gốm Thanh Hà",
        "type": "museum",
        "coordinates": (15.8720, 108.3050),
        "description": "Traditional pottery village where you can try your hand at making ceramics.",
        "estimatedVisitTime": 90,
        "image": "/images/thanh-ha-pottery.jpg",
        "rating": 4.5
    },
    {
        "id": "a3",
        "name": "Làng rau Trà Quế",
        "type": "park",
        "coordinates": (15.9000, 108.3450),
        "description": "Small organic farming village specializing in high-quality herbs and vegetables.",
        "estimatedVisitTime": 120,
        "image": "/images/tra-que-village.jpg",
        "rating": 4.7
    },
    {
        "id": "a4",
        "name": "Đi thuyền sông Hoài",
        "type": "entertainment",
        "coordinates": (15.8765, 108.3280),
        "description": "Romantic evening boat ride on the river, releasing paper lanterns for good luck.",
        "estimatedVisitTime": 30,
        "image": "/images/hoai-river-boat.jpg",
        "rating": 4.7
    }
]
