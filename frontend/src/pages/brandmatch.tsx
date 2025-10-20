import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import BrandMatchCard from "@/components/BrandMatchCard";
import FlowNavigator from "@/components/FlowNavigator";
import { LoadingComponent } from "@/components/Loading";

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
  brand: string;
  location: string;
}

const BrandMatch: React.FC = () => {
  const { state } = useLocation();
  const { formData, apiResponse, inputResponse } = state || {} as { formData: FormData; apiResponse: GenerateBrandResponse };
  const [isLoadingProducts, setIsLoadingProducts] = useState(false);

  console.log("data received", inputResponse);
  const collaborations = apiResponse?.result?.results?.top_collaborations || [];

  // Handle when a card starts loading
  const handleCardLoading = (isLoading: boolean) => {
    setIsLoadingProducts(isLoading);
  };

  // Show loading component when any card is loading
  if (isLoadingProducts) {
    return (
      <LoadingComponent
        loadingTexts={[
          "Generating product ideas for your collaboration...",
          "Analyzing market potential and sustainability impact...",
          "Creating innovative product concepts...",
          "Almost there... Great things take a few seconds",
          "Finalizing your collaboration results..."
        ]}
        textChangeInterval={2500}
      />
    );
  }

  if (!formData || !apiResponse || apiResponse.status !== "success") {
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

  const cardsData = collaborations.map((collab) => ({
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

        {cardsData.length === 0 ? (
          <p className="text-center text-gray-500 font-mulish">
            No brand matches found for the selected criteria.
          </p>
        ) : (
          <div className="flex flex-col gap-10">
            {cardsData.map((card, idx) => (
              <BrandMatchCard
                key={card.brand + idx}
                {...card}
                inputResponse={inputResponse}
                onLoadingChange={handleCardLoading}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default BrandMatch;