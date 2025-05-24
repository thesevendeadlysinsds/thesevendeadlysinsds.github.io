document.getElementById('copyButton').addEventListener('click', function() {
    var copyText = document.getElementById('copyText');
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand('copy');
    alert('URL copiée dans le presse-papiers !');
});
