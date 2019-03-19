// document.addEventListener('DOMContentLoaded', function() {
	document.body.insertAdjacentHTML('beforeend', "<div>hahahahahaha</div>");
// });

chrome.window.executeScript(null, {
	code: "alert('hi');"
});
// alert('hi');
// document.addEventListener('DOMContentLoaded', function () {
// });