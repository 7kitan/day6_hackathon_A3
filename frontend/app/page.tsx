'use client'

import IPhoneFrame from '@/components/iphone-frame'
import TravelAppContent from '@/components/travel-app-content'

export default function DemoPage() {
  return (
    <>
      {/* Mobile: Show app directly (fullscreen) */}
      <div className="md:hidden h-screen w-screen">
        <TravelAppContent mode="fullscreen" />
      </div>

      {/* Desktop: Show iPhone frame demo */}
      <div className="hidden md:flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex-col items-center justify-center p-8">
        {/* Demo header */}
        <div className="text-center mb-8 max-w-2xl">
          <h1 className="text-3xl font-bold text-white mb-3">
            Travel Itinerary Feature
          </h1>
          <p className="text-slate-400 text-lg">
            An AI-powered travel planning feature for ride-hailing apps. Explore nearby attractions, 
            chat with the AI assistant, and build personalized itineraries.
          </p>
        </div>

        {/* iPhone demo */}
        <IPhoneFrame>
          <TravelAppContent mode="framed" />
        </IPhoneFrame>

        {/* Feature highlights */}
        <div className="mt-8 flex flex-wrap justify-center gap-4 max-w-2xl">
          <FeatureTag>Interactive Map</FeatureTag>
          <FeatureTag>AI Travel Assistant</FeatureTag>
          <FeatureTag>Smart Itinerary Builder</FeatureTag>
          <FeatureTag>Cost Estimation</FeatureTag>
          <FeatureTag>Radius Search</FeatureTag>
        </div>

        {/* Instructions */}
        <div className="mt-6 text-center text-slate-500 text-sm max-w-md">
          <p>
            Tap markers on the map to select destinations. Click the chat bubble 
            in the corner to interact with the AI travel assistant.
          </p>
        </div>
      </div>
    </>
  )
}

function FeatureTag({ children }: { children: React.ReactNode }) {
  return (
    <span className="px-3 py-1.5 bg-white/10 text-white/80 rounded-full text-sm font-medium backdrop-blur-sm border border-white/10">
      {children}
    </span>
  )
}
