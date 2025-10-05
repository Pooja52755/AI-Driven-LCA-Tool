// Utility functions for the LCA tool

export function formatNumber(value, decimals = 2) {
    if (value === null || value === undefined) return 'N/A';
    return Number(value).toFixed(decimals);
}

export function formatPercentage(value, decimals = 1) {
    if (value === null || value === undefined) return 'N/A';
    return `${Number(value).toFixed(decimals)}%`;
}

export function formatCapacity(value) {
    if (value === null || value === undefined) return 'N/A';
    if (value >= 1000000) {
        return `${(value / 1000000).toFixed(1)}M tonnes/year`;
    } else if (value >= 1000) {
        return `${(value / 1000).toFixed(1)}K tonnes/year`;
    }
    return `${value} tonnes/year`;
}

export function getPerformanceLevel(score) {
    if (score >= 80) return { level: 'Excellent', color: 'text-green-600', bg: 'bg-green-100' };
    if (score >= 65) return { level: 'Good', color: 'text-blue-600', bg: 'bg-blue-100' };
    if (score >= 50) return { level: 'Moderate', color: 'text-yellow-600', bg: 'bg-yellow-100' };
    return { level: 'Poor', color: 'text-red-600', bg: 'bg-red-100' };
}

export function getEmissionLevel(gwp) {
    if (gwp < 8) return { level: 'Low', color: 'text-green-600', bg: 'bg-green-100' };
    if (gwp < 15) return { level: 'Moderate', color: 'text-yellow-600', bg: 'bg-yellow-100' };
    if (gwp < 25) return { level: 'High', color: 'text-orange-600', bg: 'bg-orange-100' };
    return { level: 'Very High', color: 'text-red-600', bg: 'bg-red-100' };
}

export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

export function validateProcessInput(input) {
    const errors = {};
    
    if (!input.metal_type) {
        errors.metal_type = 'Metal type is required';
    }
    
    if (!input.process_route) {
        errors.process_route = 'Process route is required';
    }
    
    if (!input.production_capacity || input.production_capacity <= 0) {
        errors.production_capacity = 'Production capacity must be greater than 0';
    }
    
    if (!input.energy_source) {
        errors.energy_source = 'Energy source is required';
    }
    
    if (!input.processing_location) {
        errors.processing_location = 'Processing location is required';
    }
    
    if (!input.end_of_life_option) {
        errors.end_of_life_option = 'End of life option is required';
    }
    
    if (input.energy_consumption && input.energy_consumption < 0) {
        errors.energy_consumption = 'Energy consumption cannot be negative';
    }
    
    if (input.transport_distance && input.transport_distance < 0) {
        errors.transport_distance = 'Transport distance cannot be negative';
    }
    
    if (input.ore_grade && (input.ore_grade < 0 || input.ore_grade > 100)) {
        errors.ore_grade = 'Ore grade must be between 0 and 100';
    }
    
    if (input.recycling_rate && (input.recycling_rate < 0 || input.recycling_rate > 100)) {
        errors.recycling_rate = 'Recycling rate must be between 0 and 100';
    }
    
    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
}

export function generateColors(count) {
    const colors = [
        '#0f766e', '#06b6d4', '#f59e0b', '#10b981', '#ef4444',
        '#8b5cf6', '#f97316', '#06d6a0', '#ffd23f', '#3b82f6'
    ];
    
    if (count <= colors.length) {
        return colors.slice(0, count);
    }
    
    const result = [...colors];
    for (let i = colors.length; i < count; i++) {
        const hue = (i * 137.508) % 360; // Golden angle approximation
        result.push(`hsl(${hue}, 70%, 50%)`);
    }
    
    return result;
}

export function downloadData(data, filename, type = 'json') {
    let content, mimeType;
    
    if (type === 'json') {
        content = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
    } else if (type === 'csv') {
        content = arrayToCSV(data);
        mimeType = 'text/csv';
    } else {
        throw new Error('Unsupported download type');
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.${type}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function arrayToCSV(data) {
    if (!Array.isArray(data) || data.length === 0) {
        return '';
    }
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => 
            headers.map(header => {
                const value = row[header];
                return typeof value === 'string' && value.includes(',') 
                    ? `"${value}"` 
                    : value;
            }).join(',')
        )
    ].join('\n');
    
    return csvContent;
}

export function getMetalColor(metal) {
    const colors = {
        'Aluminium': '#c0c0c0',
        'Copper': '#b87333',
        'Steel': '#71797e',
        'Zinc': '#7b68ee',
        'Lead': '#2f4f4f'
    };
    return colors[metal] || '#6b7280';
}

export function formatDuration(seconds) {
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
    return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
}

export function createToast(message, type = 'info') {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-50 px-4 py-2 rounded shadow-lg text-white max-w-sm ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        type === 'warning' ? 'bg-yellow-500' :
        'bg-blue-500'
    }`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (document.body.contains(toast)) {
            document.body.removeChild(toast);
        }
    }, 5000);
}

export const SUPPORTED_METALS = [
    { name: 'Aluminium', symbol: 'Al', density: 2.70 },
    { name: 'Copper', symbol: 'Cu', density: 8.96 },
    { name: 'Steel', symbol: 'Fe', density: 7.87 },
    { name: 'Zinc', symbol: 'Zn', density: 7.14 },
    { name: 'Lead', symbol: 'Pb', density: 11.34 }
];

export const ENERGY_SOURCES = [
    'Coal',
    'Grid',
    'Solar',
    'Wind',
    'Hydro',
    'Gas',
    'Mixed (Coal + Solar)',
    'Grid + Hydro',
    'Coal + Wind',
    'Grid + Solar',
    'Grid + Gas'
];

export const INDIAN_LOCATIONS = [
    'Odisha, India',
    'Khetri, Rajasthan',
    'Jamshedpur, India',
    'Chhattisgarh, India',
    'Andhra Pradesh, India',
    'Karnataka, India',
    'Gujarat, India',
    'Maharashtra, India'
];