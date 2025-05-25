import { useState } from "react";
import axios, { AxiosError } from "axios";

interface GenerateBrandData {
    brand: string;
    plastic_type: string;
    location: string;
}

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

interface GenerateBrandHookResponse {
    isLoading: boolean;
    error: string | null;
    submit: (data: GenerateBrandData) => Promise<GenerateBrandResponse>;
}

export const useGenerateBrand = (): GenerateBrandHookResponse => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const submit = async (data: GenerateBrandData): Promise<GenerateBrandResponse> => {
        setError(null);
        setIsLoading(true);

        try {
            if (!data.location) {
                throw new Error("Factory location is required.");
            }
            if (!data.plastic_type) {
                throw new Error("Material type is required.");
            }

            console.log("Sending payload to /generatebrand:", data);

            const response = await axios.post<GenerateBrandResponse>("http://0.0.0.0:8000/generatebrand", {
                brand: data.brand || "",
                plastic_type: data.plastic_type,
                location: data.location,
            });

            console.log("Received response from /generatebrand:", response.data);
            return response.data;
        } catch (err) {
            const error = err as AxiosError<GenerateBrandResponse>;
            const errorMessage = error.response?.data?.message || error.response?.data?.detail || "Failed to submit form. Please check your inputs and try again.";
            setError(errorMessage);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    return { isLoading, error, submit };
};