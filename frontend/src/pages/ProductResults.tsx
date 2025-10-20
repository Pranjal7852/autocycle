import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import FlowNavigator from "@/components/FlowNavigator";
import ReactMarkdown from "react-markdown";

interface Product {
  product_name: string;
  status: string;
  result: {
    brand: string;
    target_brand: string;
    product_type: string;
    product_name: string;
    product_description: string;
    pitch: string;
    image_url: string;
  };
}

interface LocationState {
  response: {
    status: string;
    result: {
      status: string;
      results: Product[];
    };
  };
  inputData?: any;
  combinedReach?: string;
  estimatedImpact?: string;
  confidenceScore?: string;
}

const ProductResults: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const {
    response,
    inputData,
    combinedReach,
    estimatedImpact,
    confidenceScore,
  } = (location.state || {}) as LocationState;

  if (!response || !response.result?.results?.length) {
    return (
      <div className="min-h-screen flex items-center justify-center text-red-600">
        No product data found. Please go back and try again.
      </div>
    );
  }

  const products = response.result.results;
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [showFullPitch, setShowFullPitch] = useState(false);

  const selectedProduct = products[selectedIndex].result;

  const userInput = {
    company: selectedProduct.brand,
    nameOfProduct: selectedProduct.product_name,
    collaborator: selectedProduct.target_brand,
    material: inputData?.material || "Plastic/PP",
    location: inputData?.location || "Munich",
    description: selectedProduct.product_description,
    estimatedImpact: estimatedImpact || "120.000€",
    combinedReach: combinedReach || "20 Million",
    confidenceScore: confidenceScore || "75 Tons",
  };

  return (
    <div className="bg-background min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-8">
        <FlowNavigator currentStep="result" brandType="have" />

        <div className="relative w-full h-100 z-10 pt-[55%]">
          <h1 className="absolute top-0 font-[Figtree,sans-serif] text-[60px] sm:text-[90px] font-extrabold uppercase leading-[1] text-primart z-20">
            {userInput.company}
            <br />
            X
            <br />
            {userInput.collaborator}
          </h1>

          <div className="absolute top-14 right-0 bg-[#F8F4EE] w-[45%] max-h-[420] aspect-square z-10">
            <div className="pl-[6rem] pt-[10rem]">
              <h3 className="text-lg font-bold mb-4 text-primary font-poppins">USER INPUT:</h3>
              <div className="grid grid-cols-2 gap-y-3 font-mulish text-base">
                <div>Company Name</div>
                <div className="font-bold">{userInput.company}</div>
                <div>Collab. Company</div>
                <div className="font-bold">{userInput.collaborator}</div>
                <div>Material</div>
                <div className="font-bold">{userInput.material}</div>
                <div>Location</div>
                <div className="font-bold">{userInput.location}</div>
              </div>
              <Button
                className="absolute -right-5 -bottom-4 z-10 bg-black text-white text-lg font-light px-8 py-2"
                type="button"
                onClick={() => navigate(-1)}
              >
                Change
              </Button>
            </div>
          </div>
        </div>

        <div className="relative z-10 pt-[55%]">
          <div className="absolute w-[55%] left-0 top-0 z-10 aspect-square">
            <div className="bg-muted items-center min-h-[320px] aspect-square">
              <img
                src={selectedProduct.image_url}
                alt={selectedProduct.product_name}
                className="absolute -left-8 w-full max-w-[400px]"
              />
            </div>
          </div>

          <div className="absolute top-10 right-0 w-[50%] z-20">
            <div>
              <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">Product Name</h4>
              <p className="text-lg font-semibold">{selectedProduct.product_name}</p>
            </div>

            <p className="text-base mb-8 text-primary font-mulish">{selectedProduct.product_description}</p>

            <div>
              <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">Pitch</h4>
              <div
                className={`prose prose-p:text-base prose-p:font-mulish prose-p:text-primary prose-headings:font-semibold prose-headings:text-muted-foreground prose-headings:uppercase prose-headings:text-xs prose-ul:pl-5 transition-all duration-300 ease-in-out ${showFullPitch ? "" : "max-h-[200px] overflow-hidden"
                  }`}
              >
                <ReactMarkdown>{selectedProduct.pitch}</ReactMarkdown>
              </div>
              <button
                className="mt-2 text-sm underline text-muted-foreground hover:text-primary"
                onClick={() => setShowFullPitch((prev) => !prev)}
              >
                {showFullPitch ? "Show Less" : "Show More"}
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10 mt-6">
              <div>
                <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">CO2 Saved</h4>
                <p className="text-lg font-semibold">{userInput.estimatedImpact}</p>
              </div>
              <div>
                <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">COMBINED REACH</h4>
                <p className="text-lg font-semibold">{userInput.combinedReach}</p>
              </div>
              <div>
                <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">Confidence Score</h4>
                <p className="text-lg font-semibold">{userInput.confidenceScore}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="relative mt-16 z-10">
          <h3 className="text-lg font-semibold mb-6 font-mulish text-primary">Explore more inspiration &gt;</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-16">
            {products.map((item, idx) => {
              if (idx === selectedIndex) return null;

              const product = item.result;

              return (
                <div
                  key={idx}
                  className="flex flex-col cursor-pointer"
                  onClick={() => setSelectedIndex(idx)}
                >
                  <div className="bg-muted aspect-square mb-4 flex items-center justify-center">
                    <img
                      src={product.image_url}
                      alt={product.product_name}
                      className="w-3/4 h-3/4 object-cover rounded"
                    />
                  </div>
                  <h4 className="font-semibold font-poppins text-primary">{product.product_name}</h4>
                  <p className="text-sm text-muted-foreground font-mulish">
                    {product.product_description.slice(0, 60)}...
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductResults;
