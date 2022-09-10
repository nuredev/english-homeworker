[...document.getElementsByTagName("header"), ...document.getElementsByTagName("span")].forEach(span => {
    if (span.dataset && span.dataset.translation) {
        function selectionChanged() {
            clear_tooltips();

            let start = window.getSelection().anchorNode.parentNode;
            let end = window.getSelection().focusNode.parentNode;
            let selection = [];
            let selecting = false;

            for (let i = 0; i < span.parentNode.children.length; i++) {
                if (span.parentNode.children[i].innerText.includes(start.innerText)) selecting = true;
                if (selecting) {
                    selection = [...selection, span.parentNode.children[i].dataset.translation];
                    span.parentNode.children[i].classList.add("highlighted");
                }
                if (span.parentNode.children[i].innerText.includes(end.innerText)) selecting = false;
            }
            if (selection.length > 0) create_tooltip(start, selection.join(" "));

            if (window.getSelection) {
                if (window.getSelection().empty) {  // Chrome
                    window.getSelection().empty();
                } else if (window.getSelection().removeAllRanges) {  // Firefox
                    window.getSelection().removeAllRanges();
                }
            } else if (document.selection) {  // IE?
                document.selection.empty();
            }
        }
        span.onmouseup = span.onselectionchange = span.onkeyup = function (e) {
            if (e.ctrlKey) selectionChanged();
        };
    }
});


window.addEventListener('scroll', _ => {clear_tooltips()});


function create_tooltip(origin, content) {
    let tooltip = document.createElement("div");
    tooltip.classList.add("tooltip");
    tooltip.innerHTML = content;
    tooltip.style.setProperty("top", origin.getBoundingClientRect().top + "px");
    tooltip.onclick = function (_) {clear_tooltips()};
    document.body.append(tooltip);
}


function clear_tooltips() {
    document.querySelectorAll(".tooltip").forEach(el => el.remove());
    document.querySelectorAll(".highlighted").forEach(el => el.classList.remove("highlighted"));
}
