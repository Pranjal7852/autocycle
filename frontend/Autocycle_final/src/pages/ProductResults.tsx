import React from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import FlowNavigator from "@/components/FlowNavigator";

const ProductResults: React.FC = () => {
  const { brand } = useParams();
  const navigate = useNavigate();

  // Mock data based on selected brand
  const brandData = {
    company: "BMW",
    collaborator: brand?.toUpperCase() || "DECATHLON",
    material: "Plastic/PP",
    location: "Munich",
    description:
      "This piece of furniture is a striking collaboration between BMW and IKEA, embodying the essence of circular design and functional minimalism. The structure features a sleek, aerodynamic silhouette reminiscent of automotive form language—its gently rounded edges and precise panel alignment evoke the precision of a BMW dashboard, while its matte black drawer fronts contrast elegantly with the soft olive green frame, nodding to sustainable material palettes and calm interior moods. The unit comprises four integrated drawers with recessed pull handles, echoing the ergonomic intuitiveness of car interiors, and a spacious open shelf that brings in IKEA's signature functionality and accessibility. Ideal for both home offices and living rooms, this item offers a visual and emotional bridge between high-performance engineering and relaxed domestic living.",
    matchValue: "120.000€",
    combinedReach: "20 Million",
    annualPlasticVolume: "75 Tons"
  };

  return (
    <div className="bg-background min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-8">
        {/*Navigation*/}
        <FlowNavigator currentStep="result" brandType="have" />
        
        {/*First Section*/}
        <div className="relative w-full h-100 z-10 pt-[55%]">
          {/* Brand header */}
          <h1 className="absolute top-0 font-[Figtree,sans-serif] text-[60px] sm:text-[90px] font-extrabold uppercase leading-[1] text-primart z-20">
            {brandData.company}<br />X<br />{brandData.collaborator}
          </h1>

          {/* User Input - Change*/}
          <div className="absolute top-14 right-0 bg-[#F8F4EE] w-[45%] max-h-[420] aspect-square z-10">
              <div className="pl-[6rem] pt-[10rem]">
                <h3 className="text-lg font-bold mb-4 text-primary font-poppins">USER INPUT:</h3>
                <div className="grid grid-cols-2 gap-y-3 font-mulish text-base">
                  <div>Company Name</div>
                  <div className="font-bold">{brandData.company}</div>
                  <div>Collab. Company</div>
                  <div className="font-bold">{brandData.collaborator}</div>
                  <div>Material</div>
                  <div className="font-bold">{brandData.material}</div>
                  <div>Location</div>
                  <div className="font-bold">{brandData.location}</div>
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

        {/* Main content */}
        <div className="relative z-10 pt-[55%]">
          {/* Left side - Product image */}
          <div className="absolute w-[55%] left-0 top-0 z-10 aspect-square">
            <div className="bg-muted items-center min-h-[320px] aspect-square">
              <img
                src="/images/bmwxdecathlon.png"
                alt="BMW Collaboration Product"
                className="absolute -left-8 w-full max-w-[400px]"
              />
            </div>
          </div>

          {/* Right side - Product details */}
          <div className="absolute top-10 right-0 w-[50%] z-20">
            {/* User input summary */}
            

            {/* Product description */}
            <p className="text-base mb-8 text-primary font-mulish">{brandData.description}</p>

            {/* Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
              <div>
                <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">MATCH VALUE</h4>
                <p className="text-lg font-semibold">{brandData.matchValue}</p>
              </div>
              <div>
                <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">COMBINED REACH</h4>
                <p className="text-lg font-semibold">{brandData.combinedReach}</p>
              </div>
              <div>
                <h4 className="uppercase text-xs font-bold text-muted-foreground mb-1 font-mulish">ANNUAL PLASTIC VOLUME</h4>
                <p className="text-lg font-semibold">{brandData.annualPlasticVolume}</p>
              </div>
            </div>
          </div>
        
        </div>

        {/* More inspiration section */}
        <div className="relative mt-16 z-10">
          <h3 className="text-lg font-semibold mb-6 font-mulish text-primary">Explore more inspiration &gt;</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-16">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex flex-col">
                <div className="bg-muted aspect-square mb-4 flex items-center justify-center">
                  <img
                    src={`/images/bmwxvitra${i}.png`}
                    alt={`BMW x VITRA Product ${i}`}
                    className="w-3/4 h-3/4 object-cover rounded"
                  />
                </div>
                <h4 className="font-semibold font-poppins text-primary">Dynamic Comfort</h4>
                <p className="text-sm text-muted-foreground font-mulish">
                  Eco-friendly materials for furniture and home products
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductResults;
