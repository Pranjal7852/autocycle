import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useNavigate } from "react-router-dom";
import FlowNavigator from "@/components/FlowNavigator";
import { useGenerateBrand } from "@/hooks/useGenerateBrand";
import { useGenerateProducts } from "@/hooks/useGenerateProducts";
import { LoadingComponent } from "@/components/Loading";

const NeedMaterial: React.FC = () => {
  const navigate = useNavigate();
  const { isLoading: isGeneratingBrand, error: brandError, submit: submitBrand } = useGenerateBrand();
  const { isLoading: isGeneratingProducts, error: productsError, submit: submitProducts } = useGenerateProducts();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    brand: "",
    plastic_type: "PP",
    location: "",
    collaborationCompany: "",
  });

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const newFormData = { ...prev, [name]: value };
      console.log("Form data:", newFormData);
      return newFormData;
    });
  };

  // Handle select change for material type
  const handleMaterialChange = (value: string) => {
    setFormData((prev) => {
      const newFormData = { ...prev, plastic_type: value };
      console.log("Form data after material change:", newFormData);
      return newFormData;
    });
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true); // Show loading screen

    try {
      // Check if collaboration company is filled
      const hasCollaborationCompany = formData.collaborationCompany.trim() !== "";

      if (hasCollaborationCompany) {
        // Use the products hook for collaboration and redirect to product results
        const response = await submitProducts({
          source_brand: formData.brand,
          plastic_type: formData.plastic_type,
          location: formData.location,
          target_brand: formData.collaborationCompany,
        });

        // Hard-coded values for now
        const combinedReach = "2.5M users";
        const estimatedImpact = "450 kg CO2";
        const confidenceScore = "87%";

        const inputData = {
          sourceBrand: formData.brand,
          location: formData.location,
          plasticType: formData.plastic_type,
        };

        navigate("/product-results", {
          state: {
            response,
            inputData,
            combinedReach,
            estimatedImpact,
            confidenceScore
          }
        });
      } else {
        // Use the original brand hook and redirect to nm_brandmatch page
        const response = await submitBrand({
          brand: formData.brand,
          plastic_type: formData.plastic_type,
          location: formData.location,
        });

        navigate("/brandmatch", {
          state: {
            formData,
            apiResponse: response,
            inputResponse: {
              sourceBrand: formData.brand,
              location: formData.location,
              plasticType: formData.plastic_type,
            },
          },
        });
      }
    } catch (err) {
      // Handled in hooks
      setIsSubmitting(false);
    }
  };

  // Determine which loading state to show
  const isLoading = isGeneratingBrand || isGeneratingProducts;
  const error = brandError || productsError;

  if (isSubmitting) {
    return <LoadingComponent />;
  }

  return (
    <div className="relative max-w-5xl mx-auto bg-background min-h-screen px-4 py-12 sm:py-16">
      <FlowNavigator currentStep="form" brandType="need" />

      <div className="relative z-10">
        <h1 className="font-mulish text-3xl font-extrabold text-primary text-center uppercase mb-12 max-w-3xl mx-auto sm:text-2xl">
          Find the material that brings your product to life
        </h1>

        {error && <div className="text-red-500 text-center mb-4 font-sans">{error}</div>}

        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-10">
          <div>
            <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
              Your Company Name
            </label>
            <Input
              type="text"
              name="brand"
              value={formData.brand}
              onChange={handleInputChange}
              placeholder="Company Name"
              className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg"
            />
          </div>

          <div className="flex gap-8 max-md:flex-col">
            <div className="flex-1">
              <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
                What type of material do you need?
              </label>
              <Select onValueChange={handleMaterialChange} value={formData.plastic_type}>
                <SelectTrigger className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg">
                  <SelectValue placeholder="Polypropylene (PP)" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="PP">Polypropylene (PP)</SelectItem>
                  <SelectItem value="PET">Polyethylene Terephthalate (PET)</SelectItem>
                  <SelectItem value="HDPE">High-Density Polyethylene (HDPE)</SelectItem>
                  <SelectItem value="PVC">Polyvinyl Chloride (PVC)</SelectItem>
                  <SelectItem value="LDPE">Low-Density Polyethylene (LDPE)</SelectItem>
                  <SelectItem value="PC/ABS">Polycarbonate/Acrylonitrile-Butadiene-Styrene (PC/ABS)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex-1">
              <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
                Where is your factory located?
              </label>
              <Input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                placeholder="City (e.g., München)"
                className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg"
              />
            </div>
          </div>

          <div>
            <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
              Is there a company you intend to collaborate with? <span className="text-muted-foreground">(optional)</span>
            </label>
            <Input
              type="text"
              name="collaborationCompany"
              value={formData.collaborationCompany}
              onChange={handleInputChange}
              placeholder="Company Name"
              className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg"
            />
            <p className="font-sans text-sm text-muted-foreground mt-2">
              If you don't have a brand in mind, the next step will offer you to choose between 5 Brands that would make a perfect collaboration.
            </p>
          </div>

          <div className="flex justify-end">
            <Button
              type="submit"
              disabled={isLoading}
              className="mt-4 py-3 px-12 bg-primary border border-primary text-primary-foreground font-poppins text-xl rounded-lg hover:bg-primary/90 transition"
            >
              Get inspired
              <img src="/icons/arrow_outward.svg" alt="Arrow icon" className="ml-2 w-5 h-5" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NeedMaterial;