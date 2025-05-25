import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import BrandMatchCard from "@/components/BrandMatchCard";
import FlowNavigator from "@/components/FlowNavigator";

interface CollaborationBrand {
  brand_name: string;
  brand_placement: string[];
  sustainability_placement: string;
  product_assumptions: string[];
  collaboration_summary: string;
  estimated_impact: number;
  confidence_score: number;
  combined_reach: number;
  logo_url: string;
  company_domain: string;
}

interface GenerateBrandResponse {
  status: "success" | "error";
  result?: {
    status: "collaboration_complete";
    results: {
      input_summary: {
        brand: string;
        plastic: string;
      };
      top_collaborations: CollaborationBrand[];
    };
  };
  message?: string;
}

interface FormData {
  materialType: string;
  // Add other form fields as needed
}

const BrandMatch: React.FC = () => {
  const { state } = useLocation();
  const { formData, apiResponse } = state || {} as { formData: FormData; apiResponse: GenerateBrandResponse };
  const [isLoading, setIsLoading] = useState(true);

  // Simulate loading delay
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000); // 1-second delay
    return () => clearTimeout(timer);
  }, []);

  // Loading screen
  if (isLoading) {
    return (
      <div className="bg-background min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary mx-auto"></div>
          <p className="font-mulish text-lg text-primary mt-4">Loading brand matches...</p>
        </div>
      </div>
    );
  }

  // Fallback if no data
  if (!formData || !apiResponse || apiResponse.status !== "success" || !apiResponse.result?.results?.top_collaborations) {
    return (
      <div className="bg-background min-h-screen">
        <div className="max-w-5xl mx-auto px-4 sm:px-8 py-12">
          <FlowNavigator currentStep="brand" brandType="have" />
          <h1 className="font-mulish text-2xl sm:text-3xl font-extrabold uppercase text-center text-primary mb-14">
            Brand Match Results
          </h1>
          <p className="text-red-500 text-center">
            {apiResponse?.message || "No data available. Please complete the form first."}
          </p>
        </div>
      </div>
    );
  }

  // Map API data to BrandMatchCard props
  const cardsData = apiResponse.result.results.top_collaborations.map((collab) => ({
    brand: collab.brand_name,
    selectUrl: `/have-material/${collab.brand_name.toLowerCase().replace(/\s/g, "-")}`,
    brandPlacement: collab.brand_placement.join(", "),
    sustainabilityPlacement: collab.sustainability_placement,
    productAssumptions: collab.product_assumptions.join(", "),
    estimatedImpact: `${collab.estimated_impact}M Tons`,
    combinedReach: `${collab.combined_reach}M People`,
    confidenceScore: `${collab.confidence_score}.00%`,
    logoUrl: collab.logo_url,
    companyDomain: collab.company_domain,
  }));

  return (
    <div className="bg-background min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-8 py-12">
        <FlowNavigator currentStep="brand" brandType="have" />
        <h1 className="font-mulish text-2xl sm:text-3xl font-extrabold uppercase text-center text-primary mb-14">
          All set. Your results are ready to explore
        </h1>
        <div className="flex flex-col gap-10">
          {cardsData.map((card, idx) => (
            <BrandMatchCard
              key={card.brand + idx}
              brand={card.brand}
              selectUrl={card.selectUrl}
              brandPlacement={card.brandPlacement}
              sustainabilityPlacement={card.sustainabilityPlacement}
              productAssumptions={card.productAssumptions}
              estimatedImpact={card.estimatedImpact}
              combinedReach={card.combinedReach}
              confidenceScore={card.confidenceScore}
              logoUrl={card.logoUrl}
              companyDomain={card.companyDomain}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default BrandMatch;