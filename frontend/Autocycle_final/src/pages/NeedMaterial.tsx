import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useNavigate } from "react-router-dom";
import FlowNavigator from "@/components/FlowNavigator";

const NeedMaterial: React.FC = () => {
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/nm_brandmatch");
  };

  return (
    <div className="relative max-w-5xl mx-auto bg-background min-h-screen px-4 py-12 sm:py-16">
      {/* Form header */}
      <FlowNavigator currentStep="form" brandType="need" />
      
      {/* Main content */}
      <div className="relative z-10">
        <h1 className="font-mulish text-3xl font-extrabold text-primary text-center uppercase mb-12 max-w-3xl mx-auto sm:text-2xl">
          Find the material that brings your product to life
        </h1>
        
        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-10">
          {/* Company name field */}
          <div>
            <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
              Your Company Name
            </label>
            <Input 
              type="text" 
              placeholder="Company Name"
              className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg"
            />
          </div>
          
          {/* Material Type and Factory Location */}
          <div className="flex gap-8 max-md:flex-col">
            <div className="flex-1">
              <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
                What type of material do you need?
              </label>
              <Select>
                <SelectTrigger className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg">
                  <SelectValue placeholder="Polypropylene (PP)" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pp">Polypropylene (PP)</SelectItem>
                  <SelectItem value="pet">Polyethylene Terephthalate (PET)</SelectItem>
                  <SelectItem value="hdpe">High-Density Polyethylene (HDPE)</SelectItem>
                  <SelectItem value="pvc">Polyvinyl Chloride (PVC)</SelectItem>
                  <SelectItem value="ldpe">Low-Density Polyethylene (LDPE)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex-1">
              <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
                Where is your factory located?
              </label>
              <Input 
                type="text" 
                placeholder="City (e.g., München)"
                className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg"
              />
            </div>
          </div>
          
          {/* Collaboration company field */}
          <div>
            <label className="font-mulish text-lg font-extrabold text-primary mb-3 block">
              Is there a company you intend to collaborate with? <span className="text-muted-foreground">(optional)</span>
            </label>
            <Input 
              type="text" 
              placeholder="Company Name"
              className="w-full h-16 px-4 border-2 border-border font-sans text-base text-muted-foreground rounded-lg"
            />
            <p className="font-sans text-sm text-muted-foreground mt-2">
              If you don't have a brand in mind, the next step will offer you to choose between 5 Brands that would make a perfect collaboration.
            </p>
          </div>
        
          {/* Submit button */}
          <div className="flex justify-end">
            <Button
              type="submit"
              className="mt-4 py-3 px-12 bg-primary border border-primary text-primary-foreground font-poppins text-xl rounded-lg hover:bg-primary/90 transition"
            >
              Get inspired
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NeedMaterial;
