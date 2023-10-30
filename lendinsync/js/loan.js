const customer_id = "A123456";
const get_borrowed_loans_by_customer_id = "http://127.0.0.1:9000/loan/borrowing/" + customer_id;
const get_lent_loans_by_customer_id = "http://127.0.0.1:9000/loan/lending/" + customer_id;
const create_borrow_application = "http://127.0.0.1:9000/loan/borrowing/" + customer_id;
const create_lending_application = "http://127.0.0.1:9000/loan/lending/" + customer_id;

const loan = Vue.createApp({
    data() {
        return {
            customer_borrowed_loans: [],
            message: "",
        };
    },
    methods: {
        async get_borrowed_loans_by_customer_id() {
            const response = await fetch(get_borrowed_loans_by_customer_id);
            const data = await response.json();

            if (data.code === 404) {
                this.message = data.message;
            } else {
                this.customer_borrowed_loans = data.data.;
        },
    }

})