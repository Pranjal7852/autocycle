import React from "react";
import { Link } from "react-router-dom";

const BrandMatchCard = ({
  brand,
  selectUrl,
  brandPlacement,
  sustainabilityPlacement,
  productAssumptions,
  matchValue,
  combinedReach,
  annualVolume,
}) => (
  <div className="relative flex flex-col md:flex-row w-full max-w-4xl min-h-[420px] border border-black mx-auto mt-10 mb-14 bg-white">
    {/* Select Button */}
    <Link
      to={selectUrl}
      className="absolute -right-5 -top-6 z-10 bg-black text-white text-3xl md:text-2xl font-light px-8 py-2 flex items-center gap-2"
      style={{ borderTop: "1px solid black", borderRight: "1px solid black" }}
    >
      Select
      <svg width="28" height="28" viewBox="0 0 28 28" className="ml-1">
        <path d="M8 20L20 8M20 8H9M20 8V19" stroke="white" strokeWidth="2"/>
      </svg>
    </Link>

    {/* Card Content */}
    <div className="flex-1 px-8 pt-10 pl-[280px] pb-10 flex-col">
      {/* Brand Placement */}
      <div>
        <div className="uppercase font-bold text-sm tracking-wider text-gray-400 mb-1">
          Brand Placement
        </div>
        <div className="text-lg font-normal text-black leading-snug">
          {brandPlacement}
        </div>
      </div>
      {/* Sustainability Placement */}
      <div>
        <div className="uppercase font-bold text-sm tracking-wider text-gray-400 mb-1">
          Sustainability Placement
        </div>
        <div className="text-lg font-normal text-black leading-snug">
          {sustainabilityPlacement}
        </div>
      </div>
      {/* Product Assumptions */}
      <div>
        <div className="uppercase font-bold text-sm tracking-wider text-gray-400 mb-1">
          Product Assumptions
        </div>
        <div className="text-lg font-normal text-black leading-snug">
          {productAssumptions}
        </div>
      </div>
      {/* Stats */}
      <div className="flex gap-10 md:gap-12 mt-4 flex-wrap">
        <div>
          <div className="uppercase text-xs font-extrabold text-gray-400 tracking-wider mb-1">
            Match Value
          </div>
          <div className="text-lg text-black">{matchValue}</div>
        </div>
        <div>
          <div className="uppercase text-xs font-extrabold text-gray-400 tracking-wider mb-1">
            Combined Reach
          </div>
          <div className="text-lg text-black">{combinedReach}</div>
        </div>
        <div>
          <div className="uppercase text-xs font-extrabold text-gray-400 tracking-wider mb-1">
            Annual Plastic Volume
          </div>
          <div className="text-lg text-black">{annualVolume}</div>
        </div>
      </div>
    </div>

    {/* Brand Name, Bottom Left */}
    <div className="absolute -left-5 -bottom-5 bg-white">
      <span className="text-[72px] md:text-[120px] font-extrabold uppercase leading-none tracking-wide text-black md:mb-0 mb-[-1em]">
        {brand}
      </span>
    </div>
  </div>
);
export default BrandMatchCard;
