import React from "react";
import { Link } from "react-router-dom";

interface FlowNavigatorProps {
  currentStep: "home" | "form" | "brand" | "result";
  brandType?: "have" | "need";
}

const FlowNavigator: React.FC<FlowNavigatorProps> = ({ currentStep, brandType }) => {
  const steps = [
    {
      label: "Home",
      link: "/",
      key: "home",
    },
    {
      label: "Getting Started",
      link: "/collaborations",
      key: "form",
    },
    {
      label: "Brands",
      link: "/brandmatch",
      key: "brand",
    },
    {
      label: "Suggestion",
      key: "result",
    }
  ];

  const getStepContent = (step: typeof steps[number], index: number) => {
    const isActive = currentStep === step.key;
    const isVisible =
      step.key === "home" ||
      step.key === "form" ||
      (step.key === "brand" && ["brand", "result"].includes(currentStep)) ||
      (step.key === "result" && currentStep === "result");

    if (!isVisible) return null;

    return (
      <React.Fragment key={step.key}>
        {index > 0 && (
          <svg width="20" height="21" fill="none" className="text-muted-foreground">
            <path d="M6.31971 15.4084L11.1962 10.5319L6.31971 5.65543L7.295 3.70483L14.1221 10.5319L7.295 17.359L6.31971 15.4084Z" fill="currentColor" />
          </svg>
        )}
        {step.link && !isActive ? (
          <Link to={step.link} className="text-muted-foreground hover:underline">
            {step.label}
          </Link>
        ) : (
          <span className={isActive ? "text-primary" : "text-muted-foreground"}>
            {step.label}
          </span>
        )}
      </React.Fragment>
    );
  };

  return (
    <div className="flex items-center gap-4 font-poppins text-base text-muted-foreground mt-[70px] mb-[60px]">
      {steps.map(getStepContent)}
    </div>
  );
};

export default FlowNavigator;