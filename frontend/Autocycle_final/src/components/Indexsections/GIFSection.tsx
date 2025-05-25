import React from "react";
import { Link } from "react-router-dom";

const HeroSection: React.FC = () => {
  return (
      <div className= "flex full-width border-2 border-green-600">
        <div className="flex w-[50%] mx-auto px-4 py-16 border-2 border-green-600">
                <img
                  src="/gifs/rotating.gif"
                  alt="AutoCycle collaboration showcase"
                  className="w-full h-auto object-cover"
                />
              </div>
      </div>
    )
};

export default HeroSection;