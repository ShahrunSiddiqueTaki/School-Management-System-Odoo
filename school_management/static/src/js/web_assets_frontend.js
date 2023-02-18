function print_(){
    var divContents = document.getElementById("print_card").innerHTML;
    var a = window.open('', '', 'height=720, width=720');
    a.document.write('<html>');
    a.document.write('<body >');
    a.document.write(divContents);
    a.document.write('</body></html>');
    a.document.close();
    a.print();
}
