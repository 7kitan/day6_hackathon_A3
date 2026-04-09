export type AttractionType = 'temple' | 'museum' | 'park' | 'restaurant' | 'landmark' | 'market' | 'entertainment'

export interface Attraction {
  id: string
  name: string
  type: AttractionType
  coordinates: [number, number] // [lat, lng]
  description: string
  estimatedVisitTime: number // in minutes
  image: string
  rating: number
  distance?: number // calculated from user location
}

export interface Itinerary {
  destinations: Attraction[]
  totalDistance: number // km
  totalTime: number // minutes
  estimatedCost: number // THB
  routes: RouteSegment[]
}

export interface RouteSegment {
  from: Attraction
  to: Attraction
  distance: number // km
  travelTime: number // minutes
  cost: number // THB
}

// Demo location: Hoi An, Vietnam
export const USER_LOCATION: [number, number] = [15.8801, 108.3380]

// Mock attractions data - Now managed by backend
export const ATTRACTIONS: Attraction[] = []

// Calculate distance between two coordinates using Haversine formula
export function calculateDistance(
  coord1: [number, number],
  coord2: [number, number]
): number {
  const R = 6371 // Earth radius in km
  const dLat = toRad(coord2[0] - coord1[0])
  const dLon = toRad(coord2[1] - coord1[1])
  const lat1 = toRad(coord1[0])
  const lat2 = toRad(coord2[0])

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

function toRad(deg: number): number {
  return deg * (Math.PI / 180)
}

// Get attractions within a certain radius
export function getAttractionsWithinRadius(
  userLocation: [number, number],
  radius: number,
  attractions: Attraction[] = ATTRACTIONS
): Attraction[] {
  return attractions
    .map((attraction) => ({
      ...attraction,
      distance: calculateDistance(userLocation, attraction.coordinates)
    }))
    .filter((attraction) => attraction.distance! <= radius)
    .sort((a, b) => a.distance! - b.distance!)
}

// Estimate travel cost using Xanh SM pricing (example: 15,000 VND/km)
export function estimateTravelCost(distanceKm: number): number {
  const ratePerKm = 15000
  return Math.round(distanceKm * ratePerKm)
}

// Estimate travel time (assuming average speed in Bangkok traffic)
export function estimateTravelTime(distanceKm: number): number {
  // Average speed ~15 km/h in Bangkok traffic
  const avgSpeedKmh = 15
  return Math.round((distanceKm / avgSpeedKmh) * 60)
}

// Get type label for display
export function getTypeLabel(type: AttractionType): string {
  const labels: Record<AttractionType, string> = {
    temple: 'Temple',
    museum: 'Museum',
    park: 'Park',
    restaurant: 'Restaurant',
    landmark: 'Landmark',
    market: 'Market',
    entertainment: 'Entertainment'
  }
  return labels[type]
}

// Get type color for markers
export function getTypeColor(type: AttractionType): string {
  const colors: Record<AttractionType, string> = {
    temple: '#E74C3C',
    museum: '#9B59B6',
    park: '#27AE60',
    restaurant: '#F39C12',
    landmark: '#3498DB',
    market: '#E67E22',
    entertainment: '#1ABC9C'
  }
  return colors[type]
}
