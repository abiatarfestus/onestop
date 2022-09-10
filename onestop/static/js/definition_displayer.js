function displayDefinition() {
var selectedDef = document.getElementById("id_definition").value;
// console.log(selectedDef);
// console.log(definitionsDict);
if (selectedDef != '') {
    var defIndex = selectedDef;
    var engDef = definitionsDict[defIndex][0];
    var oshDef = definitionsDict[defIndex][1];
    document.getElementById("english_definition").innerHTML = `<strong>English:</strong> ${engDef}`;
    document.getElementById("oshindonga_definition").innerHTML = `<strong>Oshindonga:</strong> ${oshDef}`;
}
}