'use client'

import { useEffect, useRef, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap, Polyline } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { type Attraction, type Itinerary, USER_LOCATION, getTypeColor, getTypeLabel } from '@/lib/attractions'
import { Button } from '@/components/ui/button'
import { Star, Clock, MapPin } from 'lucide-react'

// Fix for default markers in Next.js
const createCustomIcon = (type: Attraction['type']) => {
  const color = getTypeColor(type)
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 32px;
        height: 32px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 2px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
      ">
        <div style="
          transform: rotate(45deg);
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 14px;
        "></div>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
  })
}

const userIcon = L.divIcon({
  className: 'user-marker',
  html: `
    <div style="
      background-color: #00A86B;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 4px solid white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    "></div>
  `,
  iconSize: [20, 20],
  iconAnchor: [10, 10],
})

// Component to fit bounds when itinerary changes
function FitBoundsToItinerary({ itinerary }: { itinerary: Itinerary | null }) {
  const map = useMap()
  
  useEffect(() => {
    if (itinerary && itinerary.destinations.length > 0) {
      const bounds = L.latLngBounds(
        itinerary.destinations.map(d => d.coordinates)
      )
      bounds.extend(USER_LOCATION)
      map.fitBounds(bounds, { padding: [50, 50] })
    }
  }, [itinerary, map])
  
  return null
}

interface MapViewProps {
  attractions: Attraction[]
  radius: number
  selectedAttractions: Attraction[]
  itinerary: Itinerary | null
  onAttractionSelect: (attraction: Attraction) => void
  onAttractionDetails: (attraction: Attraction) => void
}

export default function MapView({
  attractions,
  radius,
  selectedAttractions,
  itinerary,
  onAttractionSelect,
  onAttractionDetails,
}: MapViewProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className="h-full w-full flex items-center justify-center bg-muted">
        <div className="text-muted-foreground">Loading map...</div>
      </div>
    )
  }

  const isSelected = (attraction: Attraction) => 
    selectedAttractions.some(a => a.id === attraction.id)

  // Generate route polyline from itinerary
  const routeCoordinates = itinerary 
    ? [USER_LOCATION, ...itinerary.destinations.map(d => d.coordinates)]
    : []

  return (
    <MapContainer
      center={USER_LOCATION}
      zoom={13}
      className="h-full w-full z-0"
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {/* User location marker */}
      <Marker position={USER_LOCATION} icon={userIcon}>
        <Popup>
          <div className="text-center font-medium">Your Location</div>
        </Popup>
      </Marker>
      
      {/* Radius circle */}
      <Circle
        center={USER_LOCATION}
        radius={radius * 1000}
        pathOptions={{
          color: '#00A86B',
          fillColor: '#00A86B',
          fillOpacity: 0.1,
          weight: 2,
          dashArray: '5, 5',
        }}
      />
      
      {/* Attraction markers */}
      {attractions.map((attraction) => (
        <Marker
          key={attraction.id}
          position={attraction.coordinates}
          icon={createCustomIcon(attraction.type)}
        >
          <Popup className="attraction-popup" minWidth={250}>
            <div className="p-1">
              <div className="flex items-center gap-2 mb-2">
                <span 
                  className="px-2 py-0.5 rounded-full text-xs text-white"
                  style={{ backgroundColor: getTypeColor(attraction.type) }}
                >
                  {getTypeLabel(attraction.type)}
                </span>
                <div className="flex items-center gap-1 text-amber-500">
                  <Star className="h-3 w-3 fill-current" />
                  <span className="text-xs">{attraction.rating}</span>
                </div>
              </div>
              <h3 className="font-semibold text-foreground mb-1">{attraction.name}</h3>
              <p className="text-xs text-muted-foreground mb-2 line-clamp-2">
                {attraction.description}
              </p>
              <div className="flex items-center gap-3 text-xs text-muted-foreground mb-3">
                <div className="flex items-center gap-1">
                  <MapPin className="h-3 w-3" />
                  <span>{attraction.distance?.toFixed(1)} km</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  <span>{attraction.estimatedVisitTime} min</span>
                </div>
              </div>
              <div className="flex gap-2">
                <Button 
                  size="sm" 
                  variant={isSelected(attraction) ? "secondary" : "default"}
                  className="flex-1 h-8 text-xs"
                  onClick={() => onAttractionSelect(attraction)}
                >
                  {isSelected(attraction) ? 'Selected' : 'Add to Trip'}
                </Button>
                <Button 
                  size="sm" 
                  variant="outline"
                  className="h-8 text-xs"
                  onClick={() => onAttractionDetails(attraction)}
                >
                  Details
                </Button>
              </div>
            </div>
          </Popup>
        </Marker>
      ))}
      
      {/* Route polyline */}
      {routeCoordinates.length > 1 && (
        <Polyline
          positions={routeCoordinates}
          pathOptions={{
            color: '#00A86B',
            weight: 4,
            opacity: 0.8,
          }}
        />
      )}
      
      <FitBoundsToItinerary itinerary={itinerary} />
    </MapContainer>
  )
}
