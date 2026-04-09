'use client'

import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card } from '@/components/ui/card'
import { type Attraction, getTypeColor, getTypeLabel } from '@/lib/attractions'
import { Star, Clock, MapPin, Plus, Check, X } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAppMode } from './travel-app-content'

interface LocationSheetProps {
  attraction: Attraction | null
  isOpen: boolean
  onClose: () => void
  isSelected: boolean
  onToggleSelect: (attraction: Attraction) => void
}

export default function LocationSheet({
  attraction,
  isOpen,
  onClose,
  isSelected,
  onToggleSelect,
}: LocationSheetProps) {
  const mode = useAppMode()
  const isFramed = mode === 'framed'
  
  if (!attraction || !isOpen) return null

  return (
    <div 
      className={cn(
        "z-50 flex items-end",
        isFramed ? "absolute inset-0" : "fixed inset-0"
      )}
      onClick={onClose}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/40" />
      
      {/* Panel */}
      <Card 
        className={cn(
          "relative w-full rounded-t-2xl border-0 shadow-2xl",
          "animate-in slide-in-from-bottom duration-300",
          !isFramed && "sm:max-w-md sm:mx-auto"
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Handle */}
        <div className="flex justify-center pt-2 pb-1">
          <div className={cn(
            "bg-muted-foreground/30 rounded-full",
            isFramed ? "w-10 h-1" : "w-12 h-1.5"
          )} />
        </div>
        
        {/* Close button */}
        <button 
          onClick={onClose}
          className={cn(
            "absolute top-2 right-2 hover:bg-muted rounded-full transition-colors",
            isFramed ? "p-1.5" : "p-2"
          )}
        >
          <X className={`${isFramed ? 'h-4 w-4' : 'h-5 w-5'} text-muted-foreground`} />
        </button>

        <div className={isFramed ? "px-4 pb-4" : "px-5 pb-5"}>
          {/* Header */}
          <div className={`flex items-center ${isFramed ? 'gap-2 mb-2' : 'gap-3 mb-3'}`}>
            <Badge 
              style={{ backgroundColor: getTypeColor(attraction.type) }}
              className={`text-white ${isFramed ? 'text-xs' : 'text-sm'}`}
            >
              {getTypeLabel(attraction.type)}
            </Badge>
            <div className={`flex items-center text-amber-500 ${isFramed ? 'gap-0.5' : 'gap-1'}`}>
              <Star className={`${isFramed ? 'h-3 w-3' : 'h-4 w-4'} fill-current`} />
              <span className={`font-medium ${isFramed ? 'text-xs' : 'text-sm'}`}>{attraction.rating}</span>
            </div>
          </div>
          
          <h3 className={`font-semibold text-foreground ${isFramed ? 'text-lg mb-1' : 'text-xl mb-2'}`}>{attraction.name}</h3>
          <p className={cn(
            "text-muted-foreground line-clamp-2",
            isFramed ? "text-xs mb-3" : "text-sm mb-4"
          )}>
            {attraction.description}
          </p>

          {/* Stats */}
          <div className={`flex ${isFramed ? 'gap-4 mb-3' : 'gap-6 mb-4'}`}>
            <div className={`flex items-center ${isFramed ? 'gap-1.5' : 'gap-2'}`}>
              <div className={cn(
                "rounded-full bg-primary/10 flex items-center justify-center",
                isFramed ? "w-7 h-7" : "w-9 h-9"
              )}>
                <MapPin className={`${isFramed ? 'h-3.5 w-3.5' : 'h-4 w-4'} text-primary`} />
              </div>
              <div>
                <p className={`text-muted-foreground ${isFramed ? 'text-[10px]' : 'text-xs'}`}>Distance</p>
                <p className={`font-semibold ${isFramed ? 'text-xs' : 'text-sm'}`}>{attraction.distance?.toFixed(1)} km</p>
              </div>
            </div>
            <div className={`flex items-center ${isFramed ? 'gap-1.5' : 'gap-2'}`}>
              <div className={cn(
                "rounded-full bg-accent/20 flex items-center justify-center",
                isFramed ? "w-7 h-7" : "w-9 h-9"
              )}>
                <Clock className={`${isFramed ? 'h-3.5 w-3.5' : 'h-4 w-4'} text-accent-foreground`} />
              </div>
              <div>
                <p className={`text-muted-foreground ${isFramed ? 'text-[10px]' : 'text-xs'}`}>Visit Time</p>
                <p className={`font-semibold ${isFramed ? 'text-xs' : 'text-sm'}`}>{attraction.estimatedVisitTime} min</p>
              </div>
            </div>
          </div>

          {/* Image placeholder */}
          <div className={cn(
            "w-full rounded-lg bg-muted flex items-center justify-center",
            isFramed ? "h-20 mb-3" : "h-28 mb-4"
          )}>
            <span className={`text-muted-foreground ${isFramed ? 'text-xs' : 'text-sm'}`}>Photo of {attraction.name}</span>
          </div>

          {/* Action buttons */}
          <div className="flex gap-2">
            <Button 
              className={`flex-1 ${isFramed ? 'h-9 text-sm' : 'h-11 text-base'}`}
              variant={isSelected ? "secondary" : "default"}
              onClick={() => {
                onToggleSelect(attraction)
                onClose()
              }}
            >
              {isSelected ? (
                <>
                  <Check className={`${isFramed ? 'h-3.5 w-3.5 mr-1.5' : 'h-4 w-4 mr-2'}`} />
                  Added
                </>
              ) : (
                <>
                  <Plus className={`${isFramed ? 'h-3.5 w-3.5 mr-1.5' : 'h-4 w-4 mr-2'}`} />
                  Add to Trip
                </>
              )}
            </Button>
            <Button variant="outline" onClick={onClose} className={isFramed ? "h-9 text-sm" : "h-11 text-base"}>
              Close
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}
