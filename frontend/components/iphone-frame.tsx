'use client'

import { ReactNode } from 'react'

interface IPhoneFrameProps {
  children: ReactNode
}

export default function IPhoneFrame({ children }: IPhoneFrameProps) {
  return (
    <div className="relative mx-auto">
      {/* iPhone 15 Pro frame */}
      <div className="relative w-[375px] h-[812px] bg-[#1a1a1a] rounded-[55px] p-[14px] shadow-2xl">
        {/* Side buttons - left */}
        <div className="absolute -left-[3px] top-[120px] w-[3px] h-[30px] bg-[#2a2a2a] rounded-l-sm" />
        <div className="absolute -left-[3px] top-[170px] w-[3px] h-[60px] bg-[#2a2a2a] rounded-l-sm" />
        <div className="absolute -left-[3px] top-[240px] w-[3px] h-[60px] bg-[#2a2a2a] rounded-l-sm" />
        
        {/* Side button - right */}
        <div className="absolute -right-[3px] top-[180px] w-[3px] h-[80px] bg-[#2a2a2a] rounded-r-sm" />
        
        {/* Inner bezel */}
        <div className="relative w-full h-full bg-[#0a0a0a] rounded-[41px] overflow-hidden">
          {/* Screen content */}
          <div className="relative w-full h-full bg-background overflow-hidden">
            {/* Dynamic Island */}
            <div className="absolute top-0 left-0 right-0 z-50 flex justify-center pt-[10px] pointer-events-none">
              <div className="w-[126px] h-[37px] bg-black rounded-[20px] flex items-center justify-center">
                {/* Camera dot */}
                <div className="absolute right-[26px] w-[12px] h-[12px] rounded-full bg-[#1a1a1a] flex items-center justify-center">
                  <div className="w-[4px] h-[4px] rounded-full bg-[#2d4a5e]" />
                </div>
              </div>
            </div>
            
            {/* App content with safe area padding */}
            <div className="w-full h-full pt-[47px] pb-[34px]">
              {children}
            </div>
            
            {/* Home indicator */}
            <div className="absolute bottom-[8px] left-1/2 -translate-x-1/2 w-[134px] h-[5px] bg-foreground/30 rounded-full z-50" />
          </div>
        </div>
      </div>
    </div>
  )
}
