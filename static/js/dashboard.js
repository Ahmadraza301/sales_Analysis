// Dashboard specific JavaScript

// Load summary statistics
async function loadSummary() {
    try {
        const data = await fetchData('/api/summary');
        
        document.getElementById('total-revenue').textContent = formatCurrency(data.total_revenue);
        document.getElementById('total-orders').textContent = formatNumber(data.total_orders);
        document.getElementById('avg-order').textContent = formatCurrency(data.avg_order_value);
        document.getElementById('total-quantity').textContent = formatNumber(data.total_quantity);
    } catch (error) {
        handleError(error, 'total-revenue');
    }
}

// Load monthly sales chart
async function loadMonthlySales() {
    try {
        const data = await fetchData('/api/monthly-sales');
        const ctx = document.getElementById('monthlySalesChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.months,
                datasets: [{
                    label: 'Sales ($)',
                    data: data.sales,
                    borderColor: colors.primary,
                    backgroundColor: createGradient(ctx, 'rgba(8, 146, 165, 0.2)', 'rgba(8, 146, 165, 0.05)'),
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Sales: ' + formatCurrency(context.parsed.y);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + (value / 1000000).toFixed(1) + 'M';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading monthly sales:', error);
    }
}

// Load top cities chart
async function loadTopCities() {
    try {
        const data = await fetchData('/api/top-cities');
        const ctx = document.getElementById('topCitiesChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.cities,
                datasets: [{
                    label: 'Sales ($)',
                    data: data.sales,
                    backgroundColor: chartColors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Sales: ' + formatCurrency(context.parsed.x);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + (value / 1000000).toFixed(1) + 'M';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading top cities:', error);
    }
}

// Load top products chart
async function loadTopProducts() {
    try {
        const data = await fetchData('/api/top-products');
        const ctx = document.getElementById('topProductsChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.products,
                datasets: [{
                    label: 'Sales ($)',
                    data: data.sales,
                    backgroundColor: chartColors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Sales: ' + formatCurrency(context.parsed.x);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + (value / 1000000).toFixed(1) + 'M';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading top products:', error);
    }
}

// Load hourly sales chart
async function loadHourlySales() {
    try {
        const data = await fetchData('/api/hourly-sales');
        const ctx = document.getElementById('hourlySalesChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.hours.map(h => h + ':00'),
                datasets: [{
                    label: 'Sales ($)',
                    data: data.sales,
                    borderColor: colors.accent,
                    backgroundColor: 'rgba(80, 162, 144, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Sales: ' + formatCurrency(context.parsed.y);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + (value / 1000000).toFixed(1) + 'M';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading hourly sales:', error);
    }
}

// Load category sales chart
async function loadCategorySales() {
    try {
        const data = await fetchData('/api/category-sales');
        const ctx = document.getElementById('categorySalesChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.categories,
                datasets: [{
                    data: data.sales,
                    backgroundColor: chartColors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = formatCurrency(context.parsed);
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return label + ': ' + value + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading category sales:', error);
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadSummary();
    loadMonthlySales();
    loadTopCities();
    loadTopProducts();
    loadHourlySales();
    loadCategorySales();
});
