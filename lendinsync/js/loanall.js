const get_all_borrowed_loans = "http://localhost:5001/loan/borrowing";
const get_all_lent_loans = "http://localhost:5001/loan/lending";

const loan = Vue.createApp({
    data() {
        return {
            borrowed_loans: [],
            lent_loans: [],
            message: "",
            loan_amount: 0,
            collateral_amount: 0,
            investment_amount: 0,
            loan_term: 0,
            currency_info: [],
            selectedCurrency: "",
            exchange_rate: 0,
            interest_rate: 0,
            service_fee: 0,
            repayment_amount: 0,
            StatusLevel: "",
            borrowing_service_fee: 0,
            lending_service_fee: 0,
            validation_errors: [],
            errorsFound: false
        };
    },
    computed: {
        total_interest_amount() {
            const totalInterest = parseFloat(this.investment_amount) * (this.interest_rate / 100) * (this.loan_term / 365);
            return parseFloat(totalInterest.toFixed(2)); // Round to 2 decimal places
        },
        revenue() {
            const investmentAmount = parseFloat(this.investment_amount);
            const revenue = this.total_interest_amount + investmentAmount;
            return parseFloat(revenue.toFixed(2)); // Round to 2 decimal places
        },
    },
    methods: {
        async get_all_borrowed_loans() {
            try {
                const response = await fetch(get_all_borrowed_loans);
                const data = await response.json();

                if (data.code === 404) {
                    this.message = data.message;
                } else {
                    this.borrowed_loans = data.data.loans;
                }
            } catch (error) {
                this.message = "Error fetching all borrowed loans: " + error;
            }
        },
        async get_all_lent_loans() {
            try {
                const response = await fetch(get_all_lent_loans);
                const data = await response.json();

                if (data.code === 404) {
                    this.message = data.message;
                } else {
                    this.lent_loans = data.data.loans;
                }
            } catch (error) {
                this.message = "Error fetching all lent loans: " + error;
            }
        },
        async getCurrencyCodes() {
            const response = await fetch('http://tbankonline.com/SMUtBank_API/Gateway?Header={"serviceName": "getCurrencyList", "userID": "", "PIN": "", "OTP": ""}&Content={"baseCurrency": "SGD", "quoteCurrency": "USD"}');
            const data = await response.json();
            this.currency_info = data.Content.ServiceResponse.CurrencyList.Currency;
        },
        async getExchangeRate(currency_code) {
            const response = await fetch(`http://tbankonline.com/SMUtBank_API/Gateway?Header={"serviceName": "getExchangeRate", "userID": "", "PIN": "", "OTP": ""}&Content={"baseCurrency": "SGD", "quoteCurrency": "${currency_code}"}`);
            const data = await response.json();
            this.exchange_rate = data.Content.ServiceResponse["FX_SpotRate_Read-Response"]["Rate"];
        },
        async create_borrow_application(event) {
            event.preventDefault();
            this.validation_errors = [];
            if (this.loan_amount.value <= 0) {
                this.validation_errors.push("Loan amount must be greater than 0");
            }
            if (this.loan_amount.value > this.collateral_amount.value) {
                this.validation_errors.push("Loan amount must be less than the collateral amount");
            }
            if (this.selectedCurrency === "") {
                this.validation_errors.push("Please select a currency");
            }
            if (this.loan_term.value <= 0) {
                this.validation_errors.push("Loan term must be greater than 0");
            }
            if (this.validation_errors.length > 0) {
                this.errorsFound = true;
                return;
            } else {
                this.validation_errors = [];
                this.errorsFound = false;
                const jsonData = JSON.stringify({
                    // Remove "CustomerId" and set it on the server side
                    CurrencyCode: this.selectedCurrency,
                    LoanAmount: this.loan_amount,
                    RepaymentAmount: this.repayment_amount,
                    InterestRate: this.interest_rate,
                    CollateralAmount: this.collateral_amount,
                    LoanTerm: this.loan_term,
                    ServiceFee: this.service_fee,
                    StatusLevel: "Borrowing"
                });

                const url = create_borrow_application;
                const postMethod = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: jsonData
                };

                try {
                    const response = await fetch(url, postMethod);
                    const data = await response.json();

                    switch (data.code) {
                        case 201:
                            // Handle success case
                            break;
                        case 500:
                            this.message = data.message;
                            break;
                        default:
                            throw `${data.code}: ${data.message}`;
                    }
                } catch (error) {
                    console.error('Error');
                }
            }
        },
        async create_lending_application(event) {
            event.preventDefault();
            this.validation_errors = [];
            if (this.investment_amount <= 0) {
                this.validation_errors.push("Investment amount must be greater than 0");
            }
            if (this.loan_term <= 0) {
                this.validation_errors.push("Loan term must be greater than 0");
            }
            if (this.interest_rate <= 0) {
                this.validation_errors.push("Interest rate must be greater than 0");
            }
            if (this.selectedCurrency === "") {
                this.validation_errors.push("Please select a currency");
            }
            if (this.validation_errors.length > 0) {
                this.errorsFound = true;
                return;
            } else {
                this.validation_errors = [];
                this.errorsFound = false;
                const jsonData = JSON.stringify({
                    // Remove "CustomerId" and set it on the server side
                    InvestmentAmount: this.investment_amount,
                    InterestRate: this.interest_rate,
                    RepaymentAmount: this.repayment_amount,
                    LoanTerm: this.loan_term,
                    CurrencyCode: this.selectedCurrency,
                    TotalInterestAmount: this.total_interest_amount,
                    ServiceFee: this.service_fee,
                    Revenue: this.revenue,
                    StatusLevel: "Lending"
                });

                const url = create_lending_application;
                const postMethod = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: jsonData
                };

                try {
                    const response = await fetch(url, postMethod);
                    const data = await response.json();

                    switch (data.code) {
                        case 201:
                            // Handle success case
                            break;
                        case 500:
                            this.message = data.message;
                            break;
                        default:
                            throw `${data.code}: ${data.message}`;
                    }
                } catch (error) {
                    console.error('Error');
                }
            }
        }
    },
    created() {
        this.get_all_borrowed_loans(); // Fetch all borrowed loans
        this.get_all_lent_loans();     // Fetch all lent loans
        this.getCurrencyCodes();       // Fetch currency codes
    },
});

const vm = loan.mount('#loan');
