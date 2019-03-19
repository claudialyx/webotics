document.addEventListener('DOMContentLoaded', function () {
	// This will execute inside the window of the "chrome extension"
	let bank_list = [];
	const selections = document.querySelectorAll('.sort-selection');
	let selection;
	document.addEventListener('click', function () {
		console.log(selections)
		for (select of selections) {
			if (select.checked === true) {
				selection = select.id;
				console.log(select.id)
			}
		}
	})
	// console.log(selections[0].value)
	const container = document.getElementById("container");
	fetch('http://127.0.0.1:5000/_words')
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				throw new Error(response.statusText);
			}
		})
		.then(data => {
			/**
			 * Capture list of banks and sort them out manually (in other lists)
			 */
			create_arrays(data)
			/**
			 * Reveal the data fetched from API
			 */
			populate_cards();


			function create_arrays(data) {
				// Original full collection
				bank_list = data;
				// Sorting using bank_name
				order_by_bank_name = _.sortBy(bank_list, 'bank_name').reverse();
				// Sorting using package_tag
				order_by_package_tag = _.sortBy(bank_list, 'package_tag');
				// Sorting using interest rate
				order_by_interest_rate = _.sortBy(bank_list, 'interest_rate').reverse();
				// Sorting using repayment
				order_by_repayment = _.sortBy(bank_list, 'repayment').reverse();
			}

			function populate_cards() {
				const selections = document.querySelectorAll('.sort-selection');
				let selection;
				const wrapper = document.getElementById("wrapper");
				for (bank of bank_list) {
					populate(bank, wrapper);
				}
				document.addEventListener('click', function () {
					// console.log(selections)
					for (select of selections) {
						if (select.checked === true) {
							selection = select.id;
							// console.log(selection);
						}
					}
					if (selection === "none") {
						erase_display(wrapper);
						for (bank of bank_list) {
							populate(bank, wrapper);
						}
					} else if (selection === "bank") {
						erase_display(wrapper);
						for (bank of order_by_bank_name) {
							populate(bank, wrapper);
						}
					} else if (selection === "type") {
						erase_display(wrapper);
						for (bank of order_by_package_tag) {
							populate(bank, wrapper)
						}
					} else if (selection === "interest") {
						erase_display(wrapper);
						for (bank of order_by_interest_rate) {
							populate(bank, wrapper)
						}
					} else if (selection === "repayment") {
						erase_display(wrapper);
						for (bank of order_by_repayment) {
							populate(bank, wrapper)
						}
					}
				});
			}

			function erase_display(placeholder) {
				while (placeholder.lastChild) {
					placeholder.removeChild(placeholder.lastChild);
				}
			}

			function populate(bank, placeholder) {
				// for (bank in bank_link) {
				let bank_image = `./img/img_${bank.bank_name.toLowerCase()}.png`;
				let bank_name = bank.bank_name;
				let package_tag;
				if (bank.package_tag === "personal") {
					package_tag = "profile";
				} else if (bank.package_tag === "islamic") {
					package_tag = "bell";
				} else if (bank.package_tag === "home") {
					package_tag = "home3";
				} else if (bank.package_tag === "car") {
					package_tag = "truck";
				} else if (bank.package_tag === "business") {
					package_tag = "office";
				}
				let bank_package = bank.package_name;
				let bank_rate = bank.interest_rate;
				let bank_repayment = bank.repayment;
				let bank_link = bank.link;
				let card_bank =
					`<div class="col-4 cardholder">
					<a href="${bank_link}" target="_blank">
						<div class="card mb-4">
							<span title="${bank_name}">
								<img class="card-img-top" src="${bank_image}" alt="${bank_name}">
							</span>
							<div class="card-body">
								<div class="card-text">
									<div><span class="icon icon-${package_tag}"></span>: <span class="package">${bank_package}</span></div>
									<div>Interest Rate: <span>${bank_rate} %</span></div>
									<div> Monthly Repayment: <span>${bank_repayment}</span></div>
								</div>
							</div>
						</div>
					</a>
				</div>`;
				// highlight
				placeholder.insertAdjacentHTML('afterbegin', card_bank);
				// }
			}
		});
});
