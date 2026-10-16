// Complete supplied consumer: text is shown literally.
function show(responseText, node) {
  const data = JSON.parse(responseText);
  node.textContent = data.message;
}
