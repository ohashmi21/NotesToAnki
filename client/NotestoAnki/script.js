
document.getElementById('submitBtn').addEventListener('click', function(){
    const files = document.getElementById('notes').files
    const deckName = document.getElementById('deckName').value
    console.log(deckName)
})
const formData = new formData();
for (let i = 0; i<files; i++){
    formData.append('notes', files[i])
}formData.append('dname', deckName)