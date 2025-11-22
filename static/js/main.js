// Main JavaScript file for common functionality

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

// Format number with commas
function formatNumber(value) {
    return new Intl.NumberFormat('en-US').format(value);
}

// Show loading state
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<span class="loading"></span>';
    }
}

// Chart.js default configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.color = '#2c3e50';
Chart.defaults.plugins.legend.display = true;
Chart.defaults.plugins.legend.position = 'top';

// Color palette
const colors = {
    primary: '#0892a5',
    secondary: '#2e9b9b',
    accent: '#50a290',
    success: '#6fa985',
    warning: '#c4b383',
    danger: '#e74c3c',
    info: '#3498db',
    purple: '#9b59b6'
};

const chartColors = [
    '#0892a5', '#2e9b9b', '#50a290', '#6fa985',
    '#8dad7f', '#a9b17e', '#c4b383', '#dbb68f'
];

// Create gradient for charts
function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}

// Error handling
function handleError(error, elementId) {
    console.error('Error:', error);
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = 'Error loading data';
    }
}

// Fetch data with error handling
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded successfully');
});
