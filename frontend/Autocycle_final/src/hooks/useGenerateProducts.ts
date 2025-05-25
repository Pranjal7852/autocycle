import { useState } from "react";
import axios, { AxiosError } from "axios";

interface GenerateProductsData {
    source_brand: string;
    plastic_type: string;
    location: string;
    target_brand: string;
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

interface GenerateProductsResponse {
    status: "success" | "error";
    result?: {
        status: string;
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

interface GenerateProductsHookResponse {
    isLoading: boolean;
    error: string | null;
    submit: (data: GenerateProductsData) => Promise<GenerateProductsResponse>;
}

export const useGenerateProducts = (): GenerateProductsHookResponse => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const submit = async (data: GenerateProductsData): Promise<GenerateProductsResponse> => {
        setError(null);
        setIsLoading(true);

        try {
            if (!data.location) {
                throw new Error("Factory location is required.");
            }

            const response = await axios.post<GenerateProductsResponse>("http://0.0.0.0:8000/generateproducts", {
                source_brand: data.source_brand,
                plastic_type: data.plastic_type,
                location: data.location,
                target_brand: data.target_brand,
            });

            return response.data;
        } catch (err) {
            const error = err as AxiosError<GenerateProductsResponse>;
            const errorMessage = error.response?.data?.message || "Failed to submit form. Please try again.";
            setError(errorMessage);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    return { isLoading, error, submit };
}; 