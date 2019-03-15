document.addEventListener('DOMContentLoaded', function () {
	// 1. Select the portion of the document to be processed
	debugger
	let body = document.body;
	// 2. Make a copy of the portion and perform operation from here in order not to affect the "current"  webpage
	let cloned_body = body.cloneNode(true);
	// 3. select the " undesired parts" to be dumped
	const deletes = [
		'nav',
		'header',
		'footer',
		'img',
		'a',
		'span',
		'link',
		'script',
		'noscript'
	];
	// 4. Perform the deletion of parts via destructuring each individual selected "portion"
	for (i in deletes) {
		const item = cloned_body.querySelectorAll(deletes[i]);
		[...item].forEach(e => e.remove());
	}
	// 5. Select the partially "cleansed" data to be "purified"
	cloned_body = cloned_body.textContent;
	cloned_body = cloned_body.replace(/[\n\r]+|[\s]{2,}/g, ' ').trim();
	cloned_body = cloned_body.replace(/<\!--.*?-->/g, "");
	cloned_body = cloned_body.toLowerCase();
	// 6. Perform suitable "formatting" to convert "cleansed" data into JSON
	let stringified_body = JSON.stringify(cloned_body);
	// let parsed_body = JSON.parse(stringified_body);
	// 7. Send the data a specific website
	document.addEventListener('change', postData);
	function postData(e) {
		e.preventDefault();
		debugger
		fetch('http://127.0.0.1:5000/_words',
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ data: stringified_body })
			})
			.then(checkStatus)
			.then(res => res.json())
			.then(data => console.log(data))
	}
	/**
	 * Operations after receiving response from website
	 * Perform if else condition from here on
	 */
	url = `http://127.0.0.1:5000/_words`;
	fetchData(url)
		.then(data => populate(data.message))

	function fetchData(url) {
		return fetch(url)
			.then(checkStatus)
			.then(response => response.json())
			.catch(error => console.log("Looks like there was a problem", error))
	}

	function checkStatus(response) {
		if (response.ok) {
			return Promise.resolve(response);
		} else {
			return Promise.reject(new Error(response.statusText));
		}
	}

	function populate(dog_list) {
		const container = document.getElementById("container");
		for (dog in dog_list) {
			let li = document.createElement("li");
			let node = document.createTextNode(dog);
			li.appendChild(node);
			container.appendChild(li);
		}
	}

	/**
	 * Original function for retrieving data and display them
	 */
	// 	let dog_list = [];
	// const container = document.getElementById("container");
	// fetch('https://dog.ceo/api/breeds/list/all')
	//     .then(response => {
	//         if (response.ok) {
	//             return response.json();
	//         } else {
	//             throw new Error(response.statusText);
	//         }
	//     })
	//     .then(data => {
	//         dog_list = data.message;
	//         for (dog in dog_list) {
	//             let li = document.createElement("li");
	//             let node = document.createTextNode(dog);
	//             li.appendChild(node);
	//             container.appendChild(li);
	//         }
	//     });

	/**
	 * Original function for posting data to a specific website
	 */
	// document.addEventListener('change', postData);
	// function postData(e) {
	// 	e.preventDefault();

	// 	fetch('https://jsonplaceholder.typicode.com/comments', 
	// 	{
	// 		method: "POST",
	// 		headers: {
	// 			"Content-Type": "application/json"
	// 		},
	// 		body: JSON.stringify({ data: stringified_body})
	// 	})
	// 		.then(checkStatus)
	// 		.then(res => res.json())
	// 		.then(data => console.log(data))
	// }
});