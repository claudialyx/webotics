document.addEventListener('DOMContentLoaded', () => {
    // console.log("Working");
    // set background color
    let first_bank;

    const counts = [];

    function checkStatus(response) {
        if (response.ok) {
            return Promise.resolve(response);
        } else {
            return Promise.reject(new Error(response.statusText));
        }
    }

    fetch('http://127.0.0.1:5000/_words')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(response.statusText);
            }
        })
        .then(data => {
            first_bank = data[0];
            // console.log(first_bank);
        })
        .then(data => {
            web_content = filter_text();
            send_and_fetch_details(web_content);
        })
        .then(data => {
            $('body').append(`
        <style type="text/css" media="screen">
        .flash {
            z-index: 1500 !important;
            position: fixed !important;
            bottom: 3em !important;
            right: 0 !important;
            background-color: rgb(254, 254, 162) !important;
            box-shadow: 0 5px 10px #ddd !important;
            border: 2px solid rgb(244, 244, 86) !important;
            padding: 0.1em 0.5em !important;
            border-top-left-radius: 1.25em !important;
            border-bottom-left-radius: 1.25em !important;
            /* animation: disappear 3s !important; */
            /* width: 15vw !important; */
            width: 18em !important;
            margin-right: -16em !important;
            transition: all 1.5s cubic-bezier(0.075, 0.82, 0.165, 1) !important;
            display: grid !important;
            grid-template-areas: "arrow item";
        }
        
        plain {
            text-decoration: none !important;
            color: inherit !important;
            border-bottom-style: none !important;
        }
        
        .arrow {
            grid-area: arrow;
            margin-right: 0.7em !important;
            transition: all 1.5s cubic-bezier(0.075, 0.82, 0.165, 1) !important;
        }
        
        .item {
            grid-area: item;
        }
        
        .flash:hover {
            margin-right: 0 !important;
        }
        </style >
            `);

            let injected_section = `
            <a class="plain" href="${first_bank.link}" target="_blank">
            <div class="flash">
                <div class="arrow">
                    <span class="icon">👋</span>
                </div>
                <div class="item">
                    <span class="icon icon-${first_bank.package_tag}"></span>
                    <span>Hey! ${first_bank.package_name} is currently offering ${first_bank.package_tag} loan at
                        ${first_bank.interest_rate}% ! Click me to find out more! </span>
                </div>
            </div>
        </a>
`
            $('body').append(injected_section)
        })

    function filter_text() {
        // 1. Select the portion of the document to be processed
        let body = document.body;
        // 2. Make a copy of the portion and perform operation from here in order not to affect the "current" webpage
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
        // let parsed_body = JSON.parse(stringified_body);
        let stringified_body = JSON.stringify(cloned_body);
        return stringified_body;
    }

    function send_and_fetch_details(text_details) {
        // 7. Send the data a specific website
        fetch('http://127.0.0.1:5000/_words', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                data: text_details
            })
        })
            // Check the response of fetching "data" after submitting to the specified website
            // .then(checkStatus)
            .then(res => res.json())
            .then(data => {
                console.log(data);
                // const distinct_matches = [...new Set(data)];

                for (let i = 0; i < data.length; i++) {
                    let num = data[i];
                    counts[num] = counts[num] ? counts[num] + 1 : 1;
                }
                console.log(counts);
                // console.log(distinct_matches);
            })
        // Perform operation on the "altered" data format

    }

    var InstantSearch = {

        "highlight": function (container, highlightText) {
            var internalHighlighter = function (options) {

                var id = {
                    container: "container",
                    tokens: "tokens",
                    all: "all",
                    token: "token",
                    className: "className",
                    sensitiveSearch: "sensitiveSearch"
                },
                    tokens = options[id.tokens],
                    allClassName = options[id.all][id.className],
                    allSensitiveSearch = options[id.all][id.sensitiveSearch];


                function checkAndReplace(node, tokenArr, classNameAll, sensitiveSearchAll) {
                    var nodeVal = node.nodeValue,
                        parentNode = node.parentNode,
                        i, j, curToken, myToken, myClassName, mySensitiveSearch,
                        finalClassName, finalSensitiveSearch,
                        foundIndex, begin, matched, end,
                        textNode, span, isFirst;

                    for (i = 0, j = tokenArr.length; i < j; i++) {
                        curToken = tokenArr[i];
                        myToken = curToken[id.token];
                        myClassName = curToken[id.className];
                        mySensitiveSearch = curToken[id.sensitiveSearch];

                        finalClassName = (classNameAll ? myClassName + " " + classNameAll : myClassName);

                        finalSensitiveSearch = (typeof sensitiveSearchAll !== "undefined" ? sensitiveSearchAll : mySensitiveSearch);

                        isFirst = true;
                        while (true) {
                            if (finalSensitiveSearch)
                                foundIndex = nodeVal.indexOf(myToken);
                            else
                                foundIndex = nodeVal.toLowerCase().indexOf(myToken);

                            if (foundIndex < 0) {
                                if (isFirst)
                                    break;

                                if (nodeVal) {
                                    textNode = document.createTextNode(nodeVal);
                                    parentNode.insertBefore(textNode, node);
                                } // End if (nodeVal)

                                parentNode.removeChild(node);
                                break;
                            } // End if (foundIndex < 0)

                            isFirst = false;


                            begin = nodeVal.substring(0, foundIndex);
                            matched = nodeVal.substr(foundIndex, myToken.length);

                            if (begin) {
                                textNode = document.createTextNode(begin);
                                parentNode.insertBefore(textNode, node);
                            } // End if (begin)

                            span = document.createElement("span");
                            span.className += finalClassName;
                            span.appendChild(document.createTextNode(matched));
                            parentNode.insertBefore(span, node);

                            nodeVal = nodeVal.substring(foundIndex + myToken.length);
                        } // Whend

                    } // Next i 
                }; // End Function checkAndReplace 

                function iterator(p) {
                    if (p === null) return;

                    var children = Array.prototype.slice.call(p.childNodes),
                        i, cur;

                    if (children.length) {
                        for (i = 0; i < children.length; i++) {
                            cur = children[i];
                            if (cur.nodeType === 3) {
                                checkAndReplace(cur, tokens, allClassName, allSensitiveSearch);
                            } else if (cur.nodeType === 1) {
                                iterator(cur);
                            }
                        }
                    }
                }; // End Function iterator

                iterator(options[id.container]);
            } // End Function highlighter
                ;
            internalHighlighter({
                container: container,
                all: {
                    className: "highlighter"
                },
                tokens: [{
                    token: highlightText,
                    className: "highlight",
                    sensitiveSearch: false
                }]
            }); // End Call internalHighlighter 

        } // End Function highlight

    };

    function highlight_matches(highlightText) {
        const body = document.body;
        InstantSearch.highlight(body, highlightText);
    }

})