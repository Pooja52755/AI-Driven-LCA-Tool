import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Request interceptor
        this.client.interceptors.request.use(
            (config) => {
                console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
                return config;
            },
            (error) => {
                console.error('API Request Error:', error);
                return Promise.reject(error);
            }
        );
        
        // Response interceptor
        this.client.interceptors.response.use(
            (response) => {
                console.log(`API Response: ${response.status} ${response.config.url}`);
                return response;
            },
            (error) => {
                console.error('API Response Error:', error.response?.data || error.message);
                return Promise.reject(error);
            }
        );
    }
    
    // Health check
    async checkHealth() {
        try {
            const response = await this.client.get('/api/health');
            return response.data;
        } catch (error) {
            throw new Error(`Health check failed: ${error.message}`);
        }
    }
    
    // Get supported metals
    async getSupportedMetals() {
        try {
            const response = await this.client.get('/api/metals');
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get supported metals: ${error.message}`);
        }
    }
    
    // Perform LCA analysis
    async analyzeLCA(processInput) {
        try {
            const response = await this.client.post('/api/lca/analyze', processInput);
            return response.data;
        } catch (error) {
            throw new Error(`LCA analysis failed: ${error.response?.data?.detail || error.message}`);
        }
    }
    
    // Analyze circularity
    async analyzeCircularity(processInput) {
        try {
            const response = await this.client.post('/api/circularity/analyze', processInput);
            return response.data;
        } catch (error) {
            throw new Error(`Circularity analysis failed: ${error.response?.data?.detail || error.message}`);
        }
    }
    
    // Get circularity graph
    async getCircularityGraph(processId) {
        try {
            const response = await this.client.get(`/api/circularity/graph/${processId}`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get circularity graph: ${error.message}`);
        }
    }
    
    // Compare processes
    async compareProcesses(processes) {
        try {
            const response = await this.client.post('/api/compare', processes);
            return response.data;
        } catch (error) {
            throw new Error(`Process comparison failed: ${error.message}`);
        }
    }
    
    // Generate report
    async generateReport(processInput) {
        try {
            const response = await this.client.post('/api/report/generate', processInput);
            return response.data;
        } catch (error) {
            throw new Error(`Report generation failed: ${error.message}`);
        }
    }
    
    // Get model metrics
    async getModelMetrics() {
        try {
            const response = await this.client.get('/api/model/metrics');
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get model metrics: ${error.message}`);
        }
    }
    
    // Get stored comparisons
    async getStoredComparisons() {
        try {
            const response = await this.client.get('/api/comparisons');
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get stored comparisons: ${error.message}`);
        }
    }
    
    // Get mock data
    async getMockData() {
        try {
            const response = await this.client.get('/api/data/mock');
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get mock data: ${error.message}`);
        }
    }
    
    // Simulate scenarios
    async simulateScenarios(scenarios) {
        try {
            const response = await this.client.post('/api/data/simulate', scenarios);
            return response.data;
        } catch (error) {
            throw new Error(`Scenario simulation failed: ${error.message}`);
        }
    }
}

export const apiService = new ApiService();
export default apiService;