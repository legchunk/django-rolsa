// Carbon Footprint Calculator
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('carbon-form');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Get input values
        const electricity = parseFloat(document.getElementById('electricity').value) || 0;
        const gas = parseFloat(document.getElementById('gas').value) || 0;
        const milesDriven = parseFloat(document.getElementById('miles').value) || 0;

        // Carbon emission factors (kg CO2 per unit)
        const electricityFactor = 0.92; // kg CO2 per kWh
        const gasFactor = 5.3; // kg CO2 per therm
        const milesFactor = 0.404; // kg CO2 per mile (average car)

        // Cost factors (approximate USD)
        const electricityCost = 0.13; // per kWh
        const gasCost = 1.09; // per therm
        const gasolineCost = 0.12; // per mile (at $3/gallon, 25 mpg)

        // Calculate carbon footprint (monthly)
        const electricityCarbon = electricity * electricityFactor;
        const gasCarbon = gas * gasFactor;
        const milesCarbon = milesDriven * milesFactor;
        const totalCarbon = electricityCarbon + gasCarbon + milesCarbon;

        // Calculate costs (monthly)
        const electricityExpense = electricity * electricityCost;
        const gasExpense = gas * gasCost;
        const milesExpense = milesDriven * gasolineCost;
        const totalCost = electricityExpense + gasExpense + milesExpense;

        // Annual estimates
        const annualCarbon = (totalCarbon * 12) / 1000; // Convert to metric tons
        const annualCost = totalCost * 12;

        // Display results
        resultsDiv.innerHTML = `
            <div class="result-card">
                <h3>Your Monthly Carbon Footprint</h3>
                <p class="large-number">${totalCarbon.toFixed(2)} kg CO₂</p>
                <p class="annual">Annual: ${annualCarbon.toFixed(2)} metric tons CO₂</p>
            </div>
            <div class="result-card">
                <h3>Your Monthly Cost</h3>
                <p class="large-number">$${totalCost.toFixed(2)}</p>
                <p class="annual">Annual: $${annualCost.toFixed(2)}</p>
            </div>
            <div class="breakdown">
                <h4>Breakdown:</h4>
                <ul>
                    <li>Electricity: ${electricityCarbon.toFixed(2)} kg CO₂ / $${electricityExpense.toFixed(2)}</li>
                    <li>Natural Gas: ${gasCarbon.toFixed(2)} kg CO₂ / $${gasExpense.toFixed(2)}</li>
                    <li>Driving: ${milesCarbon.toFixed(2)} kg CO₂ / $${milesExpense.toFixed(2)}</li>
                </ul>
            </div>
        `;
        resultsDiv.style.display = 'block';
    });
});