// Israeli Salary Calculator (Bruto to Neto)
// Simplified logic for demonstration purposes (2024 approximation)

function calculateSimpleNeto(bruto) {
    // 2024 Tax Brackets (Monthly)
    const brackets = [
        { limit: 7010, rate: 0.10 },
        { limit: 10060, rate: 0.14 },
        { limit: 16150, rate: 0.20 },
        { limit: 22440, rate: 0.31 },
        { limit: 46690, rate: 0.35 },
        { limit: Infinity, rate: 0.47 }
    ];

    let tax = 0;
    let previousLimit = 0;

    for (let bracket of brackets) {
        if (bruto > previousLimit) {
            let taxableAmount = Math.min(bruto, bracket.limit) - previousLimit;
            tax += taxableAmount * bracket.rate;
            previousLimit = bracket.limit;
        } else {
            break;
        }
    }

    // Credit Points (2.25 for average male resident) -> 2.25 * 242 NIS
    const creditPointsValue = 2.25 * 242;
    tax = Math.max(0, tax - creditPointsValue);

    // Bituach Leumi & Health Tax (Approximate)
    // ~3.5% up to 7,522, ~12% above
    let socialSecurity = 0;
    const step1Limit = 7522;

    if (bruto <= step1Limit) {
        socialSecurity = bruto * 0.035;
    } else {
        socialSecurity = (step1Limit * 0.035) + ((bruto - step1Limit) * 0.12);
    }
    // Max cap exists but ignoring for simple demo

    return Math.floor(bruto - tax - socialSecurity);
}


// Mortgage Calculator (Mashkanta)
function calculateMortgage(principal, years, yearlyInterestRate) {
    const monthlyRate = (yearlyInterestRate / 100) / 12;
    const numberOfPayments = years * 12;

    // Formula: M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1 ]

    if (yearlyInterestRate === 0) return principal / numberOfPayments;

    const x = Math.pow(1 + monthlyRate, numberOfPayments);
    const monthlyPayment = principal * ( (monthlyRate * x) / (x - 1) );

    return monthlyPayment.toFixed(2);
}

// Export functions for usage
window.calculateSimpleNeto = calculateSimpleNeto;
window.calculateMortgage = calculateMortgage;
