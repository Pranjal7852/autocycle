import React from "react";
import { Link } from "react-router-dom";
import { useGenerateProducts } from "@/hooks/useGenerateProducts";

interface BrandMatchCardProps {
  brand: string;
  selectUrl: string;
  brandPlacement: string;
  sustainabilityPlacement: string;
  productAssumptions: string;
  estimatedImpact: string;
  combinedReach: string;
  confidenceScore: string;
  logoUrl: string;
  companyDomain: string;
  inputResponse: {
    sourceBrand: string;
    location: string;
    plasticType: string;
  };
  onProductsGenerated?: (response: any) => void;
}

const BrandMatchCard: React.FC<BrandMatchCardProps> = ({
  brand,
  selectUrl,
  brandPlacement,
  sustainabilityPlacement,
  productAssumptions,
  estimatedImpact,
  combinedReach,
  confidenceScore,
  logoUrl,
  companyDomain,
  inputResponse,
  onProductsGenerated,
}) => {
  const { isLoading, error, submit } = useGenerateProducts();

  const handleSelect = async () => {
    try {
      const response = await submit({
        source_brand: inputResponse.sourceBrand,
        plastic_type: inputResponse.plasticType,
        location: inputResponse.location,
        target_brand: brand,
      });

      if (onProductsGenerated) {
        onProductsGenerated(response);
      }

      // You can also navigate or perform other actions here
      // window.location.href = selectUrl; // if you still want to navigate
    } catch (err) {
      console.error('Error generating products:', err);
      // Handle error as needed
    }
  };

  return (
    <div className="relative flex w-full max-w-4xl min-h-[490px] border border-black mx-auto mt-10 mb-14 bg-white">
      {/* Select Button */}
      <button
        onClick={handleSelect}
        disabled={isLoading}
        className={`absolute -right-5 -top-6 z-10 bg-black text-white text-3xl md:text-2xl font-light px-8 py-2 flex items-center gap-2 ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-800'
          }`}
        style={{ borderTop: "1px solid black", borderRight: "1px solid black" }}
      >
        {isLoading ? 'Loading...' : 'Select'}
        {!isLoading && (
          <svg width="28" height="28" viewBox="0 0 28 28" className="ml-1">
            <path d="M8 20L20 8M20 8H9M20 8V19" stroke="white" strokeWidth="2" />
          </svg>
        )}
      </button>

      {/* Left Side - Image and Brand Name */}
      <div className="flex flex-col justify-between w-80 relative">
        {/* Brand Logo and Domain */}
        <div className="p-8 pb-4">
          {logoUrl && (
            <img src={logoUrl} alt={`${brand} logo`} className="h-[100%] w-auto mb-4" />
          )}
         
        </div>

        {/* Brand Name, Bottom Left */}
        <div className="absolute -left-10 -bottom-5 bg-white">
          <a
            href={`https://${companyDomain}`}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline"
          >
            <span className="text-[72px] md:text-[120px] font-extrabold uppercase leading-none tracking-wide text-black whitespace-nowrap">
              {brand}
            </span>
          </a>
        </div>
      </div>

      {/* Right Side - Content */}
      <div className="flex-1 px-8 pt-10 pb-10 flex flex-col space-y-6">
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
              Combined Reach
            </div>
            <div className="text-lg text-black">{combinedReach}</div>
          </div>
          <div>
            <div className="uppercase text-xs font-extrabold text-gray-400 tracking-wider mb-1">
              CO2 Saved
            </div>
            <div className="text-lg text-black">{estimatedImpact}</div>
          </div>
          <div>
            <div className="uppercase text-xs font-extrabold text-gray-400 tracking-wider mb-1">
              Confidence Score
            </div>
            <div className="text-lg text-black">{confidenceScore}</div>
          </div>
        </div>

        {/* Error display */}
        {error && (
          <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default BrandMatchCard;