const stocksByCategory = {
    tech: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA'],
    finance: ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
    health: ['JNJ', 'PFE', 'ABBV', 'MRK', 'UNH'],
    retail: ['WMT', 'TGT', 'COST', 'HD', 'LOW'],
    energy: ['XOM', 'CVX', 'COP', 'BP', 'SHEL']
 };
 
 document.getElementById('categorySelect').addEventListener('change', function() {
    const category = this.value;
    const stockSelect = document.getElementById('stockSelect');
    stockSelect.innerHTML = '<option value="">Select Stock</option>';
    
    if (category) {
        stocksByCategory[category].forEach(stock => {
            stockSelect.innerHTML += `<option value="${stock}">${stock}</option>`;
        });
    }
 });
 
 let priceChart = null;
 
 async function analyzeStock() {
    const symbol = document.getElementById('stockSelect').value || 
                  document.getElementById('customSymbol').value;
    if (!symbol) return;
 
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `symbol=${symbol}`
        });
        
        const data = await response.json();
        console.log("Received data:", data); // Debug line
        
        if (data.success) {
            updateResults(data);
            if (data.chart_data && data.chart_data.dates) {
                updateChart(data.chart_data);
                updateSentiment(symbol);
            }
        } else {
            document.getElementById('currentPrice').innerHTML = data.message;
        }
    } catch (error) {
        console.error('Analysis failed:', error);
    }
 }
 
 function updateResults(data) {
    console.log("Updating with data:", data); // Debug line
    
    // Current Price
    document.getElementById('currentPrice').innerHTML = `Current Price: $${data.current_price.toFixed(2)}`;
    
    // Predictions
    document.getElementById('predictions').innerHTML = `
        Next Day: $${data.predictions.next_day.toFixed(2)}<br>
        Next Week: $${data.predictions.next_week.toFixed(2)}<br>
        Next Month: $${data.predictions.next_month.toFixed(2)}
    `;
    
    // Technical Indicators
    document.getElementById('indicators').innerHTML = `
        RSI: ${data.indicators.rsi.toFixed(2)}<br>
        MACD: ${data.indicators.macd.toFixed(2)}
    `;
    
    // Blockchain
    document.getElementById('blockchain').innerHTML = `Hash: ${data.hash}`;
 }
 
 function updateChart(chartData) {
    const ctx = document.getElementById('priceChart');
    if (!ctx) {
        console.error('Chart canvas not found');
        return;
    }
 
    if (priceChart) {
        priceChart.destroy();
    }
 
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [{
                label: 'Stock Price',
                data: chartData.prices,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
 }
 
 function exportPDF() {
    const symbol = document.getElementById('stockSelect').value || 
                  document.getElementById('customSymbol').value;
    if (!symbol) return;
    window.location.href = `/export-pdf/${symbol}`;
 }


function toggleInfo() {
    const modal = document.getElementById('infoModal');
    modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
}

document.querySelector('.close').onclick = function() {
    document.getElementById('infoModal').style.display = 'none';
}

async function updateSentiment(symbol) {
    try {
        const response = await fetch(`/sentiment/${symbol}`);
        const data = await response.json();
        
        document.getElementById('sentiment').innerHTML = `
            <div>Overall: ${data.sentiment}</div>
            <div>Score: ${data.score}</div>
            <div class="headlines">
                ${data.headlines.map(h => `
                    <div class="headline">${h.title}</div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        console.error('Sentiment analysis failed:', error);
    }
}


